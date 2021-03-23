#! /usr/bin/env python3
# |*****************************************************
# * Copyright         : Copyright (C) 2019
# * Author            : ddc
# * License           : GPL v3
# |*****************************************************
# # -*- coding: utf-8 -*-

import os
import shutil
import zipfile
import requests
from PyQt6 import QtCore, QtWidgets
from src.sql.games_sql import GamesSql
from src.create_files import CreateFiles
from PyQt6.QtGui import QDesktopServices
from src.sql.config_sql import ConfigSql
from src import constants, messages, utils, qtutils


def donate_clicked():
    href = QtCore.QUrl(constants.PAYPAL_URL)
    QDesktopServices.openUrl(href)


def update_clicked():
    href = QtCore.QUrl(constants.GITHUB_LATEST_VERSION_URL)
    QDesktopServices.openUrl(href)


def add_game(self):
    filename_path = qtutils.open_qt_file_dialog()
    if filename_path is not None:
        file_name, extension = os.path.splitext(os.path.basename(filename_path))
        if extension.lower() == ".exe":
            games_sql = GamesSql(self)
            rs_name = games_sql.get_game_by_path(filename_path)
            if rs_name is None:
                self.selected_game = None
                self.added_game_path = filename_path
                binary_type = utils.get_binary_type(self, filename_path)
                if binary_type in ["AMD64", "IA64"]:
                    architecture = "64bits"
                elif binary_type in ["IA32"]:
                    architecture = "32bits"
                else:
                    qtutils.show_message_window(self.log, "error", f"{messages.not_valid_game}")
                    return

                self.show_game_config_form(file_name, architecture)
            elif rs_name is not None and len(rs_name) > 0:
                qtutils.show_message_window(self.log, "error", f"{messages.game_already_exist}\n\n{file_name}")
        else:
            qtutils.show_message_window(self.log, "error", f"{messages.not_valid_game}")


def delete_game(self):
    game_not_found = False
    if not utils.check_game_file(self):
        game_not_found = True

    self.enable_widgets(True)
    if self.selected_game is not None:
        game_path = os.path.dirname(self.selected_game.path)
        game_name = self.selected_game.name

        # remove dll from game path
        if self.selected_game.api == constants.OPENGL_DISPLAY_NAME:
            reshade_dll = os.path.join(game_path, constants.OPENGL_DLL)
            opengl_log = f"{os.path.splitext(constants.OPENGL_DLL)[0]}.log"
            reshade_log_file = os.path.join(game_path, opengl_log)
        elif self.selected_game.api == constants.DX9_DISPLAY_NAME:
            reshade_dll = os.path.join(game_path, constants.D3D9_DLL)
            d3d9_log = f"{os.path.splitext(constants.D3D9_DLL)[0]}.log"
            reshade_log_file = os.path.join(game_path, d3d9_log)
        else:
            reshade_dll = os.path.join(game_path, constants.DXGI_DLL)
            dxgi_log = f"{os.path.splitext(constants.DXGI_DLL)[0]}.log"
            reshade_log_file = os.path.join(game_path, dxgi_log)

        if os.path.isfile(reshade_dll):
            try:
                os.remove(reshade_dll)
            except OSError as e:
                self.log.error(f"remove_file: {str(e)}")
                qtutils.show_message_window(self.log, "error", f"{messages.error_delete_dll} {game_name} dll\n\n{str(e)}")
                self.enable_widgets(False)
                return

        try:
            # remove reshade.ini from game path
            reshade_ini = os.path.join(game_path, constants.RESHADE_INI)
            if os.path.isfile(reshade_ini):
                os.remove(reshade_ini)

            # remove ReShadePreset.ini from game path
            reshade_plug_ini = os.path.join(game_path, constants.RESHADE_PRESET_INI)
            if os.path.isfile(reshade_plug_ini):
                os.remove(reshade_plug_ini)

            # remove Reshade log files from game path
            if os.path.isfile(reshade_log_file):
                os.remove(reshade_log_file)

            # remove from database
            games_sql = GamesSql(self)
            games_sql.delete_game(self.selected_game.id)

            # populate datagrid
            self.populate_datagrid()
            if game_not_found:
                qtutils.show_message_window(self.log, "info", f"{messages.game_not_in_path_deleted}\n\n{game_name}")
            else:
                qtutils.show_message_window(self.log, "info", f"{messages.game_deleted}\n\n{game_name}")
        except OSError as e:
            self.log.error(f"delete_game: {str(e)}")
            qtutils.show_message_window(self.log, "error", f"{game_name} files\n\n{str(e)}")

        self.enable_widgets(False)


def edit_game_path(self):
    if self.selected_game is not None:
        old_game_path = self.selected_game.path
        new_game_path = qtutils.open_qt_file_dialog()

        if new_game_path is not None:
            new_game_dir = os.path.dirname(new_game_path)

            if old_game_path == new_game_path:
                self.enable_widgets(False)
                qtutils.show_message_window(self.log, "info", f"{messages.no_change_path}")
                return

            old_file_name, old_extension = os.path.splitext(os.path.basename(old_game_path))
            new_file_name, new_extension = os.path.splitext(os.path.basename(new_game_path))
            if old_file_name != new_file_name:
                self.enable_widgets(False)
                qtutils.show_message_window(self.log, "error", f"{messages.not_same_game}\n\n{old_file_name}")
                return

            if new_extension.lower() != ".exe":
                self.enable_widgets(False)
                qtutils.show_message_window(self.log, "error", f"{messages.not_valid_game}\n\n{new_file_name}")
                return

            # save into database
            games_obj = utils.Object()
            games_sql = GamesSql(self)
            games_obj.id = self.selected_game.id
            games_obj.path = new_game_path
            games_sql.update_game_path(games_obj)

            # create Reshade.ini to replace edit CurrentPresetPath
            game_screenshots_path = _get_screenshot_path(self, new_game_dir, self.selected_game.name)
            self.selected_game.game_dir = new_game_dir

            try:
                dst_res_ini_path = os.path.join(new_game_dir, constants.RESHADE_INI)
                create_files = CreateFiles(self)
                create_files.create_reshade_ini_file(dst_res_ini_path, game_screenshots_path)
            except Exception as e:
                self.log.error(f"create_files: {str(e)}")

            # populate list
            self.populate_datagrid()
            qtutils.show_message_window(self.log, "info", f"{messages.path_changed_success}\n\n{new_game_path}")

        self.enable_widgets(False)


def open_reshade_config_file(self):
    self.enable_widgets(True)
    if self.selected_game is not None:
        game_dir = os.path.dirname(self.selected_game.path)
        res_plug_ini_path = os.path.join(game_dir, constants.RESHADE_PRESET_INI)

        try:
            if not os.path.isfile(constants.RESHADE_PRESET_FILENAME):
                create_files = CreateFiles(self)
                create_files.create_reshade_preset_ini_file()
        except Exception as e:
            self.log.error(f"create_files: {str(e)}")

        try:
            if not os.path.isfile(res_plug_ini_path) and os.path.isfile(constants.RESHADE_PRESET_FILENAME):
                shutil.copy2(constants.RESHADE_PRESET_FILENAME, res_plug_ini_path)
        except Exception as e:
            self.log.error(str(e))

        try:
            os.startfile(res_plug_ini_path)
        except Exception as e:
            err_msg = f"{str(e)}\n\n{messages.check_game_uninstalled}"
            qtutils.show_message_window(self.log, "error", err_msg)

    self.enable_widgets(False)


def edit_all_games_custom_config_button(self):
    if utils.check_files(self):
        try:
            os.startfile(constants.RESHADE_PRESET_FILENAME)
        except Exception as e:
            err_msg = f"{str(e)}\n\n{constants.RESHADE_PRESET_FILENAME}{messages.unable_start}"
            qtutils.show_message_window(self.log, "error", err_msg)


def dark_theme_clicked(self, status: str):
    if status == "YES":
        self.set_style_sheet(True)
        self.use_dark_theme = True
        status = 1
    else:
        self.set_style_sheet(False)
        self.use_dark_theme = False
        status = 0

    config_sql = ConfigSql(self)
    configs_obj = utils.Object()
    configs_obj.status = status
    config_sql.update_dark_theme(configs_obj)


def check_program_updates_clicked(self, status: str):
    if status == "YES":
        self.check_program_updates = True
        status = 1
    else:
        self.check_program_updates = False
        status = 0

    config_sql = ConfigSql(self)
    configs_obj = utils.Object()
    configs_obj.status = status
    config_sql.update_check_program_updates(configs_obj)


def check_reshade_updates_clicked(self, status: str):
    if status == "YES":
        self.check_reshade_updates = True
        status = 1
    else:
        self.check_reshade_updates = False
        status = 0

    self.qtobj.silent_reshade_updates_groupBox.setEnabled(self.check_reshade_updates)
    self.qtobj.silent_reshade_updates_groupBox.setVisible(self.check_reshade_updates)

    config_sql = ConfigSql(self)
    configs_obj = utils.Object()
    configs_obj.status = status
    config_sql.update_check_resahde_updates(configs_obj)


def silent_reshade_updates_clicked(self, status: str):
    if status == "YES":
        self.silent_reshade_updates = True
        status = 1
    else:
        self.silent_reshade_updates = False
        status = 0

    config_sql = ConfigSql(self)
    configs_obj = utils.Object()
    configs_obj.status = status
    config_sql.update_silent_reshade_updates(configs_obj)


def update_shaders_clicked(self, status: str):
    if status == "YES":
        self.update_shaders = True
        status = 1
    else:
        self.update_shaders = False
        status = 0

    config_sql = ConfigSql(self)
    configs_obj = utils.Object()
    configs_obj.status = status
    config_sql.update_shaders(configs_obj)


def create_screenshots_folder_clicked(self, status: str):
    if status == "YES":
        self.create_screenshots_folder = True
        status = 1
    else:
        self.create_screenshots_folder = False
        status = 0

    config_sql = ConfigSql(self)
    configs_obj = utils.Object()
    configs_obj.status = status
    config_sql.update_create_screenshots_folder(configs_obj)


def reset_reshade_files_clicked(self, status: str):
    if status == "YES":
        self.reset_reshade_files = True
        status = 1
    else:
        self.reset_reshade_files = False
        status = 0

    config_sql = ConfigSql(self)
    configs_obj = utils.Object()
    configs_obj.status = status
    config_sql.update_reset_reshade_files(configs_obj)


def custom_config_clicked(self, status: str):
    if status == "YES":
        self.use_custom_config = True
        status = 1
    else:
        self.use_custom_config = False
        status = 0

    config_sql = ConfigSql(self)
    configs_obj = utils.Object()
    configs_obj.status = status
    config_sql.update_custom_config(configs_obj)


def programs_tableWidget_clicked(self, item):
    self.enable_widgets(True)
    #clicked_item = self.qtobj.programs_tableWidget.currentItem()
    clicked_row = self.qtobj.programs_tableWidget.selectedItems()

    self.selected_game = utils.Object()
    #self.selected_game.column = item.column()
    #self.selected_game.row = item.row()
    self.selected_game.name = clicked_row[0].text()
    self.selected_game.architecture = clicked_row[1].text()
    self.selected_game.api = clicked_row[2].text()
    self.selected_game.path = clicked_row[3].text()
    self.selected_game.game_dir = os.path.dirname(self.selected_game.path)

    search_pattern = self.selected_game.name
    games_sql = GamesSql(self)
    rs = games_sql.get_game_by_name(search_pattern)
    if rs is not None and len(rs) > 0:
        self.selected_game.id = rs[0].get("id")


def apply_all(self):
    games_sql = GamesSql(self)
    rs_all_games = games_sql.get_games()
    len_games = len(rs_all_games)
    # len_games = self.qtobj.programs_tableWidget.rowCount()

    if len_games > 0:
        if self.reset_reshade_files:
            msg = messages.reset_config_files_question
            reply = qtutils.show_message_window(self.log, "question", msg)
            if reply == QtWidgets.QMessageBox.No:
                self.reset_reshade_files = False

        if rs_all_games is not None:
            self.enable_form(False)
            self.enable_widgets(False)
            self.qtobj.apply_button.setEnabled(False)

            # download shaders
            _download_shaders(self)

            # begin games update section
            errors = []
            games_obj = utils.Object()
            self.progressBar.set_values(messages.copying_DLLs, 0)
            for i in range(len(rs_all_games)):
                self.progressBar.set_values(messages.copying_DLLs, 100 / len_games)
                games_obj.api = rs_all_games[i]["api"]
                games_obj.architecture = rs_all_games[i]["architecture"]
                games_obj.game_name = rs_all_games[i]["name"]
                games_obj.path = rs_all_games[i]["path"]
                len_games = len_games - 1
                result = _apply_single(self, games_obj)
                if result is not None:
                    errors.append(result)

            self.enable_form(True)
            self.qtobj.apply_button.setEnabled(True)

            if len(errors) == 0 and self.need_apply is False:
                qtutils.show_message_window(self.log, "info", messages.apply_success)
            elif len(errors) > 0:
                err = "\n".join(errors)
                qtutils.show_message_window(self.log, "error", f"{messages.apply_success_with_errors}\n\n{err}")

            self.progressBar.close()


def game_config_form_result(self, architecture, status):
    dx9_name = constants.DX9_DISPLAY_NAME
    dxgi_name = constants.DXGI_DISPLAY_NAME
    opengl_name = constants.OPENGL_DISPLAY_NAME

    if status == "OK":
        self.progressBar.set_values(messages.copying_DLLs, 50)
        if self.game_config_form.qtObj.game_name_lineEdit.text() == "":
            self.progressBar.close()
            qtutils.show_message_window(self.log, "error", messages.missing_game_name)
            return

        if not self.game_config_form.qtObj.opengl_radioButton.isChecked() \
            and not self.game_config_form.qtObj.dx9_radioButton.isChecked() \
            and not self.game_config_form.qtObj.dx_radioButton.isChecked():
            self.progressBar.close()
            qtutils.show_message_window(self.log, "error", messages.missing_api)
            return

        sql_games_obj = utils.Object()
        sql_games_obj.game_name = self.game_config_form.qtObj.game_name_lineEdit.text()

        if architecture == "32bits":
            sql_games_obj.architecture = "32bits"
            src_path = constants.RESHADE32_PATH
        else:
            sql_games_obj.architecture = "64bits"
            src_path = constants.RESHADE64_PATH

        games_sql = GamesSql(self)
        if self.selected_game is not None:
            if self.game_config_form.qtObj.dx9_radioButton.isChecked():
                sql_games_obj.api = dx9_name
                dst_path = os.path.join(self.selected_game.game_dir, constants.D3D9_DLL)
            elif self.game_config_form.qtObj.dx_radioButton.isChecked():
                sql_games_obj.api = dxgi_name
                dst_path = os.path.join(self.selected_game.game_dir, constants.DXGI_DLL)
            else:
                sql_games_obj.api = opengl_name
                dst_path = os.path.join(self.selected_game.game_dir, constants.OPENGL_DLL)

            if self.selected_game.name != sql_games_obj.game_name or (self.selected_game.api != sql_games_obj.api):
                # checking name changes
                # create Reshade.ini to replace edit CurrentPresetPath
                old_screenshots_path = _get_screenshot_path(self, self.selected_game.game_dir, self.selected_game.name)
                if len(old_screenshots_path) > 0:
                    scrrenshot_dir_path = os.path.dirname(old_screenshots_path)
                    new_screenshots_path = os.path.join(scrrenshot_dir_path, sql_games_obj.game_name)
                else:
                    new_screenshots_path = ""

                try:
                    dst_res_ini_path = os.path.join(self.selected_game.game_dir, constants.RESHADE_INI)
                    create_files = CreateFiles(self)
                    create_files.create_reshade_ini_file(dst_res_ini_path, new_screenshots_path)
                except Exception as e:
                    self.log.error(f"create_reshade_ini_file: {str(e)}")

                try:
                    # rename screenshot folder
                    if os.path.isdir(old_screenshots_path):
                        os.rename(old_screenshots_path, new_screenshots_path)
                except OSError as e:
                    self.log.error(f"rename_screenshot_dir: {str(e)}")

                try:
                    # deleting Reshade.dll
                    if self.selected_game.api == dx9_name:
                        d3d9_game_path = os.path.join(self.selected_game.game_dir, constants.D3D9_DLL)
                        if os.path.isfile(d3d9_game_path):
                            os.remove(d3d9_game_path)
                    elif self.selected_game.api == opengl_name:
                        opengl_game_path = os.path.join(self.selected_game.game_dir, constants.OPENGL_DLL)
                        if os.path.isfile(opengl_game_path):
                            os.remove(opengl_game_path)
                    else:
                        dxgi_game_path = os.path.join(self.selected_game.game_dir, constants.DXGI_DLL)
                        if os.path.isfile(dxgi_game_path):
                            os.remove(dxgi_game_path)
                except OSError as e:
                    self.log.error(f"remove_reshade_file: {str(e)}")

                try:
                    # creating Reshade.dll
                    shutil.copy2(src_path, dst_path)
                except shutil.Error as e:
                    self.log.error(f"copyfile: {src_path} to {dst_path} - {str(e)}")

                qtutils.show_message_window(self.log, "info", f"{messages.game_updated}\n\n{sql_games_obj.game_name}")

            sql_games_obj.id = self.selected_game.id
            games_sql.update_game(sql_games_obj)
            self.progressBar.close()
        else:
            # new game added
            if self.game_config_form.qtObj.dx9_radioButton.isChecked():
                sql_games_obj.api = dx9_name
            elif self.game_config_form.qtObj.opengl_radioButton.isChecked():
                sql_games_obj.api = opengl_name
            else:
                sql_games_obj.api = dxgi_name

            sql_games_obj.path = self.added_game_path
            games_sql.insert_game(sql_games_obj)
            del self.added_game_path
            if self.update_shaders:
                _download_shaders(self)
            self.progressBar.close()
            _apply_single(self, sql_games_obj)
            qtutils.show_message_window(self.log, "info", f"{messages.game_added}\n\n{sql_games_obj.game_name}")

        self.populate_datagrid()
        self.game_config_form.close()
        self.enable_widgets(False)
    else:
        self.game_config_form.close()


def _get_screenshot_path(self, game_dir, game_name):
    game_screenshots_path = ""
    if self.qtobj.yes_screenshots_folder_radioButton.isChecked():
        game_screenshots_path = os.path.join(constants.RESHADE_SCREENSHOT_PATH, game_name)
        try:
            if not os.path.exists(constants.RESHADE_SCREENSHOT_PATH):
                os.makedirs(constants.RESHADE_SCREENSHOT_PATH)
        except OSError as e:
            self.log.error(f"mkdir: {constants.RESHADE_SCREENSHOT_PATH} {str(e)}")

        try:
            if not os.path.exists(game_screenshots_path):
                os.makedirs(game_screenshots_path)
        except OSError as e:
            self.log.error(f"mkdir: {game_screenshots_path} {str(e)}")
    else:
        reshade_ini_filepath = os.path.join(game_dir, constants.RESHADE_INI)
        reshade_config_screenshot_path = utils.get_ini_settings(reshade_ini_filepath, "GENERAL", "ScreenshotPath")
        if reshade_config_screenshot_path is not None:
            game_screenshots_path = reshade_config_screenshot_path
        elif os.path.isdir(os.path.join(constants.RESHADE_SCREENSHOT_PATH, game_name)):
            game_screenshots_path = os.path.join(constants.RESHADE_SCREENSHOT_PATH, game_name)

    return game_screenshots_path


def _apply_single(self, games_obj):
    errors = None
    game_dir = os.path.dirname(games_obj.path)
    game_name = games_obj.game_name
    dst_res_ini_path = os.path.join(game_dir, constants.RESHADE_INI)
    dst_res_plug_ini_path = os.path.join(game_dir, constants.RESHADE_PRESET_INI)
    game_screenshots_path = _get_screenshot_path(self, game_dir, game_name)

    if games_obj.architecture.lower() == "32bits":
        src_dll_path = constants.RESHADE32_PATH
    else:
        src_dll_path = constants.RESHADE64_PATH

    if games_obj.api == constants.DX9_DISPLAY_NAME:
        dst_dll_path = os.path.join(game_dir, constants.D3D9_DLL)
    elif games_obj.api == constants.OPENGL_DISPLAY_NAME:
        dst_dll_path = os.path.join(game_dir, constants.OPENGL_DLL)
    else:
        dst_dll_path = os.path.join(game_dir, constants.DXGI_DLL)

    try:
        try:
            # copying Reshade.dll
            shutil.copy2(src_dll_path, dst_dll_path)
        except Exception as e:
            self.log.error(f"[apply_single]: {str(e)}")

        create_files = CreateFiles(self)
        if self.reset_reshade_files:
            try:
                # create Reshade.ini for each game, because each game has different paths
                create_files.create_reshade_ini_file(dst_res_ini_path, game_screenshots_path)
            except Exception as e:
                self.log.error(f"[apply_single]:[create_reshade_ini_file]: {str(e)}")

            try:
                # create ReShadePreset.ini inside program dir, then copy to game path
                create_files.create_reshade_preset_ini_file()
                shutil.copy2(constants.RESHADE_PRESET_FILENAME, dst_res_plug_ini_path)
            except shutil.Error as e:
                self.log.error(f"[apply_single]:[create_reshade_preset_ini_file]: {str(e)}")

            try:
                # create style.qss nside program dir
                create_files.create_style_file()
            except shutil.Error as e:
                self.log.error(f"[apply_single]:[create_style_file]: {str(e)}")
        else:
            if not os.path.exists(dst_res_ini_path):
                try:
                    create_files.create_reshade_ini_file(dst_res_ini_path, game_screenshots_path)
                except Exception as e:
                    self.log.error(f"[apply_single]:[create_reshade_ini_file]: {str(e)}")

            if not os.path.exists(constants.RESHADE_PRESET_FILENAME):
                try:
                    create_files.create_reshade_preset_ini_file()
                    shutil.copy2(constants.RESHADE_PRESET_FILENAME, dst_res_plug_ini_path)
                except shutil.Error as e:
                    self.log.error(f"[apply_single]:[create_reshade_preset_ini_file]: {str(e)}")
            else:
                shutil.copy2(constants.RESHADE_PRESET_FILENAME, dst_res_plug_ini_path)

            if not os.path.exists(constants.STYLE_QSS_FILENAME):
                try:
                    create_files.create_style_file()
                except shutil.Error as e:
                    self.log.error(f"[apply_single]:[create_style_file]: {str(e)}")
    except Exception as e:
        self.log.error(f"apply:[{game_name}]:[{str(e)}]")
        errors = f"- {game_name}: {str(e)}"

    return errors


def _download_shaders(self):
    downloaded_new_shaders = None
    if not os.path.exists(constants.SHADERS_SRC_PATH)\
            or (self.update_shaders is not None and self.update_shaders is True):
        downloaded_new_shaders = True
    elif self.update_shaders is not None and self.update_shaders is False:
        downloaded_new_shaders = False

    if downloaded_new_shaders is not None and downloaded_new_shaders is True:
        try:
            self.progressBar.set_values(messages.downloading_shaders, 50)
            r = requests.get(constants.SHADERS_ZIP_URL)
            with open(constants.SHADERS_ZIP_PATH, "wb") as outfile:
                outfile.write(r.content)
        except Exception as e:
            err_msg = f"{messages.dl_new_shaders_timeout} {str(e)}"
            qtutils.show_message_window(self.log, "error", err_msg)

        try:
            if os.path.isdir(constants.SHADERS_SRC_PATH):
                shutil.rmtree(constants.SHADERS_SRC_PATH)
        except OSError as e:
            self.log.error(f"rmtree: {str(e)}")

        try:
            if os.path.isdir(constants.RES_SHAD_MPATH):
                shutil.rmtree(constants.RES_SHAD_MPATH)
        except OSError as e:
            self.log.error(f"rmtree: {str(e)}")

        self.progressBar.set_values(messages.downloading_shaders, 75)
        if os.path.isfile(constants.SHADERS_ZIP_PATH):
            try:
                utils.unzip_file(constants.SHADERS_ZIP_PATH, constants.PROGRAM_PATH)
            except FileNotFoundError as e:
                self.log.error(str(e))
            except zipfile.BadZipFile as e:
                self.log.error(str(e))

            try:
                os.remove(constants.SHADERS_ZIP_PATH)
            except OSError as e:
                self.log.error(f"remove_file: {str(e)}")

        try:
            if os.path.exists(constants.RES_SHAD_MPATH):
                out_dir = f"{constants.PROGRAM_PATH}\\{constants.RESHADE_SHADERS}"
                os.rename(constants.RES_SHAD_MPATH, out_dir)
        except OSError as e:
            self.log.error(f"rename_path: {str(e)}")

        self.progressBar.set_values(messages.downloading_shaders, 99)

# -*- coding: utf-8 -*-
import os
import shutil
from PyQt6 import QtCore
from src.files import Files
from src.database.dal.games_dal import GamesDal
from src.database.dal.config_dal import ConfigDal
from PyQt6.QtGui import QDesktopServices
from src import constants, messages
from src.utils import utils, qtutils


def donate_clicked():
    href = QtCore.QUrl(constants.PAYPAL_URL)
    QDesktopServices.openUrl(href)


def update_program_clicked():
    href = QtCore.QUrl(constants.GITHUB_LATEST_VERSION_URL)
    QDesktopServices.openUrl(href)


def add_game(self):
    filename_path = qtutils.open_exe_file_dialog()
    if filename_path is not None:
        file_name, extension = os.path.splitext(
            os.path.basename(filename_path)
        )
        if extension.lower() == ".exe":
            games_sql = GamesDal(self)
            rs_name = games_sql.get_game_by_path(filename_path)
            if rs_name is None:
                self.selected_game = None
                self.added_game_path = filename_path
                binary_type = utils.get_binary_type(self, filename_path)
                if binary_type.upper() in ["AMD64", "IA64"]:
                    architecture = "64bits"
                elif binary_type.upper() in ["IA32"]:
                    architecture = "32bits"
                else:
                    qtutils.show_message_window(self.log,
                                                "error",
                                                messages.not_valid_game)
                    return

                qtutils.show_game_config_form(self, file_name, architecture)
            elif rs_name is not None and len(rs_name) > 0:
                qtutils.show_message_window(self.log,
                                            "error",
                                            f"{messages.game_already_exist}"
                                            f"\n\n{file_name}")
        else:
            qtutils.show_message_window(self.log,
                                        "error",
                                        messages.not_valid_game)


def delete_game(self):
    game_not_found = False
    if not utils.check_game_file(self):
        game_not_found = True

    # self.enable_widgets(True)
    if self.selected_game is not None:
        game_dir = os.path.dirname(self.selected_game.path)
        game_name = self.selected_game.name

        # remove dll from game path
        reshade_dll, log_file_path = _get_reshade_dll_name(self, game_dir)
        if os.path.isfile(log_file_path):
            try:
                os.remove(log_file_path)
            except OSError:
                pass

        if os.path.isfile(reshade_dll):
            try:
                os.remove(reshade_dll)
            except OSError as e:
                self.log.error(f"remove_file: {utils.get_exception(e)}")
                qtutils.show_message_window(self.log,
                                            "error",
                                            f"{messages.error_delete_dll} "
                                            f"{game_name} dll"
                                            f"\n\n{utils.get_exception(e)}")
                self.enable_widgets(False)
                return

        try:
            # remove Reshade.ini
            all_reshade_game_dir_files = utils.list_files(game_dir,
                                                          "reshade")
            for f in all_reshade_game_dir_files:
                try:
                    os.remove(f)
                except OSError:
                    pass

            games_sql = GamesDal(self)
            games_sql.delete_game(self.selected_game.id)

            if self.show_info_messages:
                if game_not_found:
                    qtutils.show_message_window(
                        self.log,
                        "info",
                        f"{messages.game_not_in_path_deleted}"
                        f"\n\n{game_name}"
                    )
                else:
                    qtutils.show_message_window(
                        self.log,
                        "info",
                        f"{messages.game_deleted}"
                        f"\n\n{game_name}"
                    )

            self.populate_table_widget()
        except OSError as e:
            qtutils.show_message_window(
                self.log,
                "error",
                f"ERROR deleting {game_name} files"
                f"\n\n{utils.get_exception(e)}"
            )

        self.enable_widgets(False)


def edit_selected_game_path(self):
    if self.selected_game is not None:
        old_game_file_path = self.selected_game.path
        new_game_file_path = qtutils.open_exe_file_dialog()

        if new_game_file_path is not None:
            old_game_dir = os.path.dirname(old_game_file_path)
            new_game_dir = os.path.dirname(new_game_file_path)

            if old_game_file_path == new_game_file_path:
                self.enable_widgets(False)
                if self.show_info_messages:
                    qtutils.show_message_window(
                        self.log,
                        "info",
                        messages.no_change_path
                    )
                return

            old_file_name, old_extension = os.path.splitext(
                os.path.basename(old_game_file_path)
            )
            new_file_name, new_extension = os.path.splitext(
                os.path.basename(new_game_file_path)
            )
            if old_file_name != new_file_name:
                self.enable_widgets(False)
                qtutils.show_message_window(
                    self.log,
                    "error",
                    f"{messages.not_same_game}"
                    f"\n\n{old_file_name}"
                )
                return

            if new_extension.lower() != ".exe":
                self.enable_widgets(False)
                qtutils.show_message_window(
                    self.log,
                    "error",
                    f"{messages.not_valid_game}"
                    f"\n\n{new_file_name}"
                )
                return

            # create Reshade.ini
            self.selected_game.game_dir = new_game_dir
            game_screenshots_path = utils.get_screenshot_path(
                self,
                new_game_dir,
                self.selected_game.name
            )
            try:
                files = Files(self)
                files.apply_reshade_ini_file(new_game_dir,
                                             game_screenshots_path)
            except Exception as e:
                self.log.error(f"create_files: {utils.get_exception(e)}")

            # remove dll from game path
            reshade_dll, log_file_path = _get_reshade_dll_name(self,
                                                               old_game_dir)

            try:
                shutil.move(reshade_dll,
                            os.path.join(new_game_dir,
                                         os.path.basename(reshade_dll))
                            )
            except OSError:
                pass

            if os.path.isfile(log_file_path):
                try:
                    os.remove(log_file_path)
                except OSError:
                    pass

            # move all reshade files and remove reshade.ini with old path
            all_old_game_dir_files = utils.list_files(old_game_dir, "reshade")
            for f in all_old_game_dir_files:
                if os.path.basename(f) == constants.RESHADE_INI\
                        or os.path.basename(f).lower().endswith("log"):
                    try:
                        os.remove(f)
                    except OSError:
                        pass
                else:
                    try:
                        shutil.move(f, os.path.join(new_game_dir,
                                                    os.path.basename(f)))
                    except OSError:
                        pass

            # save into database
            games_obj = utils.Object()
            games_sql = GamesDal(self)
            games_obj.id = self.selected_game.id
            games_obj.path = new_game_file_path
            games_sql.update_game_path(games_obj)

            if self.show_info_messages:
                qtutils.show_message_window(self.log,
                                            "info",
                                            f"{messages.path_changed_success}"
                                            f"\n\n{new_game_file_path}")

        self.log.info(f"{messages.path_changed_success}:{new_game_file_path}")
        self.populate_table_widget()
        self.enable_widgets(False)


def edit_selected_game_plugin_config_file(self):
    self.enable_widgets(True)
    if self.selected_game is not None:
        game_dir = os.path.dirname(self.selected_game.path)
        res_plug_ini_path = os.path.join(game_dir,
                                         constants.RESHADE_PRESET_INI)

        try:
            if not os.path.isfile(constants.RESHADE_PRESET_PATH):
                create_files = Files(self)
                create_files.download_reshade_preset_file()
        except Exception as e:
            self.log.error(f"create_files: {utils.get_exception(e)}")

        try:
            if not os.path.isfile(res_plug_ini_path) and os.path.isfile(
                    constants.RESHADE_PRESET_PATH):
                shutil.copy2(constants.RESHADE_PRESET_PATH, res_plug_ini_path)
        except Exception as e:
            self.log.error(utils.get_exception(e))

        try:
            utils.open_file(res_plug_ini_path)
        except Exception as e:
            err_msg = f"{utils.get_exception(e)}" \
                      f"\n\n{messages.check_game_uninstalled}"
            qtutils.show_message_window(self.log, "error", err_msg)

    self.enable_widgets(False)


def edit_default_preset_plugin_button_clicked(self):
    try:
        utils.check_local_files(self)
        utils.open_file(constants.RESHADE_PRESET_PATH)
    except Exception as e:
        err_msg = f"{utils.get_exception(e)}" \
                  f"\n\n{constants.RESHADE_PRESET_PATH}{messages.unable_start}"
        qtutils.show_message_window(self.log, "error", err_msg)


def reset_all_button_clicked(self):
    self.progressbar.set_values(messages.reseting_files, 25)
    Files(self).download_all_files()
    self.progressbar.set_values(messages.reseting_files, 50)
    utils.download_shaders(self)
    self.progressbar.set_values(messages.reseting_files, 75)
    apply_all(self, reset=True)
    self.progressbar.close()
    qtutils.show_message_window(self.log, "info", messages.reset_success)


def dark_theme_clicked(self, status):
    if status == "YES":
        self.use_dark_theme = True
        status = 1
    else:
        self.use_dark_theme = False
        status = 0

    self.set_style_sheet()
    config_sql = ConfigDal(self)
    config_sql.update_dark_theme(status)


def check_program_updates_clicked(self, status):
    if status == "YES":
        self.check_program_updates = True
        status = 1
    else:
        self.check_program_updates = False
        status = 0

    config_sql = ConfigDal(self)
    config_sql.update_check_program_updates(status)


def show_info_messages_clicked(self, status):
    if status == "YES":
        self.show_info_messages = True
        status = 1
    else:
        self.show_info_messages = False
        status = 0

    config_sql = ConfigDal(self)
    config_sql.update_show_info_messages(status)


def check_reshade_updates_clicked(self, status):
    if status == "YES":
        self.check_reshade_updates = True
        status = 1
    else:
        self.check_reshade_updates = False
        status = 0

    config_sql = ConfigDal(self)
    config_sql.update_check_resahde_updates(status)


def update_shaders_clicked(self, status):
    if status == "YES":
        self.update_shaders = True
        status = 1
    else:
        self.update_shaders = False
        status = 0

    config_sql = ConfigDal(self)
    config_sql.update_shaders(status)


def create_screenshots_folder_clicked(self, status):
    if status == "YES":
        self.create_screenshots_folder = True
        status = 1
    else:
        self.create_screenshots_folder = False
        status = 0

    config_sql = ConfigDal(self)
    config_sql.update_create_screenshots_folder(status)


def programs_tableWidget_clicked(self, item):
    self.enable_widgets(True)
    # clicked_item = self.qtobj.programs_tableWidget.currentItem()
    clicked_row = self.qtobj.programs_tableWidget.selectedItems()

    self.selected_game = utils.Object()
    # self.selected_game.column = item.column()
    # self.selected_game.row = item.row()
    self.selected_game.name = clicked_row[0].text()
    self.selected_game.architecture = clicked_row[1].text()
    self.selected_game.api = clicked_row[2].text()
    self.selected_game.path = clicked_row[3].text()
    self.selected_game.game_dir = os.path.dirname(self.selected_game.path)

    search_pattern = self.selected_game.name
    games_sql = GamesDal(self)
    rs = games_sql.get_game_by_name(search_pattern)
    if rs is not None and len(rs) > 0:
        self.selected_game.id = rs[0].get("id")


def game_config_form_result(self, architecture, status):
    self.game_config_form.close()
    dx9_name = constants.DX9_DISPLAY_NAME
    dxgi_name = constants.DXGI_DISPLAY_NAME
    opengl_name = constants.OPENGL_DISPLAY_NAME

    if status == "OK":
        if self.game_config_form.qtObj.game_name_lineEdit.text() == "":
            qtutils.show_message_window(self.log,
                                        "error",
                                        messages.missing_game_name)
            return

        if not self.game_config_form.qtObj.opengl_radioButton.isChecked() \
                and not self.game_config_form.qtObj.dx9_radioButton.isChecked()\
                and not self.game_config_form.qtObj.dx_radioButton.isChecked():
            qtutils.show_message_window(self.log, "error", messages.missing_api)
            return

        sql_games_obj = utils.Object()
        sql_games_obj.game_name = (
            self.game_config_form.qtObj.game_name_lineEdit.text()
        )

        if architecture == "32bits":
            sql_games_obj.architecture = "32bits"
            src_path = constants.RESHADE32_PATH
        else:
            sql_games_obj.architecture = "64bits"
            src_path = constants.RESHADE64_PATH

        games_sql = GamesDal(self)
        if self.selected_game is not None:
            if self.game_config_form.qtObj.dx9_radioButton.isChecked():
                sql_games_obj.api = dx9_name
                dst_path = os.path.join(self.selected_game.game_dir,
                                        constants.D3D9_DLL)
            elif self.game_config_form.qtObj.dx_radioButton.isChecked():
                sql_games_obj.api = dxgi_name
                dst_path = os.path.join(self.selected_game.game_dir,
                                        constants.DXGI_DLL)
            else:
                sql_games_obj.api = opengl_name
                dst_path = os.path.join(self.selected_game.game_dir,
                                        constants.OPENGL_DLL)

            if self.selected_game.name != sql_games_obj.game_name or (
                    self.selected_game.api != sql_games_obj.api):
                # checking name changes
                # create Reshade.ini to replace edit CurrentPresetPath
                old_screenshots_path = utils.get_screenshot_path(
                    self,
                    self.selected_game.game_dir,
                    self.selected_game.name
                )
                if len(old_screenshots_path) > 0:
                    scrrenshot_dir_path = os.path.dirname(old_screenshots_path)
                    new_screenshots_path = os.path.join(
                        scrrenshot_dir_path,
                        sql_games_obj.game_name
                    )
                else:
                    new_screenshots_path = ""

                try:
                    files = Files(self)
                    files.apply_reshade_ini_file(self.selected_game.game_dir,
                                                 new_screenshots_path)
                except Exception as e:
                    self.log.error(f"download_reshade_ini_file: "
                                   f"{utils.get_exception(e)}")

                try:
                    # rename screenshot folder
                    if os.path.isdir(old_screenshots_path):
                        os.rename(old_screenshots_path, new_screenshots_path)
                except OSError as e:
                    self.log.error(f"rename_screenshot_dir: "
                                   f"{utils.get_exception(e)}")

                try:
                    # deleting Reshade.dll
                    if self.selected_game.api == dx9_name:
                        d3d9_game_path = os.path.join(
                            self.selected_game.game_dir,
                            constants.D3D9_DLL
                        )
                        if os.path.isfile(d3d9_game_path):
                            os.remove(d3d9_game_path)
                    elif self.selected_game.api == opengl_name:
                        opengl_game_path = os.path.join(
                            self.selected_game.game_dir,
                            constants.OPENGL_DLL
                        )
                        if os.path.isfile(opengl_game_path):
                            os.remove(opengl_game_path)
                    else:
                        dxgi_game_path = os.path.join(
                            self.selected_game.game_dir,
                            constants.DXGI_DLL
                        )
                        if os.path.isfile(dxgi_game_path):
                            os.remove(dxgi_game_path)
                except OSError as e:
                    self.log.error(f"remove_reshade_file: "
                                   f"{utils.get_exception(e)}")

                try:
                    # creating Reshade.dll
                    shutil.copy2(src_path, dst_path)
                except shutil.Error as e:
                    self.log.error(f"copyfile: {src_path} to {dst_path} - "
                                   f"{utils.get_exception(e)}")

                if self.show_info_messages:
                    qtutils.show_message_window(
                        self.log,
                        "info",
                        f"{messages.game_updated}"
                        f"\n\n{sql_games_obj.game_name}"
                    )

            sql_games_obj.id = self.selected_game.id
            games_sql.update_game(sql_games_obj)
            self.populate_table_widget()
            self.enable_widgets(False)
        else:
            # new game added
            if self.game_config_form.qtObj.dx9_radioButton.isChecked():
                sql_games_obj.api = dx9_name
            elif self.game_config_form.qtObj.opengl_radioButton.isChecked():
                sql_games_obj.api = opengl_name
            else:
                sql_games_obj.api = dxgi_name

            if self.added_game_path is not None:
                sql_games_obj.path = self.added_game_path
            elif self.selected_game is not None:
                sql_games_obj.path = self.selected_game.game_dir
            else:
                if self.show_info_messages:
                    qtutils.show_message_window(
                        self.log,
                        "error",
                        f"{sql_games_obj.game_name}\n\n"
                        f"{messages.error_change_game_name}"
                    )
                return

            games_sql.insert_game(sql_games_obj)
            del self.added_game_path
            _apply_single(self, sql_games_obj)
            self.populate_table_widget()
            self.enable_widgets(False)
            if self.show_info_messages:
                qtutils.show_message_window(self.log,
                                            "info",
                                            f"{messages.game_added}\n\n"
                                            f"{sql_games_obj.game_name}")


def apply_all(self, reset=False):
    games_sql = GamesDal(self)
    rs_all_games = games_sql.get_games()
    # len_games = self.qtobj.programs_tableWidget.rowCount()
    len_games = len(rs_all_games)
    if len_games > 0:
        self.enable_form(False)
        self.enable_widgets(False)
        self.qtobj.apply_button.setEnabled(False)
        errors = []
        games_obj = utils.Object()
        self.progressbar.set_values(messages.copying_DLLs, 0)
        for i in range(len_games):
            self.progressbar.set_values(
                messages.copying_DLLs, 100 // len_games
            )
            games_obj.api = rs_all_games[i]["api"]
            games_obj.architecture = rs_all_games[i]["architecture"]
            games_obj.game_name = rs_all_games[i]["name"]
            games_obj.path = rs_all_games[i]["path"]
            len_games = len_games - 1
            result = _apply_single(self,
                                   games_obj,
                                   reset)
            if result is not None:
                errors.append(result)

        self.progressbar.close()
        self.enable_form(True)
        self.qtobj.apply_button.setEnabled(True)

        if len(errors) == 0 \
                and self.need_apply is False \
                and self.show_info_messages:
            qtutils.show_message_window(self.log,
                                        "info",
                                        messages.apply_success)
        elif len(errors) > 0:
            err = "\n".join(errors)
            qtutils.show_message_window(self.log,
                                        "error",
                                        f"{messages.apply_success_with_errors}"
                                        f"\n\n{err}")


def _apply_single(self, games_obj, reset=False):
    errors = None
    game_dir = os.path.dirname(games_obj.path)
    game_name = games_obj.game_name
    utils.check_local_files(self)
    files = Files(self)

    if games_obj.architecture.lower() == "32bits":
        src_dll_path = constants.RESHADE32_PATH
    else:
        src_dll_path = constants.RESHADE64_PATH

    if not os.path.isfile(src_dll_path):
        utils.unzip_reshade(self, self.local_reshade_path)

    try:
        # Reshade.dll
        if os.path.isfile(src_dll_path) or reset:
            if games_obj.api == constants.DX9_DISPLAY_NAME:
                dst_dll_path = os.path.join(game_dir, constants.D3D9_DLL)
            elif games_obj.api == constants.OPENGL_DISPLAY_NAME:
                dst_dll_path = os.path.join(game_dir, constants.OPENGL_DLL)
            else:
                dst_dll_path = os.path.join(game_dir, constants.DXGI_DLL)
            ret = files.apply_reshade_dll_file(src_dll_path, dst_dll_path)
            if ret is not None:
                self.log.error(f"[{game_name}]:[{str(ret)}]")

        # Reshade.ini
        dst_res_ini_path = os.path.join(game_dir, constants.RESHADE_INI)
        if os.path.isfile(constants.RESHADE_INI_PATH) and not os.path.isfile(
                dst_res_ini_path) or reset:
            game_screenshots_path = utils.get_screenshot_path(self,
                                                              game_dir,
                                                              game_name)
            ret = files.apply_reshade_ini_file(game_dir, game_screenshots_path)
            if ret is not None:
                self.log.error(f"[{game_name}]:[{str(ret)}]")

        # ReShadePreset.ini
        dst_preset_path = os.path.join(game_dir, constants.RESHADE_PRESET_INI)
        if os.path.isfile(constants.RESHADE_PRESET_PATH) \
                and not os.path.isfile(dst_preset_path) or reset:
            ret = files.apply_reshade_preset_file(game_dir)
            if ret is not None:
                self.log.error(f"[{game_name}]:[{str(ret)}]")

            if isinstance(ret, FileNotFoundError):
                errors = f"[{game_name}]: No such file or directory"

    except Exception as e:
        self.log.error(f"[{game_name}]:[{utils.get_exception(e)}]")
        errors = f"[{game_name}]: {utils.get_exception(e)}"

    return errors


def open_selected_game_location(self):
    self.enable_widgets(True)
    if self.selected_game is not None:
        game_dir = os.path.dirname(self.selected_game.path)

        try:
            utils.open_file(game_dir)
        except Exception as e:
            err_msg = f"{utils.get_exception(e)}" \
                      f"\n\n{messages.check_game_uninstalled}"
            qtutils.show_message_window(self.log, "error", err_msg)

    self.enable_widgets(False)


def reset_all_selected_game_files_btn(self):
    self.enable_widgets(True)
    if self.selected_game is not None:
        self.progressbar.set_values(messages.reseting_files, 25)
        Files(self).download_all_files()
        self.progressbar.set_values(messages.reseting_files, 50)
        utils.download_shaders(self)
        self.progressbar.set_values(messages.reseting_files, 75)
        games_obj = utils.Object()
        games_obj.api = self.selected_game.api
        games_obj.architecture = self.selected_game.architecture
        games_obj.game_name = self.selected_game.name
        games_obj.path = self.selected_game.path
        _apply_single(self, games_obj, True)
        self.progressbar.close()
        qtutils.show_message_window(self.log, "info", messages.reset_success)
    self.enable_widgets(False)


def _get_reshade_dll_name(self, game_dir):
    if self.selected_game.api == constants.OPENGL_DISPLAY_NAME:
        reshade_dll = os.path.join(game_dir, constants.OPENGL_DLL)
        log_file = f"{os.path.splitext(constants.OPENGL_DLL)[0]}.log"
        log_file_path = os.path.join(game_dir, log_file)
    elif self.selected_game.api == constants.DX9_DISPLAY_NAME:
        reshade_dll = os.path.join(game_dir, constants.D3D9_DLL)
        log_file = f"{os.path.splitext(constants.D3D9_DLL)[0]}.log"
        log_file_path = os.path.join(game_dir, log_file)
    else:
        reshade_dll = os.path.join(game_dir, constants.DXGI_DLL)
        log_file = f"{os.path.splitext(constants.DXGI_DLL)[0]}.log"
        log_file_path = os.path.join(game_dir, log_file)

    return [reshade_dll, log_file_path]

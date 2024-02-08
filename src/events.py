# -*- coding: utf-8 -*-
import os
import shutil
from ddcUtils import FileUtils, get_exception, Object
from PyQt6 import QtCore
from PyQt6.QtGui import QDesktopServices
from src.constants import messages, variables
from src.database.dal.config_dal import ConfigDal
from src.database.dal.games_dal import GamesDal
from src.files import Files
from src.tools import file_utils, program_utils, reshade_utils
from src.tools.qt import qt_utils


def donate_clicked():
    href = QtCore.QUrl(variables.PAYPAL_URL)
    QDesktopServices.openUrl(href)


def update_program_clicked():
    href = QtCore.QUrl(variables.GITHUB_LATEST_VERSION_URL)
    QDesktopServices.openUrl(href)


def add_game(self):
    filename_path = qt_utils.open_exe_file_dialog()
    if filename_path is not None:
        file_name, extension = os.path.splitext(os.path.basename(filename_path))
        if extension.lower() == ".exe":
            games_sql = GamesDal(self.db_session, self.log)
            rs_name = games_sql.get_game_by_path(filename_path)
            if len(rs_name) == 0:
                self.selected_game = None
                self.added_game_path = filename_path
                exe_binary_type = FileUtils.get_exe_binary_type(filename_path)
                match exe_binary_type.upper():
                    case "AMD64" | "IA64":
                        architecture = "64bits"
                    case "IA32":
                        architecture = "32bits"
                    case _:
                        qt_utils.show_message_window(self.log, "error", messages.not_valid_game)
                        return

                qt_utils.show_game_config_form(self, file_name, architecture)
            elif rs_name is not None and len(rs_name) > 0:
                qt_utils.show_message_window(self.log,
                                             "error",
                                             f"{messages.game_already_exist}\n\n"
                                             f"{file_name}")
        else:
            qt_utils.show_message_window(self.log, "error", messages.not_valid_game)


def delete_game(self):
    game_not_found = False
    if not file_utils.check_game_file(self):
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
                self.log.error(f"remove_file: {get_exception(e)}")
                qt_utils.show_message_window(self.log,
                                             "error",
                                             f"{messages.error_delete_dll} "
                                             f"{game_name} dll\n\n"
                                             f"{get_exception(e)}")
                self.enable_widgets(False)
                return

        try:
            # remove Reshade.ini
            all_reshade_game_dir_files = file_utils.list_reshade_files(game_dir)
            for f in all_reshade_game_dir_files:
                try:
                    os.remove(f)
                except OSError:
                    pass

            games_sql = GamesDal(self.db_session, self.log)
            games_sql.delete_game(self.selected_game.id)

            if self.show_info_messages:
                if game_not_found:
                    qt_utils.show_message_window(
                        self.log,
                        "info",
                        f"{messages.game_not_in_path_deleted}\n\n"
                        f"{game_name}"
                    )
                else:
                    qt_utils.show_message_window(
                        self.log,
                        "info",
                        f"{messages.game_deleted}"
                        f"\n\n{game_name}"
                    )

            self.populate_table_widget()
        except OSError as e:
            qt_utils.show_message_window(
                self.log,
                "error",
                f"ERROR deleting {game_name} files\n\n"
                f"{get_exception(e)}"
            )

        self.enable_widgets(False)


def edit_selected_game_path(self):
    if self.selected_game is not None:
        old_game_file_path = self.selected_game.path
        new_game_file_path = qt_utils.open_exe_file_dialog()

        if new_game_file_path is not None:
            old_game_dir = os.path.dirname(old_game_file_path)
            new_game_dir = os.path.dirname(new_game_file_path)

            if old_game_file_path == new_game_file_path:
                self.enable_widgets(False)
                if self.show_info_messages:
                    qt_utils.show_message_window(
                        self.log,
                        "info",
                        messages.no_change_path
                    )
                return

            old_file_name, _ = os.path.splitext(os.path.basename(old_game_file_path))
            new_file_name, new_extension = os.path.splitext(os.path.basename(new_game_file_path))
            if old_file_name != new_file_name:
                self.enable_widgets(False)
                qt_utils.show_message_window(
                    self.log,
                    "error",
                    f"{messages.not_same_game}"
                    f"\n\n{old_file_name}"
                )
                return

            if new_extension.lower() != ".exe":
                self.enable_widgets(False)
                qt_utils.show_message_window(
                    self.log,
                    "error",
                    f"{messages.not_valid_game}"
                    f"\n\n{new_file_name}"
                )
                return

            # create Reshade.ini
            self.selected_game.game_dir = new_game_dir
            game_screenshots_path = program_utils.get_screenshot_path(
                self,
                new_game_dir,
                self.selected_game.name
            )
            try:
                files = Files(self)
                files.apply_reshade_ini_file(new_game_dir,
                                             game_screenshots_path)
            except Exception as e:
                self.log.error(f"create_files: {get_exception(e)}")

            # remove dll from game path
            reshade_dll, log_file_path = _get_reshade_dll_name(self, old_game_dir)

            try:
                shutil.move(reshade_dll, os.path.join(new_game_dir, os.path.basename(reshade_dll)))
            except OSError:
                pass

            if os.path.isfile(log_file_path):
                try:
                    os.remove(log_file_path)
                except OSError:
                    pass

            # move all reshade files and remove reshade.ini with old path
            all_old_game_dir_files = file_utils.list_reshade_files(old_game_dir)
            for f in all_old_game_dir_files:
                if os.path.basename(f) == variables.RESHADE_INI or os.path.basename(f).lower().endswith("log"):
                    try:
                        os.remove(f)
                    except OSError:
                        pass
                else:
                    try:
                        shutil.move(f, os.path.join(new_game_dir, os.path.basename(f)))
                    except OSError:
                        pass

            # save into database
            games_sql = GamesDal(self.db_session, self.log)
            game_id = self.selected_game.id
            game_path = new_game_file_path
            games_sql.update_game_path(game_id, game_path)

            if self.show_info_messages:
                qt_utils.show_message_window(self.log,
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
        res_plug_ini_path = str(os.path.join(game_dir, variables.RESHADE_PRESET_INI))

        try:
            if not os.path.isfile(variables.RESHADE_PRESET_PATH):
                create_files = Files(self)
                create_files.download_reshade_preset_file()
        except Exception as e:
            self.log.error(f"create_files: {get_exception(e)}")

        try:
            if not os.path.isfile(res_plug_ini_path) and os.path.isfile(variables.RESHADE_PRESET_PATH):
                shutil.copy2(variables.RESHADE_PRESET_PATH, res_plug_ini_path)
        except Exception as e:
            self.log.error(get_exception(e))

        try:
            FileUtils.open_file(res_plug_ini_path)
        except Exception as e:
            err_msg = f"{get_exception(e)}\n\n" \
                      f"{messages.check_game_uninstalled}"
            qt_utils.show_message_window(self.log, "error", err_msg)

    self.enable_widgets(False)


def edit_default_preset_plugin_button_clicked(self):
    try:
        file_utils.check_local_files(self)
        FileUtils.open_file(variables.RESHADE_PRESET_PATH)
    except Exception as e:
        err_msg = f"{get_exception(e)}\n\n" \
                  f"{variables.RESHADE_PRESET_PATH} {messages.unable_start}"
        qt_utils.show_message_window(self.log, "error", err_msg)


def dark_theme_clicked(self, status):
    if status == "YES":
        self.use_dark_theme = True
        status = True
    else:
        self.use_dark_theme = False
        status = False

    self.set_style_sheet()
    config_sql = ConfigDal(self.db_session, self.log)
    config_sql.update_dark_theme(status)


def check_program_updates_clicked(self, status):
    if status == "YES":
        self.check_program_updates = True
        status = True
    else:
        self.check_program_updates = False
        status = False

    config_sql = ConfigDal(self.db_session, self.log)
    config_sql.update_check_program_updates(status)


def show_info_messages_clicked(self, status):
    if status == "YES":
        self.show_info_messages = True
        status = True
    else:
        self.show_info_messages = False
        status = False

    config_sql = ConfigDal(self.db_session, self.log)
    config_sql.update_show_info_messages(status)


def check_reshade_updates_clicked(self, status):
    if status == "YES":
        self.check_reshade_updates = True
        status = True
    else:
        self.check_reshade_updates = False
        status = False

    config_sql = ConfigDal(self.db_session, self.log)
    config_sql.update_check_resahde_updates(status)


def update_shaders_clicked(self, status):
    if status == "YES":
        self.update_shaders = True
        status = True
    else:
        self.update_shaders = False
        status = False

    config_sql = ConfigDal(self.db_session, self.log)
    config_sql.update_shaders(status)


def create_screenshots_folder_clicked(self, status):
    if status == "YES":
        self.create_screenshots_folder = True
        status = True
    else:
        self.create_screenshots_folder = False
        status = False

    config_sql = ConfigDal(self.db_session, self.log)
    config_sql.update_create_screenshots_folder(status)


def programs_tableWidget_clicked(self, item):
    self.enable_widgets(True)
    # clicked_item = self.qtobj.programs_tableWidget.currentItem()
    clicked_row = self.qtobj.programs_tableWidget.selectedItems()

    self.selected_game = Object()
    # self.selected_game.column = item.column()
    # self.selected_game.row = item.row()
    self.selected_game.name = clicked_row[0].text()
    self.selected_game.architecture = clicked_row[1].text()
    self.selected_game.api = clicked_row[2].text()
    self.selected_game.path = clicked_row[3].text()
    self.selected_game.game_dir = os.path.dirname(self.selected_game.path)

    search_pattern = self.selected_game.name
    games_sql = GamesDal(self.db_session, self.log)
    rs = games_sql.get_game_by_name(search_pattern)
    if rs is not None and len(rs) > 0:
        self.selected_game.id = rs[0].get("id")


def game_config_form_result(self, architecture, status):
    self.game_config_form.close()
    dx9_name = variables.DX9_DISPLAY_NAME
    dxgi_name = variables.DXGI_DISPLAY_NAME
    opengl_name = variables.OPENGL_DISPLAY_NAME

    if status == "OK":
        if self.game_config_form.qtObj.game_name_lineEdit.text() == "":
            qt_utils.show_message_window(self.log, "error", messages.missing_game_name)
            return

        if not self.game_config_form.qtObj.opengl_radioButton.isChecked() \
                and not self.game_config_form.qtObj.dx9_radioButton.isChecked()\
                and not self.game_config_form.qtObj.dx_radioButton.isChecked():
            qt_utils.show_message_window(self.log, "error", messages.missing_api)
            return

        sql_games_dict = {
            "game_name": self.game_config_form.qtObj.game_name_lineEdit.text()
        }

        if architecture == "32bits":
            sql_games_dict["architecture"] = "32bits"
            src_path = variables.RESHADE32_PATH
        else:
            sql_games_dict["architecture"] = "64bits"
            src_path = variables.RESHADE64_PATH

        games_sql = GamesDal(self.db_session, self.log)
        if self.selected_game is not None:
            if self.game_config_form.qtObj.dx9_radioButton.isChecked():
                sql_games_dict["api"] = dx9_name
                dst_path = os.path.join(self.selected_game.game_dir,
                                        variables.D3D9_DLL)
            elif self.game_config_form.qtObj.dx_radioButton.isChecked():
                sql_games_dict["api"] = dxgi_name
                dst_path = os.path.join(self.selected_game.game_dir,
                                        variables.DXGI_DLL)
            else:
                sql_games_dict["api"] = opengl_name
                dst_path = os.path.join(self.selected_game.game_dir,
                                        variables.OPENGL_DLL)

            if (self.selected_game.name != sql_games_dict["game_name"]
                    or (self.selected_game.api != sql_games_dict["api"])):
                # checking name changes
                # create Reshade.ini to replace edit CurrentPresetPath
                old_screenshots_path = program_utils.get_screenshot_path(
                    self,
                    self.selected_game.game_dir,
                    self.selected_game.name
                )
                if len(old_screenshots_path) > 0:
                    scrrenshot_dir_path = os.path.dirname(old_screenshots_path)
                    new_screenshots_path = os.path.join(scrrenshot_dir_path, sql_games_dict["game_name"])
                else:
                    new_screenshots_path = ""

                try:
                    files = Files(self)
                    files.apply_reshade_ini_file(self.selected_game.game_dir, new_screenshots_path)
                except Exception as e:
                    self.log.error(f"download_reshade_ini_file: {get_exception(e)}")

                try:
                    # rename screenshot folder
                    if os.path.isdir(old_screenshots_path):
                        os.rename(old_screenshots_path, new_screenshots_path)
                except OSError as e:
                    self.log.error(f"rename_screenshot_dir: {get_exception(e)}")

                try:
                    # deleting Reshade.dll
                    if self.selected_game.api == dx9_name:
                        d3d9_game_path = os.path.join(self.selected_game.game_dir, variables.D3D9_DLL)
                        if os.path.isfile(d3d9_game_path):
                            os.remove(d3d9_game_path)
                    elif self.selected_game.api == opengl_name:
                        opengl_game_path = os.path.join(self.selected_game.game_dir, variables.OPENGL_DLL)
                        if os.path.isfile(opengl_game_path):
                            os.remove(opengl_game_path)
                    else:
                        dxgi_game_path = os.path.join(self.selected_game.game_dir, variables.DXGI_DLL)
                        if os.path.isfile(dxgi_game_path):
                            os.remove(dxgi_game_path)
                except OSError as e:
                    self.log.error(f"remove_reshade_file: {get_exception(e)}")

                try:
                    # creating Reshade.dll
                    shutil.copy2(src_path, dst_path)
                except shutil.Error as e:
                    self.log.error(f"copyfile: {src_path} to {dst_path} - {get_exception(e)}")

                if self.show_info_messages:
                    qt_utils.show_message_window(
                        self.log,
                        "info",
                        f"{messages.game_updated}\n\n"
                        f"{sql_games_dict['game_name']}"
                    )

            sql_games_dict["id"] = self.selected_game.id
            games_sql.update_game(sql_games_dict)
            self.populate_table_widget()
            self.enable_widgets(False)
        else:
            # new game added
            if self.game_config_form.qtObj.dx9_radioButton.isChecked():
                sql_games_dict["api"] = dx9_name
            elif self.game_config_form.qtObj.opengl_radioButton.isChecked():
                sql_games_dict["api"] = opengl_name
            else:
                sql_games_dict["api"] = dxgi_name

            if self.added_game_path is not None:
                sql_games_dict["path"] = self.added_game_path
            elif self.selected_game is not None:
                sql_games_dict["path"] = self.selected_game.game_dir
            else:
                if self.show_info_messages:
                    qt_utils.show_message_window(
                        self.log,
                        "error",
                        f"{sql_games_dict['game_name']}\n\n"
                        f"{messages.error_change_game_name}"
                    )
                return

            _apply_single(self, sql_games_dict)
            games_sql.insert_game(sql_games_dict)
            del self.added_game_path
            self.populate_table_widget()
            self.enable_widgets(False)
            if self.show_info_messages:
                qt_utils.show_message_window(self.log,
                                             "info",
                                             f"{messages.game_added}\n\n"
                                             f"{sql_games_dict['game_name']}")


def apply_all(self, reset=False):
    games_sql = GamesDal(self.db_session, self.log)
    rs_all_games = games_sql.get_all_games()
    len_games = len(rs_all_games)
    if len_games > 0:
        self.enable_form(False)
        self.enable_widgets(False)
        self.qtobj.apply_button.setEnabled(False)
        errors = []
        self.progressbar.set_values(messages.copying_DLLs, 0)
        for i in range(len_games):
            self.progressbar.set_values(messages.copying_DLLs, 100 // len_games)
            len_games = len_games - 1
            games_dict = {
                "api": rs_all_games[i]["api"],
                "architecture": rs_all_games[i]["architecture"],
                "game_name": rs_all_games[i]["name"],
                "path": rs_all_games[i]["path"]
            }
            result = _apply_single(self, games_dict, reset)
            if result is not None:
                errors.append(result)

        self.progressbar.close()
        self.enable_form(True)
        self.qtobj.apply_button.setEnabled(True)

        if len(errors) == 0 and self.need_apply is False and self.show_info_messages:
            qt_utils.show_message_window(self.log, "info", messages.apply_success)
        elif len(errors) > 0:
            err = "\n".join(errors)
            qt_utils.show_message_window(self.log,
                                         "error",
                                         f"{messages.apply_success_with_errors}\n\n"
                                         f"{err}")


def _apply_single(self, games_dict, reset=False):
    errors = None
    game_dir = os.path.dirname(games_dict["path"])
    game_name = games_dict["game_name"]
    file_utils.check_local_files(self)
    files = Files(self)

    if games_dict["architecture"].lower() == "32bits":
        src_dll_path = variables.RESHADE32_PATH
    else:
        src_dll_path = variables.RESHADE64_PATH

    if not os.path.isfile(src_dll_path):
        file_utils.unzip_reshade(self, self.local_reshade_path)

    try:
        # Reshade.dll
        if os.path.isfile(src_dll_path) or reset:
            if games_dict["api"] == variables.DX9_DISPLAY_NAME:
                dst_dll_path = os.path.join(game_dir, variables.D3D9_DLL)
            elif games_dict["api"] == variables.OPENGL_DISPLAY_NAME:
                dst_dll_path = os.path.join(game_dir, variables.OPENGL_DLL)
            else:
                dst_dll_path = os.path.join(game_dir, variables.DXGI_DLL)
            ret = files.apply_reshade_dll_file(src_dll_path, dst_dll_path)
            if ret is not None:
                self.log.error(f"[{game_name}]:[{str(ret)}]")

        # Reshade.ini
        dst_res_ini_path = os.path.join(game_dir, variables.RESHADE_INI)
        if os.path.isfile(variables.RESHADE_INI_PATH) and not os.path.isfile(dst_res_ini_path) or reset:
            game_screenshots_path = program_utils.get_screenshot_path(self, game_dir, game_name)
            ret = files.apply_reshade_ini_file(game_dir, game_screenshots_path)
            if ret is not None:
                self.log.error(f"[{game_name}]:[{str(ret)}]")

        # ReShadePreset.ini
        dst_preset_path = os.path.join(game_dir, variables.RESHADE_PRESET_INI)
        if os.path.isfile(variables.RESHADE_PRESET_PATH) and not os.path.isfile(dst_preset_path) or reset:
            ret = files.apply_reshade_preset_file(game_dir)
            if ret is not None:
                self.log.error(f"[{game_name}]:[{str(ret)}]")
            if isinstance(ret, FileNotFoundError):
                errors = f"[{game_name}]: No such file or directory"

    except Exception as e:
        self.log.error(f"[{game_name}]:[{get_exception(e)}]")
        errors = f"[{game_name}]: {get_exception(e)}"

    return errors


def open_selected_game_location(self):
    self.enable_widgets(True)
    if self.selected_game is not None:
        game_dir = os.path.dirname(self.selected_game.path)

        try:
            FileUtils.open_file(game_dir)
        except Exception as e:
            err_msg = f"{get_exception(e)}\n\n" \
                      f"{messages.check_game_uninstalled}"
            qt_utils.show_message_window(self.log, "error", err_msg)

    self.enable_widgets(False)


def reset_all_button_clicked(self):
    self.progressbar.set_values(messages.reseting_files, 25)
    Files(self).download_all_files()
    self.progressbar.set_values(messages.reseting_files, 50)
    reshade_utils.download_shaders(self)
    self.progressbar.set_values(messages.reseting_files, 75)
    apply_all(self, reset=True)
    self.progressbar.close()
    qt_utils.show_message_window(self.log, "info", messages.reset_success)


def reset_all_selected_game_files_btn(self):
    self.enable_widgets(True)
    if self.selected_game is not None:
        self.progressbar.set_values(messages.reseting_game_files, 25)
        files = Files(self)
        files.download_reshade_files(self.selected_game.game_dir)
        self.progressbar.set_values(messages.reseting_game_files, 50)
        reshade_utils.download_shaders(self)
        self.progressbar.set_values(messages.reseting_game_files, 75)
        games_dict = {
            "api": self.selected_game.api,
            "architecture": self.selected_game.architecture,
            "game_name": self.selected_game.name,
            "path": self.selected_game.path
        }
        res = _apply_single(self, games_dict, True)
        self.progressbar.close()
        if res:
            qt_utils.show_message_window(self.log, "info", messages.reset_success)
    self.enable_widgets(False)


def _get_reshade_dll_name(self, game_dir):
    if self.selected_game.api == variables.OPENGL_DISPLAY_NAME:
        reshade_dll = os.path.join(game_dir, variables.OPENGL_DLL)
        log_file = f"{os.path.splitext(variables.OPENGL_DLL)[0]}.log"
        log_file_path = os.path.join(game_dir, log_file)
    elif self.selected_game.api == variables.DX9_DISPLAY_NAME:
        reshade_dll = os.path.join(game_dir, variables.D3D9_DLL)
        log_file = f"{os.path.splitext(variables.D3D9_DLL)[0]}.log"
        log_file_path = os.path.join(game_dir, log_file)
    else:
        reshade_dll = os.path.join(game_dir, variables.DXGI_DLL)
        log_file = f"{os.path.splitext(variables.DXGI_DLL)[0]}.log"
        log_file_path = os.path.join(game_dir, log_file)
    return [reshade_dll, log_file_path]

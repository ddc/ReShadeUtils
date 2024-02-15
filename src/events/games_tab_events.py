# -*- coding: utf-8 -*-
import os
import shutil
from ddcUtils import FileUtils, get_exception
from PyQt6 import QtCore
from PyQt6.QtGui import QDesktopServices
from src.constants import messages, variables
from src.database.dal.config_dal import ConfigDal
from src.database.dal.games_dal import GamesDal
from src.tools import program_utils, reshade_utils
from src.tools.qt import qt_utils
from src.tools.qt.progressbar import ProgressBar
from src.events import edit_form_events


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

                edit_form_events.show_game_config_form(self, file_name, architecture)
            elif rs_name is not None and len(rs_name) > 0:
                qt_utils.show_message_window(self.log, "error",
                                             f"{messages.game_already_exist}\n\n"
                                             f"{file_name}")
        else:
            qt_utils.show_message_window(self.log, "error", messages.not_valid_game)


def delete_game(self):
    game_not_found = False
    if not reshade_utils.check_game_path_exists(self):
        game_not_found = True

    # self.enable_widgets(True)
    if self.selected_game is not None:
        game_dir = os.path.dirname(self.selected_game.path)
        game_name = self.selected_game.name

        # remove dll from game path
        reshade_dll, log_file_path = reshade_utils.get_reshade_dll_name(self, game_dir)
        FileUtils.remove(log_file_path)
        FileUtils.remove(str(os.path.join(game_dir, variables.RESHADE_INI)))
        FileUtils.remove(str(os.path.join(game_dir, variables.RESHADE_PRESET_INI)))
        FileUtils.remove(str(os.path.join(game_dir, variables.RESHADEGUI_INI)))
        if not FileUtils.remove(reshade_dll):
            self.log.error(f"remove_file: {reshade_dll}")
            qt_utils.show_message_window(self.log, "error",
                                         f"{messages.error_delete_dll}\n\n"
                                         f"{game_name} dll")
            self.enable_widgets(False)
            return

        try:
            games_sql = GamesDal(self.db_session, self.log)
            games_sql.delete_game(self.selected_game.id)

            if self.show_info_messages:
                if game_not_found:
                    qt_utils.show_message_window(self.log, "info",
                                                 f"{messages.game_not_in_path_deleted}\n\n"
                                                 f"{game_name}")
                else:
                    qt_utils.show_message_window(self.log, "info",
                                                 f"{messages.game_deleted}\n\n"
                                                 f"{game_name}")

            self.populate_games_tab()
        except OSError as e:
            qt_utils.show_message_window(self.log, "error",
                                         f"ERROR deleting {game_name} files\n\n"
                                         f"{get_exception(e)}")

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
                    qt_utils.show_message_window(self.log, "info", messages.no_change_path)
                return

            old_file_name, _ = os.path.splitext(os.path.basename(old_game_file_path))
            new_file_name, new_extension = os.path.splitext(os.path.basename(new_game_file_path))
            if old_file_name != new_file_name:
                self.enable_widgets(False)
                qt_utils.show_message_window(self.log, "error",
                                             f"{messages.not_same_game}\n\n"
                                             f"{old_file_name}")
                return

            if new_extension.lower() != ".exe":
                self.enable_widgets(False)
                qt_utils.show_message_window(self.log, "error",
                                             f"{messages.not_valid_game}\n\n"
                                             f"{new_file_name}")
                return

            # create Reshade.ini
            self.selected_game.game_dir = new_game_dir
            game_screenshots_path = program_utils.get_screenshot_path(self, new_game_dir, self.selected_game.name)
            try:
                reshade_utils.apply_reshade_ini_file(new_game_dir, game_screenshots_path)
            except Exception as e:
                self.log.error(f"create_files: {get_exception(e)}")

            # remove dll from game path
            reshade_dll, log_file_path = reshade_utils.get_reshade_dll_name(self, old_game_dir)

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
            all_old_game_dir_files = FileUtils.list_files(directory=old_game_dir, starts_with="reshade")
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
                qt_utils.show_message_window(self.log, "info",
                                             f"{messages.path_changed_success}\n\n"
                                             f"{new_game_file_path}")

        self.log.info(f"{messages.path_changed_success}:{new_game_file_path}")
        self.populate_games_tab()
        self.enable_widgets(False)


def edit_selected_game_plugin_config_file(self):
    self.enable_widgets(True)
    if self.selected_game is not None:
        game_dir = os.path.dirname(self.selected_game.path)
        res_plug_ini_path = str(os.path.join(game_dir, variables.RESHADE_PRESET_INI))

        try:
            if not os.path.isfile(variables.RESHADE_PRESET_PATH):
                reshade_utils.download_reshade_preset_file()
        except Exception as e:
            self.log.error(f"create_files: {get_exception(e)}")

        try:
            if not os.path.isfile(res_plug_ini_path) and os.path.isfile(variables.RESHADE_PRESET_PATH):
                shutil.copy2(variables.RESHADE_PRESET_PATH, res_plug_ini_path)
        except Exception as e:
            self.log.error(get_exception(e))

        try:
            FileUtils.show(res_plug_ini_path)
        except Exception as e:
            err_msg = (f"{get_exception(e)}\n\n"
                       f"{messages.check_game_uninstalled}")
            qt_utils.show_message_window(self.log, "error", err_msg)

    self.enable_widgets(False)


def get_selected_game(qtobj, item=None):
    """
    Called when a game is double-clicked
    clicked_item = qtobj.programs_tableWidget.currentItem()
    clicked_row = qtobj.programs_tableWidget.selectedItems()
    :param qtobj:
    :param item:
    :return:
    """

    class SelectedGame:
        def __init__(self):
            self.id = None
            self.column = None
            self.row = None
            self.name = None
            self.architecture = None
            self.api = None
            self.path = None
            self.game_dir = None

    selected_game = SelectedGame()

    if item:
        selected_game.column = item.column()
        selected_game.row = item.row()

    clicked_row = qtobj.programs_tableWidget.selectedItems()
    selected_game.name = clicked_row[0].text()
    selected_game.architecture = clicked_row[1].text()
    selected_game.api = clicked_row[2].text()
    selected_game.path = clicked_row[3].text()
    selected_game.game_dir = os.path.dirname(selected_game.path)
    return selected_game


def game_clicked(log, qtobj, item):
    """
    Called when a game is clicked
    :param log:
    :param qtobj:
    :param item:
    :return:
    """

    qt_utils.enable_widgets(qtobj, True)
    selected_game = get_selected_game(qtobj, item)
    log.debug(f"game_clicked: {selected_game.name}")


def apply_all_clicked(db_session, log, qtobj):
    errors = apply_all(db_session, log, qtobj)
    config_sql = ConfigDal(db_session, log)
    rs_config = config_sql.get_configs()
    if len(errors) == 0 and rs_config is not None and rs_config[0]["show_info_messages"]:
        qt_utils.show_message_window(log, "info", messages.apply_success)
    else:
        err = "\n".join(errors)
        qt_utils.show_message_window(log, "error",
                                     f"{messages.apply_success_with_errors}\n\n"
                                     f"{err}")


def apply_all(db_session, log, qtobj, reset=False):
    progressbar = ProgressBar(log=log)
    errors = []
    games_sql = GamesDal(db_session, log)
    rs_all_games = games_sql.get_all_games()
    len_games = len(rs_all_games)
    if len_games > 0:
        qt_utils.enable_form(qtobj, False)
        qt_utils.enable_widgets(qtobj, False)
        qtobj.apply_button.setEnabled(False)
        progressbar.set_values(messages.copying_DLLs, 0)
        for i in range(len_games):
            progressbar.set_values(messages.copying_DLLs, 100 // len_games)
            len_games = len_games - 1
            games_dict = {
                "api": rs_all_games[i]["api"],
                "architecture": rs_all_games[i]["architecture"],
                "game_name": rs_all_games[i]["name"],
                "path": rs_all_games[i]["path"]
            }
            err_result = apply_single(db_session, log, games_dict, reset)
            if err_result:
                errors.append(err_result)

        progressbar.close()
        qt_utils.enable_form(qtobj, True)
        qtobj.apply_button.setEnabled(True)

    return errors


def apply_single(db_session, log, games_dict, reset=False):
    errors = None
    game_dir = os.path.dirname(games_dict["path"])
    game_name = games_dict["game_name"]

    match games_dict["architecture"]:
        case "32bits":
            src_dll_path = variables.RESHADE32_PATH
        case _:
            src_dll_path = variables.RESHADE64_PATH

    try:
        # Reshade.dll
        if os.path.isfile(src_dll_path) or reset:
            match games_dict["api"]:
                case variables.DX9_DISPLAY_NAME:
                    dst_dll_path = os.path.join(game_dir, variables.D3D9_DLL)
                case variables.OPENGL_DISPLAY_NAME:
                    dst_dll_path = os.path.join(game_dir, variables.OPENGL_DLL)
                case _:
                    dst_dll_path = os.path.join(game_dir, variables.DXGI_DLL)

            try:
                FileUtils.copy(src_dll_path, dst_dll_path)
            except Exception as e:
                log.error(f"[{game_name}]:[{get_exception(e)}]")

        # Reshade.ini
        dst_res_ini_path = os.path.join(game_dir, variables.RESHADE_INI)
        if os.path.isfile(variables.RESHADE_INI_PATH) and not os.path.isfile(dst_res_ini_path) or reset:
            game_screenshots_path = program_utils.get_screenshot_path(db_session, log, game_dir, game_name)
            ret = reshade_utils.apply_reshade_ini_file(game_dir, game_screenshots_path)
            if ret is not None:
                log.error(f"[{game_name}]:[{str(ret)}]")

        # ReShadePreset.ini
        dst_preset_path = os.path.join(game_dir, variables.RESHADE_PRESET_INI)
        if os.path.isfile(variables.RESHADE_PRESET_PATH) and not os.path.isfile(dst_preset_path) or reset:
            try:
                FileUtils.copy(variables.RESHADE_PRESET_PATH, game_dir)
            except FileNotFoundError:
                errors = f"[{game_name}]: No such file or directory"
            except Exception as e:
                log.error(f"[{game_name}]:[{get_exception(e)}]")

    except Exception as e:
        log.error(f"[{game_name}]:[{get_exception(e)}]")
        errors = f"[{game_name}]: {get_exception(e)}"

    return errors


def open_selected_game_location(self):
    self.enable_widgets(True)
    if self.selected_game is not None:
        game_dir = os.path.dirname(self.selected_game.path)
        res = FileUtils.show(game_dir)
        if not res:
            qt_utils.show_message_window(self.log, "error", messages.check_game_uninstalled)
    self.enable_widgets(False)


def reset_selected_game_files_button(db_session, log, qtobj, item):
    log.debug("reset_selected_game_files_button")
    progressbar = ProgressBar(log=log)
    progressbar.set_values(messages.reseting_game_files, 25)
    selected_game = get_selected_game(qtobj, item)
    games_dict = {
        "api": selected_game.api,
        "architecture": selected_game.architecture,
        "game_name": selected_game.name,
        "path": selected_game.path
    }
    result = apply_single(db_session, log, games_dict, True)
    progressbar.close()
    if result is None:
        qt_utils.show_message_window(log, "info", messages.reset_success)
    qt_utils.enable_widgets(qtobj, False)

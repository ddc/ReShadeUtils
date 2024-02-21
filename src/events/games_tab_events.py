# -*- coding: utf-8 -*-
import os
import shutil
from ddcUtils import FileUtils, get_exception
from PyQt6 import QtCore
from PyQt6.QtGui import QDesktopServices
from src.constants import messages, variables
from src.database.dal.config_dal import ConfigDal
from src.database.dal.games_dal import GamesDal
from src.events import edit_form_events
from src.tools import program_utils, reshade_utils
from src.tools.qt import qt_utils
from src.tools.qt.progressbar import ProgressBar


def update_program_clicked():
    href = QtCore.QUrl(variables.GITHUB_LATEST_VERSION_URL)
    QDesktopServices.openUrl(href)


def get_selected_game(db_session, log, qtobj, item=None):
    """
    Called when a game is double-clicked
    clicked_item = qtobj.programs_table_widget.currentItem()
    clicked_row = qtobj.programs_table_widget.selectedItems()
    :param db_session:
    :param log:
    :param qtobj:
    :param item:
    :return:
    """

    selected_game = {
        "id": None,
        "row": None,
        "column": None,
        "name": None,
        "architecture": None,
        "api": None,
        "path": None,
        "dir": None,
        "dll": None,
        "dll_path": None
    }

    if item:
        selected_game["column"] = item.column()
        selected_game["row"] = item.row()

    clicked_row = qtobj.programs_table_widget.selectedItems()
    selected_game["name"] = clicked_row[0].text()
    selected_game["architecture"] = clicked_row[1].text()
    selected_game["api"] = clicked_row[2].text()
    selected_game["dll"] = clicked_row[3].text()
    selected_game["path"] = clicked_row[4].text()
    selected_game["dir"] = str(os.path.dirname(selected_game["path"]))
    selected_game["dll_path"] = str(os.path.join(selected_game["dir"], selected_game["dll"]))
    games_sql = GamesDal(db_session, log)
    db_game_result = games_sql.get_game_by_name_and_path(selected_game["name"], selected_game["path"])
    if db_game_result:
        selected_game["id"] = db_game_result["id"]
    return selected_game


def add_game(db_session, log, qtobj):
    log.debug("add_game")
    filename_path = qt_utils.open_exe_file_dialog()
    if filename_path is not None:
        file_name, extension = os.path.splitext(os.path.basename(filename_path))
        if extension.lower() == ".exe":
            games_sql = GamesDal(db_session, log)
            rs_name = games_sql.get_game_by_path(filename_path)
            if not rs_name:
                edit_form_events.show_game_config_form_insert(db_session, log, qtobj, filename_path)
            elif rs_name is not None and len(rs_name) > 0:
                qt_utils.show_message_window(log, "error", f"{messages.game_already_exist}\n\n{file_name}")
        else:
            qt_utils.show_message_window(log, "error", messages.not_valid_game)


def delete_game(db_session, log, qtobj, item):
    log.debug("delete_game")
    selected_game = get_selected_game(db_session, log, qtobj, item)
    game_dir = os.path.dirname(selected_game["path"])
    game_name = selected_game["name"]
    game_found = True if reshade_utils.check_game_path_exists(selected_game["path"]) else False

    if selected_game is not None:
        try:
            reshade_dll, log_file = reshade_utils.get_reshade_dll_log_names(selected_game["api"])
            game_dll_path = os.path.join(game_dir, reshade_dll)
            log_file_path = os.path.join(game_dir, log_file)

            if os.path.exists(game_dll_path):
                if not FileUtils.remove(str(game_dll_path)):
                    log.error(f"remove_file: {game_dll_path}")
                    qt_utils.show_message_window(log, "error", f"{messages.error_delete_dll}\n\n{game_name} dll")
                    qt_utils.enable_widgets(qtobj, False)
                    return

            FileUtils.remove(str(log_file_path))
            FileUtils.remove(str(os.path.join(game_dir, variables.RESHADE_INI)))
            FileUtils.remove(str(os.path.join(game_dir, variables.RESHADE_PRESET_INI)))
            FileUtils.remove(str(os.path.join(game_dir, variables.RESHADEGUI_INI)))

            games_sql = GamesDal(db_session, log)
            games_sql.delete_game(selected_game["id"])

            qt_utils.populate_games_tab(db_session, log, qtobj)
            qt_utils.enable_widgets(qtobj, False)

            config_sql = ConfigDal(db_session, log)
            conf_res = config_sql.get_configs()
            if conf_res[0]["show_info_messages"]:
                if game_found:
                    qt_utils.show_message_window(log, "info", f"{messages.game_not_in_path_deleted}\n\n{game_name}")
                else:
                    qt_utils.show_message_window(log, "info", f"{messages.game_deleted}\n\n{game_name}")
        except OSError as e:
            qt_utils.show_message_window(log, "error", f"ERROR deleting {game_name} files\n\n{get_exception(e)}")


def edit_selected_game_plugin_config_file(db_session, log, qtobj, item):
    log.debug("edit_selected_game_plugin_config_file")
    qt_utils.enable_widgets(qtobj, True)

    selected_game = get_selected_game(db_session, log, qtobj, item)
    game_dir = os.path.dirname(selected_game["path"])
    res_plug_ini_path = str(os.path.join(game_dir, variables.RESHADE_PRESET_INI))

    try:
        if not os.path.isfile(variables.RESHADE_PRESET_PATH):
            reshade_utils.download_reshade_preset_file()
    except Exception as e:
        log.error(f"create_files: {get_exception(e)}")

    try:
        if not os.path.isfile(res_plug_ini_path) and os.path.isfile(variables.RESHADE_PRESET_PATH):
            shutil.copy2(variables.RESHADE_PRESET_PATH, res_plug_ini_path)
    except Exception as e:
        log.error(get_exception(e))

    try:
        FileUtils.show(res_plug_ini_path)
    except Exception as e:
        err_msg = f"{get_exception(e)}\n\n{messages.check_game_uninstalled}"
        qt_utils.show_message_window(log, "error", err_msg)

    qt_utils.enable_widgets(qtobj, False)


def edit_selected_game_path(db_session, log, qtobj, item):
    log.debug("edit_selected_game_path")
    selected_game = get_selected_game(db_session, log, qtobj, item)

    config_sql = ConfigDal(db_session, log)
    rs_config = config_sql.get_configs()
    show_info_messages = rs_config[0]["show_info_messages"]

    old_game_file_path = selected_game["path"]
    new_game_file_path = qt_utils.open_exe_file_dialog()

    if new_game_file_path is not None:
        old_game_dir = os.path.dirname(old_game_file_path)
        new_game_dir = os.path.dirname(new_game_file_path)

        if old_game_file_path == new_game_file_path:
            qt_utils.enable_widgets(qtobj, False)
            if show_info_messages:
                qt_utils.show_message_window(log, "info", messages.no_change_path)
            return

        old_file_name, _ = os.path.splitext(os.path.basename(old_game_file_path))
        new_file_name, new_extension = os.path.splitext(os.path.basename(new_game_file_path))
        if old_file_name != new_file_name:
            qt_utils.enable_widgets(qtobj, False)
            qt_utils.show_message_window(log, "error", f"{messages.not_same_game}\n\n{old_file_name}")
            return

        if new_extension.lower() != ".exe":
            qt_utils.enable_widgets(qtobj, False)
            qt_utils.show_message_window(log, "error", f"{messages.not_valid_game}\n\n{new_file_name}")
            return

        # create Reshade.ini
        selected_game["dir"] = new_game_dir
        game_screenshots_path = program_utils.get_screenshot_path(db_session, log, new_game_dir, selected_game["name"])
        try:
            reshade_utils.apply_reshade_ini_file(new_game_dir, game_screenshots_path)
        except Exception as e:
            log.error(f"create_files: {get_exception(e)}")

        # remove dll from game path
        reshade_dll, log_file_path = reshade_utils.get_reshade_dll_log_names(selected_game["api"])

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
        games_sql = GamesDal(db_session, log)
        game_id = selected_game["id"]
        game_path = new_game_file_path
        games_sql.update_game_path(game_id, game_path)

        if show_info_messages:
            qt_utils.show_message_window(log, "info", f"{messages.path_changed_success}\n\n{new_game_file_path}")

    log.info(f"{messages.path_changed_success}:{new_game_file_path}")
    qt_utils.populate_games_tab(db_session, log, qtobj)
    qt_utils.enable_widgets(qtobj, False)


def game_clicked(db_session, log, qtobj, item):
    """
    Called when a game is clicked
    :param db_session:
    :param log:
    :param qtobj:
    :param item:
    :return:
    """

    qt_utils.enable_widgets(qtobj, True)
    selected_game = get_selected_game(db_session, log, qtobj, item)
    log.debug(f"game_clicked: {selected_game['name']}")


def apply_all_clicked(db_session, log, qtobj):
    log.debug("apply_all_clicked")
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
    log.debug("apply_all")
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
            game_dict = {
                "api": rs_all_games[i]["api"],
                "architecture": rs_all_games[i]["architecture"],
                "name": rs_all_games[i]["name"],
                "path": rs_all_games[i]["path"]
            }
            err_result = apply_single(db_session, log, game_dict, reset)
            if err_result:
                errors.append(err_result)

        progressbar.close()
        qt_utils.enable_form(qtobj, True)
        qtobj.apply_button.setEnabled(True)

    return errors


def apply_single(db_session, log, game_dict, reset=False):
    errors = None
    game_dir = os.path.dirname(game_dict["path"])
    game_name = game_dict["name"]
    log.debug(f"apply_single: {game_name}")

    match game_dict["architecture"]:
        case "32bits":
            src_dll_path = variables.RESHADE32_PATH
        case _:
            src_dll_path = variables.RESHADE64_PATH

    try:
        # Reshade.dll
        if os.path.isfile(src_dll_path) or reset:
            match game_dict["api"]:
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


def open_selected_game_location(db_session, log, qtobj, item):
    log.debug("open_selected_game_location")
    qt_utils.enable_widgets(qtobj, True)
    selected_game = get_selected_game(db_session, log, qtobj, item)
    game_dir = os.path.dirname(selected_game["path"])
    res = FileUtils.show(game_dir)
    if not res:
        qt_utils.show_message_window(log, "error", messages.check_game_uninstalled)
    qt_utils.enable_widgets(qtobj, False)


def reset_selected_game_files_button(db_session, log, qtobj, item):
    log.debug("reset_selected_game_files_button")
    progressbar = ProgressBar(log=log)
    progressbar.set_values(messages.reseting_game_files, 25)
    selected_game = get_selected_game(db_session, log, qtobj, item)
    game_dict = {
        "api": selected_game["api"],
        "architecture": selected_game["architecture"],
        "name": selected_game["name"],
        "path": selected_game["path"]
    }
    result = apply_single(db_session, log, game_dict, True)
    progressbar.close()
    if result is None:
        qt_utils.show_message_window(log, "info", messages.reset_success)
    qt_utils.enable_widgets(qtobj, False)

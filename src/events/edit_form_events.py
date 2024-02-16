# -*- coding: utf-8 -*-
import os
import shutil
from ddcUtils import get_exception
from PyQt6 import QtWidgets
from src.constants import messages, variables
from src.database.dal.config_dal import ConfigDal
from src.database.dal.games_dal import GamesDal
from src.edit_form import UiEditForm
from src.events import games_tab_events
from src.tools import program_utils, reshade_utils
from src.tools.qt import qt_utils


def _create_edit_form_widget():
    game_edit_form = QtWidgets.QWidget()
    qt_obj = UiEditForm()
    qt_obj.setup_ui(game_edit_form)
    game_edit_form.components = qt_obj
    return game_edit_form


def show_game_config_form_insert(db_session, log, main_qtobj):
    log.debug("show_game_config_form_insert")
    game_edit_form = _create_edit_form_widget()

    if not game_edit_form.components.opengl_radio_button.isChecked() \
            and not game_edit_form.components.dx9_radio_button.isChecked()\
            and not game_edit_form.components.dxgi_radio_button.isChecked():
        qt_utils.show_message_window(log, "error", messages.missing_api)
        return

    if added_game_path is not None:
        edit_form_result["path"] = added_game_path
    elif selected_game is not None:
        edit_form_result["path"] = selected_game.dir
    else:
        if show_info_messages:
            qt_utils.show_message_window(log, "error",
                                         f"{edit_form_result['name']}\n\n"
                                         f"{messages.error_change_game_name}")
        return

    result = games_tab_events.apply_single(self, edit_form_result)
    if result is None:
        games_sql.insert_game(edit_form_result)
        if show_info_messages:
            qt_utils.show_message_window(log, "info",
                                         f"{messages.game_added}\n\n"
                                         f"{edit_form_result['name']}")


def show_game_config_form_update(db_session, log, main_qtobj, item):
    log.debug("show_game_config_form_update")

    selected_game = games_tab_events.get_selected_game(main_qtobj, item)
    if not reshade_utils.check_game_path_exists(selected_game.path):
        qt_utils.show_message_window(log, "error", messages.error_game_not_found)
        return

    game_edit_form = _create_edit_form_widget()

    show_info_messages = True
    config_sql = ConfigDal(db_session, log)
    rs_config = config_sql.get_configs()
    if rs_config:
        show_info_messages = rs_config[0]["show_info_messages"]
        if rs_config[0]["use_dark_theme"]:
            game_edit_form.setStyleSheet(open(variables.QSS_PATH, "r").read())

    game_edit_form.components.game_name_line_edit.setFocus()
    game_edit_form.show()
    QtWidgets.QApplication.processEvents()

    game_edit_form.components.game_name_line_edit.setText(selected_game.name)
    match selected_game.api:
        case variables.DX9_DISPLAY_NAME:
            game_edit_form.components.dx9_radio_button.setChecked(True)
            game_edit_form.components.dxgi_radio_button.setChecked(False)
            game_edit_form.components.opengl_radio_button.setChecked(False)
        case variables.OPENGL_DISPLAY_NAME:
            game_edit_form.components.dx9_radio_button.setChecked(False)
            game_edit_form.components.dxgi_radio_button.setChecked(False)
            game_edit_form.components.opengl_radio_button.setChecked(True)
        case _:
            game_edit_form.components.dx9_radio_button.setChecked(False)
            game_edit_form.components.dxgi_radio_button.setChecked(True)
            game_edit_form.components.opengl_radio_button.setChecked(False)

    kwargs = {
        "show_info_messages": show_info_messages,
        "selected_game": selected_game,
    }

    game_edit_form.components.ok_push_button.clicked.connect(lambda: _game_config_form_result_ok(db_session, log, main_qtobj, game_edit_form, **kwargs))
    game_edit_form.components.cancel_push_button.clicked.connect(lambda: _game_config_form_result_cancel(log, game_edit_form))


def _game_config_form_result_cancel(log, game_edit_form):
    log.debug("_game_config_form_result_cancel")
    game_edit_form.close()


def _game_config_form_result_ok(db_session, log, main_qtobj, game_edit_form, **kwargs):
    log.debug("game_config_form_result: OK")
    game_edit_form.close()

    show_info_messages = kwargs["show_info_messages"]
    selected_game = kwargs["selected_game"]

    if game_edit_form.components.game_name_line_edit.text() == "":
        qt_utils.show_message_window(log, "error", messages.missing_game_name)
        return

    if game_edit_form.components.dx9_radio_button.isChecked():
        dll_name = variables.D3D9_DLL
        api = variables.DX9_DISPLAY_NAME
    elif game_edit_form.components.dxgi_radio_button.isChecked():
        dll_name = variables.DXGI_DLL
        api = variables.DXGI_DISPLAY_NAME
    else:
        dll_name = variables.OPENGL_DLL
        api = variables.OPENGL_DISPLAY_NAME

    edit_form_result = {
        "api": api,
        "name": game_edit_form.components.game_name_line_edit.text(),
    }

    if (selected_game.name != edit_form_result["name"]) or (selected_game.api != edit_form_result["api"]):
        match selected_game.architecture:
            case "32bits":
                edit_form_result["architecture"] = "32bits"
                src_path = variables.RESHADE32_PATH
            case _:
                edit_form_result["architecture"] = "64bits"
                src_path = variables.RESHADE64_PATH

        dll_dst_path = os.path.join(selected_game.dir, dll_name)

        games_sql = GamesDal(db_session, log)
        db_game_result = games_sql.get_game_by_name_and_path(selected_game.name, selected_game.path)
        if db_game_result:
            edit_form_result["id"] = db_game_result["id"]

        new_screenshots_path = ""
        old_screenshots_path = program_utils.get_screenshot_path(db_session, log, selected_game.dir, selected_game.name)
        if len(old_screenshots_path) > 0:
            scrrenshot_dir_path = os.path.dirname(old_screenshots_path)
            new_screenshots_path = os.path.join(scrrenshot_dir_path, edit_form_result["name"])

        try:
            # creating reshade.ini file inside game dir
            reshade_utils.apply_reshade_ini_file(selected_game.dir, new_screenshots_path)
        except Exception as e:
            log.error(f"download_reshade_ini_file: {get_exception(e)}")

        try:
            # rename screenshot folder
            if os.path.isdir(old_screenshots_path):
                os.rename(old_screenshots_path, new_screenshots_path)
        except OSError as e:
            log.error(f"rename_screenshot_dir: {get_exception(e)}")

        try:
            # deleting Reshade.dll
            if os.path.isfile(dll_dst_path):
                os.remove(dll_dst_path)
        except OSError as e:
            log.error(f"remove_reshade_file: {get_exception(e)}")

        try:
            # copying Reshade.dll
            shutil.copy2(str(src_path), str(dll_dst_path))
        except shutil.Error as e:
            log.error(f"copyfile: {src_path} to {dll_dst_path} - {get_exception(e)}")

        if show_info_messages:
            qt_utils.show_message_window(log, "info",
                                         f"{messages.game_updated}\n\n"
                                         f"{edit_form_result['name']}")

        games_sql.update_game(edit_form_result)

    qt_utils.populate_games_tab(db_session, log, main_qtobj)
    qt_utils.enable_widgets(main_qtobj, False)

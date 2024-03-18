# -*- coding: utf-8 -*-
import os
import shutil
from ddcUtils import FileUtils, get_exception
from PyQt6 import QtWidgets
from src.constants import messages, variables
from src.database.dal.config_dal import ConfigDal
from src.database.dal.games_dal import GamesDal
from src.edit_form import UiEditForm
from src.events import games_tab_events
from src.tools import program_utils, reshade_utils
from src.tools.qt import qt_utils


def _create_edit_form_widget(db_session, log):
    edit_form = QtWidgets.QWidget()
    qt_obj = UiEditForm()
    qt_obj.setup_ui(edit_form)
    qt_obj.game_name_line_edit.setFocus()
    edit_form.qtobj = qt_obj
    edit_form.show()
    QtWidgets.QApplication.processEvents()

    config_sql = ConfigDal(db_session, log)
    rs_config = config_sql.get_configs()
    if rs_config and rs_config[0]["use_dark_theme"]:
        edit_form.setStyleSheet(open(variables.QSS_PATH, "r").read())
    return edit_form


def _game_config_form_result_cancel(log, game_edit_form):
    log.debug("_game_config_form_result_cancel")
    game_edit_form.close()


def _game_config_form_result_success(db_session, log, main_qtobj, game_name):
    qt_utils.populate_games_tab(db_session, log, main_qtobj)
    qt_utils.enable_widgets(main_qtobj, False)
    if program_utils.show_info_messages(db_session, log):
        qt_utils.show_message_window(log, "info", f"{messages.game_added}\n\n{game_name}")


# ##########################
# Insert
# ##########################
def show_game_config_form_insert(db_session, log, main_qtobj, filename_path):
    log.debug("show_game_config_form_insert")
    edit_form = _create_edit_form_widget(db_session, log)
    edit_form.qtobj.game_name_line_edit.setText(os.path.splitext(os.path.basename(filename_path))[0])
    edit_form.qtobj.ok_push_button.clicked.connect(lambda: _game_config_form_result_insert_ok(db_session, log, main_qtobj, edit_form, filename_path))
    edit_form.qtobj.cancel_push_button.clicked.connect(lambda: _game_config_form_result_cancel(log, edit_form))


def _game_config_form_result_insert_ok(db_session, log, main_qtobj, edit_form, filename_path):
    log.debug("_game_config_form_result_insert_ok")
    edit_form.close()

    if edit_form.qtobj.game_name_line_edit.text() == "":
        qt_utils.show_message_window(log, "error", messages.missing_game_name)
        return

    exe_binary_type = FileUtils.get_exe_binary_type(filename_path)
    match exe_binary_type.upper():
        case "AMD64" | "IA64":
            architecture = "64bits"
            dll_src_path = variables.RESHADE64_PATH
        case _:
            architecture = "32bits"
            dll_src_path = variables.RESHADE32_PATH

    if edit_form.qtobj.dx9_radio_button.isChecked():
        dll_name = variables.D3D9_DLL
        api = variables.DX9_DISPLAY_NAME
    elif edit_form.qtobj.dxgi_radio_button.isChecked():
        dll_name = variables.DXGI_DLL
        api = variables.DXGI_DISPLAY_NAME
    else:
        dll_name = variables.OPENGL_DLL
        api = variables.OPENGL_DISPLAY_NAME

    form_results = {
        "name": edit_form.qtobj.game_name_line_edit.text(),
        "architecture": architecture,
        "api": api,
        "dll": dll_name,
        "path": filename_path,
        "dir": os.path.dirname(filename_path)
    }

    screenshots_path = program_utils.get_screenshot_path(db_session, log, form_results["dir"], form_results["name"])
    dst_dll_path = os.path.join(form_results["dir"], form_results["dll"])

    try:
        # create screenshot folder
        if not os.path.isdir(screenshots_path):
            os.mkdir(screenshots_path)
    except OSError as e:
        log.error(f"create_screenshot_dir: {get_exception(e)}")

    try:
        # creating reshade.ini file inside game dir
        reshade_utils.apply_reshade_ini_file(form_results["dir"], screenshots_path)
    except Exception as e:
        log.error(f"download_reshade_ini_file: {get_exception(e)}")

    try:
        # copying Reshade.dll
        shutil.copy2(str(dll_src_path), str(dst_dll_path))
    except shutil.Error as e:
        log.error(f"copyfile: {dll_src_path} to {dst_dll_path} - {get_exception(e)}")

    try:
        # copying ReShadePreset.ini
        shutil.copy2(variables.RESHADE_PRESET_PATH, form_results["dir"])
    except shutil.Error as e:
        log.error(f"copyfile: {variables.RESHADE_PRESET_PATH} to {dst_dll_path} - {get_exception(e)}")

    games_sql = GamesDal(db_session, log)
    games_sql.insert_game(form_results)

    _game_config_form_result_success(db_session, log, main_qtobj, form_results["name"])


# ##########################
# Update
# ##########################
def show_game_config_form_update(db_session, log, main_qtobj, item):
    log.debug("show_game_config_form_update")

    selected_game = games_tab_events.get_selected_game(db_session, log, main_qtobj, item)
    if not reshade_utils.check_game_path_exists(selected_game["path"]):
        qt_utils.show_message_window(log, "error", messages.error_game_not_found)
        return

    edit_form = _create_edit_form_widget(db_session, log)
    edit_form.qtobj.game_name_line_edit.setText(selected_game["name"])
    match selected_game["api"]:
        case variables.DX9_DISPLAY_NAME:
            edit_form.qtobj.dx9_radio_button.setChecked(True)
            edit_form.qtobj.dxgi_radio_button.setChecked(False)
            edit_form.qtobj.opengl_radio_button.setChecked(False)
        case variables.OPENGL_DISPLAY_NAME:
            edit_form.qtobj.dx9_radio_button.setChecked(False)
            edit_form.qtobj.dxgi_radio_button.setChecked(False)
            edit_form.qtobj.opengl_radio_button.setChecked(True)
        case _:
            edit_form.qtobj.dx9_radio_button.setChecked(False)
            edit_form.qtobj.dxgi_radio_button.setChecked(True)
            edit_form.qtobj.opengl_radio_button.setChecked(False)

    edit_form.qtobj.ok_push_button.clicked.connect(lambda: _game_config_form_result_update_ok(db_session, log, main_qtobj, edit_form, selected_game))
    edit_form.qtobj.cancel_push_button.clicked.connect(lambda: _game_config_form_result_cancel(log, edit_form))


def _game_config_form_result_update_ok(db_session, log, main_qtobj, edit_form, selected_game):
    log.debug("_game_config_form_result_update_ok")
    edit_form.close()

    if edit_form.qtobj.game_name_line_edit.text() == "":
        qt_utils.show_message_window(log, "error", messages.missing_game_name)
        return

    if edit_form.qtobj.dx9_radio_button.isChecked():
        dll_name = variables.D3D9_DLL
        api = variables.DX9_DISPLAY_NAME
    elif edit_form.qtobj.dxgi_radio_button.isChecked():
        dll_name = variables.DXGI_DLL
        api = variables.DXGI_DISPLAY_NAME
    else:
        dll_name = variables.OPENGL_DLL
        api = variables.OPENGL_DISPLAY_NAME

    edit_form_result = {
        "id": selected_game["id"],
        "name": edit_form.qtobj.game_name_line_edit.text(),
        "api": api,
        "dll": dll_name
    }

    if selected_game["name"] != edit_form_result["name"]:
        old_screenshots_path = program_utils.get_screenshot_path(db_session, log, selected_game["dir"], selected_game["name"])
        if old_screenshots_path:
            scrrenshot_dir_path = os.path.dirname(old_screenshots_path)
            new_screenshots_path = os.path.join(scrrenshot_dir_path, edit_form_result["name"])

            try:
                # creating reshade.ini file inside game dir
                reshade_utils.apply_reshade_ini_file(selected_game["dir"], new_screenshots_path)
            except Exception as e:
                log.error(f"download_reshade_ini_file: {get_exception(e)}")

            try:
                # rename screenshot folder
                if os.path.isdir(old_screenshots_path):
                    os.rename(old_screenshots_path, new_screenshots_path)
            except OSError as e:
                log.error(f"rename_screenshot_dir: {get_exception(e)}")

    if selected_game["api"] != edit_form_result["api"]:
        match selected_game["architecture"]:
            case "32bits":
                edit_form_result["architecture"] = "32bits"
                src_path = variables.RESHADE32_PATH
            case _:
                edit_form_result["architecture"] = "64bits"
                src_path = variables.RESHADE64_PATH

        dll_dst_path = os.path.join(selected_game["dir"], dll_name)
        try:
            # deleting Reshade.dll
            if os.path.isfile(selected_game["dll_path"]):
                os.remove(selected_game["dll_path"])
        except OSError as e:
            log.error(f"remove_reshade_file: {get_exception(e)}")

        try:
            # copying Reshade.dll
            shutil.copy2(str(src_path), str(dll_dst_path))
        except shutil.Error as e:
            log.error(f"copyfile: {src_path} to {dll_dst_path} - {get_exception(e)}")

    games_sql = GamesDal(db_session, log)
    games_sql.update_game(edit_form_result)

    _game_config_form_result_success(db_session, log, main_qtobj, edit_form_result["name"])

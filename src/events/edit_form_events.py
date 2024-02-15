# -*- coding: utf-8 -*-
import os
import shutil
from ddcUtils import get_exception
from PyQt6 import QtWidgets
from src.constants import messages, variables
from src.database.dal.config_dal import ConfigDal
from src.database.dal.games_dal import GamesDal
from src.edit_form import Ui_config
from src.events import games_tab_events
from src.tools import program_utils, reshade_utils
from src.tools.qt import qt_utils


def show_game_config_form(db_session, log, qtobj, item):
    log.debug("show_game_config_form")

    selected_game = games_tab_events.get_selected_game(qtobj, item)
    if not reshade_utils.check_game_path_exists(selected_game.path):
        qt_utils.show_message_window(log, "error", messages.error_game_not_found)
        return

    game_edit_form = QtWidgets.QWidget()
    qt_obj = Ui_config()
    qt_obj.setupUi(game_edit_form)
    game_edit_form.qtObj = qt_obj

    show_info_messages = True
    config_sql = ConfigDal(db_session, log)
    rs_config = config_sql.get_configs()
    if rs_config:
        show_info_messages = rs_config[0]["show_info_messages"]
        if rs_config[0]["use_dark_theme"]:
            game_edit_form.setStyleSheet(open(variables.QSS_PATH, "r").read())

    game_edit_form.qtObj.game_name_lineEdit.setFocus()
    game_edit_form.show()
    QtWidgets.QApplication.processEvents()

    game_edit_form.qtObj.ok_pushButton.clicked.connect(lambda: _game_config_form_result(db_session, log, qtobj, show_info_messages, game_edit_form, selected_game, "OK"))
    game_edit_form.qtObj.cancel_pushButton.clicked.connect(lambda: _game_config_form_result(db_session, log, qtobj, show_info_messages, game_edit_form, selected_game, "CANCEL"))

    game_edit_form.qtObj.game_name_lineEdit.setText(selected_game.name)
    match selected_game.api:
        case variables.DX9_DISPLAY_NAME:
            game_edit_form.qtObj.dx9_radioButton.setChecked(True)
            game_edit_form.qtObj.dx_radioButton.setChecked(False)
            game_edit_form.qtObj.opengl_radioButton.setChecked(False)
        case variables.OPENGL_DISPLAY_NAME:
            game_edit_form.qtObj.dx9_radioButton.setChecked(False)
            game_edit_form.qtObj.dx_radioButton.setChecked(False)
            game_edit_form.qtObj.opengl_radioButton.setChecked(True)
        case _:
            game_edit_form.qtObj.dx9_radioButton.setChecked(False)
            game_edit_form.qtObj.dx_radioButton.setChecked(True)
            game_edit_form.qtObj.opengl_radioButton.setChecked(False)


def _game_config_form_result(db_session, log, qtobj, show_info_messages, game_edit_form, selected_game, status):
    log.debug(f"game_config_form_result: {status}")

    game_edit_form.close()
    dx9_name = variables.DX9_DISPLAY_NAME
    dxgi_name = variables.DXGI_DISPLAY_NAME
    opengl_name = variables.OPENGL_DISPLAY_NAME

    if status == "OK":
        if game_edit_form.qtObj.game_name_lineEdit.text() == "":
            qt_utils.show_message_window(log, "error", messages.missing_game_name)
            return

        if not game_edit_form.qtObj.opengl_radioButton.isChecked() \
                and not game_edit_form.qtObj.dx9_radioButton.isChecked()\
                and not game_edit_form.qtObj.dx_radioButton.isChecked():
            qt_utils.show_message_window(log, "error", messages.missing_api)
            return

        updated_game_dict = {
            "game_name": game_edit_form.qtObj.game_name_lineEdit.text()
        }

        if selected_game.architecture == "32bits":
            updated_game_dict["architecture"] = "32bits"
            src_path = variables.RESHADE32_PATH
        else:
            updated_game_dict["architecture"] = "64bits"
            src_path = variables.RESHADE64_PATH

        games_sql = GamesDal(db_session, log)
        if selected_game is not None:
            if game_edit_form.qtObj.dx9_radioButton.isChecked():
                updated_game_dict["api"] = dx9_name
                dst_path = os.path.join(selected_game.game_dir, variables.D3D9_DLL)
            elif game_edit_form.qtObj.dx_radioButton.isChecked():
                updated_game_dict["api"] = dxgi_name
                dst_path = os.path.join(selected_game.game_dir, variables.DXGI_DLL)
            else:
                updated_game_dict["api"] = opengl_name
                dst_path = os.path.join(selected_game.game_dir, variables.OPENGL_DLL)

            if selected_game.name != updated_game_dict["game_name"] or (selected_game.api != updated_game_dict["api"]):
                # checking name changes
                # create Reshade.ini to replace edit CurrentPresetPath
                old_screenshots_path = program_utils.get_screenshot_path(log, qtobj, selected_game.game_dir, selected_game.name)
                if len(old_screenshots_path) > 0:
                    scrrenshot_dir_path = os.path.dirname(old_screenshots_path)
                    new_screenshots_path = os.path.join(scrrenshot_dir_path, updated_game_dict["game_name"])
                else:
                    new_screenshots_path = ""

                try:
                    reshade_utils.apply_reshade_ini_file(selected_game.game_dir, new_screenshots_path)
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
                    if selected_game.api == dx9_name:
                        d3d9_game_path = os.path.join(selected_game.game_dir, variables.D3D9_DLL)
                        if os.path.isfile(d3d9_game_path):
                            os.remove(d3d9_game_path)
                    elif selected_game.api == opengl_name:
                        opengl_game_path = os.path.join(selected_game.game_dir, variables.OPENGL_DLL)
                        if os.path.isfile(opengl_game_path):
                            os.remove(opengl_game_path)
                    else:
                        dxgi_game_path = os.path.join(selected_game.game_dir, variables.DXGI_DLL)
                        if os.path.isfile(dxgi_game_path):
                            os.remove(dxgi_game_path)
                except OSError as e:
                    log.error(f"remove_reshade_file: {get_exception(e)}")

                try:
                    # creating Reshade.dll
                    shutil.copy2(src_path, dst_path)
                except shutil.Error as e:
                    log.error(f"copyfile: {src_path} to {dst_path} - {get_exception(e)}")

                if show_info_messages:
                    qt_utils.show_message_window(log, "info",
                                                 f"{messages.game_updated}\n\n"
                                                 f"{updated_game_dict['game_name']}")

            updated_game_dict["id"] = selected_game.id
            games_sql.update_game(updated_game_dict)
            qt_utils.populate_games_tab(db_session, log, qtobj)
            qt_utils.enable_widgets(qtobj, False)
        else:
            # new game added
            if game_edit_form.qtObj.dx9_radioButton.isChecked():
                updated_game_dict["api"] = dx9_name
            elif game_edit_form.qtObj.opengl_radioButton.isChecked():
                updated_game_dict["api"] = opengl_name
            else:
                updated_game_dict["api"] = dxgi_name

            if added_game_path is not None:
                updated_game_dict["path"] = added_game_path
            elif selected_game is not None:
                updated_game_dict["path"] = selected_game.game_dir
            else:
                if show_info_messages:
                    qt_utils.show_message_window(log, "error",
                                                 f"{updated_game_dict['game_name']}\n\n"
                                                 f"{messages.error_change_game_name}")
                return

            result = games_tab_events.apply_single(self, updated_game_dict)
            if result is None:
                games_sql.insert_game(updated_game_dict)
                del added_game_path
                qt_utils.populate_games_tab(db_session, log, qtobj)
                qt_utils.enable_widgets(qtobj, False)
                if show_info_messages:
                    qt_utils.show_message_window(log, "info",
                                                 f"{messages.game_added}\n\n"
                                                 f"{updated_game_dict['game_name']}")

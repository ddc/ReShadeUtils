# -*- coding: utf-8 -*-
from ddcUtils import FileUtils, get_exception
from src.constants import messages, variables
from src.database.dal.config_dal import ConfigDal
from src.events import games_tab_events
from src.tools import program_utils, reshade_utils
from src.tools.qt import qt_utils
from src.tools.qt.progressbar import ProgressBar


def update_shaders_button(db_session, log):
    reshade_utils.download_shaders(db_session, log)


def dark_theme_clicked(db_session, form, log, status):
    qt_utils.set_style_sheet(db_session, form, log, status)
    config_sql = ConfigDal(db_session, log)
    config_sql.update_dark_theme(status)


def check_program_updates_clicked(db_session, log, status):
    config_sql = ConfigDal(db_session, log)
    config_sql.update_check_program_updates(status)


def show_info_messages_clicked(db_session, log, status):
    config_sql = ConfigDal(db_session, log)
    config_sql.update_show_info_messages(status)


def check_reshade_updates_clicked(db_session, log, status):
    config_sql = ConfigDal(db_session, log)
    config_sql.update_check_reshade_updates(status)


def create_screenshots_folder_clicked(db_session, log, status):
    config_sql = ConfigDal(db_session, log)
    config_sql.update_create_screenshots_folder(status)


def edit_global_plugins_button(log):
    try:
        reshade_utils.check_reshade_config_files(log)
        FileUtils.show(variables.RESHADE_PRESET_PATH)
    except Exception as e:
        err_msg = (f"{get_exception(e)}\n\n"
                   f"{variables.RESHADE_PRESET_PATH} {messages.unable_start}")
        qt_utils.show_message_window(log, "error", err_msg)


def reset_all_game_files_button(db_session, log, qtobj):
    progressbar = ProgressBar(log=log)

    progressbar.set_values(messages.reseting_files, 25)
    reshade_utils.download_all_files()

    progressbar.set_values(messages.reseting_files, 50)
    reshade_utils.check_shaders_and_textures(log)

    progressbar.set_values(messages.reseting_files, 75)
    games_tab_events.apply_all(db_session, log, qtobj, reset=True)

    progressbar.close()

    if program_utils.show_info_messages(db_session, log):
        qt_utils.show_message_window(log, "info", messages.reset_success)

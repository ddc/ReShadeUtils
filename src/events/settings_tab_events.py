# -*- coding: utf-8 -*-
from ddcUtils import FileUtils, get_exception
from src.constants import messages, variables
from src.database.dal.config_dal import ConfigDal
from src.events import games_tab_events
from src.tools import reshade_utils
from src.tools.qt import qt_utils


def update_shaders_button(log):
    reshade_utils.download_shaders(log)


def dark_theme_clicked(db_session, log, status):
    if status == "YES":
        status = True
    else:
        status = False

    qt_utils.set_style_sheet(db_session, form, log, use_dark_theme)
    config_sql = ConfigDal(db_session, log)
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
        self.get_remote_reshade_version = True
        status = True
    else:
        self.get_remote_reshade_version = False
        status = False

    config_sql = ConfigDal(self.db_session, self.log)
    config_sql.update_check_resahde_updates(status)


def create_screenshots_folder_clicked(self, status):
    if status == "YES":
        self.create_screenshots_folder = True
        status = True
    else:
        self.create_screenshots_folder = False
        status = False

    config_sql = ConfigDal(self.db_session, self.log)
    config_sql.update_create_screenshots_folder(status)


def edit_global_plugins_button(self):
    try:
        reshade_utils.check_reshade_config_files(self)
        FileUtils.show(variables.RESHADE_PRESET_PATH)
    except Exception as e:
        err_msg = (f"{get_exception(e)}\n\n"
                   f"{variables.RESHADE_PRESET_PATH} {messages.unable_start}")
        qt_utils.show_message_window(self.log, "error", err_msg)


def reset_all_game_files_button(self):
    self.progressbar.set_values(messages.reseting_files, 25)
    reshade_utils.download_all_files()
    self.progressbar.set_values(messages.reseting_files, 50)
    reshade_utils.check_shaders_and_textures(self)
    self.progressbar.set_values(messages.reseting_files, 75)
    games_tab_events.apply_all(self, reset=True)
    self.progressbar.close()
    qt_utils.show_message_window(self.log, "info", messages.reset_success)

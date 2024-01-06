# -*- coding: utf-8 -*-
import os
import requests
from src.constants import variables, messages
from alembic import command
from alembic.config import Config
from src.tools import misc_utils, file_utils
from src.tools.qt import qt_utils


def run_alembic_migrations():
    alembic_cfg = Config(variables.ALEMBIC_CONFIG_PATH)
    command.upgrade(alembic_cfg, "head")


def check_program_updates(self):
    self.qtobj.update_button.setVisible(False)
    if self.check_program_updates:
        new_version_obj = get_new_program_version(self)
        if new_version_obj.new_version_available:
            self.qtobj.updateAvail_label.clear()
            self.qtobj.updateAvail_label.setText(new_version_obj.new_version_msg)
            self.qtobj.update_button.setVisible(True)


def get_new_program_version(self):
    client_version = self.client_version
    remote_version = None
    remote_version_filename = variables.REMOTE_VERSION_FILENAME
    obj_return = misc_utils.Object()
    obj_return.new_version_available = False
    obj_return.new_version = None

    try:
        req = requests.get(remote_version_filename, stream=True)
        if req.status_code == 200:
            for line in req.iter_lines(decode_unicode=True):
                if line:
                    remote_version = line.rstrip()
                    break

            if remote_version is not None and (float(remote_version) > float(client_version)):
                obj_return.new_version_available = True
                obj_return.new_version_msg = f"Version {remote_version} available for download"
                obj_return.new_version = float(remote_version)
        else:
            err_msg = (
                f"{messages.error_check_new_version}\n"
                f"{messages.remote_version_file_not_found}\n"
                f"code: {req.status_code}"
            )
            qt_utils.show_message_window(self.log, "error", err_msg)
    except requests.exceptions.ConnectionError:
        qt_utils.show_message_window(self.log, "error", messages.dl_new_version_timeout)

    return obj_return


def get_screenshot_path(self, game_dir, game_name):
    game_screenshots_path = ""
    if self.qtobj.yes_screenshots_folder_radioButton.isChecked():
        game_screenshots_path = os.path.join(variables.RESHADE_SCREENSHOT_PATH, game_name)
        try:
            if not os.path.isdir(variables.RESHADE_SCREENSHOT_PATH):
                os.makedirs(variables.RESHADE_SCREENSHOT_PATH)
        except OSError as e:
            self.log.error(f"mkdir: {variables.RESHADE_SCREENSHOT_PATH}: {misc_utils.get_exception(e)}")

        try:
            if not os.path.isdir(game_screenshots_path):
                os.makedirs(game_screenshots_path)
        except OSError as e:
            self.log.error(f"mkdir: {game_screenshots_path}: {misc_utils.get_exception(e)}")
    else:
        reshade_ini_filepath = os.path.join(game_dir, variables.RESHADE_INI)
        reshade_config_screenshot_path = file_utils.get_ini_file_settings(
            reshade_ini_filepath,
            "SCREENSHOT",
            "SavePath"
        )
        if reshade_config_screenshot_path is not None:
            game_screenshots_path = reshade_config_screenshot_path
        elif os.path.isdir(os.path.join(variables.RESHADE_SCREENSHOT_PATH, game_name)):
            game_screenshots_path = os.path.join(variables.RESHADE_SCREENSHOT_PATH, game_name)
    return game_screenshots_path

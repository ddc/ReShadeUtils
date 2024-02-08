# -*- coding: utf-8 -*-
import os
import requests
from alembic import command
from alembic.config import Config
from ddcUtils import FileUtils, get_exception
from src.constants import messages, variables
from src.tools.qt import qt_utils


def run_alembic_migrations():
    alembic_cfg = Config(variables.ALEMBIC_CONFIG_FILE)
    command.upgrade(alembic_cfg, "head")


def check_program_updates(self):
    self.qtobj.update_button.setVisible(False)
    if self.check_program_updates:
        new_version_dict = get_new_program_version(self)
        client_version = new_version_dict["client_version"]
        remote_version = new_version_dict["remote_version"]
        if remote_version > client_version:
            new_version_msg = f"Version {remote_version} available for download"
            self.qtobj.updateAvail_label.clear()
            self.qtobj.updateAvail_label.setText(new_version_msg)
            self.qtobj.update_button.setVisible(True)
            return True
        return False
    return None


def get_new_program_version(self):
    remote_version = 0
    remote_version_filename = variables.REMOTE_VERSION_FILENAME
    result = {
        "client_version": float(self.client_version),
        "remote_version": remote_version,
    }

    try:
        req = requests.get(remote_version_filename, stream=True)
        if req.status_code == 200:
            for line in req.iter_lines(decode_unicode=True):
                if line:
                    remote_version = line.rstrip()
                    break
            result["remote_version"] = float(remote_version)
        else:
            err_msg = (
                f"{messages.error_check_new_version}\n"
                f"{messages.remote_version_file_not_found}\n"
                f"code: {req.status_code}"
            )
            qt_utils.show_message_window(self.log, "error", err_msg)
            result["error_msg"] = err_msg
    except requests.exceptions.ConnectionError:
        qt_utils.show_message_window(self.log, "error", messages.dl_new_version_timeout)

    return result


def get_screenshot_path(self, game_dir, game_name):
    game_screenshots_path = ""
    if self.qtobj.yes_screenshots_folder_radioButton.isChecked():
        game_screenshots_path = os.path.join(variables.RESHADE_SCREENSHOT_PATH, game_name)
        try:
            if not os.path.isdir(variables.RESHADE_SCREENSHOT_PATH):
                os.makedirs(variables.RESHADE_SCREENSHOT_PATH)
        except OSError as e:
            self.log.error(f"mkdir: {variables.RESHADE_SCREENSHOT_PATH}: {get_exception(e)}")

        try:
            if not os.path.isdir(game_screenshots_path):
                os.makedirs(game_screenshots_path)
        except OSError as e:
            self.log.error(f"mkdir: {game_screenshots_path}: {get_exception(e)}")
    else:
        reshade_ini_filepath = str(os.path.join(game_dir, variables.RESHADE_INI))
        reshade_config_screenshot_path = FileUtils().get_file_value(reshade_ini_filepath, "SCREENSHOT", "SavePath")
        if reshade_config_screenshot_path is not None:
            game_screenshots_path = reshade_config_screenshot_path
        elif os.path.isdir(os.path.join(variables.RESHADE_SCREENSHOT_PATH, game_name)):
            game_screenshots_path = os.path.join(variables.RESHADE_SCREENSHOT_PATH, game_name)
    return game_screenshots_path

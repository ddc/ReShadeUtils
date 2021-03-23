#! /usr/bin/env python3
# |*****************************************************
# * Copyright         : Copyright (C) 2019
# * Author            : ddc
# * License           : GPL v3
# |*****************************************************
# # -*- coding: utf-8 -*-

import os
import sys
import requests
import subprocess
from PyQt6 import QtWidgets
from src.sql.config_sql import ConfigSql
from src import constants, messages, utils, qtutils, log


class Launcher:
    def __init__(self):
        self.progressBar = qtutils.ProgressBar()
        self.log = None
        self.new_version = None
        self.new_version_msg = None
        self.client_version = None


    def init(self):
        utils.check_dirs()
        self.progressBar.set_values(messages.checking_files, 25)
        self.log = log.setup_logging(constants.DIR_LOGS)
        if utils.check_files(self):
            self.progressBar.set_values(messages.checking_db_connection, 50)
            utils.check_db_connection(self)
            utils.set_default_database_configs(self)

            self.progressBar.set_values(messages.checking_new_version, 75)
            self._check_update_required()
            self.progressBar.close()
            self._call_program()


    def _check_update_required(self):
        config_sql = ConfigSql(self)
        rs_config = config_sql.get_configs()

        if rs_config[0].get("program_version") is None:
            self.client_version = constants.VERSION
        else:
            self.client_version = rs_config[0].get("program_version")

        if rs_config[0].get("check_program_updates"):
            new_version_obj = utils.check_new_program_version(self)
            if new_version_obj.new_version_available:
                self.new_version = new_version_obj.new_version
                self.new_version_msg = new_version_obj.new_version_msg
                self._download_new_program_version()


    def _download_new_program_version(self):
        program_url = f"{constants.GITHUB_EXE_PROGRAM_URL}{self.new_version}/{constants.EXE_PROGRAM_NAME}"
        downloaded_program_path = os.path.join(utils.get_current_path(), constants.EXE_PROGRAM_NAME)

        r = requests.get(program_url)
        if r.status_code == 200:
            with open(downloaded_program_path, "wb") as outfile:
                outfile.write(r.content)
            qtutils.show_message_window(self.log, "info", f"{messages.program_updated}v{self.new_version}")
        else:
            qtutils.show_message_window(self.log, "error", messages.error_dl_new_version)
            self.log.error(f"{messages.error_dl_new_version} {r.status_code} {r}")


    def _call_program(self):
        code = None
        cmd = [os.path.join(utils.get_current_path(), constants.EXE_PROGRAM_NAME)]
        try:
            process = subprocess.run(cmd, shell=True, check=True, universal_newlines=True)
            code = process.returncode
        except Exception as e:
            if code is None:
                code = e.returncode
            emsg = f"cmd:{cmd} - code:{code} - {e}"
            msg = f"{messages.error_executing_program}{constants.EXE_PROGRAM_NAME}"\
                  f" - {messages.error_check_installation}"
            if emsg:
                msg += emsg
            qtutils.show_message_window(self.log, "error", msg)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    launcher = Launcher()
    launcher.init()

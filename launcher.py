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
from src.log import Log
from PyQt5 import QtWidgets
from src.progressbar import ProgressBar
from src.sql.config_sql import ConfigSql
from src.sql.database import DatabaseClass
from src import constants, messages, utils, qtutils


class Launcher:
    def __init__(self):
        self.progressbar = ProgressBar()
        self.program_path = self.program_path = os.path.join(utils.get_current_path(), constants.EXE_PROGRAM_NAME)
        self.log = None
        self.new_version = None
        self.new_version_msg = None
        self.client_version = None
        self.database = None


    def init(self):
        utils.check_dirs()
        self.progressbar.set_values(messages.checking_files, 25)
        self.log = Log().setup_logging()
        if not os.path.isfile(self.program_path):
            os.path.join(constants.PROGRAM_PATH, constants.EXE_PROGRAM_NAME)
        self.database = DatabaseClass(self.log)
        utils.check_db_connection(self)
        utils.create_default_tables(self)
        utils.check_database_configs(self)
        if utils.create_local_reshade_files(self):
            self.progressbar.set_values(messages.checking_db_connection, 50)
            self.progressbar.set_values(messages.checking_new_version, 75)
            self._check_update_required()
            self.progressbar.close()
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
        r = requests.get(program_url)
        if r.status_code == 200:
            with open(self.program_path, "wb") as outfile:
                outfile.write(r.content)
            qtutils.show_message_window(self.log, "info", f"{messages.program_updated}v{self.new_version}")
        else:
            qtutils.show_message_window(self.log, "error", messages.error_dl_new_version)
            self.log.error(f"{messages.error_dl_new_version} {r.status_code} {r}")


    def _call_program(self):
        code = None
        try:
            process = subprocess.run(self.program_path, shell=True, check=True, universal_newlines=True)
            code = process.returncode
        except Exception as e:
            if code is None and hasattr(e, "returncode"):
                self.log.error(f"cmd:{self.program_path} - code:{e.returncode} - {e}")
            msg = f"{messages.error_executing_program}{constants.EXE_PROGRAM_NAME}\n"\
                  f"{messages.error_check_installation}"
            qtutils.show_message_window(self.log, "error", msg)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    launcher = Launcher()
    launcher.init()

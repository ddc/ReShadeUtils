#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import requests
import subprocess
from src.log import Log
from PyQt6 import QtWidgets
from src.progressbar import ProgressBar
from src.database.dal.config_dal import ConfigDal
from src import constants, messages
from src.utils import utils, qtutils


class Launcher:
    def __init__(self):
        self.log = Log().setup_logging()
        self.progressbar = ProgressBar()
        # self.database = DatabaseClass(self.log)
        self.program_path = os.path.join(utils.get_current_path(),
                                         constants.EXE_PROGRAM_NAME)
        self.new_version = None
        self.new_version_msg = None
        self.client_version = None

    def start(self):
        self.progressbar.set_values(messages.checking_files, 25)
        utils.check_local_files(self)
        if not os.path.isfile(self.program_path):
            self.program_path = os.path.join(constants.PROGRAM_PATH,
                                             constants.EXE_PROGRAM_NAME)
        self.progressbar.set_values(messages.checking_database, 50)
        utils.check_database_connection(self)
        utils.check_default_database_tables(self)
        utils.check_default_database_configs(self)
        self.progressbar.set_values(messages.checking_program_updates, 75)
        self.check_program_updates()
        self.progressbar.close()
        self.call_program()

    def check_program_updates(self):
        config_sql = ConfigDal(self)
        rs_config = config_sql.get_configs()
        if rs_config[0].get("program_version") is None:
            self.client_version = constants.VERSION
        else:
            self.client_version = rs_config[0].get("program_version")
        if rs_config[0].get("check_program_updates"):
            new_version_obj = utils.get_new_program_version(self)
            if new_version_obj.new_version_available:
                self.new_version = new_version_obj.new_version
                self.new_version_msg = new_version_obj.new_version_msg
                self.download_new_program_version()

    def download_new_program_version(self):
        program_url = f"{constants.GITHUB_EXE_PROGRAM_URL}" \
                      f"{self.new_version}/" \
                      f"{constants.EXE_PROGRAM_NAME}"
        r = requests.get(program_url)
        if r.status_code == 200:
            with open(self.program_path, "wb") as outfile:
                outfile.write(r.content)
            qtutils.show_message_window(self.log,
                                        "info",
                                        f"{messages.program_updated}"
                                        f"v{self.new_version}")
        else:
            qtutils.show_message_window(self.log,
                                        "error",
                                        messages.error_dl_new_version)
            self.log.error(f"{messages.error_dl_new_version} "
                           f"{r.status_code} "
                           f"{r}")

    def call_program(self):
        code = None
        try:
            process = subprocess.run(self.program_path,
                                     shell=True,
                                     check=True,
                                     universal_newlines=True)
            code = process.returncode
        except Exception as e:
            if code is None and hasattr(e, "returncode"):
                self.log.error(f"cmd:{self.program_path}"
                               f" - code:{e.returncode} - {e}")
            msg = f"{messages.error_executing_program}" \
                  f"{constants.EXE_PROGRAM_NAME}\n"\
                  f"{messages.error_check_installation}"
            qtutils.show_message_window(self.log, "error", msg)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    launcher = Launcher()
    launcher.start()

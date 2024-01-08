#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import requests
import subprocess
from src.log import Log
from PyQt6 import QtWidgets
from src.tools.qt.progressbar import ProgressBar
from src.database.dal.config_dal import ConfigDal
from src.constants import variables, messages
from src.tools import file_utils, program_utils, misc_utils
from src.tools.qt import qt_utils
from src.database.db import Database


class Launcher:
    def __init__(self):
        self.log = Log().setup_logging()
        self.progressbar = ProgressBar()
        self.program_path = os.path.join(misc_utils.get_current_path(), variables.EXE_PROGRAM_NAME)
        self.db_session = None
        self.new_version = None
        self.new_version_msg = None
        self.client_version = None

    def start(self):
        database = Database(self.log)
        database_engine = database.get_db_engine()
        with database.get_db_session(database_engine) as db_session:
            self.db_session = db_session
            self.progressbar.set_values(messages.checking_files, 25)
            file_utils.check_local_files(self)

            if not os.path.isfile(self.program_path):
                self.program_path = os.path.join(variables.PROGRAM_PATH, variables.EXE_PROGRAM_NAME)

            self.progressbar.set_values(messages.checking_database, 50)
            program_utils.run_alembic_migrations()

            self.progressbar.set_values(messages.checking_program_updates, 75)
            self.check_program_updates()
            self.progressbar.close()
            self.call_program()

    def check_program_updates(self):
        config_sql = ConfigDal(self.db_session, self.log)
        rs_config = config_sql.get_configs()
        if rs_config[0].get("program_version") is None:
            self.client_version = variables.VERSION
        else:
            self.client_version = rs_config[0].get("program_version")
        if rs_config[0].get("check_program_updates"):
            new_version_dict = program_utils.get_new_program_version(self)
            client_version = new_version_dict['client_version']
            remote_version = new_version_dict['remote_version']
            if float(remote_version) > float(client_version):
                self.new_version = remote_version
                self.new_version_msg = f"Version {remote_version} available for download"
                self.download_new_program_version()

    def download_new_program_version(self):
        program_url = f"{variables.GITHUB_EXE_PROGRAM_URL}/v{self.new_version}/{variables.EXE_PROGRAM_NAME}"
        r = requests.get(program_url)
        if r.status_code == 200:
            with open(self.program_path, "wb") as outfile:
                outfile.write(r.content)
            qt_utils.show_message_window(self.log,
                                         "info",
                                         f"{messages.program_updated} {self.new_version}")
        else:
            qt_utils.show_message_window(self.log,
                                         "error",
                                         messages.error_dl_new_version)
            self.log.error(f"{messages.error_dl_new_version} {r.status_code} {r}")

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
            msg = f"{messages.error_executing_program} {variables.EXE_PROGRAM_NAME}\n" \
                  f"{messages.error_check_installation}"
            qt_utils.show_message_window(self.log, "error", msg)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    launcher = Launcher()
    launcher.start()

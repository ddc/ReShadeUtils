#! /usr/bin/env python3
# |*****************************************************
# * Copyright         : Copyright (C) 2019
# * Author            : ddc
# * License           : GPL v3
# * Python            : 3.6
# |*****************************************************
# # -*- coding: utf-8 -*-

import os
import subprocess
import sys

import requests
from PyQt5 import QtCore, QtWidgets

from src.sql.configs_sql import ConfigsSql
from src.utils import constants, messages, utilities


class Launcher:
    def __init__(self):
        utilities.show_progress_bar(self, messages.checking_files, 25)
        utilities.check_dirs(self)
        self.log = utilities.setup_logging(self)
        sys.excepthook = utilities.log_uncaught_exceptions
        utilities.check_files(self)
        self.database_settings = utilities.get_all_ini_file_settings(constants.DB_SETTINGS_FILENAME)
        self.client_version = constants.VERSION

        utilities.show_progress_bar(self, messages.checking_db_connection, 50)
        utilities.check_db_connection(self)
        utilities.set_default_database_configs(self)
        utilities.check_database_updated_columns(self)

        utilities.show_progress_bar(self, messages.checking_new_version, 75)
        self._check_update_required()

        utilities.show_progress_bar(self, messages.checking_new_version, 100)
        self._call_program()

    ################################################################################
    def _check_update_required(self):
        configSql = ConfigsSql(self)
        rsConfig = configSql.get_configs()

        if rsConfig[0]["check_program_updates"].upper() == "Y":
            new_version_obj = utilities.check_new_program_version(self)
            if new_version_obj.new_version_available:
                self.new_version = new_version_obj.new_version
                self.new_version_msg = new_version_obj.new_version_msg
                self._download_new_program_version(False)

    ################################################################################
    def _download_new_program_version(self, show_dialog=True):
        if show_dialog:
            msg = f"""{messages.new_version_available}
                                \nYour version: v{self.client_version}\nNew version: v{self.new_version}
                                \n{messages.check_downloaded_dir}
                                \n{messages.confirm_download}"""
            reply = utilities.show_message_window("question", self.new_version_msg, msg)

            if reply == QtWidgets.QMessageBox.No:
                new_title = f"{constants.FULL_PROGRAM_NAME} ({self.new_version_msg})"
                _translate = QtCore.QCoreApplication.translate
                self.form.setWindowTitle(_translate("Main", new_title))
                return

        program_url = f"{constants.GITHUB_EXE_PROGRAM_URL}{self.new_version}/{constants.EXE_PROGRAM_NAME}"
        downloaded_program_path = f"{os.path.abspath(os.getcwd())}\\{constants.EXE_PROGRAM_NAME}"
        dl_new_version_msg = messages.dl_new_version

        utilities.show_progress_bar(self, dl_new_version_msg, 50)
        r = requests.get(program_url)
        if r.status_code == 200:
            with open(downloaded_program_path, 'wb') as outfile:
                outfile.write(r.content)
            utilities.show_message_window("Info", "INFO", f"{messages.program_updated}v{self.new_version}")
        else:
            utilities.show_message_window("error", "ERROR", f"{messages.error_dl_new_version}")
            self.log.error(f"{messages.error_dl_new_version} {r.status_code} {r}")

        utilities.show_progress_bar(self, dl_new_version_msg, 100)

    ################################################################################
    def _call_program(self):
        code = None
        cmd = [f"{os.path.abspath(os.getcwd())}\\{constants.EXE_PROGRAM_NAME}"]
        try:
            process = subprocess.run(cmd, shell=True, check=True, universal_newlines=True)
            #output = process.stdout
            code = process.returncode
        except Exception as e:
            emsg = None
            if code is None:
                code = e.returncode
                emsg = f"cmd:{cmd} - code:{code} - {e}"
            self.log.error(f"{messages.error_executing_program}{constants.EXE_PROGRAM_NAME}"
                           f" - {messages.error_check_installation} - {emsg}")
            utilities.show_message_window("error", "ERROR",
                                          f"{messages.error_executing_program}{constants.EXE_PROGRAM_NAME}\n"
                                          f"{messages.error_check_installation}")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    launcher = Launcher()
    sys.exit(0)

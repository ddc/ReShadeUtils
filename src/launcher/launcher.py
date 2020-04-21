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
from src.sql.initial_tables_sql import InitialTablesSql
from src.sql.triggers_sql import TriggersSql
from src.sql.update_tables_sql import UpdateTablesSql
from src.utils import constants, messages, utilities
from src.utils.create_files import CreateFiles


class Launcher:
    def __init__(self):
        utilities.show_progress_bar(self, messages.checking_files, 25)
        self._check_dirs()
        self.log = utilities.setup_logging(self)
        sys.excepthook = utilities.log_uncaught_exceptions
        self._check_files()
        self.database_settings = utilities.get_all_ini_file_settings(constants.DB_SETTINGS_FILENAME)
        self.client_version = constants.VERSION

        utilities.show_progress_bar(self, messages.checking_db_connection, 50)
        self._check_db_connection()
        self._set_default_database_configs()
        self._check_database_updated_columns()

        utilities.show_progress_bar(self, messages.checking_new_version, 75)
        self._check_update_required()

        utilities.show_progress_bar(self, messages.checking_new_version, 100)
        self._init_program()

    ################################################################################
    def _check_dirs(self):
        try:
            if not os.path.exists(constants.PROGRAM_PATH):
                os.makedirs(constants.PROGRAM_PATH)
        except OSError as e:
            utilities.show_message_window("error", "ERROR", f"Error creating program directories.\n{e}")
            #self.log.error(f"{e}")

    ################################################################################
    def _check_files(self):
        create_files = CreateFiles(self)

        try:
            if not os.path.exists(constants.DB_SETTINGS_FILENAME):
                create_files.create_settings_file()
        except Exception as e:
            self.log.error(f"{e}")

        try:
            if not os.path.exists(constants.STYLE_QSS_FILENAME):
                create_files.create_style_file()
        except Exception as e:
            self.log.error(f"{e}")

        try:
            if not os.path.exists(constants.RESHADE_PLUGINS_FILENAME):
                create_files.create_reshade_plugins_ini_file()
        except Exception as e:
            self.log.error(f"{e}")

    ################################################################################
    def _check_db_connection(self):
        db_conn = utilities.check_database_connection(self)
        if db_conn is None:
            error_db_conn = messages.error_db_connection
            msg_exit = messages.exit_program
            utilities.show_message_window("error", "ERROR", f"{error_db_conn}\n\n{msg_exit}")
            sys.exit(0)

    ################################################################################
    def _set_default_database_configs(self):
        initialTablesSql = InitialTablesSql(self)
        it = initialTablesSql.create_initial_tables()
        if it is not None:
            err_msg = messages.error_create_sql_config_msg
            self.log.error(err_msg)
            print(err_msg)
            # sys.exit()

        configSql = ConfigsSql(self)
        rsConfig = configSql.get_configs()
        if rsConfig is not None and len(rsConfig) == 0:
            configSql.set_default_configs()

        triggersSql = TriggersSql(self)
        tr = triggersSql.create_triggers()
        if tr is not None:
            err_msg = messages.error_create_sql_config_msg
            self.log.error(err_msg)
            print(err_msg)
            # sys.exit()

    ################################################################################
    def _check_database_updated_columns(self):
        updateTablesSql = UpdateTablesSql(self)
        configSql = ConfigsSql(self)
        rsConfig = configSql.get_configs()
        if len(rsConfig) > 0:
            for eac in constants.NEW_CONFIG_TABLE_COLUMNS:
                if eac != "id".lower() and not eac in rsConfig[0].keys():
                        ut = updateTablesSql.update_config_table()

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
        downloaded_program_path = f"{constants.PROGRAM_PATH}\\{constants.EXE_PROGRAM_NAME}"
        dl_new_version_msg = messages.dl_new_version

        try:
            utilities.show_progress_bar(self, dl_new_version_msg, 50)
            r = requests.get(program_url)
            with open(downloaded_program_path, 'wb') as outfile:
                outfile.write(r.content)
            utilities.show_progress_bar(self, dl_new_version_msg, 100)
            utilities.show_message_window("Info", "INFO", f"{messages.program_updated}v{self.new_version}")
            ##sys.exit()
        except Exception as e:
            utilities.show_progress_bar(self, dl_new_version_msg, 100)
            self.log.error(f"{messages.error_check_new_version} {e}")
            if e.code == 404:
                utilities.show_message_window("error", "ERROR", messages.remote_file_not_found)
            else:
                utilities.show_message_window("error", "ERROR", messages.error_check_new_version)

    ################################################################################
    def _init_program(self):
        code = None
        cmd = [f"{constants.PROGRAM_PATH}\\{constants.EXE_PROGRAM_NAME}"]
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
    sys.exit(app.exec_())

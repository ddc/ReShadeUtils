#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import subprocess
import sys
from ddcUtils import OsUtils
from ddcUtils.databases import DBSqlite
from PyQt6 import QtWidgets
from src.constants import messages, variables
from src.log import Log
from src.tools import program_utils
from src.tools.qt import qt_utils
from src.tools.qt.progressbar import ProgressBar


class Launcher:
    def __init__(self):
        self.log = Log(self.__class__.__name__).setup_logging()
        self.progressbar = ProgressBar()
        self.program_name = variables.EXE_PROGRAM_NAME if OsUtils.is_windows() else variables.SHORT_PROGRAM_NAME
        self.program_path = os.path.join(OsUtils.get_current_path(), self.program_name)
        self.db_session = None

    def start(self):
        database = DBSqlite(variables.DATABASE_PATH)
        with database.session() as db_session:
            self.db_session = db_session
            self.progressbar.set_values(messages.checking_files, 25)
            new_version = program_utils.check_program_updates(self.log, db_session)
            if new_version:
                if not os.path.isfile(self.program_path):
                    self.program_path = os.path.join(variables.PROGRAM_PATH, self.program_name)
                self.progressbar.set_values(messages.checking_files, 50)
                program_utils.download_new_program_version(self.log, self.program_path, new_version)

            self.progressbar.close()
            self.call_program()

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
            msg = (f"{messages.error_executing_program} {self.program_name}\n"
                   f"{messages.error_check_installation}")
            qt_utils.show_message_window(self.log, "error", msg)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    launcher = Launcher()
    launcher.start()

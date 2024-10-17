#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import subprocess
import sys
from ddcDatabases import DBSqlite
from ddcLogs import TimedRotatingLog
from ddcUtils import FileUtils, OsUtils
from PyQt6 import QtWidgets
from src.constants import messages, variables
from src.tools import program_utils
from src.tools.qt import qt_utils
from src.tools.qt.progressbar import ProgressBar


class Launcher:
    def __init__(self):
        self.log = TimedRotatingLog(
            directory=variables.LOGS_DIR,
            filenames=(variables.LOG_FILE_NAME,),
            days_to_keep=int(variables.DAYS_TO_KEEP_LOGS),
            level="debug" if variables.DEBUG else "info",
        ).init()
        self.progressbar = ProgressBar(log=self.log)
        self.program_name = variables.EXE_PROGRAM_NAME if OsUtils.is_windows() else variables.SHORT_PROGRAM_NAME
        self.program_path = os.path.join(OsUtils.get_current_path(), self.program_name)

    def start(self):
        database = DBSqlite(variables.DATABASE_PATH)
        with database.session() as db_session:
            self.progressbar.set_values(messages.checking_alembic_files, 25)
            alembic_files = FileUtils.list_files(variables.ALEMBIC_MIGRATIONS_DIR)
            if not alembic_files:
                program_utils.download_alembic_dir(self.log)
            program_utils.run_alembic_migrations(self.log)

            self.progressbar.set_values(messages.checking_files, 50)
            new_version = program_utils.check_program_updates(self.log, db_session)
            if new_version:
                if not os.path.isfile(self.program_path):
                    self.program_path = os.path.join(variables.PROGRAM_DIR, self.program_name)
                self.progressbar.set_values(messages.checking_files, 75)
                program_utils.download_new_program_version(db_session, self.log, self.program_path, new_version)

            self.progressbar.close()
            self.call_program()

    def call_program(self):
        self.log.debug("Calling program")
        code = None
        try:
            process = subprocess.run(self.program_path,
                                     shell=True,
                                     check=True,
                                     universal_newlines=True)
            code = process.returncode
        except Exception as e:
            if code is None and hasattr(e, "returncode"):
                self.log.error(f"cmd:{self.program_path} | code:{e.returncode} - {e}")
            msg = f"{messages.error_executing_program} {self.program_name}\n{messages.error_check_installation}"
            qt_utils.show_message_window(self.log, "error", msg)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    launcher = Launcher()
    launcher.start()

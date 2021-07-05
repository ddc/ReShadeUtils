# |*****************************************************
# * Copyright         : Copyright (C) 2019
# * Author            : ddc
# * License           : GPL v3
# |*****************************************************
# -*- encoding: utf-8 -*-
import os
import sys
import gzip
import logging.handlers
from src import constants


class Log:
    def __init__(self, dir_logs, debug):
        self.dir = dir_logs
        self.date_formatter = "%Y-%m-%d"
        self.time_formatter = "%H:%M:%S"
        self.backup_days = 30
        self.level = logging.DEBUG if debug else logging.INFO


    def setup_logging(self):
        try:
            os.makedirs(self.dir, exist_ok=True) if not os.path.isdir(self.dir) else None
        except Exception as e:
            sys.stderr.write(f"[ERROR]:[EXITING]:[{str(e)}]:Unable to create logs directory: {self.dir}\n")
            sys.exit(1)

        log_filename = f"{constants.SHORT_PROGRAM_NAME}.log"
        log_file_path = f"{self.dir}/{log_filename}"

        try:
            open(log_file_path, "a+").close()
        except IOError as e:
            sys.stderr.write(f"[ERROR]:[EXITING]:[{str(e)}]:Unable to open the log file for writing: {log_file_path}\n")
            sys.exit(1)

        if self.level == logging.DEBUG:
            formatt = "[%(asctime)s.%(msecs)03d]:[%(levelname)s]:[%(filename)s:%(funcName)s:%(lineno)d]:%(message)s"
        else:
            formatt = "[%(asctime)s.%(msecs)03d]:[%(levelname)s]:%(message)s"

        formatter = logging.Formatter(formatt, datefmt=f"{self.date_formatter}T{self.time_formatter}")
        logger = logging.getLogger()
        logger.setLevel(self.level)
        file_hdlr = logging.handlers.RotatingFileHandler(
            filename=log_file_path,
            maxBytes=1 * 1024 * 1024,
            encoding="UTF-8",
            backupCount=self.backup_days,
            mode="a")

        file_hdlr.setFormatter(formatter)
        file_hdlr.suffix = "%Y%m%d"
        file_hdlr.rotator = GZipRotator(self.dir, self.backup_days)
        logger.addHandler(file_hdlr)

        stream_hdlr = logging.StreamHandler()
        stream_hdlr.setFormatter(formatter)
        stream_hdlr.setLevel(self.level)
        logger.addHandler(stream_hdlr)
        return logger


class GZipRotator:
    def __init__(self, logs_dir, backup_days):
        self.logs_dir = logs_dir
        self.backup_days = backup_days

    def __call__(self, source, dest):
        RemoveOldLogs(self.logs_dir, self.backup_days)
        if os.path.isfile(source) and os.stat(source).st_size > 0:
            try:
                sfname, sext = os.path.splitext(source)
                dfname, dext = os.path.splitext(dest)
                renamed_dst = f"{sfname}_{dext.replace('.', '')}{sext}.gz"
                with open(source, "rb") as fin:
                    with gzip.open(renamed_dst, "wb") as fout:
                        fout.writelines(fin)
                os.remove(source)
            except Exception as e:
                sys.stderr.write(f"[ERROR]:Unable to compress the log file:[{str(e)}]: {source}\n")


class RemoveOldLogs:
    def __init__(self, logs_dir, backup_days):
        files_list = [f for f in os.listdir(logs_dir)
                      if os.path.isfile(f"{logs_dir}/{f}") and os.path.splitext(f)[1] == ".gz"]
        for file in files_list:
            file_path = f"{logs_dir}/{file}"
            if self._is_file_older_than_x_days(file_path, backup_days):
                try:
                    os.remove(file_path)
                except Exception as e:
                    sys.stderr.write(f"[ERROR]:Unable to removed old logs:{str(e)}: {file_path}\n")

    @staticmethod
    def _is_file_older_than_x_days(file_path, days):
        from datetime import datetime, timedelta
        file_time = datetime.fromtimestamp(os.path.getctime(file_path))
        if int(days) == 1:
            cutoff_time = datetime.today()
        else:
            cutoff_time = datetime.today() - timedelta(days=days)
        file_time = file_time.replace(hour=0, minute=0, second=0, microsecond=0)
        cutoff_time = cutoff_time.replace(hour=0, minute=0, second=0, microsecond=0)
        if file_time < cutoff_time:
            return True
        return False

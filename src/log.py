# |*****************************************************
# * Copyright         : Copyright (C) 2022
# * Author            : ddc
# * License           : GPL v3
# |*****************************************************
# -*- encoding: utf-8 -*-
import os
import sys
import gzip
import logging.handlers
from src import constants, qtutils, utils


class Log:
    def __init__(self):
        self.dir = constants.PROGRAM_PATH
        self.days_to_keep = int(constants.DAYS_TO_KEEP_LOGS)
        self.level = logging.DEBUG if constants.DEBUG else logging.INFO

    def setup_logging(self):
        try:
            os.makedirs(self.dir, exist_ok=True) \
                if not os.path.isdir(self.dir) else None
        except Exception as e:
            err_msg = f"[ERROR]:[EXITING]:[{utils.get_exception(e)}]:" \
                      f"Unable to create logs directory: {self.dir}\n"
            qtutils.show_message_window(None, "error", err_msg)
            sys.stderr.write(err_msg)
            sys.exit(1)

        log_filename = f"{constants.SHORT_PROGRAM_NAME}.log"
        log_file_path = f"{self.dir}/{log_filename}"

        try:
            open(log_file_path, "a+").close()
        except IOError as e:
            err_msg = f"[ERROR]:[EXITING]:[{utils.get_exception(e)}]:" \
                      f"Unable to open the log file for writing: " \
                      f"{log_file_path}\n"
            qtutils.show_message_window(None, "error", err_msg)
            sys.stderr.write(err_msg)
            sys.exit(1)

        if self.level == logging.DEBUG:
            formatt = f"[%(asctime)s.%(msecs)03d]:[%(levelname)s]:" \
                      f"[PID:{os.getpid()}]:" \
                      f"[%(filename)s:%(funcName)s:%(lineno)d]:%(message)s"
        else:
            formatt = "[%(asctime)s.%(msecs)03d]:[%(levelname)s]:%(message)s"

        formatter = logging.Formatter(formatt, datefmt="%Y-%m-%dT%H:%M:%S")
        logger = logging.getLogger()
        logger.setLevel(self.level)
        file_hdlr = logging.handlers.RotatingFileHandler(
            filename=log_file_path,
            maxBytes=1 * 1024 * 1024,
            encoding="UTF-8",
            backupCount=self.days_to_keep,
            mode="a")

        file_hdlr.setFormatter(formatter)
        file_hdlr.suffix = "%Y%m%d"
        file_hdlr.rotator = GZipRotator(self.dir, self.days_to_keep)
        logger.addHandler(file_hdlr)

        stream_hdlr = logging.StreamHandler()
        stream_hdlr.setFormatter(formatter)
        stream_hdlr.setLevel(self.level)
        logger.addHandler(stream_hdlr)
        return logger


class GZipRotator:
    def __init__(self, logs_dir, days_to_keep):
        self.logs_dir = logs_dir
        self.days_to_keep = days_to_keep

    def __call__(self, source, dest):
        RemoveOldLogs(self.logs_dir, self.days_to_keep)
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
                err_msg = f"[ERROR]:Unable to compress the log file:" \
                          f"[{utils.get_exception(e)}]: {source}\n"
                qtutils.show_message_window(None, "error", err_msg)
                sys.stderr.write(err_msg)


class RemoveOldLogs:
    def __init__(self, logs_dir, days_to_keep):
        files_list = [f for f in os.listdir(logs_dir)
                      if os.path.isfile(f"{logs_dir}/{f}")
                      and f.lower().endswith(".gz")]
        for file in files_list:
            file_path = f"{logs_dir}/{file}"
            if self._is_file_older_than_x_days(file_path, days_to_keep):
                try:
                    os.remove(file_path)
                except Exception as e:
                    err_msg = f"[ERROR]:Unable to removed old logs:" \
                              f"{utils.get_exception(e)}: {file_path}\n"
                    qtutils.show_message_window(None, "error", err_msg)
                    sys.stderr.write(err_msg)

    @staticmethod
    def _is_file_older_than_x_days(file_path, days_to_keep):
        from datetime import datetime, timedelta
        file_time = datetime.fromtimestamp(os.path.getctime(file_path))
        if int(days_to_keep) == 1:
            cutoff_time = datetime.today()
        else:
            cutoff_time = datetime.today() - timedelta(days=days_to_keep)
        file_time = file_time.replace(hour=0, minute=0, second=0,
                                      microsecond=0)
        cutoff_time = cutoff_time.replace(hour=0, minute=0, second=0,
                                          microsecond=0)
        if file_time < cutoff_time:
            return True
        return False

#! /usr/bin/env python3
# |*****************************************************
# * Copyright         : Copyright (C) 2019
# * Author            : ddc
# * License           : GPL v3
# |*****************************************************
# # -*- coding: utf-8 -*-

import os
import sys
import gzip
import logging.handlers
from src import constants


def setup_logging(dir_logs):
    backup_days = 7
    date_formatter = "%Y-%m-%d"
    time_formatter = "%H:%M:%S"
    log_level = logging.INFO

    class GZipRotator:
        def __call__(self, source, dest):
            try:
                sfname, sext = os.path.splitext(source)
                dfname, dext = os.path.splitext(dest)
                renamed_dst = f"{sfname}_{dext.replace('.', '')}{sext}"
                os.rename(source, renamed_dst)
                with open(renamed_dst, "rb") as fin:
                    with gzip.open(f"{renamed_dst}.gz", "wb") as fout:
                        fout.writelines(fin)
                os.remove(renamed_dst)
            except Exception as ex:
                print(f"[ERROR]:Unable to compact the log file:[{str(ex)}]: {source}\n")

    if not os.path.isdir(dir_logs):
        try:
            os.makedirs(dir_logs, exist_ok=True)
        except Exception as e:
            print(f"[ERROR]:[EXITING]:[{str(e)}]:Unable to create logs directory: {dir_logs}\n")
            sys.exit(1)

    log_filename = f"{constants.SHORT_PROGRAM_NAME}.log"
    log_file_path = os.path.join(dir_logs, log_filename)

    try:
        open(log_file_path, "a+").close()
    except IOError as e:
        print(f"[ERROR]:[EXITING]:[{str(e)}]:Unable to open the log file for writing: {log_file_path}\n")
        sys.exit(1)

    if log_level == logging.DEBUG:
        formatt = "%(asctime)s.%(msecs)03d]:[%(levelname)s]:[%(filename)s:%(funcName)s:%(lineno)d]:%(message)s"
    else:
        formatt = "%(asctime)s.%(msecs)03d]:[%(levelname)s]:%(message)s"

    formatter = logging.Formatter(formatt, datefmt=f"[{date_formatter} {time_formatter}")

    logger = logging.getLogger()
    logger.setLevel(log_level)
    file_hdlr = logging.handlers.RotatingFileHandler(
        filename=log_file_path,
        maxBytes=1 * 1024 * 1024,
        encoding="UTF-8",
        backupCount=backup_days,
        mode="a")

    file_hdlr.setFormatter(formatter)
    file_hdlr.suffix = "%Y%m%d"
    file_hdlr.rotator = GZipRotator()
    logger.addHandler(file_hdlr)

    stream_hdlr = logging.StreamHandler(stream=sys.stdout)
    stream_hdlr.setFormatter(formatter)
    stream_hdlr.setLevel(log_level)
    logger.addHandler(stream_hdlr)
    return logger

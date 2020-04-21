#! /usr/bin/env python3
# |*****************************************************
# * Copyright         : Copyright (C) 2019
# * Author            : ddc
# * License           : GPL v3
# * Python            : 3.6
# |*****************************************************
# # -*- coding: utf-8 -*-

import configparser
import datetime
import json
import logging
import logging.handlers
import os
import sys
import zipfile

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QFileDialog

from src.utils import constants, messages

_date_formatter = "%b/%d/%Y"
_time_formatter = "%H:%M:%S"


class Object:
    def __init__(self):
        self.created = str(datetime.datetime.now().strftime(f"{_date_formatter} {_time_formatter}"))

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def toDict(self):
        json_string = json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
        json_dict = json.loads(json_string)
        return json_dict


################################################################################
def get_all_ini_file_settings(file_name: str):
    dictionary = {}
    parser = configparser.ConfigParser(delimiters='=', allow_no_value=True)
    parser.optionxform = str  # this wont change all values to lowercase
    parser._interpolation = configparser.ExtendedInterpolation()
    parser.read(file_name)
    for section in parser.sections():
        # dictionary[section] = {}
        for option in parser.options(section):
            try:
                value = parser.get(section, option).replace("\"", "")
            except Exception:
                value = None
            if value is not None and len(value) == 0:
                value = None

            # dictionary[section][option] = value
            dictionary[option] = value
    return dictionary


################################################################################
def get_ini_settings(file_name: str, section: str, config_name: str):
    parser = configparser.ConfigParser(delimiters='=', allow_no_value=True)
    parser.optionxform = str  # this wont change all values to lowercase
    parser._interpolation = configparser.ExtendedInterpolation()
    parser.read(file_name)
    try:
        value = parser.get(section, config_name).replace("\"", "")
    except Exception:
        value = None
    if value is not None and len(value) == 0:
        value = None
    return value


################################################################################
# def set_file_settings(filename, section, config_name, value):
#     parser = configparser.ConfigParser(delimiters='=', allow_no_value=True)
#     parser.optionxform = str  # this wont change all values to lowercase
#     parser._interpolation = configparser.ExtendedInterpolation()
#     try:
#         parser.read(filename)
#         parser.set(section, config_name, value)
#         with open(filename, 'w') as configfile:
#             parser.write(configfile, space_around_delimiters=False)
#     except configparser.DuplicateOptionError:
#         return
#
#
################################################################################
# def zip_file(file_name:str, out_path:str):
#     zipOutputName = "archive"
#     fileType = "zip"
#     path = out_path
#     fileName = file_name
#     shutil.make_archive(zipOutputName,fileType,path,fileName)
#
#
################################################################################
def unzip_file(file_name: str, out_path: str):
    zipfile_path = file_name
    zipf = zipfile.ZipFile(zipfile_path)
    zipf.extractall(out_path)
    zipf.close()


################################################################################
def log_uncaught_exceptions(exc_type, exc_value, exc_traceback):
    logger = logging.getLogger(__name__)
    stderr_hdlr = logging.StreamHandler(stream=sys.stdout)
    stderr_hdlr.setLevel(constants.LOG_LEVEL)
    stderr_hdlr.setFormatter(constants.LOG_FORMATTER)
    logger.addHandler(stderr_hdlr)
    if issubclass(exc_type, KeyboardInterrupt) or issubclass(exc_type, EOFError):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logger.exception("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))


################################################################################
def setup_logging(self):
    logger = logging.getLogger()
    logger.setLevel(constants.LOG_LEVEL)
    file_hdlr = logging.handlers.RotatingFileHandler(
        filename=constants.ERROR_LOGS_FILENAME,
        maxBytes=10 * 1024 * 1024,
        encoding="utf-8",
        backupCount=5,
        mode='a')
    file_hdlr.setFormatter(constants.LOG_FORMATTER)
    logger.addHandler(file_hdlr)
    self.log = logging.getLogger(__name__)
    return self.log


################################################################################
def open_get_filename():
    filename = QFileDialog.getOpenFileName(None, 'Open file')[0]
    if filename == '':
        return None
    else:
        return str(filename)


################################################################################
# def get_download_path():
#     if constants.IS_WINDOWS:
#         import winreg
#         sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
#         downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
#         with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
#             downloads_path = winreg.QueryValueEx(key, downloads_guid)[0]
#         return downloads_path
#     else:
#         t1_path = str(os.path.expanduser("~/Downloads"))
#         t2_path = f"{t1_path}".split("\\")
#         downloads_path = '/'.join(t2_path)
#         return downloads_path.replace('\\', '/')


################################################################################
def get_pictures_path():
    if constants.IS_WINDOWS:
        import winreg
        sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
        pictures_guid = 'My Pictures'
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
            pictures_path = winreg.QueryValueEx(key, pictures_guid)[0]
        return pictures_path
    else:
        t1_path = str(os.path.expanduser("~/Pictures"))
        t2_path = f"{t1_path}".split("\\")
        pictures_path = '/'.join(t2_path)
        return pictures_path.replace('\\', '/')


################################################################################
def show_progress_bar(self, message, value):
    self.progressBar = QtWidgets.QProgressBar()
    _translate = QtCore.QCoreApplication.translate
    self.progressBar.setObjectName("progressBar")
    self.progressBar.setGeometry(QtCore.QRect(180, 150, 350, 25))
    self.progressBar.setMinimumSize(QtCore.QSize(350, 25))
    self.progressBar.setMaximumSize(QtCore.QSize(350, 25))
    self.progressBar.setSizeIncrement(QtCore.QSize(350, 25))
    self.progressBar.setBaseSize(QtCore.QSize(350, 25))
    self.progressBar.setMinimum(0)
    self.progressBar.setMaximum(100)
    self.progressBar.setWindowFlags(QtCore.Qt.FramelessWindowHint)
    self.progressBar.setAlignment(QtCore.Qt.AlignCenter)
    self.progressBar.setFormat(_translate("Main", message + "%p%"))
    self.progressBar.show()

    QtWidgets.QApplication.processEvents()
    self.progressBar.setValue(value)

    if value == 100:
        self.progressBar.hide()


################################################################################
def show_message_window(window_type: str, window_title: str, msg: str):
    if window_type.lower() == "error":
        icon = QtWidgets.QMessageBox.Critical
    elif window_type.lower() == "warning":
        icon = QtWidgets.QMessageBox.Warning
    elif window_type.lower() == "question":
        icon = QtWidgets.QMessageBox.Question
    else:
        icon = QtWidgets.QMessageBox.Information

    msgBox = QtWidgets.QMessageBox()
    msgBox.setIcon(icon)
    msgBox.setWindowTitle(window_title)
    msgBox.setInformativeText(msg)

    if window_type.lower() == "question":
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        msgBox.setDefaultButton(QtWidgets.QMessageBox.Yes)
    else:
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msgBox.setDefaultButton(QtWidgets.QMessageBox.Ok)

    user_answer = msgBox.exec_()
    return user_answer


################################################################################
def check_new_program_version(self):
    import requests
    remote_version_filename = constants.REMOTE_VERSION_FILENAME
    obj_return = Object()
    obj_return.new_version_available = False
    obj_return.new_version = None

    try:
        req = requests.get(remote_version_filename, stream=True, timeout=3)
        if req.status_code == 200:
            remote_version = req.text
            # getting rid of \n at the end of line
            remote_version = remote_version.replace("\\n", "").replace("\n", "")

            if float(remote_version) > float(self.client_version):
                obj_return.new_version_available = True
                obj_return.new_version_msg = f"Version {remote_version} available for download. " \
                                             "Restart the program to apply the update."
                obj_return.new_version = float(remote_version)
        else:
            self.log.error(
                f"{messages.error_check_new_version}\n{messages.remote_version_file_not_found} code:"
                f"{req.status_code}")
            show_message_window("critical", "ERROR", f"{messages.error_check_new_version}")
    except requests.exceptions.ConnectionError as e:
        self.log.error(f"{messages.dl_new_version_timeout} {e}")
        show_message_window("error", "ERROR", messages.dl_new_version_timeout)
    finally:
        return obj_return


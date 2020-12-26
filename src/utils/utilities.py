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

import requests
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog

from src.utils import constants, messages
from src.utils.create_files import CreateFiles

_date_formatter = "%b/%d/%Y"
_time_formatter = "%H:%M:%S"


class Object:
    def __init__(self):
        self._created = str(datetime.datetime.now().strftime(f"{_date_formatter} {_time_formatter}"))

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def toDict(self):
        json_string = json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
        json_dict = json.loads(json_string)
        return json_dict


################################################################################
class ProgressBar:
    def __init__(self):
        _width = 350
        _height = 25
        self.progressBar = QtWidgets.QProgressBar()
        self.progressBar.setObjectName("progressBar")
        self.progressBar.setMinimumSize(QtCore.QSize(_width, _height))
        self.progressBar.setMaximumSize(QtCore.QSize(_width, _height))
        self.progressBar.setSizeIncrement(QtCore.QSize(_width, _height))
        self.progressBar.setBaseSize(QtCore.QSize(_width, _height))
        # self.progressBar.setGeometry(QtCore.QRect(960, 540, width, height))
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(100)
        self.progressBar.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.progressBar.setAlignment(QtCore.Qt.AlignCenter)

    def setValues(self, message="", value=0):
        _translate = QtCore.QCoreApplication.translate
        self.progressBar.setFormat(_translate("Main", f"{message}  %p%"))
        self.progressBar.show()
        QtWidgets.QApplication.processEvents()
        self.progressBar.setValue(value)
        if value == 100:
            self.progressBar.close()

    def close(self):
        self.progressBar.close()


################################################################################
def get_current_path():
    return os.path.abspath(os.getcwd())


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
    _qfd = QFileDialog()
    _title = 'Open file'
    _path = "C:"
    _filter = "exe(*.exe)"
    _filename = QFileDialog.getOpenFileName(parent=_qfd, caption=_title, directory=_path, filter=_filter)
    if _filename[0] == '':
        return None
    else:
        return str(_filename[0])


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
    client_version = self.client_version
    remote_version = None
    remote_version_filename = constants.REMOTE_VERSION_FILENAME
    obj_return = Object()
    obj_return.new_version_available = False
    obj_return.new_version = None

    try:
        req = requests.get(remote_version_filename, stream=True)
        if req.status_code == 200:
            for line in req.iter_lines(decode_unicode=True):
                if line:
                    remote_version = line
                    break

            if remote_version is not None and (float(remote_version) > float(client_version)):
                obj_return.new_version_available = True
                obj_return.new_version_msg = f"Version {remote_version} available for download"
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


################################################################################
def check_dirs():
    try:
        if not os.path.exists(constants.PROGRAM_PATH):
            os.makedirs(constants.PROGRAM_PATH)
    except OSError as e:
        show_message_window("error", "ERROR", f"Error creating program directories.\n{e}")
        exit(1)


################################################################################
def check_files(self):
    create_files = CreateFiles(self)

    try:
        if not os.path.exists(constants.STYLE_QSS_FILENAME):
            create_files.create_style_file()
    except Exception as e:
        self.log.error(f"{e}")

    try:
        if not os.path.exists(constants.RESHADE_PRESET_FILENAME):
            create_files.create_reshade_preset_ini_file()
    except Exception as e:
        self.log.error(f"{e}")


################################################################################
def set_default_database_configs(self):
    from src.sql.initial_tables_sql import InitialTablesSql
    from src.sql.triggers_sql import TriggersSql
    from src.sql.configs_sql import ConfigsSql

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
def check_db_connection(self):
    from src.databases.databases import Databases

    databases = Databases(self)
    db_conn = databases.check_database_connection()

    if db_conn is None:
        error_db_conn = messages.error_db_connection
        msg_exit = messages.exit_program
        show_message_window("error", "ERROR", f"{error_db_conn}\n\n{msg_exit}")
        sys.exit(0)


################################################################################
def check_database_updated_columns(self):
    from src.sql.configs_sql import ConfigsSql
    from src.sql.update_tables_sql import UpdateTablesSql

    updateTablesSql = UpdateTablesSql(self)
    configSql = ConfigsSql(self)
    rsConfig = configSql.get_configs()
    if len(rsConfig) > 0:
        for eac in constants.NEW_CONFIG_TABLE_COLUMNS:
            if eac != "id".lower() and not eac in rsConfig[0].keys():
                    ut = updateTablesSql.update_config_table()


################################################################################
def set_icons(self):
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(resource_path("images/add.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    self.qtObj.add_button.setIcon(icon)

    icon1 = QtGui.QIcon()
    icon1.addPixmap(QtGui.QPixmap(resource_path("images/arrow.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    self.qtObj.edit_path_button.setIcon(icon1)

    icon2 = QtGui.QIcon()
    icon2.addPixmap(QtGui.QPixmap(resource_path("images/delete.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    self.qtObj.delete_button.setIcon(icon2)

    icon3 = QtGui.QIcon()
    icon3.addPixmap(QtGui.QPixmap(resource_path("images/apply.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    self.qtObj.apply_button.setIcon(icon3)

    icon4 = QtGui.QIcon()
    icon4.addPixmap(QtGui.QPixmap(resource_path("images/edit.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    self.qtObj.edit_config_button.setIcon(icon4)

    icon5 = QtGui.QIcon()
    icon5.addPixmap(QtGui.QPixmap(resource_path("images/controller.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    self.qtObj.main_tabWidget.addTab(self.qtObj.games_tab, icon5, "GAMES")

    icon6 = QtGui.QIcon()
    icon6.addPixmap(QtGui.QPixmap(resource_path("images/plugin.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    self.qtObj.edit_all_games_custom_config_button.setIcon(icon6)

    icon7 = QtGui.QIcon()
    icon7.addPixmap(QtGui.QPixmap(resource_path("images/gear.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    self.qtObj.main_tabWidget.addTab(self.qtObj.settings_tab, icon7, "SETTINGS")

    icon8 = QtGui.QIcon()
    icon8.addPixmap(QtGui.QPixmap(resource_path("images/paypal.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    self.qtObj.paypal_button.setIcon(icon8)

    icon9 = QtGui.QIcon()
    icon9.addPixmap(QtGui.QPixmap(resource_path("images/help.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    self.qtObj.main_tabWidget.addTab(self.qtObj.about_tab, icon9, "ABOUT")

    icon10 = QtGui.QIcon()
    icon10.addPixmap(QtGui.QPixmap(resource_path("images/update.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    self.qtObj.update_button.setIcon(icon10)


################################################################################
def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath("./src")
    return os.path.join(base_path, relative_path)


################################################################################
def check_game_dir(self):
    if self.selected_game is not None:
        if not os.path.isfile(self.selected_game.rs[0].get("path")):
            return False
    else:
        if not os.path.isfile(self.added_game_path):
            return False
    return True


################################################################################
def set_file_settings(filename: str, section: str, config_name: str, value):
    parser = configparser.ConfigParser(delimiters='=', allow_no_value=False)
    parser.optionxform = str  # this wont change all values to lowercase
    parser._interpolation = configparser.ExtendedInterpolation()
    parser.read(filename)
    parser.set(section, config_name, value)
    try:
        with open(filename, 'w') as configfile:
            parser.write(configfile, space_around_delimiters=False)
    except configparser.DuplicateOptionError:
        return

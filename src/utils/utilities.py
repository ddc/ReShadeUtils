#! /usr/bin/env python3
# |*****************************************************
# * Copyright         : Copyright (C) 2019
# * Author            : ddc
# * License           : GPL v3
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
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QFileDialog
from src.utils import constants, messages
from src.utils.create_files import CreateFiles


class Object:
    def __init__(self):
        self._created = str(datetime.datetime.now().strftime("%Y-%m-%d" "%H:%M:%S"))

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def to_dict(self):
        json_string = json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
        json_dict = json.loads(json_string)
        return json_dict


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
        self.progressBar.setWindowFlags(QtCore.Qt.WindowFlags.FramelessWindowHint)
        self.progressBar.setAlignment(QtCore.Qt.Alignment.AlignCenter)


    def set_values(self, message="", value=0):
        _translate = QtCore.QCoreApplication.translate
        self.progressBar.setFormat(_translate("Main", f"{message}  %p%"))
        self.progressBar.show()
        QtWidgets.QApplication.processEvents()
        self.progressBar.setValue(value)
        if value == 100:
            self.progressBar.close()


    def close(self):
        self.progressBar.close()


def get_current_path():
    return os.path.abspath(os.getcwd())


def get_ini_settings(file_name: str, section: str, config_name: str):
    parser = configparser.ConfigParser(delimiters="=", allow_no_value=True)
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


def unzip_file(file_name: str, out_path: str):
    zipfile_path = file_name
    zipf = zipfile.ZipFile(zipfile_path)
    zipf.extractall(out_path)
    zipf.close()


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


def setup_logging(self):
    logger = logging.getLogger()
    logger.setLevel(constants.LOG_LEVEL)
    file_hdlr = logging.handlers.RotatingFileHandler(
        filename=constants.ERROR_LOGS_FILENAME,
        maxBytes=10 * 1024 * 1024,
        encoding="UTF-8",
        backupCount=5,
        mode="a")
    file_hdlr.setFormatter(constants.LOG_FORMATTER)
    logger.addHandler(file_hdlr)
    self.log = logging.getLogger(__name__)
    return self.log


def open_get_filename():
    _qfd = QFileDialog()
    _title = "Open file"
    _path = "C:"
    _filter = "exe(*.exe)"
    _filename = QFileDialog.getOpenFileName(parent=_qfd, caption=_title, directory=_path, filter=_filter)
    if _filename[0] == "":
        return None
    else:
        return str(_filename[0])


# def get_download_path():
#     if constants.IS_WINDOWS:
#         import winreg
#         sub_key = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders"
#         downloads_guid = "{374DE290-123F-4565-9164-39C4925E467B}"
#         with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
#             downloads_path = winreg.QueryValueEx(key, downloads_guid)[0]
#         return downloads_path
#     else:
#         t1_path = str(os.path.expanduser("~/Downloads"))
#         t2_path = f"{t1_path}".split("\\")
#         downloads_path = "/".join(t2_path)
#         return downloads_path.replace("\\", "/")


def get_pictures_path():
    if constants.IS_WINDOWS:
        import winreg
        sub_key = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders"
        pictures_guid = "My Pictures"
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
            pictures_path = winreg.QueryValueEx(key, pictures_guid)[0]
        return pictures_path
    else:
        t1_path = str(os.path.expanduser("~/Pictures"))
        t2_path = t1_path.split("\\")
        pictures_path = "/".join(t2_path)
        return pictures_path.replace("\\", "/")


def show_message_window(window_type: str, window_title: str, msg: str):
    if window_type.lower() == "error":
        icon = QtWidgets.QMessageBox.Icon.Critical
    elif window_type.lower() == "warning":
        icon = QtWidgets.QMessageBox.Icon.Warning
    elif window_type.lower() == "question":
        icon = QtWidgets.QMessageBox.Icon.Question
    else:
        icon = QtWidgets.QMessageBox.Icon.Information

    msg_box = QtWidgets.QMessageBox()
    msg_box.setIcon(icon)
    msg_box.setWindowTitle(window_title)
    msg_box.setInformativeText(msg)

    if window_type.lower() == "question":
        msg_box.setStandardButtons(QtWidgets.QMessageBox.StandardButtons.Yes | QtWidgets.QMessageBox.StandardButtons.No)
        msg_box.setDefaultButton(QtWidgets.QMessageBox.StandardButtons.Yes)
    else:
        msg_box.setStandardButtons(QtWidgets.QMessageBox.StandardButtons.Ok)
        msg_box.setDefaultButton(QtWidgets.QMessageBox.StandardButtons.Ok)

    user_answer = msg_box.exec()
    return user_answer


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
                    remote_version = line.rstrip()
                    break

            if remote_version is not None and (float(remote_version) > float(client_version)):
                obj_return.new_version_available = True
                obj_return.new_version_msg = f"Version {remote_version} available for download"
                obj_return.new_version = float(remote_version)
        else:
            self.log.error(messages.error_check_new_version)
            self.log.error(f"{messages.remote_version_file_not_found} code: {req.status_code}")
            show_message_window("critical", "ERROR", f"{messages.error_check_new_version}")
    except requests.exceptions.ConnectionError as e:
        self.log.error(f"{messages.dl_new_version_timeout} {e}")
        show_message_window("error", "ERROR", messages.dl_new_version_timeout)
    finally:
        return obj_return


def check_dirs():
    try:
        if not os.path.exists(constants.PROGRAM_PATH):
            os.makedirs(constants.PROGRAM_PATH)
    except OSError as e:
        show_message_window("error", "ERROR", f"Error creating program directories.\n{e}")
        exit(1)


def check_files(self):
    create_files = CreateFiles(self)

    try:
        if not os.path.exists(constants.STYLE_QSS_FILENAME):
            create_files.create_style_file()
    except Exception as e:
        self.log.error(str(e))

    try:
        if not os.path.exists(constants.RESHADE_PRESET_FILENAME):
            create_files.create_reshade_preset_ini_file()
    except Exception as e:
        self.log.error(str(e))


def set_default_database_configs(self):
    from src.sql.initial_tables_sql import InitialTablesSql
    from src.sql.triggers_sql import TriggersSql
    from src.sql.configs_sql import ConfigsSql

    initial_tables_sql = InitialTablesSql(self)
    it = initial_tables_sql.create_initial_tables()
    if it is not None:
        err_msg = messages.error_create_sql_config_msg
        self.log.error(err_msg)

    config_sql = ConfigsSql(self)
    rs_config = config_sql.get_configs()
    if rs_config is not None and len(rs_config) == 0:
        config_sql.set_default_configs()

    triggers_sql = TriggersSql(self)
    tr = triggers_sql.create_triggers()
    if tr is not None:
        err_msg = messages.error_create_sql_config_msg
        self.log.error(err_msg)


def check_db_connection(self):
    from src.sql.sqlite3_connection import Sqlite3
    sqlite3 = Sqlite3(self)
    conn = sqlite3.create_connection()
    if conn is None:
        error_db_conn = messages.error_db_connection
        msg_exit = messages.exit_program
        show_message_window("error", "ERROR", f"{error_db_conn}\n\n{msg_exit}")
        sys.exit(1)
    else:
        conn.close()


def check_database_updated_columns(self):
    from src.sql.configs_sql import ConfigsSql
    from src.sql.update_tables_sql import UpdateTablesSql

    update_tables_sql = UpdateTablesSql(self)
    config_sql = ConfigsSql(self)
    rs_config = config_sql.get_configs()
    if len(rs_config) > 0:
        for eac in constants.NEW_CONFIG_TABLE_COLUMNS:
            if eac != "id".lower() and eac not in rs_config[0].keys():
                update_tables_sql.update_config_table()


def set_icons(self):
    icon_add = QtGui.QIcon()
    icon_add_pixmap = QtGui.QPixmap(resource_path("images/add.png"))
    icon_add.addPixmap(icon_add_pixmap, QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)

    icon_arrow = QtGui.QIcon()
    icon_arrow_pixmap = QtGui.QPixmap(resource_path("images/arrow.png"))
    icon_arrow.addPixmap(icon_arrow_pixmap, QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)

    icon_delete = QtGui.QIcon()
    icon_delete_pixmap = QtGui.QPixmap(resource_path("images/delete.png"))
    icon_delete.addPixmap(icon_delete_pixmap, QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)

    icon_apply = QtGui.QIcon()
    icon_apply_pixmap = QtGui.QPixmap(resource_path("images/apply.png"))
    icon_apply.addPixmap(icon_apply_pixmap, QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)

    icon_edit = QtGui.QIcon()
    icon_edit_pixmap = QtGui.QPixmap(resource_path("images/edit.png"))
    icon_edit.addPixmap(icon_edit_pixmap, QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)

    icon_controller = QtGui.QIcon()
    icon_controller_pixmap = QtGui.QPixmap(resource_path("images/controller.png"))
    icon_controller.addPixmap(icon_controller_pixmap, QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)

    icon_plugin = QtGui.QIcon()
    icon_plugin_pixmap = QtGui.QPixmap(resource_path("images/plugin.png"))
    icon_plugin.addPixmap(icon_plugin_pixmap, QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)

    icon_gear = QtGui.QIcon()
    icon_gear_pixmap = QtGui.QPixmap(resource_path("images/gear.png"))
    icon_gear.addPixmap(icon_gear_pixmap, QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)

    icon_paypal = QtGui.QIcon()
    icon_paypal_pixmap = QtGui.QPixmap(resource_path("images/paypal.png"))
    icon_paypal.addPixmap(icon_paypal_pixmap, QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)

    icon_help = QtGui.QIcon()
    icon_help_pixmap = QtGui.QPixmap(resource_path("images/help.png"))
    icon_help.addPixmap(icon_help_pixmap, QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)

    icon_update = QtGui.QIcon()
    icon_update_pixmap = QtGui.QPixmap(resource_path("images/update.png"))
    icon_update.addPixmap(icon_update_pixmap, QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)

    self.qtobj.add_button.setIcon(icon_add)
    self.qtobj.edit_path_button.setIcon(icon_arrow)
    self.qtobj.delete_button.setIcon(icon_delete)
    self.qtobj.apply_button.setIcon(icon_apply)
    self.qtobj.apply_all_games_custom_config_button.setIcon(icon_apply)
    self.qtobj.edit_config_button.setIcon(icon_edit)
    self.qtobj.main_tabWidget.addTab(self.qtobj.games_tab, icon_controller, "GAMES")
    self.qtobj.edit_all_games_custom_config_button.setIcon(icon_plugin)
    self.qtobj.main_tabWidget.addTab(self.qtobj.settings_tab, icon_gear, "SETTINGS")
    self.qtobj.paypal_button.setIcon(icon_paypal)
    self.qtobj.main_tabWidget.addTab(self.qtobj.about_tab, icon_help, "ABOUT")
    self.qtobj.update_button.setIcon(icon_update)


def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath("./src")
    return os.path.join(base_path, relative_path)


def check_game_dir(self):
    if self.selected_game is not None:
        if not os.path.isfile(self.selected_game.path):
            return False
    else:
        if not os.path.isfile(self.added_game_path):
            return False
    return True


def set_file_settings(filename: str, section: str, config_name: str, value):
    parser = configparser.ConfigParser(delimiters="=", allow_no_value=False)
    parser.optionxform = str  # this wont change all values to lowercase
    parser._interpolation = configparser.ExtendedInterpolation()
    parser.read(filename)
    parser.set(section, config_name, value)
    try:
        with open(filename, "w") as configfile:
            parser.write(configfile, space_around_delimiters=False)
    except configparser.DuplicateOptionError:
        return

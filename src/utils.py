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
import os
import sys
import zipfile
import requests
from src import constants, messages, qtutils
from src.create_files import CreateFiles


class Object:
    def __init__(self):
        self._created = str(datetime.datetime.now().strftime("%Y-%m-%d" "%H:%M:%S"))

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def to_dict(self):
        json_string = json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
        json_dict = json.loads(json_string)
        return json_dict


def get_current_path():
    path = os.path.abspath(os.getcwd())
    if path is not None:
        return os.path.normpath(path)
    return None


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
    if os.name == "nt":
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
            err_msg = f"{messages.error_check_new_version}\n{messages.remote_version_file_not_found}\ncode: {req.status_code}"
            qtutils.show_message_window(self.log, "error", err_msg)
    except requests.exceptions.ConnectionError as e:
        qtutils.show_message_window(self.log, "error", messages.dl_new_version_timeout)
    finally:
        return obj_return


def check_dirs():
    try:
        if not os.path.isdir(constants.PROGRAM_PATH):
            os.makedirs(constants.PROGRAM_PATH)
    except OSError as e:
        err_msg = f"{messages.unable_create_dirs}\n{e}"
        qtutils.show_message_window(None, "error", err_msg)
        exit(1)


def check_files(self):
    create_files = CreateFiles(self)

    try:
        if not os.path.isfile(constants.STYLE_QSS_FILENAME):
            create_files.create_style_file()
    except Exception as e:
        err_msg = f"{str(e)}\n\n{constants.STYLE_QSS_FILENAME}{messages.not_found}"
        qtutils.show_message_window(self.log, "error", err_msg)
        return False

    try:
        if not os.path.isfile(constants.RESHADE_PRESET_FILENAME):
            create_files.create_reshade_preset_ini_file()
    except Exception as e:
        err_msg = f"{str(e)}\n\n{constants.RESHADE_PRESET_FILENAME}{messages.not_found}"
        qtutils.show_message_window(self.log, "error", err_msg)
        return False

    return True


def set_default_database_configs(self):
    from src.sql.initial_tables_sql import InitialTablesSql
    from src.sql.triggers_sql import TriggersSql
    from src.sql.config_sql import ConfigSql

    initial_tables_sql = InitialTablesSql(self)
    it = initial_tables_sql.create_initial_tables()
    if it is not None:
        err_msg = messages.error_create_sql_config_msg
        self.log.error(err_msg)

    config_sql = ConfigSql(self)
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
        err_msg = f"{error_db_conn}\n\n{msg_exit}"
        if qtutils.show_message_window(self.log, "error", err_msg):
            sys.exit(1)
    else:
        conn.close()


def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath("src")
    return os.path.join(base_path, relative_path)


def check_game_file(self):
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


def get_binary_type(self, game_path):
    import struct

    image_file_machine_i386 = 332
    image_file_machine_ia64 = 512
    image_file_machine_amd64 = 34404
    image_file_machine_arm = 452
    image_file_machine_aarch64 = 43620

    with open(game_path, "rb") as f:
        s = f.read(2)
        if s != b"MZ":
            self.log.info("Not an EXE file")
            return None
        else:
            f.seek(60)
            s = f.read(4)
            header_offset = struct.unpack("<L", s)[0]
            f.seek(header_offset+4)
            s = f.read(2)
            machine = struct.unpack("<H", s)[0]

            if machine == image_file_machine_i386:
                # self.log.info("IA32 (32-bit x86)")
                return "IA32"
            elif machine == image_file_machine_ia64:
                # self.log.info("IA64 (Itanium)")
                return "IA64"
            elif machine == image_file_machine_amd64:
                # self.log.info("AMD64 (64-bit x86)")
                return "AMD64"
            elif machine == image_file_machine_arm:
                # self.log.info("ARM eabi (32-bit)")
                return "ARM-32bits"
            elif machine == image_file_machine_aarch64:
                # self.log.info("AArch64 (ARM-64, 64-bit)")
                return "ARM-64bits"
            else:
                # self.log.info(f"Unknown architecture {machine}")
                return None

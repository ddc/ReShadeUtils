# -*- coding: utf-8 -*-
import os
import struct
import sys
import zipfile
import subprocess
import configparser
from src.constants import variables, messages
from src.tools import misc_utils, reshade_utils
from src.database.dal.config_dal import ConfigDal
from src.tools.qt import qt_utils


def open_file(file_path):
    match variables.OS_NAME:
        case "Darwin":
            subprocess.call(("open", file_path))
        case "Windows":
            os.startfile(file_path)
        case _:
            subprocess.call(("xdg-open", file_path))


def list_files(directory, prefix):
    files_list = []
    if os.path.isdir(directory):
        files_list = [os.path.join(directory, f) for f in os.listdir(directory)
                      if os.path.isfile(os.path.join(directory, f))
                      and f.lower().startswith(prefix.lower())]
        files_list.sort(key=os.path.getmtime)
    return files_list


def get_ini_file_settings(file_name, section, config_name):
    parser = configparser.ConfigParser(delimiters="=", allow_no_value=True)
    parser.optionxform = str  # this will not change all values to lowercase
    parser._interpolation = configparser.ExtendedInterpolation()
    parser.read(file_name)
    try:
        value = parser.get(section, config_name).replace("\"", "")
    except:
        value = None
    if value is not None and len(value) == 0:
        value = None
    return value


def set_ini_file_settings(filename, section, config_name, value):
    parser = configparser.ConfigParser(delimiters="=", allow_no_value=True)
    parser.optionxform = str # this will not change all values to lowercase
    parser._interpolation = configparser.ExtendedInterpolation()
    parser.read(filename)
    parser.set(section, config_name, value)
    try:
        with open(filename, "w") as configfile:
            parser.write(configfile, space_around_delimiters=False)
    except configparser.DuplicateOptionError:
        return None


def unzip_reshade(self, local_reshade_exe):
    try:
        if os.path.isfile(variables.RESHADE32_PATH):
            os.remove(variables.RESHADE32_PATH)
        if os.path.isfile(variables.RESHADE64_PATH):
            os.remove(variables.RESHADE64_PATH)
        unzip_file(local_reshade_exe, variables.PROGRAM_PATH)
    except Exception as e:
        self.log.error(misc_utils.get_exception(e))


def unzip_file(file_name, out_path):
    zipfile_path = file_name
    zipf = zipfile.ZipFile(zipfile_path)
    zipf.extractall(out_path)
    zipf.close()


def check_reshade_dll_files(self):
    missing_reshade = True
    files_list = sorted(os.listdir(variables.PROGRAM_PATH))
    for filename in files_list:
        if variables.RESHADE_SETUP in filename:
            missing_reshade = False
    if missing_reshade:
        reshade_utils.download_reshade(self)

    config_sql = ConfigDal(self.db_session, self.log)
    rs_config = config_sql.get_configs()
    if rs_config is not None \
            and rs_config[0].get("reshade_version") is not None:
        self.reshade_version = rs_config[0].get("reshade_version")
        self.local_reshade_path = os.path.join(variables.PROGRAM_PATH,
                                               f"{variables.RESHADE_SETUP}_{self.reshade_version}.exe")
        self.qtobj.reshade_version_label.setText(f"{messages.info_reshade_version}{self.reshade_version}")
        self.enable_form(True)


def check_local_files(self):
    from src.files import Files
    files = Files(self)

    if not os.path.isfile(variables.RESHADE_INI_PATH):
        result = files.download_reshade_ini_file()
        if not result:
            err_msg = f"{variables.RESHADE_INI_PATH} {messages.not_found}"
            qt_utils.show_message_window(self.log, "error", err_msg)
            sys.exit(1)

    if not os.path.isfile(variables.RESHADE_PRESET_PATH):
        result = files.download_reshade_preset_file()
        if not result:
            err_msg = f"{variables.RESHADE_PRESET_PATH} {messages.not_found}"
            qt_utils.show_message_window(self.log, "error", err_msg)
            sys.exit(1)

    if not os.path.isfile(variables.QSS_PATH):
        result = files.download_qss_file()
        if not result:
            err_msg = f"{variables.QSS_PATH} {messages.not_found}"
            qt_utils.show_message_window(self.log, "error", err_msg)
            sys.exit(1)

    if not os.path.isfile(variables.ALEMBIC_CONFIG_PATH):
        result = files.download_alembic_file()
        if not result:
            err_msg = f"{variables.ALEMBIC_CONFIG_PATH} {messages.not_found}"
            qt_utils.show_message_window(self.log, "error", err_msg)
            sys.exit(1)


def check_game_file(self):
    if self.selected_game is not None:
        if not os.path.isfile(self.selected_game.path):
            return False
    else:
        if not os.path.isfile(self.added_game_path):
            return False
    return True


def get_binary_type(self, game_path):
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

            match machine:
                case 332:
                    self.log.debug("IA32 (32-bit x86)")
                    return "IA32"
                case 512:
                    self.log.debug("IA64 (Itanium)")
                    return "IA64"
                case 34404:
                    self.log.debug("AMD64 (64-bit x86)")
                    return "AMD64"
                case 452:
                    self.log.debug("ARM eabi (32-bit)")
                    return "ARM-32bits"
                case 43620:
                    self.log.debug("AArch64 (ARM-64, 64-bit)")
                    return "ARM-64bits"
                case _:
                    self.log.debug(f"Unknown architecture {machine}")
                    return None

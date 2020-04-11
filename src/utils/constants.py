#! /usr/bin/env python3
# |*****************************************************
# * Copyright         : Copyright (C) 2019
# * Author            : ddc
# * License           : GPL v3
# * Python            : 3.6
# |*****************************************************
# # -*- coding: utf-8 -*-

import logging
import os
import platform
import sys

from src.utils import utilities

VERSION = "3.3"
PROGRAM_NAME = "Reshade Utils"
SHORT_PROGRAM_NAME = "ReshadeUtils"
FULL_PROGRAM_NAME = f"{PROGRAM_NAME} v{VERSION}"
EXE_PROGRAM_NAME = f"{SHORT_PROGRAM_NAME}.exe"
################################################################################
DATE_FORMATTER = "%b/%d/%Y"
TIME_FORMATTER = "%H:%M:%S"
LOG_LEVEL = logging.INFO  # INFO or DEBUG
LOG_FORMATTER = logging.Formatter('%(asctime)s:[%(levelname)s]:[%(filename)s:%(funcName)s:%(lineno)d]:%(message)s',
                                  datefmt=f"[{DATE_FORMATTER} {TIME_FORMATTER}]")
################################################################################
IS_WINDOWS = os.name == "nt"
IS_MAC = sys.platform == "darwin"
IS_LINUX = sys.platform == "linux"
IS_64BIT = platform.machine().endswith("64")
PYTHON_OK = sys.version_info >= (3, 6)
################################################################################
APPDATA_PATH = os.getenv('APPDATA')  # returns AppData\Roaming. 'LOCALAPPDATA' == AppData\Local.
PROGRAM_PATH = f"{APPDATA_PATH}\\{SHORT_PROGRAM_NAME}"
################################################################################
DXGI = "dxgi.dll"
D3D9 = "d3d9.dll"
RESHADE_SHADERS = "Reshade-shaders"
RESHADE_INI = "Reshade.ini"
RESHADE_PLUGINS_INI = "Reshade_plugins.ini"
RESHADE_X64LOG = "dxgi.log"
RESHADE_X32LOG = "d3d9.log"
RESHADE32 = "Reshade32.dll"
RESHADE64 = "ReShade64.dll"
################################################################################
RESHADE32_PATH = f"{PROGRAM_PATH}\\{RESHADE32}"
RESHADE64_PATH = f"{PROGRAM_PATH}\\{RESHADE64}"
SHADERS_ZIP_PATH = f"{PROGRAM_PATH}\\{RESHADE_SHADERS}.zip"
SHADERS_SRC_PATH = f"{PROGRAM_PATH}\\{RESHADE_SHADERS}"
RES_SHAD_MPATH = f"{PROGRAM_PATH}\\{RESHADE_SHADERS}-master"
RESHADE_SCREENSHOT_PATH = f"{utilities.get_pictures_path()}\\Screenshots"
################################################################################
DB_SETTINGS_FILENAME = f"{PROGRAM_PATH}\\db_settings.ini"
SQLITE3_FILENAME = f"{PROGRAM_PATH}\\database.db"
STYLE_QSS_FILENAME = f"{PROGRAM_PATH}\\style.qss"
ERROR_LOGS_FILENAME = f"{PROGRAM_PATH}\\errors.log"
RESHADE_PLUGINS_FILENAME = f"{PROGRAM_PATH}\\{RESHADE_PLUGINS_INI}"
################################################################################
GITHUB_EXE_PROGRAM_URL = f"https://github.com/ddc/{SHORT_PROGRAM_NAME}/releases/download/v"
REMOTE_VERSION_FILENAME = f"https://raw.github.com/ddc/{SHORT_PROGRAM_NAME}/master/VERSION"
CSS_REMOTE_FILENAME = f"https://raw.github.com/ddc/{SHORT_PROGRAM_NAME}/master/src/utils/style.qss"
SHADERS_ZIP_URL = "https://github.com/crosire/reshade-shaders/archive/master.zip"
RESHADE_WEBSITE_URL = "https://reshade.me"
RESHADE_EXE_URL = "https://reshade.me/downloads/ReShade_Setup_"
################################################################################
# table columns after fisrt release
NEW_CONFIG_TABLE_COLUMNS = ["silent_reshade_updates", "program_version"]

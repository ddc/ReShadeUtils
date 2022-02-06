# |*****************************************************
# * Copyright         : Copyright (C) 2022
# * Author            : ddc
# * License           : GPL v3
# |*****************************************************
# -*- coding: utf-8 -*-
import os
import sys
from src import utils


DEBUG = False

VERSION = "4.4"
PROGRAM_NAME = "Reshade Utils"
SHORT_PROGRAM_NAME = "ReshadeUtils"
FULL_PROGRAM_NAME = f"{PROGRAM_NAME} v{VERSION}"
EXE_PROGRAM_NAME = f"{SHORT_PROGRAM_NAME}.exe"
DAYS_TO_KEEP_LOGS = 30
################################################################################
RESET_DATABASE_VERSION = "4.2"
PROGRAM_PATH = os.path.normpath(os.path.join(os.path.dirname(sys.argv[0]), "dev") if DEBUG
                                else os.path.join(os.getenv("LOCALAPPDATA"), SHORT_PROGRAM_NAME))
################################################################################
RESHADE_SETUP = "ReShade_Setup"
RESHADE_SHADERS = "Reshade-shaders"
RESHADE_INI = "Reshade.ini"
RESHADE_PRESET_INI = "ReShadePreset.ini"
RESHADEGUI_INI = "ReShadeGUI.ini"
RESHADE32_DLL = "Reshade32.dll"
RESHADE64_DLL = "ReShade64.dll"
DXGI_DLL = "dxgi.dll"
D3D9_DLL = "d3d9.dll"
OPENGL_DLL = "opengl32.dll"
################################################################################
DX9_DISPLAY_NAME = "DirectX 9"
DXGI_DISPLAY_NAME = "DirectX (10,11,12)"
OPENGL_DISPLAY_NAME = "OpenGL"
################################################################################
RESHADE32_PATH = os.path.join(PROGRAM_PATH, RESHADE32_DLL)
RESHADE64_PATH = os.path.join(PROGRAM_PATH, RESHADE64_DLL)
SHADERS_ZIP_PATH = os.path.join(PROGRAM_PATH, f"{RESHADE_SHADERS}.zip")
SHADERS_SRC_PATH = os.path.join(PROGRAM_PATH, RESHADE_SHADERS)
RES_SHAD_MPATH = os.path.join(PROGRAM_PATH, f"{RESHADE_SHADERS}-master")
RESHADE_SCREENSHOT_PATH = os.path.join(utils.get_pictures_path(), "Screenshots")
################################################################################
SQLITE3_PATH = os.path.join(PROGRAM_PATH, "database.db")
QSS_PATH = os.path.join(PROGRAM_PATH, "style.qss")
RESHADE_INI_PATH = os.path.join(PROGRAM_PATH, RESHADE_INI)
RESHADE_PRESET_PATH = os.path.join(PROGRAM_PATH, RESHADE_PRESET_INI)
################################################################################
BRANCH = "dev" if DEBUG else "master"
GITHUB_EXE_PROGRAM_URL = f"https://github.com/ddc/{SHORT_PROGRAM_NAME}/releases/download/v"
GITHUB_LATEST_VERSION_URL = f"https://github.com/ddc/{SHORT_PROGRAM_NAME}/releases/latest"
REMOTE_VERSION_FILENAME = f"https://raw.github.com/ddc/{SHORT_PROGRAM_NAME}/{BRANCH}/VERSION"
RESHADE_REMOTE_FILENAME = f"https://raw.github.com/ddc/{SHORT_PROGRAM_NAME}/{BRANCH}/resources/files/Reshade.ini"
PRESET_REMOTE_FILENAME = f"https://raw.github.com/ddc/{SHORT_PROGRAM_NAME}/{BRANCH}/resources/files/ReShadePreset.ini"
QSS_REMOTE_FILENAME = f"https://raw.github.com/ddc/{SHORT_PROGRAM_NAME}/{BRANCH}/resources/files/style.qss"
SHADERS_ZIP_URL = "https://github.com/crosire/reshade-shaders/archive/refs/heads/master.zip"
RESHADE_WEBSITE_URL = "https://reshade.me"
RESHADE_EXE_URL = f"https://reshade.me/downloads/{RESHADE_SETUP}_"
PAYPAL_URL = "https://www.paypal.com/donate/?cmd=_s-xclick&hosted_button_id=ENK474GPJMVTE"
################################################################################

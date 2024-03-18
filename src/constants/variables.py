# -*- coding: utf-8 -*-
import os
import platform
from ddcUtils import MiscUtils, OsUtils


DEBUG = False
VERSION = (5, 0, 0)
VERSION_STR = ".".join(map(str, VERSION))
RESHADE_NAME = "ReShade"
PROGRAM_NAME = f"{RESHADE_NAME} Utils"
SHORT_PROGRAM_NAME = f"{RESHADE_NAME}Utils"
FULL_PROGRAM_NAME = f"{PROGRAM_NAME} v{VERSION_STR}"
EXE_PROGRAM_NAME = f"{SHORT_PROGRAM_NAME}.exe"
LOG_FILE_NAME = f"{SHORT_PROGRAM_NAME}.log"
DAYS_TO_KEEP_LOGS = 7
MAX_LOG_MBYTES = 5
OS_NAME = platform.system()
# ############################################################################
_local_app_data = os.getenv("LOCALAPPDATA") if OsUtils.is_windows() else os.path.join(os.getenv("HOME"), ".local", "share")
PROGRAM_DIR = os.path.normpath(os.path.join(_local_app_data, SHORT_PROGRAM_NAME))
# ############################################################################
RESHADE_SETUP = f"{RESHADE_NAME}_Setup"
RESHADE_INI = f"{RESHADE_NAME}.ini"
RESHADE_PRESET_INI = f"{RESHADE_NAME}Preset.ini"
RESHADEGUI_INI = f"{RESHADE_NAME}GUI.ini"
RESHADE32 = f"{RESHADE_NAME}32"
RESHADE64 = f"{RESHADE_NAME}64"
RESHADE32_DLL = f"{RESHADE32}.dll"
RESHADE64_DLL = f"{RESHADE64}.dll"
RESHADE_SHADERS = f"{RESHADE_NAME}-shaders".lower()
D3D9_DLL = "d3d9.dll"
DXGI_DLL = "dxgi.dll"
OPENGL_DLL = "opengl32.dll"
QSS_FILE_NAME = "style.qss"
ABOUT_FILE_NAME = "about.html"
ALL_DLL_NAMES = (D3D9_DLL, DXGI_DLL, OPENGL_DLL)
# ############################################################################
DX9_DISPLAY_NAME = "DirectX 9"
DXGI_DISPLAY_NAME = "DirectX (10,11,12)"
OPENGL_DISPLAY_NAME = "OpenGL"
ALL_ARCHITECTURES = ("32bits", "64bits")
ALL_APIS = (DX9_DISPLAY_NAME, DXGI_DISPLAY_NAME, OPENGL_DISPLAY_NAME)
# ############################################################################
DATABASE_PATH = os.path.join(PROGRAM_DIR, "database.db")
ALEMBIC_MIGRATIONS_DIR = os.path.join(PROGRAM_DIR, "src", "database", "migrations")
ALEMBIC_INI_FILE_PATH = os.path.join(ALEMBIC_MIGRATIONS_DIR, "alembic.ini")
LOGS_DIR = os.path.join(PROGRAM_DIR, "logs")
# ############################################################################
RESHADE32_PATH = os.path.join(PROGRAM_DIR, RESHADE32_DLL)
RESHADE64_PATH = os.path.join(PROGRAM_DIR, RESHADE64_DLL)
RESHADE_INI_PATH = os.path.join(PROGRAM_DIR, RESHADE_INI)
RESHADE_PRESET_PATH = os.path.join(PROGRAM_DIR, RESHADE_PRESET_INI)
# ############################################################################
SRC_DIR = os.path.join(PROGRAM_DIR, "src")
QSS_PATH = os.path.join(SRC_DIR, "ui", QSS_FILE_NAME)
ABOUT_PATH = os.path.join(SRC_DIR, "ui", ABOUT_FILE_NAME)
SHADERS_AND_TEXTURES_LOCAL_DIR = os.path.join(SRC_DIR, RESHADE_SHADERS)
SHADERS_LOCAL_DIR = os.path.join(SHADERS_AND_TEXTURES_LOCAL_DIR, "Shaders")
TEXTURES_LOCAL_DIR = os.path.join(SHADERS_AND_TEXTURES_LOCAL_DIR, "Textures")
SHADERS_NVIDIA_LOCAL_TEMP_DIR = os.path.join(SHADERS_AND_TEXTURES_LOCAL_DIR, "ShadersAndTextures")
SHADERS_ZIP_PATH = os.path.join(SRC_DIR, f"{RESHADE_SHADERS}-nvidia.zip")
SHADERS_AND_TEXTURES_NVIDIA_LOCAL_TEMP_DIR = os.path.join(SRC_DIR, f"{RESHADE_SHADERS}-nvidia")
RESHADE_SCREENSHOT_DIR = os.path.join(OsUtils().get_pictures_path(), "Screenshots")
# ############################################################################
_github_raw_files_uri = f"https://raw.github.com/ddc/{SHORT_PROGRAM_NAME}/master"
REMOTE_VERSION_FILENAME = f"{_github_raw_files_uri}/VERSION"
REMOTE_RESHADE_FILENAME = f"{_github_raw_files_uri}/src/data/reshade/Reshade.ini"
REMOTE_PRESET_FILENAME = f"{_github_raw_files_uri}/src/data/reshade/ReShadePreset.ini"
REMOTE_QSS_FILENAME = f"{_github_raw_files_uri}/src/data/reshade/style.qss"
REMOTE_ABOUT_FILENAME = f"{_github_raw_files_uri}/src/ui/about.html"
# ############################################################################
GITHUB_EXE_PROGRAM_URL = f"https://github.com/ddc/{SHORT_PROGRAM_NAME}/releases/download"
GITHUB_LATEST_VERSION_URL = f"https://github.com/ddc/{SHORT_PROGRAM_NAME}/releases/latest"
SHADERS_ZIP_URL = "https://github.com/crosire/reshade-shaders/archive/refs/heads/nvidia.zip"
RESHADE_WEBSITE_URL = "https://reshade.me"
RESHADE_EXE_URL = f"https://reshade.me/downloads/{RESHADE_SETUP}_"
ALEMBIC_MIGRATIONS_REMOTE_URL = f"https://github.com/ddc/{SHORT_PROGRAM_NAME}/blob/master/src/database/migrations"
TEXTURES_REMOTE_URL = f"https://github.com/ddc/{SHORT_PROGRAM_NAME}/blob/master/src/data/reshade/textures"
PAYPAL_URL = "https://www.paypal.com/donate/?cmd=_s-xclick&hosted_button_id=ENK474GPJMVTE"

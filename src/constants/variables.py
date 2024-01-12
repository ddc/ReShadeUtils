# -*- coding: utf-8 -*-
import os
import sys
import platform
from src.tools import misc_utils


DEBUG = False
VERSION = 4.7
PROGRAM_NAME = "Reshade Utils"
SHORT_PROGRAM_NAME = "ReshadeUtils"
FULL_PROGRAM_NAME = f"{PROGRAM_NAME} v{VERSION}"
EXE_PROGRAM_NAME = f"{SHORT_PROGRAM_NAME}.exe"
DAYS_TO_KEEP_LOGS = 7
OS_NAME = platform.system()
# ############################################################################
if DEBUG:
    PROGRAM_PATH = os.path.normpath(os.path.join(os.path.dirname(sys.argv[0]), "dev"))
else:
    _local_app_data = os.getenv("LOCALAPPDATA") if OS_NAME == "Windows" \
        else os.path.join(os.getenv("HOME"), ".local", "share")
    PROGRAM_PATH = os.path.normpath(os.path.join(_local_app_data, SHORT_PROGRAM_NAME))
# ############################################################################
RESHADE_SETUP = "ReShade_Setup"
RESHADE_SHADERS = "reshade-shaders"
RESHADE_INI = "ReShade.ini"
RESHADE_PRESET_INI = "ReShadePreset.ini"
RESHADEGUI_INI = "ReShadeGUI.ini"
RESHADE32_DLL = "ReShade32.dll"
RESHADE64_DLL = "ReShade64.dll"
DXGI_DLL = "dxgi.dll"
D3D9_DLL = "d3d9.dll"
OPENGL_DLL = "opengl32.dll"
# ############################################################################
DX9_DISPLAY_NAME = "DirectX 9"
DXGI_DISPLAY_NAME = "DirectX (10,11,12)"
OPENGL_DISPLAY_NAME = "OpenGL"
ALL_ARCHITECTURES = ("32bits", "64bits",)
ALL_APIS = (DX9_DISPLAY_NAME, DXGI_DISPLAY_NAME, OPENGL_DISPLAY_NAME)
# ############################################################################
RESHADE32_PATH = os.path.join(PROGRAM_PATH, RESHADE32_DLL)
RESHADE64_PATH = os.path.join(PROGRAM_PATH, RESHADE64_DLL)
SHADERS_ZIP_PATH = os.path.join(PROGRAM_PATH, f"{RESHADE_SHADERS}-nvidia.zip")
SHADERS_SRC_PATH = os.path.join(PROGRAM_PATH, RESHADE_SHADERS)
RES_SHAD_MPATH = os.path.join(PROGRAM_PATH, f"{RESHADE_SHADERS}-nvidia")
RES_SHAD_NVIDIA_PATH = os.path.join(SHADERS_SRC_PATH, "ShadersAndTextures")
RESHADE_SCREENSHOT_PATH = os.path.join(misc_utils.get_pictures_path(), "Screenshots")
RESHADE_INI_PATH = os.path.join(PROGRAM_PATH, RESHADE_INI)
RESHADE_PRESET_PATH = os.path.join(PROGRAM_PATH, RESHADE_PRESET_INI)
DATABASE_PATH = os.path.join(PROGRAM_PATH, "database.db")
QSS_PATH = os.path.join(PROGRAM_PATH, "style.qss")
ALEMBIC_CONFIG_PATH = os.path.join(PROGRAM_PATH.replace("/dev", ""), "alembic.ini")
# ############################################################################
BRANCH = misc_utils.get_active_branch_name() if DEBUG else "master"
GITHUB_EXE_PROGRAM_URL = f"https://github.com/ddc/{SHORT_PROGRAM_NAME}/releases/download"
GITHUB_LATEST_VERSION_URL = f"https://github.com/ddc/{SHORT_PROGRAM_NAME}/releases/latest"
REMOTE_VERSION_FILENAME = f"https://raw.github.com/ddc/{SHORT_PROGRAM_NAME}/{BRANCH}/VERSION"
REMOTE_RESHADE_FILENAME = f"https://raw.github.com/ddc/{SHORT_PROGRAM_NAME}/{BRANCH}/src/data/files/Reshade.ini"
REMOTE_PRESET_FILENAME = f"https://raw.github.com/ddc/{SHORT_PROGRAM_NAME}/{BRANCH}/src/data/files/ReShadePreset.ini"
REMOTE_QSS_FILENAME = f"https://raw.github.com/ddc/{SHORT_PROGRAM_NAME}/{BRANCH}/src/data/files/style.qss"
REMOTE_ALEMBIC_FILENAME = f"https://raw.github.com/ddc/{SHORT_PROGRAM_NAME}/{BRANCH}/src/data/files/alembic.ini"
SHADERS_ZIP_URL = "https://github.com/crosire/reshade-shaders/archive/refs/heads/nvidia.zip"
RESHADE_WEBSITE_URL = "https://reshade.me"
RESHADE_EXE_URL = f"https://reshade.me/downloads/{RESHADE_SETUP}_"
PAYPAL_URL = "https://www.paypal.com/donate/?cmd=_s-xclick&hosted_button_id=ENK474GPJMVTE"

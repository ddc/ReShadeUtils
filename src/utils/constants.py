#! /usr/bin/env python3
#|*****************************************************
# * Copyright         : Copyright (C) 2019
# * Author            : ddc
# * License           : GPL v3
# * Python            : 3.6
#|*****************************************************
# # -*- coding: utf-8 -*-
import os
import sys
import platform
import logging
from src.utils import utils
################################################################################
################################################################################
################################################################################
PROGRAM_NAME            = "Reshade Utils"
VERSION                 = "1.8"
################################################################################
################################################################################
################################################################################
############### DO NOT CHANGE ANY OF THESE VARS BELLOW #########################
################################################################################
################################################################################
################################################################################
short_program_name      = "ReshadeUtils"
full_program_name       = f"{PROGRAM_NAME} v{VERSION}"
exe_program_name        = f"{short_program_name}.exe"
################################################################################
date_formatter          = "%b/%d/%Y"
time_formatter          = "%H:%M:%S"
LOG_LEVEL               = logging.INFO
LOG_FORMATTER           = logging.Formatter('%(asctime)s:[%(levelname)s]:[%(filename)s:%(funcName)s:%(lineno)d]:%(message)s',
                                datefmt=f"[{date_formatter} {time_formatter}]")
################################################################################
IS_WINDOWS              = os.name == "nt"
IS_MAC                  = sys.platform == "darwin"
IS_LINUX                = sys.platform == "linux"
IS_64BIT                = platform.machine().endswith("64")
PYTHON_OK               = sys.version_info >= (3,6)
################################################################################
my_docs_path            = str(utils.get_my_documents_path())
program_path            = f"{my_docs_path}\{short_program_name}"
################################################################################
dxgi                    = "dxgi.dll"
d3d9                    = "d3d9.dll"
reshade_shaders         = "Reshade-shaders"
reshade_ini             = "Reshade.ini"
reshade_plugins_ini     = "Reshade_plugins.ini"
reshade_x64log          = "dxgi.log"
reshade_x32log          = "d3d9.log"
################################################################################
reshade32_path          = f"{program_path}\ReShade32.dll"
reshade64_path          = f"{program_path}\ReShade64.dll"
shaders_zip_path        = f"{program_path}\{reshade_shaders}.zip"
shaders_src_path        = f"{program_path}\{reshade_shaders}"
res_shad_mpath          = f"{program_path}\{reshade_shaders}-master"
reshade_screenshot_path = f"{my_docs_path}\Screenshots\\".replace("Documents", "Pictures")  
################################################################################
db_settings_filename    = f"{program_path}\db_settings.ini"
database_filename       = f"{program_path}\database.db"
style_qss_filename      = f"{program_path}\style.qss"
error_logs_filename     = f"{program_path}\errors.log"
reshade_plugins_filename= f"{program_path}\{reshade_plugins_ini}"
################################################################################
github_exe_program_url  = f"https://github.com/ddc/{short_program_name}/releases/download/v{VERSION}/{exe_program_name}"
remote_version_filename = f"https://raw.github.com/ddc/{short_program_name}/master/VERSION"
css_remote_filename     = f"https://raw.github.com/ddc/{short_program_name}/master/src/utils/style.qss"
shaders_zip_url         = "https://github.com/crosire/reshade-shaders/archive/master.zip"
reshade_website_url     = "https://reshade.me"
reshade_exe_url         = "https://reshade.me/downloads/ReShade_Setup_"
################################################################################

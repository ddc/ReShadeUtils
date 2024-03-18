# -*- coding: utf-8 -*-
import os
import sys
from ddcUtils import FileUtils, get_exception
from src.constants import messages, variables
from src.database.dal.config_dal import ConfigDal
from src.tools import reshade_utils
from src.tools.qt import qt_utils


def list_reshade_files(directory):
    return FileUtils.list_files(directory=directory, starts_with="reshade")


def unzip_reshade(self, local_reshade_exe):
    try:
        if os.path.isfile(variables.RESHADE32_PATH):
            FileUtils.remove(variables.RESHADE32_PATH)
        if os.path.isfile(variables.RESHADE64_PATH):
            FileUtils.remove(variables.RESHADE64_PATH)
        FileUtils.unzip(local_reshade_exe, variables.PROGRAM_PATH)
    except Exception as e:
        self.log.error(get_exception(e))


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
    if rs_config is not None and rs_config[0].get("reshade_version") is not None:
        self.reshade_version = rs_config[0].get("reshade_version")
        self.local_reshade_path = os.path.join(variables.PROGRAM_PATH, f"{variables.RESHADE_SETUP}_{self.reshade_version}.exe")
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

    FileUtils.remove(variables.ALEMBIC_MIGRATIONS_DIR)
    result = files.download_alembic_dir()
    if not result:
        qt_utils.show_message_window(self.log, "error", messages.error_dl_alembic_files)
        sys.exit(1)


def check_game_file(self):
    if self.selected_game is not None:
        if not os.path.isfile(self.selected_game.path):
            return False
    else:
        if not os.path.isfile(self.added_game_path):
            return False
    return True

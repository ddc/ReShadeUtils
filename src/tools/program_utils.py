# -*- coding: utf-8 -*-
import os
import requests
from alembic import command
from alembic.config import Config
from ddcUtils import FileUtils, get_exception, OsUtils, ConfFileUtils
from src.constants import messages, variables
from src.tools.qt import qt_utils
from src.database.dal.config_dal import ConfigDal


def download_alembic_dir(log):
    FileUtils.remove(variables.ALEMBIC_MIGRATIONS_DIR)
    local_dir = variables.ALEMBIC_MIGRATIONS_DIR
    alembic_migrations_remote_url = variables.ALEMBIC_MIGRATIONS_REMOTE_URL
    result = FileUtils().download_github_dir(alembic_migrations_remote_url, local_dir)
    if not result:
        qt_utils.show_message_window(log, "error", messages.error_dl_alembic_files)
    return result


def run_alembic_migrations(log):
    if download_alembic_dir(log):
        alembic_cfg = Config(variables.ALEMBIC_INI_FILE_PATH)
        command.upgrade(alembic_cfg, "head")


def show_info_messages(db_session, log):
    show_messages = False
    config_sql = ConfigDal(db_session, log)
    rs_config = config_sql.get_configs()
    if rs_config is None or (rs_config is not None and rs_config[0]["show_info_messages"]):
        show_messages = True
    return show_messages


def check_program_updates(log, db_session):
    config_sql = ConfigDal(db_session, log)
    rs_config = config_sql.get_configs()
    if rs_config:
        check_for_updates = rs_config[0].get("check_program_updates", True)
        if check_for_updates:
            remote_version = get_program_remote_version(log)
            if remote_version > variables.VERSION:
                remote_version_str = ".".join(map(str, remote_version))
                return remote_version_str
    return None


def get_program_remote_version(log):
    remote_version = (0, 0, 0)
    remote_version_filename = variables.REMOTE_VERSION_FILENAME
    try:
        req = requests.get(remote_version_filename, stream=True)
        if req.status_code == 200:
            for line in req.iter_lines(decode_unicode=True):
                remote_version = line.rstrip()
                break
            remote_version = tuple(int(x) for x in remote_version.split("."))
        else:
            err_msg = (
                f"{messages.error_check_new_version}\n"
                f"{messages.remote_version_file_not_found}\n"
                f"code: {req.status_code}"
            )
            qt_utils.show_message_window(log, "error", err_msg)
            log.error(err_msg)
    except requests.exceptions.ConnectionError:
        qt_utils.show_message_window(log, "error", messages.dl_new_version_timeout)
    return remote_version


def download_new_program_version(db_session, log, local_path, new_version):
    program_name = variables.EXE_PROGRAM_NAME if OsUtils.is_windows() else variables.SHORT_PROGRAM_NAME
    program_url = f"{variables.GITHUB_EXE_PROGRAM_URL}/v{new_version}/{program_name}"
    r = requests.get(program_url)
    if r.status_code == 200:
        with open(local_path, "wb") as outfile:
            outfile.write(r.content)
        if show_info_messages(db_session, log):
            qt_utils.show_message_window(log, "info", f"{messages.program_updated} {new_version}")
    else:
        qt_utils.show_message_window(log, "error", messages.error_dl_new_version)
        log.error(f"{messages.error_dl_new_version} {r.status_code} {r}")


def get_screenshot_path(db_session, log, game_dir, game_name):
    game_screenshots_path = None
    config_sql = ConfigDal(db_session, log)
    rs_config = config_sql.get_configs()
    if rs_config and rs_config[0]["create_screenshots_folder"]:
        game_screenshots_path = os.path.join(variables.RESHADE_SCREENSHOT_DIR, game_name)
        try:
            if not os.path.isdir(variables.RESHADE_SCREENSHOT_DIR):
                os.makedirs(variables.RESHADE_SCREENSHOT_DIR)
        except OSError as e:
            log.error(f"mkdir: {variables.RESHADE_SCREENSHOT_DIR}: {get_exception(e)}")

        try:
            if not os.path.isdir(game_screenshots_path):
                os.makedirs(game_screenshots_path)
        except OSError as e:
            log.error(f"mkdir: {game_screenshots_path}: {get_exception(e)}")
    else:
        reshade_ini_filepath = str(os.path.join(game_dir, variables.RESHADE_INI))
        reshade_config_screenshot_path = ConfFileUtils().get_value(reshade_ini_filepath, "SCREENSHOT", "SavePath")
        if reshade_config_screenshot_path is not None:
            game_screenshots_path = reshade_config_screenshot_path
        elif os.path.isdir(os.path.join(variables.RESHADE_SCREENSHOT_DIR, game_name)):
            game_screenshots_path = os.path.join(variables.RESHADE_SCREENSHOT_DIR, game_name)
    return game_screenshots_path

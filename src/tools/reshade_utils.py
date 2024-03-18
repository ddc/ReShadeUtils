# -*- coding: utf-8 -*-
import os
import shutil
import sys
import tempfile
import zipfile
import requests
from bs4 import BeautifulSoup
from ddcUtils import ConfFileUtils, FileUtils, get_exception
from src.constants import messages, variables
from src.database.dal.config_dal import ConfigDal
from src.events import games_tab_events
from src.tools import program_utils
from src.tools.qt import qt_utils
from src.tools.qt.progressbar import ProgressBar


def check_game_path_exists(selected_game_path):
    if os.path.isfile(selected_game_path):
        return True
    return False


def get_reshade_dll_log_names(api):
    match api:
        case variables.OPENGL_DISPLAY_NAME:
            reshade_dll = variables.OPENGL_DLL
        case variables.DX9_DISPLAY_NAME:
            reshade_dll = variables.D3D9_DLL
        case _:
            reshade_dll = variables.DXGI_DLL
    return [reshade_dll, f"{os.path.splitext(reshade_dll)[0]}.log"]


def unzip_reshade(log, local_reshade_exe):
    log.debug("unzip_reshade")

    try:
        reshade_32_files = FileUtils.list_files(variables.PROGRAM_DIR, starts_with=variables.RESHADE32)
        for file in reshade_32_files:
            FileUtils.remove(file)

        reshade_64_files = FileUtils.list_files(variables.PROGRAM_DIR, starts_with=variables.RESHADE64)
        for file in reshade_64_files:
            FileUtils.remove(file)

        FileUtils.unzip(local_reshade_exe, variables.PROGRAM_DIR)
        return True
    except Exception as e:
        log.error(get_exception(e))
        return False


def check_reshade_executable_file(db_session, log, qtobj):
    log.debug("check_reshade_executable_file")

    local_reshade = FileUtils.list_files(variables.PROGRAM_DIR, starts_with=variables.RESHADE_SETUP)
    if not local_reshade:
        remote_reshade_version = get_remote_reshade_version(log)
        download_reshade(log, remote_reshade_version)

    config_sql = ConfigDal(db_session, log)
    rs_config = config_sql.get_configs()
    if rs_config and rs_config[0].get("reshade_version") is not None:
        db_reshade_version = rs_config[0].get("reshade_version")
        qtobj.reshade_version_label.setText(f"{messages.info_reshade_version}{db_reshade_version}")
        qt_utils.enable_form(qtobj, True)


def check_reshade_config_files(log):
    log.debug("check_reshade_config_files")

    if not os.path.isfile(variables.RESHADE_INI_PATH):
        result = download_reshade_ini_file()
        if not result:
            err_msg = f"{variables.RESHADE_INI_PATH} {messages.not_found}"
            qt_utils.show_message_window(log, "error", err_msg)
            sys.exit(1)

    if not os.path.isfile(variables.RESHADE_PRESET_PATH):
        result = download_reshade_preset_file()
        if not result:
            err_msg = f"{variables.RESHADE_PRESET_PATH} {messages.not_found}"
            qt_utils.show_message_window(log, "error", err_msg)
            sys.exit(1)

    if not os.path.isfile(variables.QSS_PATH):
        result = download_qss_file()
        if not result:
            err_msg = f"{variables.QSS_PATH} {messages.not_found}"
            qt_utils.show_message_window(log, "error", err_msg)
            sys.exit(1)

    if not os.path.isfile(variables.ABOUT_PATH):
        result = download_about_html_file()
        if not result:
            err_msg = f"{variables.ABOUT_PATH} {messages.not_found}"
            qt_utils.show_message_window(log, "error", err_msg)
            sys.exit(1)

    check_shaders_and_textures(log)


def get_remote_reshade_version(log):
    log.debug("get_remote_reshade_version")

    remote_reshade_version = (1, 0, 0)
    try:
        req = requests.get(variables.RESHADE_WEBSITE_URL)
        if req.status_code != 200:
            msg = f"[Code {req.status_code}]: {messages.reshade_page_error}"
            qt_utils.show_message_window(log, "error", msg)
        else:
            html = str(req.text)
            soup = BeautifulSoup(html, "html.parser")
            body = soup.body
            blist = str(body).split("<p>")

            for content in blist:
                if content.startswith("<strong>Version "):
                    remote_version_str = content.split()[1].strip("</strong>")
                    remote_reshade_version = tuple(int(x) for x in remote_version_str.split("."))
                    break
    except requests.exceptions.ConnectionError as e:
        log.error(f"{messages.reshade_website_unreacheable}: {get_exception(e)}")
        qt_utils.show_message_window(log, "error", messages.reshade_website_unreacheable)
    return remote_reshade_version


def check_and_download_new_reshade_version(db_session, log, qtobj, db_reshade_version: tuple) -> None | str:
    log.debug("check_and_download_new_reshade_version")

    remote_reshade_version_tuple = get_remote_reshade_version(log)
    if remote_reshade_version_tuple and remote_reshade_version_tuple > db_reshade_version:
        remote_reshade_version_str = ".".join(map(str, remote_reshade_version_tuple))
        res = download_reshade(log, remote_reshade_version_str)
        if res:
            downloaded_reshade_path = os.path.join(variables.PROGRAM_DIR, f"ReShade_Setup_{remote_reshade_version_str}.exe")
            uzip = unzip_reshade(log, downloaded_reshade_path)
            if uzip:
                config_sql = ConfigDal(db_session, log)
                config_sql.update_reshade_version(remote_reshade_version_str)
                errors = games_tab_events.apply_all(db_session, log, qtobj)
                if errors:
                    err = "\n".join(errors)
                    qt_utils.show_message_window(log, "error",
                                                 f"{messages.apply_success_with_errors}\n\n"
                                                 f"{err}")
                elif program_utils.show_info_messages(db_session, log):
                    qt_utils.show_message_window(log, "info",
                                                 f"{messages.new_reshade_version}\n\n"
                                                 f"Version: {remote_reshade_version_str}")
            return remote_reshade_version_str
    return None


def download_reshade(log, remote_reshade_version):
    log.debug("download_reshade")

    files_list = sorted(os.listdir(variables.PROGRAM_DIR))
    local_reshade_exe = None
    for file in files_list:
        if variables.RESHADE_SETUP in file:
            local_reshade_exe = file

    if local_reshade_exe:
        old_reshade_exe_path = os.path.join(variables.PROGRAM_DIR, local_reshade_exe)
        if os.path.isfile(old_reshade_exe_path):
            log.info(f"{messages.removing_old_reshade_file}: {local_reshade_exe}")
            os.remove(old_reshade_exe_path)

    try:
        local_reshade_path = os.path.join(variables.PROGRAM_DIR, f"ReShade_Setup_{remote_reshade_version}.exe")
        remote_reshade_download_url = f"{variables.RESHADE_EXE_URL}{remote_reshade_version}.exe"
        r = requests.get(remote_reshade_download_url)
        if r.status_code == 200:
            log.info(f"{messages.downloading_new_reshade_version}: {remote_reshade_version}")
            with open(local_reshade_path, "wb") as outfile:
                outfile.write(r.content)
            return True
        else:
            err_message = f"{messages.error_check_new_reshade_version}\n\n Code: {r.status_code}"
    except PermissionError as e:
        err_message = f"{messages.error_check_new_reshade_version}\n{messages.error_permissionError}\n{get_exception(e)}"
    except Exception as e:
        err_message = f"{messages.error_check_new_reshade_version}\n{get_exception(e)}"

    log.error(err_message)
    qt_utils.show_message_window(log, "error", err_message)
    return False


def download_shaders(db_session, log):
    log.debug("download_shaders")

    progressbar = ProgressBar(log=log)
    progressbar.set_values(messages.downloading_shaders, 20)
    if os.path.isdir(variables.SHADERS_AND_TEXTURES_LOCAL_DIR):
        FileUtils.remove(variables.SHADERS_AND_TEXTURES_LOCAL_DIR)

    progressbar.set_values(messages.downloading_shaders, 40)
    _download_crosire_shaders_and_textures(log)

    progressbar.set_values(messages.downloading_textures, 80)
    _move_textures(log)

    progressbar.close()
    if program_utils.show_info_messages(db_session, log):
        qt_utils.show_message_window(log, "info", messages.update_shaders_finished)


def check_shaders_and_textures(log):
    log.debug("check_shaders_and_textures")

    shaders_dir = FileUtils.list_files(variables.SHADERS_LOCAL_DIR)
    if not os.path.isdir(variables.SHADERS_LOCAL_DIR) or len(shaders_dir) == 0:
        _download_crosire_shaders_and_textures(log)

    texture_dir = FileUtils.list_files(variables.TEXTURES_LOCAL_DIR)
    if not os.path.isdir(variables.TEXTURES_LOCAL_DIR) or len(texture_dir) == 0:
        _move_textures(log)


def _download_crosire_shaders_and_textures(log):
    log.debug("_download_crosire_shaders_and_textures")

    # remove shaders directory
    if not FileUtils.remove(variables.SHADERS_LOCAL_DIR):
        qt_utils.show_message_window(log, "error", messages.error_remove_shaders)

    # download nvidia crosire shaders as .zip
    if not FileUtils.download_file(variables.SHADERS_ZIP_URL, variables.SHADERS_ZIP_PATH):
        qt_utils.show_message_window(log, "error", messages.dl_new_shaders_timeout)

    # check the zip file
    if os.path.isfile(variables.SHADERS_ZIP_PATH):
        try:
            # extract the zip file
            FileUtils.unzip(variables.SHADERS_ZIP_PATH, variables.SRC_DIR)
        except FileNotFoundError as e:
            log.error(get_exception(e))
        except zipfile.BadZipFile as e:
            log.error(get_exception(e))
        except Exception as e:
            log.error(get_exception(e))

        # remove the zip file after extraction
        FileUtils.remove(variables.SHADERS_ZIP_PATH)

        # remove the reshade-shaders directory completely
        FileUtils.remove(variables.SHADERS_AND_TEXTURES_LOCAL_DIR)

        # rename the extracted directory (reshade-shaders-nvidia -> reshade-shaders)
        FileUtils.rename(variables.SHADERS_AND_TEXTURES_NVIDIA_LOCAL_TEMP_DIR, variables.SHADERS_AND_TEXTURES_LOCAL_DIR)

        # rename insdie the extracted directory (ShadersAndTextures -> Shaders)
        FileUtils.rename(variables.SHADERS_NVIDIA_LOCAL_TEMP_DIR, variables.SHADERS_LOCAL_DIR)


def _move_textures(log):
    log.debug("_move_textures")

    # move all textures.png to Textures folder
    if not os.path.isdir(variables.TEXTURES_LOCAL_DIR):
        os.makedirs(variables.TEXTURES_LOCAL_DIR)

    texture_files = FileUtils.list_files(variables.SHADERS_LOCAL_DIR, ends_with=".png")
    for texture in texture_files:
        out_file = str(os.path.join(variables.TEXTURES_LOCAL_DIR, texture.name))
        shutil.move(texture, out_file)


def download_all_files(local_dir: str = None):
    download_reshade_ini_file(local_dir)
    download_reshade_preset_file(local_dir)
    download_qss_file()
    download_about_html_file()


def download_reshade_files(local_dir: str = None):
    download_reshade_ini_file(local_dir)
    download_reshade_preset_file(local_dir)


def download_reshade_ini_file(local_dir: str = None):
    remote_file = variables.REMOTE_RESHADE_FILENAME
    if local_dir is None:
        local_file_path = variables.RESHADE_INI_PATH
    else:
        local_file_path = os.path.join(local_dir, variables.RESHADE_INI)
    return FileUtils.download_file(remote_file, local_file_path)


def download_reshade_preset_file(local_dir: str = None):
    remote_file = variables.REMOTE_PRESET_FILENAME
    if local_dir is None:
        local_file_path = variables.RESHADE_PRESET_PATH
    else:
        local_file_path = os.path.join(local_dir, variables.RESHADE_PRESET_INI)
    return FileUtils.download_file(remote_file, local_file_path)


def download_qss_file():
    remote_file = variables.REMOTE_QSS_FILENAME
    local_file_path = variables.QSS_PATH
    return FileUtils.download_file(remote_file, local_file_path)


def download_about_html_file():
    remote_file = variables.REMOTE_ABOUT_FILENAME
    local_file_path = variables.ABOUT_PATH
    return FileUtils.download_file(remote_file, local_file_path)


def apply_reshade_ini_file(game_dir, screenshot_path):
    try:
        FileUtils.copy(variables.RESHADE_INI_PATH, game_dir)
    except Exception as e:
        return e

    game_reshade_ini_path = str(os.path.join(game_dir, variables.RESHADE_INI))
    preset_path = os.path.join(game_dir, variables.RESHADE_PRESET_INI)
    intermediate_cache_path = os.path.join(tempfile.gettempdir(), "ReShade")

    try:
        if not os.path.isdir(intermediate_cache_path):
            os.makedirs(intermediate_cache_path)
    except OSError:
        pass

    ConfFileUtils().set_value(game_reshade_ini_path, "GENERAL", "EffectSearchPaths", variables.SHADERS_LOCAL_DIR)
    ConfFileUtils().set_value(game_reshade_ini_path, "GENERAL", "TextureSearchPaths", variables.TEXTURES_LOCAL_DIR)
    ConfFileUtils().set_value(game_reshade_ini_path, "GENERAL", "PresetPath", preset_path)
    ConfFileUtils().set_value(game_reshade_ini_path, "GENERAL", "IntermediateCachePath", intermediate_cache_path)
    ConfFileUtils().set_value(game_reshade_ini_path, "GENERAL", "StartupPresetPath", preset_path)
    ConfFileUtils().set_value(game_reshade_ini_path, "SCREENSHOT", "SavePath", screenshot_path)
    ConfFileUtils().set_value(game_reshade_ini_path, "SCREENSHOT", "PostSaveCommandWorkingDirectory", screenshot_path)

    return None

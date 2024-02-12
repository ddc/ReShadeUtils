# -*- coding: utf-8 -*-
import os
import zipfile
import requests
import shutil
from bs4 import BeautifulSoup
from ddcUtils import FileUtils, get_exception
from src import events
from src.constants import messages, variables
from src.database.dal.config_dal import ConfigDal
from src.tools import file_utils
from src.tools.qt import qt_utils


def check_reshade_updates(self):
    if self.check_reshade_updates:
        self.remote_reshade_version = None
        self.remote_reshade_download_url = None

        try:
            req = requests.get(variables.RESHADE_WEBSITE_URL)
            if req.status_code != 200:
                msg = f"[Code {req.status_code}]: {messages.reshade_page_error}"
                qt_utils.show_message_window(self.log, "error", msg)
            else:
                html = str(req.text)
                soup = BeautifulSoup(html, "html.parser")
                body = soup.body
                blist = str(body).split("<p>")

                for content in blist:
                    if content.startswith("<strong>Version "):
                        self.remote_reshade_version = (content.split()[1].strip("</strong>"))
                        self.remote_reshade_download_url = f"{variables.RESHADE_EXE_URL}{self.remote_reshade_version}.exe"
                        break

                if self.remote_reshade_version != self.reshade_version:
                    self.need_apply = True
                    download_reshade(self)
                    return True
        except requests.exceptions.ConnectionError as e:
            self.log.error(f"{messages.reshade_website_unreacheable}: {get_exception(e)}")
            qt_utils.show_message_window(self.log, "error", messages.reshade_website_unreacheable)
        return False


def download_reshade(self):
    # removing old version
    files_list = sorted(os.listdir(variables.PROGRAM_PATH))
    old_reshade_exe = None
    for file in files_list:
        if variables.RESHADE_SETUP in file:
            old_reshade_exe = file
            break
    if old_reshade_exe:
        old_reshade_exe_path = os.path.join(variables.PROGRAM_PATH, old_reshade_exe)
        if os.path.isfile(old_reshade_exe_path):
            self.log.info(f"{messages.removing_old_reshade_file}: {old_reshade_exe}")
            os.remove(old_reshade_exe_path)

    try:
        # downloading new reshade version
        self.local_reshade_path = os.path.join(variables.PROGRAM_PATH, f"ReShade_Setup_{self.remote_reshade_version}.exe")
        r = requests.get(self.remote_reshade_download_url)
        if r.status_code == 200:
            self.log.info(f"{messages.downloading_new_reshade_version}: {self.remote_reshade_version}")
            with open(self.local_reshade_path, "wb") as outfile:
                outfile.write(r.content)
        else:
            self.log.error(messages.error_check_new_reshade_version)
            return
    except Exception as e:
        if hasattr(e, "errno") and e.errno == 13:
            qt_utils.show_message_window(self.log, "error", messages.error_permissionError)
        else:
            self.log.error(f"{messages.error_check_new_reshade_version}: {get_exception(e)}")
        return

    self.reshade_version = self.remote_reshade_version
    file_utils.unzip_reshade(self, self.local_reshade_path)

    config_sql = ConfigDal(self.db_session, self.log)
    config_sql.update_reshade_version(self.remote_reshade_version)

    self.qtobj.reshade_version_label.clear()
    self.qtobj.reshade_version_label.setText(f"{messages.info_reshade_version}"
                                             f"{self.remote_reshade_version}")

    len_games = self.qtobj.programs_tableWidget.rowCount()
    if self.need_apply and len_games > 0:
        events.apply_all(self)
        qt_utils.show_message_window(self.log, "info",
                                     f"{messages.new_reshade_version}\n"
                                     f"Version: {self.remote_reshade_version}\n\n"
                                     f"{messages.apply_success}")
        self.need_apply = False


def download_shaders(self):
    self.progressbar.set_values(messages.downloading_shaders, 20)
    if os.path.isdir(variables.SHADERS_AND_TEXTURES_LOCAL_DIR):
        FileUtils.remove(variables.SHADERS_AND_TEXTURES_LOCAL_DIR)

    self.progressbar.set_values(messages.downloading_shaders, 40)
    _download_crosire_shaders_and_textures(self)

    self.progressbar.set_values(messages.downloading_textures, 80)
    _move_textures()

    self.progressbar.close()
    qt_utils.show_message_window(self.log, "info", messages.update_shaders_finished)


def check_shaders_and_textures(self):
    shaders_dir = FileUtils.list_files(variables.SHADERS_LOCAL_DIR)
    if not os.path.isdir(variables.SHADERS_LOCAL_DIR) or len(shaders_dir) == 0:
        _download_crosire_shaders_and_textures(self)

    texture_dir = FileUtils.list_files(variables.TEXTURES_LOCAL_DIR)
    if not os.path.isdir(variables.TEXTURES_LOCAL_DIR) or len(texture_dir) == 0:
        _move_textures()


def _download_crosire_shaders_and_textures(self):
    # remove shaders directory
    if not FileUtils.remove(variables.SHADERS_LOCAL_DIR):
        qt_utils.show_message_window(self.log, "error", messages.error_remove_shaders)

    # download nvidia crosire shaders as .zip
    if not FileUtils.download_file(variables.SHADERS_ZIP_URL, variables.SHADERS_ZIP_PATH):
        qt_utils.show_message_window(self.log, "error", messages.dl_new_shaders_timeout)

    # check the zip file
    if os.path.isfile(variables.SHADERS_ZIP_PATH):
        try:
            # extract the zip file
            FileUtils.unzip(variables.SHADERS_ZIP_PATH, variables.SRC_PATH)
        except FileNotFoundError as e:
            self.log.error(get_exception(e))
        except zipfile.BadZipFile as e:
            self.log.error(get_exception(e))
        except Exception as e:
            self.log.error(get_exception(e))

        # remove the zip file after extraction
        FileUtils.remove(variables.SHADERS_ZIP_PATH)

        # remove the reshade-shaders directory completely
        FileUtils.remove(variables.SHADERS_AND_TEXTURES_LOCAL_DIR)

        # rename the extracted directory (reshade-shaders-nvidia -> reshade-shaders)
        FileUtils.rename(variables.SHADERS_AND_TEXTURES_NVIDIA_LOCAL_TEMP_DIR, variables.SHADERS_AND_TEXTURES_LOCAL_DIR)

        # rename insdie the extracted directory (ShadersAndTextures -> Shaders)
        FileUtils.rename(variables.SHADERS_NVIDIA_LOCAL_TEMP_DIR, variables.SHADERS_LOCAL_DIR)


def _move_textures():
    # move all textures.png to Textures folder
    if not os.path.isdir(variables.TEXTURES_LOCAL_DIR):
        os.makedirs(variables.TEXTURES_LOCAL_DIR)

    texture_files = FileUtils.list_files(variables.SHADERS_LOCAL_DIR, ends_with=".png")
    for texture in texture_files:
        out_file = str(os.path.join(variables.TEXTURES_LOCAL_DIR, texture.name))
        shutil.move(texture, out_file)

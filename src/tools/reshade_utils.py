# -*- coding: utf-8 -*-
import os
import zipfile
import requests
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
                msg = (
                    f"[Code {req.status_code}]: "
                    f"{messages.reshade_page_error}"
                )
                qt_utils.show_message_window(self.log, "error", msg)
            else:
                html = str(req.text)
                soup = BeautifulSoup(html, "html.parser")
                body = soup.body
                blist = str(body).split("<p>")

                for content in blist:
                    if content.startswith("<strong>Version "):
                        self.remote_reshade_version = (content.split()[1].strip("</strong>"))
                        self.remote_reshade_download_url = (
                            f"{variables.RESHADE_EXE_URL}"
                            f"{self.remote_reshade_version}.exe"
                        )
                        break

                if self.remote_reshade_version != self.reshade_version:
                    self.need_apply = True
                    download_reshade(self)

        except requests.exceptions.ConnectionError as e:
            self.log.error(
                f"{messages.reshade_website_unreacheable}:"
                f"{get_exception(e)}"
            )
            qt_utils.show_message_window(
                self.log,
                "error",
                messages.reshade_website_unreacheable
            )
            return


def download_reshade(self):
    # removing old version
    if self.reshade_version is not None:
        old_local_reshade_exe = os.path.join(variables.PROGRAM_PATH,
                                             f"ReShade_Setup_"
                                             f"{self.reshade_version}.exe")
        if os.path.isfile(old_local_reshade_exe):
            self.log.info(messages.removing_old_reshade_file)
            os.remove(old_local_reshade_exe)

    try:
        # downloading new reshade version
        self.local_reshade_path = os.path.join(variables.PROGRAM_PATH,
                                               f"ReShade_Setup_"
                                               f"{self.remote_reshade_version}"
                                               ".exe")
        r = requests.get(self.remote_reshade_download_url)
        if r.status_code == 200:
            self.log.info(f"{messages.downloading_new_reshade_version}: "
                          f"{self.remote_reshade_version}")
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
                                     f"Version: {self.remote_reshade_version}"
                                     f"\n\n{messages.apply_success}")
        self.need_apply = False


def check_shaders_and_textures(self):
    if not os.path.isdir(variables.SHADERS_LOCAL_DIR):
        _download_crosire_shaders(self)

    if not os.path.isdir(variables.TEXTURES_LOCAL_DIR):
        _download_ddc_textures(self)


def _download_crosire_shaders(self):
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
            FileUtils.unzip_file(variables.SHADERS_ZIP_PATH, variables.PROGRAM_PATH)
        except FileNotFoundError as e:
            self.log.error(get_exception(e))
        except zipfile.BadZipFile as e:
            self.log.error(get_exception(e))
        except Exception as e:
            self.log.error(get_exception(e))

        # remove the zip file after extraction
        FileUtils.remove(variables.SHADERS_ZIP_PATH)

        # rename the extracted directory (reshade-shaders-nvidia -> reshade-shaders)
        out_dir = str(os.path.join(variables.PROGRAM_PATH, variables.RESHADE_SHADERS))
        FileUtils.rename(variables.SHADERS_AND_TEXTURES_NVIDIA_LOCAL_TEMP_DIR, out_dir)

        # rename insdie the extracted directory (ShadersAndTextures -> Shaders)
        out_dir = str(os.path.join(variables.PROGRAM_PATH, variables.RESHADE_SHADERS, "Shaders"))
        FileUtils.rename(variables.SHADERS_NVIDIA_LOCAL_TEMP_DIR, out_dir)


def _download_ddc_textures(self):
    # remove textures directory
    if not FileUtils.remove(variables.TEXTURES_LOCAL_DIR):
        qt_utils.show_message_window(self.log, "error", messages.error_remove_shaders)

    # download ddc texture files
    if not FileUtils.download_filesystem_directory(
            org="ddc",
            repo="reshadeutils",
            branch="fix/textures",
            remote_dir="src/data/reshade/textures",
            local_dir=variables.TEXTURES_LOCAL_DIR
    ):
        qt_utils.show_message_window(self.log, "error", messages.error_dl_textures)

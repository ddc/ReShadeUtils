# -*- coding: utf-8 -*-
import os
import shutil
import zipfile
import requests
from bs4 import BeautifulSoup
from src.database.dal.config_dal import ConfigDal
from src import events
from src.constants import variables, messages
from src.tools import file_utils
from src.tools.qt import qt_utils
from ddcUtils import FileUtils, get_exception


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
                        self.remote_reshade_version = (
                            content.split()[1].strip("</strong>")
                        )
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


def download_shaders(self):
    try:
        r = requests.get(variables.SHADERS_ZIP_URL)
        with open(variables.SHADERS_ZIP_PATH, "wb") as outfile:
            outfile.write(r.content)
    except Exception as e:
        err_msg = f"{messages.dl_new_shaders_timeout} {get_exception(e)}"
        qt_utils.show_message_window(self.log, "error", err_msg)

    try:
        if os.path.isdir(variables.SHADERS_SRC_PATH):
            shutil.rmtree(variables.SHADERS_SRC_PATH)
    except OSError as e:
        self.log.error(f"rmtree: {get_exception(e)}")

    try:
        if os.path.isdir(variables.RES_SHAD_MPATH):
            shutil.rmtree(variables.RES_SHAD_MPATH)
    except OSError as e:
        self.log.error(f"rmtree: {get_exception(e)}")

    if os.path.isfile(variables.SHADERS_ZIP_PATH):
        try:
            FileUtils.unzip_file(variables.SHADERS_ZIP_PATH, variables.PROGRAM_PATH)
        except FileNotFoundError as e:
            self.log.error(get_exception(e))
        except zipfile.BadZipFile as e:
            self.log.error(get_exception(e))

        try:
            os.remove(variables.SHADERS_ZIP_PATH)
        except OSError as e:
            self.log.error(f"remove_file: {get_exception(e)}")

    try:
        if os.path.isdir(variables.RES_SHAD_MPATH):
            out_dir = os.path.join(variables.PROGRAM_PATH, variables.RESHADE_SHADERS)
            os.rename(variables.RES_SHAD_MPATH, out_dir)
    except OSError as e:
        self.log.error(f"rename_path: {get_exception(e)}")

    try:
        if os.path.isdir(variables.RES_SHAD_NVIDIA_PATH):
            out_dir = os.path.join(variables.PROGRAM_PATH, variables.RESHADE_SHADERS, "Shaders")
            os.rename(variables.RES_SHAD_NVIDIA_PATH, out_dir)
    except OSError as e:
        self.log.error(f"rename_path: {get_exception(e)}")

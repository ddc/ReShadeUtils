# -*- coding: utf-8 -*-
import os
import shutil
from pathlib import Path
import fsspec
import requests
from ddcUtils import FileUtils
from src.constants import variables


class Files:
    def __init__(self, main):
        self.main = main
        self.log = main.log

    def download_all_files(self):
        self.download_reshade_ini_file()
        self.download_reshade_preset_file()
        self.download_qss_file()
        self.download_alembic_dir()

    def download_reshade_ini_file(self):
        remote_file = variables.REMOTE_RESHADE_FILENAME
        local_file_path = variables.RESHADE_INI_PATH
        return self._download_file(remote_file, local_file_path)

    def download_reshade_preset_file(self):
        remote_file = variables.REMOTE_PRESET_FILENAME
        local_file_path = variables.RESHADE_PRESET_PATH
        return self._download_file(remote_file, local_file_path)

    def download_qss_file(self):
        remote_file = variables.REMOTE_QSS_FILENAME
        local_file_path = variables.QSS_PATH
        return self._download_file(remote_file, local_file_path)

    def download_alembic_dir(self):
        return self._download_alembic_dir(variables.ALEMBIC_MIGRATIONS_DIR)

    @staticmethod
    def apply_reshade_ini_file(game_dir, screenshot_path):
        try:
            shutil.copy(variables.RESHADE_INI_PATH, game_dir)
        except Exception as e:
            return e

        game_reshade_ini_path = os.path.join(game_dir, variables.RESHADE_INI)
        effect_search_paths = os.path.join(variables.PROGRAM_PATH, "Reshade-shaders", "Shaders")
        texture_search_paths = os.path.join(variables.PROGRAM_PATH, "Reshade-shaders", "Textures")
        preset_path = os.path.join(game_dir, variables.RESHADE_PRESET_INI)
        intermediate_cache_path = os.getenv("TEMP")

        FileUtils.set_file_value(game_reshade_ini_path, "GENERAL", "EffectSearchPaths", effect_search_paths)
        FileUtils.set_file_value(game_reshade_ini_path, "GENERAL", "TextureSearchPaths", texture_search_paths)
        FileUtils.set_file_value(game_reshade_ini_path, "GENERAL", "PresetPath", preset_path)
        FileUtils.set_file_value(game_reshade_ini_path, "GENERAL", "IntermediateCachePath", intermediate_cache_path)
        FileUtils.set_file_value(game_reshade_ini_path, "SCREENSHOT", "SavePath", screenshot_path)
        FileUtils.set_file_value(game_reshade_ini_path, "SCREENSHOT", "PostSaveCommandWorkingDirectory", screenshot_path)

        return None

    @staticmethod
    def apply_reshade_preset_file(game_file_path):
        try:
            shutil.copy(variables.RESHADE_PRESET_PATH, game_file_path)
        except Exception as e:
            return e
        return None

    @staticmethod
    def apply_reshade_dll_file(src_dll_path, dst_dll_path):
        try:
            shutil.copy(src_dll_path, dst_dll_path)
        except Exception as e:
            return e
        return None

    def _download_file(self, remote_file, local_file_path):
        try:
            self.log.debug(remote_file)
            req = requests.get(remote_file)
            if req.status_code == 200:
                with open(local_file_path, "wb") as outfile:
                    outfile.write(req.content)
                return True
        except requests.HTTPError as e:
            self.log.error(e)
        return False

    def _download_alembic_dir(self, local_dir):
        try:
            destination = Path(local_dir)
            destination.mkdir(exist_ok=True, parents=True)
            fs = fsspec.filesystem("github", org="ddc", repo="reshadeUtils")
            remote_files = fs.ls("src/database/migrations")
            fs.get(remote_files, destination.as_posix(), recursive=False)

            destination = Path(local_dir) / "versions"
            remote_files = fs.ls("src/database/migrations/versions")
            fs.get(remote_files, destination.as_posix(), recursive=False)

            return True
        except requests.HTTPError as e:
            self.log.error(e)
        return False

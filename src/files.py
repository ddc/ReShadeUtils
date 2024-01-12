# -*- coding: utf-8 -*-
import os
import shutil
import requests
from src.constants import variables
from src.tools import file_utils


class Files:
    def __init__(self, main):
        self.main = main
        self.log = main.log

    def download_all_files(self):
        self.download_reshade_ini_file()
        self.download_reshade_preset_file()
        self.download_qss_file()

    def download_reshade_ini_file(self):
        local_file_path = variables.RESHADE_INI_PATH
        remote_file = variables.REMOTE_RESHADE_FILENAME
        self._download_file(remote_file, local_file_path)

    def download_reshade_preset_file(self):
        local_file_path = variables.RESHADE_PRESET_PATH
        remote_file = variables.REMOTE_PRESET_FILENAME
        self._download_file(remote_file, local_file_path)

    def download_qss_file(self):
        local_file_path = variables.QSS_PATH
        remote_file = variables.REMOTE_QSS_FILENAME
        self._download_file(remote_file, local_file_path)

    def download_alembic_file(self):
        local_file_path = variables.ALEMBIC_CONFIG_PATH
        remote_file = variables.REMOTE_ALEMBIC_FILENAME
        self._download_file(remote_file, local_file_path)

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

        file_utils.set_ini_file_settings(game_reshade_ini_path, "GENERAL", "EffectSearchPaths", effect_search_paths)
        file_utils.set_ini_file_settings(game_reshade_ini_path, "GENERAL", "TextureSearchPaths", texture_search_paths)
        file_utils.set_ini_file_settings(game_reshade_ini_path, "GENERAL", "PresetPath", preset_path)
        file_utils.set_ini_file_settings(game_reshade_ini_path, "GENERAL", "IntermediateCachePath", intermediate_cache_path)
        file_utils.set_ini_file_settings(game_reshade_ini_path, "SCREENSHOT", "SavePath", screenshot_path)
        file_utils.set_ini_file_settings(game_reshade_ini_path, "SCREENSHOT", "PostSaveCommandWorkingDirectory", screenshot_path)

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
            req = requests.get(remote_file)
            if req.status_code == 200:
                with open(local_file_path, "wb") as outfile:
                    outfile.write(req.content)
                return True
        except requests.HTTPError as e:
            self.log.error(e)
        return False

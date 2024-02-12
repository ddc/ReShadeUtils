# -*- coding: utf-8 -*-
import os
import shutil
from ddcUtils import FileUtils
from src.constants import variables


class Files:
    def __init__(self, log):
        self.log = log

    def download_all_files(self, local_dir: str = None):
        self.download_reshade_ini_file(local_dir)
        self.download_reshade_preset_file(local_dir)
        self.download_qss_file()

    def download_reshade_files(self, local_dir: str = None):
        self.download_reshade_ini_file(local_dir)
        self.download_reshade_preset_file(local_dir)

    @staticmethod
    def download_reshade_ini_file(local_dir: str = None):
        remote_file = variables.REMOTE_RESHADE_FILENAME
        if local_dir is None:
            local_file_path = variables.RESHADE_INI_PATH
        else:
            local_file_path = os.path.join(local_dir, variables.RESHADE_INI)
        return FileUtils.download_file(remote_file, local_file_path)

    @staticmethod
    def download_reshade_preset_file(local_dir: str = None):
        remote_file = variables.REMOTE_PRESET_FILENAME
        if local_dir is None:
            local_file_path = variables.RESHADE_PRESET_PATH
        else:
            local_file_path = os.path.join(local_dir, variables.RESHADE_PRESET_INI)
        return FileUtils.download_file(remote_file, local_file_path)

    @staticmethod
    def download_qss_file():
        remote_file = variables.REMOTE_QSS_FILENAME
        local_file_path = variables.QSS_PATH
        return FileUtils.download_file(remote_file, local_file_path)

    @staticmethod
    def apply_reshade_ini_file(game_dir, screenshot_path):
        try:
            shutil.copy(variables.RESHADE_INI_PATH, game_dir)
        except Exception as e:
            return e

        game_reshade_ini_path = str(os.path.join(game_dir, variables.RESHADE_INI))
        effect_search_paths = os.path.join(variables.PROGRAM_PATH, "Reshade-shaders", "Shaders")
        texture_search_paths = os.path.join(variables.PROGRAM_PATH, "Reshade-shaders", "Textures")
        preset_path = os.path.join(game_dir, variables.RESHADE_PRESET_INI)
        intermediate_cache_path = os.getenv("TEMP")

        FileUtils().set_file_value(game_reshade_ini_path, "GENERAL", "EffectSearchPaths", effect_search_paths)
        FileUtils().set_file_value(game_reshade_ini_path, "GENERAL", "TextureSearchPaths", texture_search_paths)
        FileUtils().set_file_value(game_reshade_ini_path, "GENERAL", "PresetPath", preset_path)
        FileUtils().set_file_value(game_reshade_ini_path, "GENERAL", "IntermediateCachePath", intermediate_cache_path)
        FileUtils().set_file_value(game_reshade_ini_path, "SCREENSHOT", "SavePath", screenshot_path)
        FileUtils().set_file_value(game_reshade_ini_path, "SCREENSHOT", "PostSaveCommandWorkingDirectory", screenshot_path)

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

# -*- coding: utf-8 -*-
import os
import sys
import json
import datetime
from src.constants import variables
from pathlib import Path


class Object:
    def __init__(self):
        self._created = datetime.datetime.now().isoformat()

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def to_dict(self):
        json_string = json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
        json_dict = json.loads(json_string)
        return json_dict


def get_active_branch_name():
    head_dir = Path(".") / ".git" / "HEAD"
    try:
        with head_dir.open("r") as f:
            content = f.read().splitlines()
        for line in content:
            if line[0:4] == "ref:":
                return line.partition("refs/heads/")[2]
    except FileNotFoundError:
        return "master"


def get_exception(e):
    module = e.__class__.__module__
    if module is None or module == str.__class__.__module__:
        module_and_exception = f"{e.__class__.__name__}:{e}"
    else:
        module_and_exception = f"{module}.{e.__class__.__name__}:{e}"
    return module_and_exception.replace("\r\n", " ").replace("\n", " ")


def get_current_path():
    path = os.path.abspath(os.getcwd())
    if path is not None:
        return os.path.normpath(path)
    return None


def get_pictures_path():
    if variables.OS_NAME == "Windows":
        import winreg
        sub_key = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders"
        pictures_guid = "My Pictures"
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
            pictures_path = winreg.QueryValueEx(key, pictures_guid)[0]
        return pictures_path
    else:
        pictures_path = os.path.join(os.getenv("HOME"), "Pictures")
        return pictures_path


def get_download_path():
    if variables.OS_NAME == "Windows":
        import winreg
        sub_key = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders"
        downloads_guid = "{374DE290-123F-4565-9164-39C4925E467B}"
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
            downloads_path = winreg.QueryValueEx(key, downloads_guid)[0]
        return downloads_path
    else:
        t1_path = str(os.path.expanduser("~/Downloads"))
        t2_path = f"{t1_path}".split("\\")
        downloads_path = "/".join(t2_path)
        return downloads_path.replace("\\", "/")


def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except:
        base_path = os.path.abspath("./src")
    return os.path.join(base_path, relative_path)

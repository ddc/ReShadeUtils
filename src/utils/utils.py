#! /usr/bin/env python3
#|*****************************************************
# * Copyright         : Copyright (C) 2019
# * Author            : ddc
# * License           : GPL v3
# * Python            : 3.6
#|*****************************************************
# # -*- coding: utf-8 -*-

import sys, os, json
import logging
from src.utils import constants, messages
from PyQt5.QtWidgets import QFileDialog
from PyQt5 import QtCore, QtWidgets
from src.databases.databases import Databases
import requests, urllib.request
import datetime
import configparser
import zipfile
################################################################################
################################################################################
################################################################################
class Object():
    date_formatter = "%b/%d/%Y"
    time_formatter = "%H:%M:%S"
    created = str(datetime.datetime.now().strftime(f"{date_formatter} {time_formatter}"))
    def toJson(self):
        return json.dumps(self,default=lambda o: o.__dict__,sort_keys=True,indent=4)
    def toDict(self):
        jsonString = json.dumps(self,default=lambda o: o.__dict__,sort_keys=True,indent=4)
        jsonDict = json.loads(jsonString)
        return jsonDict
################################################################################
################################################################################
################################################################################
def get_file_settings(filename, section, config_name):
    settings_filename = filename
    parser = configparser.ConfigParser(delimiters=('='), allow_no_value=True)
    parser._interpolation = configparser.ExtendedInterpolation()
    parser.read(settings_filename)
    try: 
        value = parser.get(section, config_name).replace("\"","")
    except Exception:
        value = None
    return value
################################################################################
################################################################################
################################################################################
#def set_file_settings(filename, section, config_name, value):
#    settings_filename = filename
#    parser = configparser.ConfigParser(delimiters=('='), allow_no_value=True)
#    try:
#        parser.read(settings_filename)
#        parser.set(section, config_name, value)
#        with open(settings_filename, 'w') as configfile:
#            parser.write(configfile, space_around_delimiters=False)
#    except configparser.DuplicateOptionError:
#        return
################################################################################
################################################################################
################################################################################      
def get_database():
    filename = constants.db_settings_filename
    databaseInUse = get_file_settings(filename, "Bot", "DatabaseInUse")
    database = Object()
    if databaseInUse.lower() != "sqlite":
        database.name        = "PostgreSQL"
        database.host        = get_file_settings(filename, "Database", "Host")
        database.port        = get_file_settings(filename, "Database", "Port")
        database.db_name     = get_file_settings(filename, "Database", "DBname")
        database.username    = get_file_settings(filename, "Database", "Username")
        database.password    = get_file_settings(filename, "Database", "Password")
    else:
        database.name = "SQLite"
        database.host = ""
        database.port = ""
    return database
################################################################################
################################################################################
################################################################################ 
def check_database_connection(log):
    databases = Databases(log)
    conn = databases.check_database_connection()
    return conn
################################################################################  
################################################################################
################################################################################
# def zip_file(file_name:str, out_path:str):
#     zipOutputName = "archive"
#     fileType = "zip"
#     path = out_path
#     fileName = file_name
#     shutil.make_archive(zipOutputName,fileType,path,fileName)
################################################################################  
################################################################################
################################################################################
def unzip_file(file_name:str, out_path:str):
    zipfilePath = (file_name)
    zipf = zipfile.ZipFile(zipfilePath)
    zipf.extractall(out_path)
    zipf.close()
################################################################################
################################################################################
################################################################################          
def log_uncaught_exceptions(exc_type, exc_value, exc_traceback):
    logger = logging.getLogger(__name__)
    stderr_hdlr = logging.StreamHandler(stream=sys.stdout)
    stderr_hdlr.setLevel(constants.LOG_LEVEL)
    stderr_hdlr.setFormatter(constants.LOG_FORMATTER)
    logger.addHandler(stderr_hdlr)
    if issubclass(exc_type, KeyboardInterrupt)\
    or issubclass(exc_type, EOFError):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logger.exception("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))
################################################################################
################################################################################
################################################################################
def open_get_filename(self):
    filename = QFileDialog.getOpenFileName(None, 'Open file')[0]
    if filename is '':
        return None
    else:
        return str(filename)
################################################################################
################################################################################
################################################################################ 
def get_download_path():
    if os.name == 'nt':
        import winreg
        sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
        downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
            location = winreg.QueryValueEx(key, downloads_guid)[0]
        return location
    else:
        return os.path.join(os.path.expanduser('~'), 'downloads')
################################################################################
################################################################################
################################################################################
def get_my_documents_path():
    if constants.IS_WINDOWS:
        CSIDL_PERSONAL = 5 #My Documents
        SHGFP_TYPE_CURRENT = 0
        
        import ctypes.wintypes
        buf= ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
        ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_PERSONAL, None, SHGFP_TYPE_CURRENT, buf)
         
        return str(buf.value)
    else:
        t1_path = str(os.path.expanduser("~/Documents"))
        t2_path = f"{t1_path}".split("\\")
        my_docs_path = '/'.join(t2_path)
        return my_docs_path
################################################################################
################################################################################
################################################################################
def show_progress_bar(self, message, value):
    self.progressBar = QtWidgets.QProgressBar()
    _translate = QtCore.QCoreApplication.translate
    self.progressBar.setObjectName("progressBar")
    self.progressBar.setGeometry(QtCore.QRect(180, 150, 350, 25))
    self.progressBar.setMinimumSize(QtCore.QSize(350, 25))
    self.progressBar.setMaximumSize(QtCore.QSize(350, 25))
    self.progressBar.setSizeIncrement(QtCore.QSize(350, 25))
    self.progressBar.setBaseSize(QtCore.QSize(350, 25))
    self.progressBar.setMinimum(0)
    self.progressBar.setMaximum(100)
    self.progressBar.setWindowFlags(QtCore.Qt.FramelessWindowHint)
    self.progressBar.setAlignment(QtCore.Qt.AlignCenter)
    self.progressBar.setFormat(_translate("Main",  message+"%p%"))
    self.progressBar.show()

    QtWidgets.QApplication.processEvents()
    self.progressBar.setValue(value)
    
    if value == 100:
        self.progressBar.hide()
################################################################################
################################################################################
################################################################################
def show_message_window(windowType:str, window_title:str, msg:str):
    if windowType.lower() == "error":
        icon = QtWidgets.QMessageBox.Critical
    elif windowType.lower() == "warning":
        icon = QtWidgets.QMessageBox.Warning
    elif windowType.lower() == "question":
        icon = QtWidgets.QMessageBox.Question     
    else:
        icon = QtWidgets.QMessageBox.Information

    msgBox = QtWidgets.QMessageBox()
    msgBox.setIcon(icon)
    msgBox.setWindowTitle(window_title)
    msgBox.setInformativeText(msg)
    
    if windowType.lower() == "question":
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        msgBox.setDefaultButton(QtWidgets.QMessageBox.Yes)    
    else:
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msgBox.setDefaultButton(QtWidgets.QMessageBox.Ok)
    
    user_answer = msgBox.exec_()
    return user_answer
################################################################################
################################################################################
################################################################################
def check_new_program_version(self, show_dialog=True):
    remote_version_filename = constants.remote_version_filename
    client_version = constants.VERSION
    program_checking_version_msg = messages.checking_new_version
    obj_return = Object()
    obj_return.new_version_available = False
    obj_return.new_version = None
    
    try:
        show_progress_bar(self, program_checking_version_msg, 0)
        req = requests.get(remote_version_filename)
        show_progress_bar(self, program_checking_version_msg, 25)
        if req.status_code == 200: 
            remote_version = req.text
            
            show_progress_bar(self, program_checking_version_msg, 50)
            if remote_version[-2:] == "\\n" or remote_version[-2:] == "\n":
                remote_version = remote_version[:-2] #getting rid of \n at the end of line
            
            show_progress_bar(self, program_checking_version_msg, 75)
            if float(remote_version) > float(client_version):
                obj_return.new_version_available = True
                show_progress_bar(self, program_checking_version_msg, 100)
                obj_return.new_version_msg = f"Version {remote_version} available for download"
                obj_return.new_version = float(remote_version)
                
                if show_dialog:
                    msg = f"""{messages.new_version_available}
                        \nYour version: v{client_version}\nNew version: v{remote_version}
                        \n{messages.check_downloaded_dir}
                        \n{messages.confirm_download}"""
                    reply = show_message_window("question", obj_return.new_version_msg, msg)
                
                    if reply == QtWidgets.QMessageBox.Yes:
                        pb_dl_new_version_msg = messages.dl_new_version
                        program_url = f"{constants.github_exe_program_url}{remote_version}/{constants.exe_program_name}"
                        user_download_path = get_download_path()
                        downloaded_program_path = f"{user_download_path}\{constants.exe_program_name}"
                        
                        try:
                            show_progress_bar(self, pb_dl_new_version_msg, 50)
                            urllib.request.urlretrieve(program_url, downloaded_program_path)
                            show_progress_bar(self, pb_dl_new_version_msg, 100)
                            show_message_window("Info", "INFO", f"{messages.info_dl_completed}\n{downloaded_program_path}")
                            sys.exit()
                        except Exception as e:
                            show_progress_bar(self, pb_dl_new_version_msg, 100)
                            self.log.error(f"{messages.error_check_new_version} {e}")
                            if e.code == 404:
                                show_message_window("error", "ERROR", messages.remote_file_not_found) 
                            else:
                                show_message_window("error", "ERROR", messages.error_check_new_version)
                    else:
                        new_title = f"{constants.full_program_name} ({obj_return.new_version_msg})"
                        _translate = QtCore.QCoreApplication.translate
                        self.form.setWindowTitle(_translate("Main", new_title))
            show_progress_bar(self, program_checking_version_msg, 100)
        else:
            show_progress_bar(self, program_checking_version_msg, 100)
            self.log.error(f"{messages.error_check_new_version}\n{messages.remote_version_file_not_found} code:{req.status_code}")
            show_message_window("critical", "ERROR" , f"{messages.error_check_new_version}")
    except requests.exceptions.ConnectionError as e:
        show_progress_bar(self, program_checking_version_msg, 100)
        self.log.error(f"{messages.dl_new_version_timeout} {e}")
        show_message_window("error", "ERROR", messages.dl_new_version_timeout)
    finally:
        return obj_return
################################################################################
################################################################################
################################################################################

#! /usr/bin/env python3
#|*****************************************************
# * Copyright         : Copyright (C) 2019
# * Author            : ddc
# * License           : GPL v3
# * Python            : 3.6
#|*****************************************************
# # -*- coding: utf-8 -*-

from PyQt5 import QtWidgets
from src.utils.create_files import CreateFiles 
from src.utils import constants, messages, utils
import sys, os, shutil
from src.sql.configs_sql import ConfigsSql
from src.sql.games_sql import GamesSql
import zipfile
import urllib.request
################################################################################
################################################################################
################################################################################
class FormEvents():
    def __init__(self):
        pass
################################################################################
################################################################################
################################################################################      
    def add_game(self):
        game_path = utils.open_get_filename(self)
        if game_path is not None:
            file_name = str(game_path.split("/")[-1])
            extension = str(file_name.split(".")[-1])
            tl = game_path.split("/")
            game_path = '\\'.join(tl)     
            if extension.lower() == "exe":
                gamesSql = GamesSql(self.log)
                rsPath = gamesSql.get_game_by_path(game_path)
                if rsPath is not None and len(rsPath) == 0:
                    self.rs_game = None
                    self.selected_game = None
                    self.game_path = game_path                
                    self._show_game_config_form(file_name.replace(".exe",""))
                else:
                    rsName = gamesSql.get_game_by_path(game_path)
                    if rsPath is not None and len(rsPath) > 0\
                    or rsName is not None and len(rsName) > 0:
                        utils.show_message_window("error", "ERROR", f"{messages.game_already_exist}\n\n{file_name}")
            else:
                utils.show_message_window("error", "ERROR", f"{messages.not_valid_game}\n\n{file_name}")
################################################################################
################################################################################
################################################################################
    def delete_game(self):
        self.enable_widgets(True)
        if self.rs_game is not None and len(self.rs_game) > 0:
            path_list = self.rs_game[0]["path"].split("\\")[:-1]
            game_path = '\\'.join(path_list)
            game_name = self.rs_game[0]['name']
            err = False
            
            #remove dll from game path
            if self.rs_game[0]["api"] == "DX9":
                reshade_dll = f"{game_path}/{constants.d3d9}"
            else:
                reshade_dll = f"{game_path}/{constants.dxgi}"
            if os.path.isfile(reshade_dll):
                try:
                    os.remove(reshade_dll)
                except OSError as e:
                    err = True
                    utils.show_message_window("error", "ERROR", f"{messages.error_delete_dll} {game_name} dll\n\n{e.strerror}")
            
            if not err:
                try:
                    #remove reshade.ini from game path
                    reshade_ini = f"{game_path}/{constants.reshade_ini}"
                    if os.path.isfile(reshade_ini):
                        os.remove(reshade_ini)
                    #remove reshade_plugins.ini from game path
                    reshade_plug_ini = f"{game_path}/{constants.reshade_plugins_ini}"
                    if os.path.isfile(reshade_plug_ini):
                        os.remove(reshade_plug_ini)                
                    #remove Reshade log files from game path    
                    reshade_x64log_file = f"{game_path}/{constants.reshade_x64log}"
                    if os.path.isfile(reshade_x64log_file):
                        shutil.rmtree(reshade_x64log_file)
                    reshade_x32log_file = f"{game_path}/{constants.reshade_x32log}"
                    if os.path.isfile(reshade_x32log_file):
                        shutil.rmtree(reshade_x32log_file)                    
                    #remove from database
                    gamesSql = GamesSql(self.log)
                    gamesSql.delete_game(self.rs_game[0]["id"])
                    #populate list
                    self.populate_programs_listWidget()
                    utils.show_message_window("info", "SUCCESS", f"{messages.game_deleted}\n\n{game_name}")
                except OSError as e:
                    utils.show_message_window("error", "ERROR", f"{game_name} files\n\n{e.strerror}")
                    
            self.enable_widgets(False)
################################################################################
################################################################################
################################################################################
    def edit_game_path(self):
        if self.rs_game is not None and len(self.rs_game) > 0:
            old_game_path = (self.rs_game[0]["path"])
            new_game_path = utils.open_get_filename(self)
            if new_game_path is not None:
                new_game_path = new_game_path.replace("/","\\")
                if old_game_path == new_game_path:
                    self.enable_widgets(False)
                    utils.show_message_window("info", "INFO", f"{messages.no_change_path}")
                    return
                
                old_file_name = str(old_game_path.split("\\")[-1])
                new_file_name = str(new_game_path.split("\\")[-1])
                if old_file_name != new_file_name:
                    self.enable_widgets(False)
                    utils.show_message_window("error", "ERROR", f"{messages.not_same_game}\n\n{old_file_name}")
                    return
                
                extension = str(new_file_name.split(".")[-1])
                if extension.lower() != "exe":
                    self.enable_widgets(False)
                    utils.show_message_window("error", "ERROR", f"{messages.not_valid_game}\n\n{new_file_name}")
                    return
    
                gamesObj = utils.Object()
                gamesSql = GamesSql(self.log)
                gamesObj.id = self.rs_game[0]["id"]
                gamesObj.path = new_game_path
                gamesSql.update_game_path(gamesObj)
                #populate list
                self.populate_programs_listWidget()
                utils.show_message_window("info", "INFO", f"{messages.path_changed_success}\n\n{new_game_path}")

            self.enable_widgets(False)
################################################################################
################################################################################
################################################################################
    def open_reshade_config_file(self):
        self.enable_widgets(True)
        if self.rs_game is not None and len(self.rs_game) > 0:
            path_list = self.rs_game[0]["path"].split("\\")[:-1]
            game_path = '\\'.join(path_list)
            res_plug_ini_path = f"{game_path}\{constants.reshade_plugins_ini}"

            try:
                os.startfile(f"\"{res_plug_ini_path}\"")
            except Exception as e:
                self.enable_widgets(False)
                err_msg = f"{e.strerror}\n\n{messages.check_game_uninstalled}"
                utils.show_message_window("error", "ERROR", err_msg)
################################################################################
################################################################################
################################################################################
    def update_program(self):
        user_answer = utils.show_message_window("question", "Update Available", f"{messages.new_version_available}\n\n{messages.start_update_question}")
        if user_answer == QtWidgets.QMessageBox.Yes:
            pb_dl_new_version_msg = messages.dl_new_version
            user_download_path = utils.get_download_path()
            program_url = constants.github_exe_program_url
            downloaded_program_path = f"{user_download_path}\{constants.exe_program_name}"
            
            try:
                utils.show_progress_bar(self, pb_dl_new_version_msg, 50)
                urllib.request.urlretrieve(program_url, downloaded_program_path)
                utils.show_progress_bar(self, pb_dl_new_version_msg, 100)
                utils.show_message_window("Info", "INFO", f"{messages.info_dl_completed}\n{downloaded_program_path}")
                sys.exit()
            except Exception as e:
                utils.show_progress_bar(self, pb_dl_new_version_msg, 100)
                self.log.error(f"{messages.error_check_new_version} {e}")
                if e.code == 404:
                    utils.show_message_window("error", "ERROR", messages.remote_version_file_not_found) 
                else:
                    utils.show_message_window("error", "ERROR", messages.error_check_new_version)
################################################################################
################################################################################
################################################################################
    def dark_theme_clicked(self, status:str):
        if status == "YES":
            self.set_style_sheet(True)
            self.use_dark_theme = True
            status = "Y"
        else:
            self.set_style_sheet(False)
            self.use_dark_theme = False
            status = "N"           
            
        configSql = ConfigsSql(self.log)
        configsObj = utils.Object()
        configsObj.status = status
        configSql.update_dark_theme(configsObj)
################################################################################
################################################################################
################################################################################  
    def check_program_updates_clicked(self, status:str):
        if status == "YES":
            self.check_program_updates = True
            status = "Y"
        else:
            self.check_program_updates = False
            status = "N"           
            
        configSql = ConfigsSql(self.log)
        configsObj = utils.Object()
        configsObj.status = status
        configSql.update_check_program_updates(configsObj)
################################################################################
################################################################################
################################################################################ 
    def check_reshade_updates_clicked(self, status:str):
        if status == "YES":
            self.check_reshade_updates = True
            status = "Y"
        else:
            self.check_reshade_updates = False
            status = "N"           
            
        configSql = ConfigsSql(self.log)
        configsObj = utils.Object()
        configsObj.status = status
        configSql.update_check_resahde_updates(configsObj)
################################################################################
################################################################################
################################################################################  
    def update_shaders_clicked(self, status:str):
        if status == "YES":
            self.update_shaders = True
            status = "Y"
        else:
            self.update_shaders = False
            status = "N"     

        configSql = ConfigsSql(self.log)
        configsObj = utils.Object()
        configsObj.status = status
        configSql.update_shaders(configsObj)
################################################################################
################################################################################
################################################################################  
    def create_screenshots_folder_clicked(self, status:str):
        if status == "YES":
            self.create_screenshots_folder = True
            status = "Y"
        else:
            self.create_screenshots_folder = False
            status = "N"     

        configSql = ConfigsSql(self.log)
        configsObj = utils.Object()
        configsObj.status = status
        configSql.update_create_screenshots_folder(configsObj)
################################################################################
################################################################################
################################################################################  
    def reset_reshade_files_clicked(self, status:str):
        if status == "YES":
            self.reset_reshade_files = True
            status = "Y"
        else:
            self.reset_reshade_files = False
            status = "N"     

        configSql = ConfigsSql(self.log)
        configsObj = utils.Object()
        configsObj.status = status
        configSql.update_reset_reshade_files(configsObj)
################################################################################
################################################################################
################################################################################        
    def programs_tableWidget_clicked(self, item):
        self.enable_widgets(True)
        selected_game = self.qtObj.programs_tableWidget.currentItem()
        
        if hasattr(selected_game, "text"):
            self.selected_game = utils.Object()
            self.selected_game.name = selected_game.text()
            self.selected_game.column = item.column()
            self.selected_game.row = item.row()
            
            search_pattern = self.selected_game.name
            gamesSql = GamesSql(self.log)
            if item.column() == 0:
                rs = gamesSql.get_game_by_name(search_pattern)
            else:
                rs = gamesSql.get_game_by_path(search_pattern)            
            
            if rs is not None and len(rs) > 0:
                self.rs_game = rs
                if rs[0]["architecture"] == "32bits":
                    self.qtObj.radioButton_32bits.setChecked(True)
                    self.qtObj.radioButton_64bits.setChecked(False)
                else:
                    self.qtObj.radioButton_32bits.setChecked(False)
                    self.qtObj.radioButton_64bits.setChecked(True)
                    
                if rs[0]["api"] == "DX9":
                    self.qtObj.dx9_radioButton.setChecked(True)
                    self.qtObj.dx11_radioButton.setChecked(False)
                else:
                    self.qtObj.dx9_radioButton.setChecked(False)
                    self.qtObj.dx11_radioButton.setChecked(True)   
################################################################################
################################################################################
################################################################################
    def apply(self):
        errors = []
        gamesSql = GamesSql(self.log)
        rs_all_games = gamesSql.get_all_games()
        len_games = len(rs_all_games)
        downloaded_new_shaders = False
        
        if self.reset_reshade_files:
            msg = f"{messages.reset_config_files_question}"
            reply = utils.show_message_window("question", "Reset All Configs", msg)
            if reply == QtWidgets.QMessageBox.No:
                self.reset_reshade_files = False
        
        if rs_all_games is not None and len_games > 0:
            self.enable_form(False)
            self.enable_widgets(False)
            self.qtObj.apply_button.setEnabled(False)
            createFiles = CreateFiles(self.log)
            
            #update new shaders files
            if self.update_shaders is not None\
            and self.update_shaders == True:

                try:
                    utils.show_progress_bar(self, messages.downloading_shaders, (50))
                    urllib.request.urlretrieve(constants.shaders_zip_url, constants.shaders_zip_path)
                    downloaded_new_shaders = True
                except Exception as e:
                    self.log.error(f"{messages.dl_new_shaders_timeout} {e}")
                    utils.show_message_window("error", "ERROR", messages.dl_new_shaders_timeout)
                    
                if downloaded_new_shaders:
                    try:
                        if os.path.exists(constants.shaders_src_path):
                            shutil.rmtree(constants.shaders_src_path)
                    except OSError as e:
                        self.log.error(f"{e}")
                        
                    try:
                        if os.path.exists(constants.res_shad_mpath):
                            shutil.rmtree(constants.res_shad_mpath)
                    except OSError as e:
                        self.log.error(f"{e}")
            
                    utils.show_progress_bar(self, messages.downloading_shaders, (75))
                    if os.path.exists(constants.shaders_zip_path):
                        try:
                            utils.unzip_file(constants.shaders_zip_path, constants.program_path)
                        except FileNotFoundError as e:
                            self.log.error(f"{e}")
                        except zipfile.BadZipFile as e:
                            self.log.error(f"{e}")
    
                        try:
                            os.remove(constants.shaders_zip_path)
                        except OSError as e:
                            self.log.error(f"{e}")
    
                    try:
                        if os.path.exists(constants.res_shad_mpath):
                            out_dir = f"{constants.program_path}\{constants.reshade_shaders}"
                            os.rename(constants.res_shad_mpath, out_dir)
                    except OSError as e:
                        self.log.error(f"{e}")

                utils.show_progress_bar(self, messages.downloading_shaders, (100))
            
            #begin games update section
            for i in range(len(rs_all_games)):
                path_list = rs_all_games[i]["path"].split("\\")[:-1]
                game_path = '\\'.join(path_list)
                game_name = rs_all_games[i]["name"]
                dst_res_ini_path = f"{game_path}\{constants.reshade_ini}"
                dst_res_plug_ini_path = f"{game_path}\{constants.reshade_plugins_ini}"
                
                if rs_all_games[i]["architecture"] == "32bits":
                    src_path = constants.reshade32_path
                else:
                    src_path = constants.reshade64_path
                
                if rs_all_games[i]["api"] == "DX9":
                    dst_path = f"{game_path}\{constants.d3d9}"
                else:
                    dst_path = f"{game_path}\{constants.dxgi}"
                
                try:
                    utils.show_progress_bar(self, messages.copying_DLLs, (100/len_games))
                    game_screenshots_path = ""
                    
                    ##creating screenshot dir
                    if self.qtObj.yes_screenshots_folder_radioButton.isChecked():
                        game_screenshots_path = f"{constants.reshade_screenshot_path}{game_name}"
                        try:
                            if not os.path.exists(constants.reshade_screenshot_path):
                                os.makedirs(constants.reshade_screenshot_path)
                            if not os.path.exists(game_screenshots_path):
                                os.makedirs(game_screenshots_path)
                        except OSError as e:
                            self.log.error(f"{e}")

                    ##copying Reshade.dll
                    try:
                        shutil.copyfile(src_path, dst_path)
                    except shutil.Error as e:
                        self.log.error(f"{e}")                
                    
                    ##copying Reshade.ini
                    try:
                        if self.reset_reshade_files or not os.path.exists(dst_res_ini_path):
                            createFiles.create_reshade_file(dst_res_ini_path, game_screenshots_path)
                    except OSError as e:
                        self.log.error(f"{e}") 

                    ##copying Reshade_plugins.ini
                    try:
                        if self.reset_reshade_files or not os.path.exists(dst_res_plug_ini_path):
                            shutil.copyfile(constants.reshade_plugins_filename, dst_res_plug_ini_path)
                    except shutil.Error as e:
                            self.log.error(f"{e}") 
                                                                                                                            
                    len_games = len_games-1
                except OSError as e:
                    errors.append(f"{game_name}: {e.strerror.lower()}")
                    #utils.show_message_window("error", "ERROR", f"{messages.error_copying_dll}\n{game_name}\n\n{e.strerror}")

        self.enable_form(True)
        self.qtObj.apply_button.setEnabled(True)
        utils.show_progress_bar(self, messages.copying_DLLs, 100)
        if len(errors) == 0:           
            utils.show_message_window("info", "SUCCESS", f"{messages.apply_success}")
        else:
            err = '\n'.join(errors)
            utils.show_message_window("error", "ERROR", f"{messages.apply_success_with_errors}\n\n{err}")                
################################################################################
################################################################################
################################################################################

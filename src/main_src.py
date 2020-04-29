#! /usr/bin/env python3
# |*****************************************************
# * Copyright         : Copyright (C) 2019
# * Author            : ddc
# * License           : GPL v3
# * Python            : 3.6
# |*****************************************************
# # -*- coding: utf-8 -*-

import os
import sys

import requests
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from bs4 import BeautifulSoup

from src.form_events import FormEvents
from src.game_configs import UiGameConfigForm
from src.sql.configs_sql import ConfigsSql
from src.sql.games_sql import GamesSql
from src.utils import constants, messages, utilities


class MainSrc:
    def __init__(self, qtObj, form):
        self.progressBar = utilities.ProgressBar()
        self.qtObj = qtObj
        self.form = form
        self.database_settings = None
        self.selected_game = None
        self.game_config_form = None
        self.reshade_version = None
        self.local_reshade_exe = None
        self.use_dark_theme = None
        self.update_shaders = None
        self.check_program_updates = None
        self.check_reshade_updates = None
        self.silent_reshade_updates = None
        self.create_screenshots_folder = None
        self.reset_reshade_files = None
        self.need_apply = False
        self.new_version = None
        self.db_conn = None
        self.remote_reshade_version = None
        self.client_version = None
        self.log = None

    ################################################################################
    def init(self):
        self.progressBar.setValues(messages.initializing, 0)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap('src/images/paypal.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.qtObj.paypal_button.setIcon(icon)

        utilities.check_dirs()
        self.log = utilities.setup_logging(self)
        sys.excepthook = utilities.log_uncaught_exceptions

        self.progressBar.setValues(messages.checking_files, 15)
        utilities.check_files(self)
        self.database_settings = utilities.get_all_ini_file_settings(constants.DB_SETTINGS_FILENAME)
        self.client_version = constants.VERSION

        self.progressBar.setValues(messages.checking_db_connection, 30)
        utilities.check_db_connection(self)
        utilities.set_default_database_configs(self)
        utilities.check_database_updated_columns(self)

        self.progressBar.setValues(messages.checking_configs, 45)
        self.qtObj.programs_tableWidget.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)
        self._set_all_configs()
        self._register_form_events()

        self.progressBar.setValues(messages.checking_new_reshade_version, 60)
        self._check_reshade_files()
        if self.local_reshade_exe is None:
            self._download_new_reshade_version()
        else:
            self._check_new_reshade_version()

        if self.remote_reshade_version is not None:
            if self.reshade_version != self.remote_reshade_version:
                self.need_apply = True
                if self.silent_reshade_updates:
                    self._download_new_reshade_version()
                else:
                    msg = f"{messages.update_reshade_question}"
                    reply = utilities.show_message_window("question", "Download new Reshade version", msg)
                    if reply == QtWidgets.QMessageBox.Yes:
                        self._download_new_reshade_version()

        self.progressBar.setValues(messages.checking_new_version, 90)
        self._check_new_program_version()
        self.qtObj.main_tabWidget.setCurrentIndex(0)
        self.qtObj.architecture_groupBox.setEnabled(False)
        self.qtObj.api_groupBox.setEnabled(False)
        self.enable_widgets(False)
        self.progressBar.close()

    ################################################################################
    def _register_form_events(self):
        # TAB 1 - games
        self.qtObj.add_button.clicked.connect(lambda: FormEvents.add_game(self))
        self.qtObj.delete_button.clicked.connect(lambda: FormEvents.delete_game(self))
        self.qtObj.edit_path_button.clicked.connect(lambda: FormEvents.edit_game_path(self))
        self.qtObj.edit_config_button.clicked.connect(lambda: FormEvents.open_reshade_config_file(self))
        self.qtObj.apply_button.clicked.connect(lambda: FormEvents.apply_all(self))
        self.qtObj.update_button.clicked.connect(lambda: FormEvents.update_clicked())
        #########
        self.qtObj.programs_tableWidget.clicked.connect(self._programs_tableWidget_clicked)
        self.qtObj.programs_tableWidget.itemDoubleClicked.connect(self._programs_tableWidget_double_clicked)
        # TAB 2 - configs
        #########
        self.qtObj.yes_dark_theme_radioButton.clicked.connect(lambda: FormEvents.dark_theme_clicked(self, "YES"))
        self.qtObj.no_dark_theme_radioButton.clicked.connect(lambda: FormEvents.dark_theme_clicked(self, "NO"))
        #########
        self.qtObj.yes_check_reshade_updates_radioButton.clicked.connect(lambda: FormEvents.check_reshade_updates_clicked(self, "YES"))
        self.qtObj.no_check_reshade_updates_radioButton.clicked.connect(lambda: FormEvents.check_reshade_updates_clicked(self, "NO"))
        #########
        self.qtObj.yes_silent_reshade_updates_radioButton.clicked.connect(lambda: FormEvents.silent_reshade_updates_clicked(self, "YES"))
        self.qtObj.no_silent_reshade_updates_radioButton.clicked.connect(lambda: FormEvents.silent_reshade_updates_clicked(self, "NO"))
        #########
        self.qtObj.yes_check_program_updates_radioButton.clicked.connect(lambda: FormEvents.check_program_updates_clicked(self, "YES"))
        self.qtObj.no_check_program_updates_radioButton.clicked.connect(lambda: FormEvents.check_program_updates_clicked(self, "NO"))
        #########
        self.qtObj.yes_update_shaders_radioButton.clicked.connect(lambda: FormEvents.update_shaders_clicked(self, "YES"))
        self.qtObj.no_update_shaders_radioButton.clicked.connect(lambda: FormEvents.update_shaders_clicked(self, "NO"))
        #########
        self.qtObj.yes_screenshots_folder_radioButton.clicked.connect(lambda: FormEvents.create_screenshots_folder_clicked(self, "YES"))
        self.qtObj.no_screenshots_folder_radioButton.clicked.connect(lambda: FormEvents.create_screenshots_folder_clicked(self, "NO"))
        #########
        self.qtObj.yes_reset_reshade_radioButton.clicked.connect(lambda: FormEvents.reset_reshade_files_clicked(self, "YES"))
        self.qtObj.no_reset_reshade_radioButton.clicked.connect(lambda: FormEvents.reset_reshade_files_clicked(self, "NO"))
        #########
        self.qtObj.edit_default_config_button.clicked.connect(lambda: FormEvents.edit_default_config_file(self))
        # TAB 3 - about
        #########
        self.qtObj.paypal_button.clicked.connect(lambda: FormEvents.donate_clicked())

    ################################################################################
    def _check_reshade_files(self):
        configSql = ConfigsSql(self)
        rsConfig = configSql.get_configs()

        if rsConfig[0]["reshade_version"] is not None and len(rsConfig[0]["reshade_version"]) > 0:
            self.reshade_version = rsConfig[0]["reshade_version"]
            self.qtObj.reshade_version_label.setText(f"{messages.info_reshade_version}{self.reshade_version}")
            self.enable_form(True)
            self.local_reshade_exe = f"{constants.PROGRAM_PATH}\\ReShade_Setup_{self.reshade_version}.exe"

    ################################################################################
    def _check_new_reshade_version(self):
        self.remote_reshade_version = None
        if self.check_reshade_updates:
            try:
                response = requests.get(constants.RESHADE_WEBSITE_URL)
                if response.status_code != 200:
                    self.log.error(messages.reshade_page_error)
                else:
                    html = str(response.text)
                    soup = BeautifulSoup(html, "html.parser")
                    body = soup.body
                    blist = str(body).split("<p>")

                    for i, content in enumerate(blist, start=1):
                        if content.startswith('<strong>Version '):
                            self.remote_reshade_version = content.split()[1].strip("</strong>")
                            break
            except requests.exceptions.ConnectionError as e:
                self.log.error(f"{messages.reshade_website_unreacheable} {e}")
                utilities.show_message_window("error", "ERROR", messages.reshade_website_unreacheable)
                return

    ################################################################################
    def _download_new_reshade_version(self):
        self.progressBar.setValues(messages.downloading_new_reshade_version, 75)
        if not self.silent_reshade_updates:
            msg = f"{messages.update_reshade_question}"
            reply = utilities.show_message_window("question", "Download new Reshade version", msg)
            if reply == QtWidgets.QMessageBox.No:
                return

        self.remote_reshade_version = None
        exe_download_url = None
        download_path = f"{constants.PROGRAM_PATH}\\ReShade_Setup_"

        # remove old version
        if self.reshade_version is not None:
            old_local_reshade_exe = f"{download_path}{self.reshade_version}.exe"
            if os.path.isfile(old_local_reshade_exe):
                os.remove(old_local_reshade_exe)
            if os.path.isfile(constants.RESHADE32_PATH):
                os.remove(constants.RESHADE32_PATH)
            if os.path.isfile(constants.RESHADE64_PATH):
                os.remove(constants.RESHADE64_PATH)

        # get new version number
        try:
            response = requests.get(constants.RESHADE_WEBSITE_URL)
            if response.status_code != 200:
                self.log.error(messages.reshade_page_error)
            else:
                html = str(response.text)
                soup = BeautifulSoup(html, "html.parser")
                body = soup.body
                blist = str(body).split("<p>")

                for content in blist:
                    if content.startswith('<strong>Version '):
                        self.remote_reshade_version = content.split()[1].strip("</strong>")
                        exe_download_url = f"{constants.RESHADE_EXE_URL}{self.remote_reshade_version}.exe"
                        break
        except requests.exceptions.ConnectionError as e:
            self.log.error(f"{messages.reshade_website_unreacheable} {e}")
            utilities.show_message_window("error", "ERROR", messages.reshade_website_unreacheable)
            return

        # download new reshade version exe
        try:
            self.local_reshade_exe = f"{download_path}{self.remote_reshade_version}.exe"
            r = requests.get(exe_download_url)
            with open(self.local_reshade_exe, 'wb') as outfile:
                outfile.write(r.content)
        except Exception as e:
            if e.errno == 13:
                utilities.show_message_window("error", "ERROR", messages.error_permissionError)
            else:
                self.log.error(f"{messages.error_check_new_reshade_version} {e}")
            return

        # unzip reshade
        self._unzip_reshade(self.local_reshade_exe)

        # save version to sql table
        configSql = ConfigsSql(self)
        configsObj = utilities.Object()
        configsObj.reshade_version = self.remote_reshade_version
        configSql.update_reshade_version(configsObj)

        # set version label
        self.qtObj.reshade_version_label.clear()
        self.qtObj.reshade_version_label.setText(f"{messages.info_reshade_version}{self.remote_reshade_version}")

        if self.need_apply:
            FormEvents.apply_all(self)
            utilities.show_message_window("info", "INFO",
                                          f"{messages.new_reshade_version}\n"
                                          f"Version: {self.remote_reshade_version}\n\n"
                                          f"{messages.apply_success}")
            self.need_apply = False

        self.reshade_version = self.remote_reshade_version

    ################################################################################
    def _check_new_program_version(self):
        self.qtObj.update_button.setVisible(False)
        if self.check_program_updates:
            new_version_obj = utilities.check_new_program_version(self)
            if new_version_obj.new_version_available:
                self.qtObj.updateAvail_label.clear()
                self.qtObj.updateAvail_label.setText(new_version_obj.new_version_msg)
                self.qtObj.update_button.setVisible(True)

    ################################################################################
    def _unzip_reshade(self, local_reshade_exe):
        try:
            out_path = constants.PROGRAM_PATH
            utilities.unzip_file(local_reshade_exe, out_path)
        # except FileNotFoundError as e:
        #    self.log.error(f"{e}")
        # except zipfile.BadZipFile as e:
        #    self.log.error(f"{e}")
        except Exception as e:
            self.log.error(f"{e}")

    ################################################################################
    def _en_dis_apply_button(self):
        len_games = self.qtObj.programs_tableWidget.rowCount()
        if len_games == 0:
            self.qtObj.apply_button.setEnabled(False)
        else:
            self.qtObj.apply_button.setEnabled(True)

    ################################################################################
    def _programs_tableWidget_clicked(self, item):
        FormEvents.programs_tableWidget_clicked(self, item)

    ################################################################################
    def _programs_tableWidget_double_clicked(self):
        self.show_game_config_form(self.selected_game.rs[0]["name"])

    ################################################################################
    def _set_all_configs(self):
        configSql = ConfigsSql(self)
        rsConfig = configSql.get_configs()

        self.populate_programs_listWidget()

        if rsConfig is not None and len(rsConfig) > 0:
            if rsConfig[0]["use_dark_theme"].upper() == "N":
                self.use_dark_theme = False
                self.set_style_sheet(False)
                self.qtObj.yes_dark_theme_radioButton.setChecked(False)
                self.qtObj.no_dark_theme_radioButton.setChecked(True)
            else:
                self.use_dark_theme = True
                self.set_style_sheet(True)
                self.qtObj.yes_dark_theme_radioButton.setChecked(True)
                self.qtObj.no_dark_theme_radioButton.setChecked(False)

            if rsConfig[0]["update_shaders"].upper() == "N":
                self.update_shaders = False
                self.qtObj.yes_update_shaders_radioButton.setChecked(False)
                self.qtObj.no_update_shaders_radioButton.setChecked(True)
            else:
                self.update_shaders = True
                self.qtObj.yes_update_shaders_radioButton.setChecked(True)
                self.qtObj.no_update_shaders_radioButton.setChecked(False)

            if rsConfig[0]["check_program_updates"].upper() == "N":
                self.check_program_updates = False
                self.qtObj.yes_check_program_updates_radioButton.setChecked(False)
                self.qtObj.no_check_program_updates_radioButton.setChecked(True)
            else:
                self.check_program_updates = True
                self.qtObj.yes_check_program_updates_radioButton.setChecked(True)
                self.qtObj.no_check_program_updates_radioButton.setChecked(False)

            if rsConfig[0]["check_reshade_updates"].upper() == "N":
                self.check_reshade_updates = False
                self.qtObj.yes_check_reshade_updates_radioButton.setChecked(False)
                self.qtObj.no_check_reshade_updates_radioButton.setChecked(True)
            else:
                self.check_reshade_updates = True
                self.qtObj.yes_check_reshade_updates_radioButton.setChecked(True)
                self.qtObj.no_check_reshade_updates_radioButton.setChecked(False)

            if rsConfig[0]["create_screenshots_folder"].upper() == "N":
                self.create_screenshots_folder = False
                self.qtObj.yes_screenshots_folder_radioButton.setChecked(False)
                self.qtObj.no_screenshots_folder_radioButton.setChecked(True)
            else:
                self.create_screenshots_folder = True
                self.qtObj.yes_screenshots_folder_radioButton.setChecked(True)
                self.qtObj.no_screenshots_folder_radioButton.setChecked(False)

            if rsConfig[0]["reset_reshade_files"].upper() == "N":
                self.reset_reshade_files = False
                self.qtObj.yes_reset_reshade_radioButton.setChecked(False)
                self.qtObj.no_reset_reshade_radioButton.setChecked(True)
            else:
                self.reset_reshade_files = True
                self.qtObj.yes_reset_reshade_radioButton.setChecked(True)
                self.qtObj.no_reset_reshade_radioButton.setChecked(False)

            if rsConfig[0]["silent_reshade_updates"].upper() == "N":
                self.silent_reshade_updates = False
                self.qtObj.yes_silent_reshade_updates_radioButton.setChecked(False)
                self.qtObj.no_silent_reshade_updates_radioButton.setChecked(True)
            else:
                self.silent_reshade_updates = True
                self.qtObj.yes_silent_reshade_updates_radioButton.setChecked(True)
                self.qtObj.no_silent_reshade_updates_radioButton.setChecked(False)
            self.qtObj.silent_reshade_updates_groupBox.setEnabled(self.check_reshade_updates)
            self.qtObj.silent_reshade_updates_groupBox.setVisible(self.check_reshade_updates)

            if rsConfig[0]["program_version"] is None or rsConfig[0]["program_version"] != constants.VERSION:
                config_obj = utilities.Object()
                config_obj.program_version = constants.VERSION
                configSql.update_program_version(config_obj)

    ################################################################################
    def show_game_config_form(self, game_name: str):
        self.game_config_form = QtWidgets.QWidget()
        _translate = QtCore.QCoreApplication.translate
        qtObj = UiGameConfigForm()
        qtObj.setupUi(self.game_config_form)
        self.game_config_form.qtObj = qtObj
        if self.use_dark_theme:
            self.game_config_form.setStyleSheet(open(constants.STYLE_QSS_FILENAME, "r").read())
        self.game_config_form.qtObj.game_name_lineEdit.setFocus()
        self.game_config_form.show()
        QtWidgets.QApplication.processEvents()

        self.game_config_form.qtObj.ok_pushButton.clicked.connect(lambda: FormEvents.game_config_form(self, "OK"))
        self.game_config_form.qtObj.cancel_pushButton.clicked.connect(lambda: FormEvents.game_config_form(self, "CANCEL"))

        if self.selected_game is not None:
            self.game_config_form.qtObj.game_name_lineEdit.setText(self.selected_game.rs[0]["name"])
            if self.selected_game.rs[0]["architecture"] == "32bits":
                self.game_config_form.qtObj.radioButton_32bits.setChecked(True)
                self.game_config_form.qtObj.radioButton_64bits.setChecked(False)
            else:
                self.game_config_form.qtObj.radioButton_32bits.setChecked(False)
                self.game_config_form.qtObj.radioButton_64bits.setChecked(True)

            if self.selected_game.rs[0]["api"] == "DX9":
                self.game_config_form.qtObj.dx9_radioButton.setChecked(True)
                self.game_config_form.qtObj.dx11_radioButton.setChecked(False)
            else:
                self.game_config_form.qtObj.dx9_radioButton.setChecked(False)
                self.game_config_form.qtObj.dx11_radioButton.setChecked(True)
        else:
            self.game_config_form.qtObj.game_name_lineEdit.setText(game_name)

    ################################################################################
    def set_style_sheet(self, status: bool):
        if status:
            self.form.setStyleSheet(open(constants.STYLE_QSS_FILENAME, "r").read())
        else:
            self.form.setStyleSheet("")

    ################################################################################
    def populate_programs_listWidget(self):
        self.qtObj.programs_tableWidget.setRowCount(0)
        games_sql = GamesSql(self)
        rs_all_games = games_sql.get_games()
        if rs_all_games is not None and len(rs_all_games) > 0:
            for i in range(len(rs_all_games)):
                len_games = self.qtObj.programs_tableWidget.rowCount()
                self.qtObj.programs_tableWidget.insertRow(len_games)
                self.qtObj.programs_tableWidget.setItem(len_games, 0,
                                                        QtWidgets.QTableWidgetItem(rs_all_games[i]["name"]))
                self.qtObj.programs_tableWidget.setItem(len_games, 1,
                                                        QtWidgets.QTableWidgetItem(rs_all_games[i]["path"]))

    ################################################################################
    def enable_form(self, status: bool):
        self.qtObj.add_button.setEnabled(status)
        num_pages = self.qtObj.main_tabWidget.count()

        if status:
            self.qtObj.main_tabWidget.setCurrentIndex(0)  # set to first tab
        else:
            self.selected_game = None
            self.qtObj.main_tabWidget.setCurrentIndex(num_pages - 1)  # set to last tab (about)

        for x in range(0, num_pages):
            self.qtObj.main_tabWidget.setTabEnabled(x, status)

    ################################################################################
    def enable_widgets(self, status: bool):
        if not status:
            self.selected_game = None

            self.qtObj.radioButton_32bits.setAutoExclusive(False)
            self.qtObj.radioButton_32bits.setChecked(False)

            self.qtObj.radioButton_64bits.setAutoExclusive(False)
            self.qtObj.radioButton_64bits.setChecked(False)

            self.qtObj.dx9_radioButton.setAutoExclusive(False)
            self.qtObj.dx9_radioButton.setChecked(False)

            self.qtObj.dx11_radioButton.setAutoExclusive(False)
            self.qtObj.dx11_radioButton.setChecked(False)

        self._en_dis_apply_button()
        self.qtObj.delete_button.setEnabled(status)
        self.qtObj.edit_path_button.setEnabled(status)
        self.qtObj.edit_config_button.setEnabled(status)

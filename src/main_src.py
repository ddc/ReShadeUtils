#! /usr/bin/env python3
# |*****************************************************
# * Copyright         : Copyright (C) 2019
# * Author            : ddc
# * License           : GPL v3
# |*****************************************************
# # -*- coding: utf-8 -*-

import os
import requests
from PyQt5.QtCore import Qt
from bs4 import BeautifulSoup
from src.sql.games_sql import GamesSql
from src.sql.config_sql import ConfigSql
from PyQt5 import QtCore, QtGui, QtWidgets
from src.game_configs import Ui_game_config_form
from src import constants, form_events, messages, utils, log, qtutils
from src.progressbar import ProgressBar
from src.log import Logs


class MainSrc:
    def __init__(self, qtobj, form):
        self.qtobj = qtobj
        self.form = form
        self.progressBar = None
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
        self.use_custom_config = None
        self.need_apply = False
        self.new_version = None
        self.db_conn = None
        self.remote_reshade_version = None
        self.client_version = None
        self.log = None


    def init(self):
        utils.check_dirs()
        self.progressBar = ProgressBar()
        self.progressBar.set_values(messages.initializing, 0)
        self.log = Logs(constants.DIR_LOGS).setup_logging()
        self.log.info(f"Starting {constants.FULL_PROGRAM_NAME}")
        qtutils.set_icons(self)

        self.progressBar.set_values(messages.checking_files, 15)
        utils.check_files(self)
        self.client_version = constants.VERSION

        self.progressBar.set_values(messages.checking_db_connection, 30)
        utils.check_db_connection(self)
        utils.set_default_database_configs(self)

        self.progressBar.set_values(messages.checking_configs, 45)
        self.qtobj.programs_tableWidget.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)
        self._set_all_configs()
        self._register_form_events()

        self.progressBar.set_values(messages.checking_new_reshade_version, 60)
        self._check_reshade_files()

        if self.local_reshade_exe is None:
            self._download_new_reshade_version()
        else:
            if not os.path.isfile(self.local_reshade_exe):
                self._download_new_reshade_version()
            else:
                self._check_new_reshade_version()

        if self.remote_reshade_version is not None:
            if self.reshade_version != self.remote_reshade_version:
                self.need_apply = True
                if self.silent_reshade_updates:
                    self._download_new_reshade_version()
                else:
                    msg = messages.update_reshade_question
                    reply = qtutils.show_message_window(self.log, "question", msg)
                    if reply == QtWidgets.QMessageBox.Yes:
                        self._download_new_reshade_version()

        self.progressBar.set_values(messages.checking_new_version, 90)
        self._check_new_program_version()
        self.qtobj.main_tabWidget.setCurrentIndex(0)

        self.qtobj.programs_tableWidget.setColumnWidth(0, 150)
        self.qtobj.programs_tableWidget.setColumnWidth(1, 80)
        self.qtobj.programs_tableWidget.setColumnWidth(2, 110)
        self.qtobj.programs_tableWidget.horizontalHeader().setStretchLastSection(True)
        # from PyQt6.QtWidgets import QHeaderView
        # self.qtobj.programs_tableWidget.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)

        self.enable_widgets(False)
        self.progressBar.close()


    def _register_form_events(self):
        # TAB 1 - games
        self.qtobj.add_button.clicked.connect(lambda: form_events.add_game(self))
        self.qtobj.delete_button.clicked.connect(lambda: form_events.delete_game(self))
        self.qtobj.edit_path_button.clicked.connect(lambda: form_events.edit_game_path(self))
        self.qtobj.edit_config_button.clicked.connect(lambda: form_events.open_reshade_config_file(self))
        self.qtobj.apply_button.clicked.connect(lambda: form_events.apply_all(self))
        self.qtobj.update_button.clicked.connect(lambda: form_events.update_clicked())
        #########
        self.qtobj.programs_tableWidget.clicked.connect(self._programs_table_widget_clicked)
        self.qtobj.programs_tableWidget.itemDoubleClicked.connect(self._programs_table_widget_double_clicked)
        # TAB 2 - configs
        #########
        self.qtobj.yes_dark_theme_radioButton.clicked.connect(lambda: form_events.dark_theme_clicked(self, "YES"))
        self.qtobj.no_dark_theme_radioButton.clicked.connect(lambda: form_events.dark_theme_clicked(self, "NO"))
        #########
        self.qtobj.yes_check_reshade_updates_radioButton.clicked.connect(lambda: form_events.check_reshade_updates_clicked(self, "YES"))
        self.qtobj.no_check_reshade_updates_radioButton.clicked.connect(lambda: form_events.check_reshade_updates_clicked(self, "NO"))
        #########
        self.qtobj.yes_silent_reshade_updates_radioButton.clicked.connect(lambda: form_events.silent_reshade_updates_clicked(self, "YES"))
        self.qtobj.no_silent_reshade_updates_radioButton.clicked.connect(lambda: form_events.silent_reshade_updates_clicked(self, "NO"))
        #########
        self.qtobj.yes_check_program_updates_radioButton.clicked.connect(lambda: form_events.check_program_updates_clicked(self, "YES"))
        self.qtobj.no_check_program_updates_radioButton.clicked.connect(lambda: form_events.check_program_updates_clicked(self, "NO"))
        #########
        self.qtobj.yes_update_shaders_radioButton.clicked.connect(lambda: form_events.update_shaders_clicked(self, "YES"))
        self.qtobj.no_update_shaders_radioButton.clicked.connect(lambda: form_events.update_shaders_clicked(self, "NO"))
        #########
        self.qtobj.yes_screenshots_folder_radioButton.clicked.connect(lambda: form_events.create_screenshots_folder_clicked(self, "YES"))
        self.qtobj.no_screenshots_folder_radioButton.clicked.connect(lambda: form_events.create_screenshots_folder_clicked(self, "NO"))
        #########
        self.qtobj.yes_reset_reshade_radioButton.clicked.connect(lambda: form_events.reset_reshade_files_clicked(self, "YES"))
        self.qtobj.no_reset_reshade_radioButton.clicked.connect(lambda: form_events.reset_reshade_files_clicked(self, "NO"))
        #########
        self.qtobj.yes_custom_config_radioButton.clicked.connect(lambda: form_events.custom_config_clicked(self, "YES"))
        self.qtobj.no_custom_config_radioButton.clicked.connect(lambda: form_events.custom_config_clicked(self, "NO"))
        #########
        self.qtobj.edit_all_games_custom_config_button.clicked.connect(lambda: form_events.edit_all_games_custom_config_button(self))
        # TAB 3 - about
        #########
        self.qtobj.donate_button.clicked.connect(lambda: form_events.donate_clicked())


    def _check_reshade_files(self):
        config_sql = ConfigSql(self)
        rs_config = config_sql.get_configs()
        if rs_config[0].get("reshade_version") is not None and len(rs_config[0].get("reshade_version")) > 0:
            self.reshade_version = rs_config[0].get("reshade_version")
            self.qtobj.reshade_version_label.setText(f"{messages.info_reshade_version}{self.reshade_version}")
            self.enable_form(True)
            self.local_reshade_exe = os.path.join(constants.PROGRAM_PATH, f"ReShade_Setup_{self.reshade_version}.exe")


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
                        if content.startswith("<strong>Version "):
                            self.remote_reshade_version = content.split()[1].strip("</strong>")
                            break
            except requests.exceptions.ConnectionError as e:
                self.log.error(f"{messages.reshade_website_unreacheable} {str(e)}")
                qtutils.show_message_window(self.log, "error", messages.reshade_website_unreacheable)
                return


    def _download_new_reshade_version(self):
        self.progressBar.set_values(messages.downloading_new_reshade_version, 75)
        if not self.silent_reshade_updates:
            msg = messages.update_reshade_question
            reply = qtutils.show_message_window(self.log, "question", msg)
            if reply == QtWidgets.QMessageBox.No:
                return

        self.remote_reshade_version = None
        exe_download_url = None

        # remove old version
        if self.reshade_version is not None:
            old_local_reshade_exe = os.path.join(constants.PROGRAM_PATH, f"ReShade_Setup_{self.reshade_version}.exe")
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
                    if content.startswith("<strong>Version "):
                        self.remote_reshade_version = content.split()[1].strip("</strong>")
                        exe_download_url = f"{constants.RESHADE_EXE_URL}{self.remote_reshade_version}.exe"
                        break
        except requests.exceptions.ConnectionError as e:
            self.log.error(f"{messages.reshade_website_unreacheable} {str(e)}")
            qtutils.show_message_window(self.log, "error", messages.reshade_website_unreacheable)
            return

        # download new reshade version exe
        try:
            self.local_reshade_exe = os.path.join(constants.PROGRAM_PATH, f"ReShade_Setup_{self.remote_reshade_version}.exe")
            r = requests.get(exe_download_url)
            with open(self.local_reshade_exe, "wb") as outfile:
                outfile.write(r.content)
        except Exception as e:
            if hasattr(e, "errno") and e.errno == 13:
                qtutils.show_message_window(self.log, "error", messages.error_permissionError)
            else:
                self.log.error(f"{messages.error_check_new_reshade_version} {str(e)}")
            return

        # unzip reshade
        self._unzip_reshade(self.local_reshade_exe)

        # save version to sql table
        config_sql = ConfigSql(self)
        configs_obj = utils.Object()
        configs_obj.reshade_version = self.remote_reshade_version
        config_sql.update_reshade_version(configs_obj)

        # set version label
        self.qtobj.reshade_version_label.clear()
        self.qtobj.reshade_version_label.setText(f"{messages.info_reshade_version}{self.remote_reshade_version}")

        if self.need_apply:
            form_events.apply_all(self)
            qtutils.show_message_window(self.log, "info",
                                        f"{messages.new_reshade_version}\n"
                                        f"Version: {self.remote_reshade_version}\n\n"
                                        f"{messages.apply_success}")
            self.need_apply = False

        self.reshade_version = self.remote_reshade_version


    def _check_new_program_version(self):
        self.qtobj.update_button.setVisible(False)
        if self.check_program_updates:
            new_version_obj = utils.check_new_program_version(self)
            if new_version_obj.new_version_available:
                self.qtobj.updateAvail_label.clear()
                self.qtobj.updateAvail_label.setText(new_version_obj.new_version_msg)
                self.qtobj.update_button.setVisible(True)


    def _unzip_reshade(self, local_reshade_exe):
        try:
            out_path = constants.PROGRAM_PATH
            utils.unzip_file(local_reshade_exe, out_path)
        # except FileNotFoundError as e:
        #    self.log.error(str(e))
        # except zipfile.BadZipFile as e:
        #    self.log.error(str(e))
        except Exception as e:
            self.log.error(str(e))


    def _set_state_apply_button(self):
        # enable / disable  apply button
        len_games = self.qtobj.programs_tableWidget.rowCount()
        if len_games == 0:
            self.qtobj.apply_button.setEnabled(False)
        else:
            self.qtobj.apply_button.setEnabled(True)


    def _programs_table_widget_clicked(self, item):
        form_events.programs_tableWidget_clicked(self, item)


    def _programs_table_widget_double_clicked(self):
        self.show_game_config_form(self.selected_game.name, self.selected_game.architecture)


    def _set_all_configs(self):
        config_sql = ConfigSql(self)
        rs_config = config_sql.get_configs()

        self.populate_datagrid()

        if rs_config is not None and len(rs_config) > 0:
            if not rs_config[0].get("use_dark_theme"):
                self.use_dark_theme = False
                self.set_style_sheet(False)
                self.qtobj.yes_dark_theme_radioButton.setChecked(False)
                self.qtobj.no_dark_theme_radioButton.setChecked(True)
            else:
                self.use_dark_theme = True
                self.set_style_sheet(True)
                self.qtobj.yes_dark_theme_radioButton.setChecked(True)
                self.qtobj.no_dark_theme_radioButton.setChecked(False)

            if not rs_config[0].get("update_shaders"):
                self.update_shaders = False
                self.qtobj.yes_update_shaders_radioButton.setChecked(False)
                self.qtobj.no_update_shaders_radioButton.setChecked(True)
            else:
                self.update_shaders = True
                self.qtobj.yes_update_shaders_radioButton.setChecked(True)
                self.qtobj.no_update_shaders_radioButton.setChecked(False)

            if not rs_config[0].get("check_program_updates"):
                self.check_program_updates = False
                self.qtobj.yes_check_program_updates_radioButton.setChecked(False)
                self.qtobj.no_check_program_updates_radioButton.setChecked(True)
            else:
                self.check_program_updates = True
                self.qtobj.yes_check_program_updates_radioButton.setChecked(True)
                self.qtobj.no_check_program_updates_radioButton.setChecked(False)

            if not rs_config[0].get("check_reshade_updates"):
                self.check_reshade_updates = False
                self.qtobj.yes_check_reshade_updates_radioButton.setChecked(False)
                self.qtobj.no_check_reshade_updates_radioButton.setChecked(True)
            else:
                self.check_reshade_updates = True
                self.qtobj.yes_check_reshade_updates_radioButton.setChecked(True)
                self.qtobj.no_check_reshade_updates_radioButton.setChecked(False)

            if not rs_config[0].get("create_screenshots_folder"):
                self.create_screenshots_folder = False
                self.qtobj.yes_screenshots_folder_radioButton.setChecked(False)
                self.qtobj.no_screenshots_folder_radioButton.setChecked(True)
            else:
                self.create_screenshots_folder = True
                self.qtobj.yes_screenshots_folder_radioButton.setChecked(True)
                self.qtobj.no_screenshots_folder_radioButton.setChecked(False)

            if not rs_config[0].get("reset_reshade_files"):
                self.reset_reshade_files = False
                self.qtobj.yes_reset_reshade_radioButton.setChecked(False)
                self.qtobj.no_reset_reshade_radioButton.setChecked(True)
            else:
                self.reset_reshade_files = True
                self.qtobj.yes_reset_reshade_radioButton.setChecked(True)
                self.qtobj.no_reset_reshade_radioButton.setChecked(False)

            if not rs_config[0].get("use_custom_config"):
                self.use_custom_config = False
                self.qtobj.yes_custom_config_radioButton.setChecked(False)
                self.qtobj.no_custom_config_radioButton.setChecked(True)
            else:
                self.use_custom_config = True
                self.qtobj.yes_custom_config_radioButton.setChecked(True)
                self.qtobj.no_custom_config_radioButton.setChecked(False)

            if not rs_config[0].get("silent_reshade_updates"):
                self.silent_reshade_updates = False
                self.qtobj.yes_silent_reshade_updates_radioButton.setChecked(False)
                self.qtobj.no_silent_reshade_updates_radioButton.setChecked(True)
            else:
                self.silent_reshade_updates = True
                self.qtobj.yes_silent_reshade_updates_radioButton.setChecked(True)
                self.qtobj.no_silent_reshade_updates_radioButton.setChecked(False)
            self.qtobj.silent_reshade_updates_groupBox.setEnabled(self.check_reshade_updates)
            self.qtobj.silent_reshade_updates_groupBox.setVisible(self.check_reshade_updates)

            if rs_config[0].get("program_version") is None or rs_config[0].get("program_version") != constants.VERSION:
                config_obj = utils.Object()
                config_obj.program_version = constants.VERSION
                config_sql.update_program_version(config_obj)


    def show_game_config_form(self, game_name, architecture):
        if not utils.check_game_file(self):
            qtutils.show_message_window(self.log, "error", messages.error_game_not_found)
            return

        self.game_config_form = QtWidgets.QWidget()
        _translate = QtCore.QCoreApplication.translate
        qt_obj = Ui_game_config_form()
        qt_obj.setupUi(self.game_config_form)
        self.game_config_form.qtObj = qt_obj

        icon_cancel = QtGui.QIcon()
        icon_cancel_pixmap = QtGui.QPixmap(utils.resource_path("images/cancel.png"))
        icon_cancel.addPixmap(icon_cancel_pixmap, QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.game_config_form.qtObj.cancel_pushButton.setIcon(icon_cancel)

        icon_apply = QtGui.QIcon()
        icon_apply_pixmap = QtGui.QPixmap(utils.resource_path("images/apply.png"))
        icon_apply.addPixmap(icon_apply_pixmap, QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.game_config_form.qtObj.ok_pushButton.setIcon(icon_apply)

        if self.use_dark_theme:
            self.game_config_form.setStyleSheet(open(constants.STYLE_QSS_FILENAME, "r").read())

        self.game_config_form.qtObj.game_name_lineEdit.setFocus()
        self.game_config_form.show()
        QtWidgets.QApplication.processEvents()

        self.game_config_form.qtObj.ok_pushButton.clicked.connect(lambda: form_events.game_config_form_result(self, architecture, "OK"))
        self.game_config_form.qtObj.cancel_pushButton.clicked.connect(lambda: form_events.game_config_form_result(self, architecture, "CANCEL"))

        if self.selected_game is not None:
            self.game_config_form.qtObj.game_name_lineEdit.setText(self.selected_game.name)

            if self.selected_game.api == constants.DX9_DISPLAY_NAME:
                self.game_config_form.qtObj.dx9_radioButton.setChecked(True)
                self.game_config_form.qtObj.dx_radioButton.setChecked(False)
                self.game_config_form.qtObj.opengl_radioButton.setChecked(False)
            elif self.selected_game.api == constants.OPENGL_DISPLAY_NAME:
                self.game_config_form.qtObj.dx9_radioButton.setChecked(False)
                self.game_config_form.qtObj.dx_radioButton.setChecked(False)
                self.game_config_form.qtObj.opengl_radioButton.setChecked(True)
            else:
                self.game_config_form.qtObj.dx9_radioButton.setChecked(False)
                self.game_config_form.qtObj.dx_radioButton.setChecked(True)
                self.game_config_form.qtObj.opengl_radioButton.setChecked(False)
        else:
            self.game_config_form.qtObj.game_name_lineEdit.setText(game_name)


    def set_style_sheet(self, status: bool):
        if status:
            self.form.setStyleSheet(open(constants.STYLE_QSS_FILENAME, "r").read())
        else:
            self.form.setStyleSheet("")


    def populate_datagrid(self):
        self.qtobj.programs_tableWidget.setRowCount(0)
        games_sql = GamesSql(self)
        rs_all_games = games_sql.get_games()
        if rs_all_games is not None and len(rs_all_games) > 0:
            for i in range(len(rs_all_games)):
                len_games = self.qtobj.programs_tableWidget.rowCount()
                self.qtobj.programs_tableWidget.insertRow(len_games)
                self.qtobj.programs_tableWidget.setItem(len_games, 0,
                                                        QtWidgets.QTableWidgetItem(rs_all_games[i].get("name")))
                self.qtobj.programs_tableWidget.setItem(len_games, 1,
                                                        QtWidgets.QTableWidgetItem(rs_all_games[i].get("architecture")))
                self.qtobj.programs_tableWidget.setItem(len_games, 2,
                                                        QtWidgets.QTableWidgetItem(rs_all_games[i].get("api")))
                self.qtobj.programs_tableWidget.setItem(len_games, 3,
                                                        QtWidgets.QTableWidgetItem(rs_all_games[i].get("path")))


    def enable_form(self, status: bool):
        self.qtobj.add_button.setEnabled(status)
        num_pages = self.qtobj.main_tabWidget.count()

        if status:
            # set to first tab
            self.qtobj.main_tabWidget.setCurrentIndex(0)
        else:
            # set to last tab (about)
            self.selected_game = None
            self.qtobj.main_tabWidget.setCurrentIndex(num_pages - 1)

        for x in range(0, num_pages):
            self.qtobj.main_tabWidget.setTabEnabled(x, status)


    def enable_widgets(self, status: bool):
        if not status:
            self.selected_game = None

        self._set_state_apply_button()
        self.qtobj.delete_button.setEnabled(status)
        self.qtobj.edit_path_button.setEnabled(status)
        self.qtobj.edit_config_button.setEnabled(status)

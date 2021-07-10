# |*****************************************************
# * Copyright         : Copyright (C) 2019
# * Author            : ddc
# * License           : GPL v3
# |*****************************************************
# # -*- coding: utf-8 -*-


import os
from src.log import Log
from PyQt5.QtCore import Qt
from src.config import Ui_config
from src.sql.games_sql import GamesSql
from src.progressbar import ProgressBar
from src.sql.config_sql import ConfigSql
from src.sql.database import DatabaseClass
from PyQt5 import QtWidgets
from src import constants, events, messages, utils, qtutils


class MainSrc:
    def __init__(self, qtobj, form):
        self.qtobj = qtobj
        self.form = form
        self.client_version = constants.VERSION
        self.log = Log().setup_logging()
        self.database = DatabaseClass(self.log)
        self.progressbar = ProgressBar()
        self.check_program_updates = True
        self.check_reshade_updates = True
        self.create_screenshots_folder = True
        self.show_info_messages = True
        self.use_dark_theme = True
        self.update_shaders = True
        self.need_apply = False
        self.selected_game = None
        self.game_config_form = None
        self.reshade_version = None
        self.program_version = None
        self.local_reshade_path = None
        self.new_version = None
        self.remote_reshade_version = None
        self.remote_reshade_download_url = None


    def start(self):
        self.log.info(f"STARTING {constants.FULL_PROGRAM_NAME}")
        self.progressbar.set_values(messages.checking_files, 15)
        utils.check_local_files(self)

        self.progressbar.set_values(messages.checking_database, 30)
        utils.check_database_connection(self)
        utils.check_default_database_tables(self)
        utils.check_default_database_configs(self)

        self.progressbar.set_values(messages.checking_configs, 45)
        self.set_variables()
        self.register_form_events()

        self.progressbar.set_values(messages.checking_reshade_updates, 60)
        utils.check_reshade_updates(self)
        utils.check_reshade_dll_files(self)
        if not os.path.isdir(constants.SHADERS_SRC_PATH):
            utils.download_shaders(self)

        self.progressbar.set_values(messages.checking_program_updates, 90)
        utils.check_program_updates(self)

        self.progressbar.close()
        self.qtobj.main_tabWidget.setCurrentIndex(0)
        self.qtobj.programs_tableWidget.setColumnWidth(2, 130)
        self.qtobj.programs_tableWidget.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)
        self.populate_table_widget()
        self.enable_widgets(False)


    def set_variables(self):
        config_sql = ConfigSql(self)
        rs_config = config_sql.get_configs()
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

            if not rs_config[0].get("check_program_updates"):
                self.check_program_updates = False
                self.qtobj.yes_check_program_updates_radioButton.setChecked(False)
                self.qtobj.no_check_program_updates_radioButton.setChecked(True)
            else:
                self.check_program_updates = True
                self.qtobj.yes_check_program_updates_radioButton.setChecked(True)
                self.qtobj.no_check_program_updates_radioButton.setChecked(False)

            if not rs_config[0].get("show_info_messages"):
                self.show_info_messages = False
                self.qtobj.yes_show_info_messages_radioButton.setChecked(False)
                self.qtobj.no_show_info_messages_radioButton.setChecked(True)
            else:
                self.show_info_messages = True
                self.qtobj.yes_show_info_messages_radioButton.setChecked(True)
                self.qtobj.no_show_info_messages_radioButton.setChecked(False)

            if not rs_config[0].get("check_reshade_updates"):
                self.check_reshade_updates = False
                self.qtobj.yes_check_reshade_updates_radioButton.setChecked(False)
                self.qtobj.no_check_reshade_updates_radioButton.setChecked(True)
            else:
                self.check_reshade_updates = True
                self.qtobj.yes_check_reshade_updates_radioButton.setChecked(True)
                self.qtobj.no_check_reshade_updates_radioButton.setChecked(False)

            if not rs_config[0].get("update_shaders"):
                self.update_shaders = False
                self.qtobj.yes_update_shaders_radioButton.setChecked(False)
                self.qtobj.no_update_shaders_radioButton.setChecked(True)
            else:
                self.update_shaders = True
                self.qtobj.yes_update_shaders_radioButton.setChecked(True)
                self.qtobj.no_update_shaders_radioButton.setChecked(False)

            if not rs_config[0].get("create_screenshots_folder"):
                self.create_screenshots_folder = False
                self.qtobj.yes_screenshots_folder_radioButton.setChecked(False)
                self.qtobj.no_screenshots_folder_radioButton.setChecked(True)
            else:
                self.create_screenshots_folder = True
                self.qtobj.yes_screenshots_folder_radioButton.setChecked(True)
                self.qtobj.no_screenshots_folder_radioButton.setChecked(False)

            if rs_config[0].get("program_version"):
                self.program_version = rs_config[0].get("program_version")

            if rs_config[0].get("reshade_version"):
                self.reshade_version = rs_config[0].get("reshade_version")


    def register_form_events(self):
        # TAB 1 - games
        self.qtobj.add_button.clicked.connect(lambda: events.add_game(self))
        self.qtobj.delete_button.clicked.connect(lambda: events.delete_game(self))
        self.qtobj.edit_path_button.clicked.connect(lambda: events.edit_game_path(self))
        self.qtobj.edit_preset_button.clicked.connect(lambda: events.open_preset_config_file(self))
        self.qtobj.apply_button.clicked.connect(lambda: events.apply_all(self))
        self.qtobj.update_button.clicked.connect(lambda: events.update_clicked())
        self.qtobj.programs_tableWidget.clicked.connect(self._table_widget_clicked)
        self.qtobj.programs_tableWidget.itemDoubleClicked.connect(self._table_widget_double_clicked)

        # TAB 2 - configs
        self.qtobj.yes_dark_theme_radioButton.clicked.connect(lambda: events.dark_theme_clicked(self, "YES"))
        self.qtobj.no_dark_theme_radioButton.clicked.connect(lambda: events.dark_theme_clicked(self, "NO"))

        self.qtobj.yes_check_program_updates_radioButton.clicked.connect(lambda: events.check_program_updates_clicked(self, "YES"))
        self.qtobj.no_check_program_updates_radioButton.clicked.connect(lambda: events.check_program_updates_clicked(self, "NO"))

        self.qtobj.yes_show_info_messages_radioButton.clicked.connect(lambda: events.show_info_messages_clicked(self, "YES"))
        self.qtobj.no_show_info_messages_radioButton.clicked.connect(lambda: events.show_info_messages_clicked(self, "NO"))

        self.qtobj.yes_check_reshade_updates_radioButton.clicked.connect(lambda: events.check_reshade_updates_clicked(self, "YES"))
        self.qtobj.no_check_reshade_updates_radioButton.clicked.connect(lambda: events.check_reshade_updates_clicked(self, "NO"))

        self.qtobj.yes_update_shaders_radioButton.clicked.connect(lambda: events.update_shaders_clicked(self, "YES"))
        self.qtobj.no_update_shaders_radioButton.clicked.connect(lambda: events.update_shaders_clicked(self, "NO"))

        self.qtobj.yes_screenshots_folder_radioButton.clicked.connect(lambda: events.create_screenshots_folder_clicked(self, "YES"))
        self.qtobj.no_screenshots_folder_radioButton.clicked.connect(lambda: events.create_screenshots_folder_clicked(self, "NO"))

        self.qtobj.edit_default_preset_plugin_button.clicked.connect(lambda: events.edit_default_preset_plugin_button_clicked(self))
        self.qtobj.reset_all_button.clicked.connect(lambda: events.reset_all_button_clicked(self))

        # TAB 3 - about
        self.qtobj.donate_button.clicked.connect(lambda: events.donate_clicked())


    def show_game_config_form(self, game_name, architecture):
        if not utils.check_game_file(self):
            qtutils.show_message_window(self.log, "error", messages.error_game_not_found)
            return

        self.game_config_form = QtWidgets.QWidget()
        qt_obj = Ui_config()
        qt_obj.setupUi(self.game_config_form)
        self.game_config_form.qtObj = qt_obj

        if self.use_dark_theme:
            self.game_config_form.setStyleSheet(open(constants.QSS_FILENAME, "r").read())

        self.game_config_form.qtObj.game_name_lineEdit.setFocus()
        self.game_config_form.show()
        QtWidgets.QApplication.processEvents()

        self.game_config_form.qtObj.ok_pushButton.clicked.connect(lambda: events.game_config_form_result(self, architecture, "OK"))
        self.game_config_form.qtObj.cancel_pushButton.clicked.connect(lambda: events.game_config_form_result(self, architecture, "CANCEL"))

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
            self.form.setStyleSheet(open(constants.QSS_FILENAME, "r").read())
        else:
            self.form.setStyleSheet("")


    def populate_table_widget(self):
        self.qtobj.programs_tableWidget.setRowCount(0) # cleanning datagrid
        games_sql = GamesSql(self)
        rs_all_games = games_sql.get_games()
        if rs_all_games is not None and len(rs_all_games) > 0:
            for i in range(len(rs_all_games)):
                self.qtobj.programs_tableWidget.insertRow(i)
                self.qtobj.programs_tableWidget.setItem(i, 0,
                                                        QtWidgets.QTableWidgetItem(rs_all_games[i].get("name")))
                self.qtobj.programs_tableWidget.setItem(i, 1,
                                                        QtWidgets.QTableWidgetItem(rs_all_games[i].get("architecture")))
                self.qtobj.programs_tableWidget.setItem(i, 2,
                                                        QtWidgets.QTableWidgetItem(rs_all_games[i].get("api")))
                self.qtobj.programs_tableWidget.setItem(i, 3,
                                                        QtWidgets.QTableWidgetItem(rs_all_games[i].get("path")))

        self.qtobj.programs_tableWidget.resizeColumnsToContents()
        highest_column_width = self.qtobj.programs_tableWidget.columnWidth(3)
        if highest_column_width < 600:
            self.qtobj.programs_tableWidget.horizontalHeader().setStretchLastSection(True)
        else:
            self.qtobj.programs_tableWidget.horizontalHeader().setStretchLastSection(False)
            self.qtobj.programs_tableWidget.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)


    def enable_form(self, status: bool):
        if not status:
            self.selected_game = None
        self.qtobj.add_button.setEnabled(status)
        for i in range(0, self.qtobj.main_tabWidget.count()):
            self.qtobj.main_tabWidget.setTabEnabled(i, status)
        self.qtobj.main_tabWidget.setCurrentIndex(0)


    def enable_widgets(self, status: bool):
        if not status:
            self.selected_game = None
        self._set_state_apply_button()
        self.qtobj.delete_button.setEnabled(status)
        self.qtobj.edit_path_button.setEnabled(status)
        self.qtobj.edit_preset_button.setEnabled(status)
        self.qtobj.main_tabWidget.setCurrentIndex(0)


    def _set_state_apply_button(self):
        len_games = self.qtobj.programs_tableWidget.rowCount()
        if len_games == 0:
            self.qtobj.apply_button.setEnabled(False)
        else:
            self.qtobj.apply_button.setEnabled(True)


    def _table_widget_clicked(self, item):
        events.programs_tableWidget_clicked(self, item)


    def _table_widget_double_clicked(self):
        if self.selected_game is not None:
            self.show_game_config_form(self.selected_game.name, self.selected_game.architecture)

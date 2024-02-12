# -*- coding: utf-8 -*-
from ddcUtils.databases import DBSqlite
from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt
from src import events
from src.constants import messages, variables
from src.database.dal.config_dal import ConfigDal
from src.database.dal.games_dal import GamesDal
from src.log import Log
from src.tools import file_utils, program_utils, reshade_utils
from src.tools.qt import qt_utils
from src.tools.qt.progressbar import ProgressBar


class MainSrc:
    def __init__(self, qtobj, form):
        self.qtobj = qtobj
        self.form = form
        self.client_version = variables.VERSION_STR
        self.log = Log().setup_logging()
        self.progressbar = ProgressBar()
        self.db_session = None
        self.check_program_updates = True
        self.check_reshade_updates = True
        self.create_screenshots_folder = True
        self.show_info_messages = True
        self.use_dark_theme = False
        self.need_apply = False
        self.selected_game = None
        self.game_config_form = None
        self.reshade_version = None
        self.local_reshade_path = None
        self.new_version = None
        self.remote_reshade_version = None
        self.remote_reshade_download_url = None

    def start(self):
        self.log.info(f"STARTING {variables.FULL_PROGRAM_NAME}")

        database = DBSqlite(variables.DATABASE_PATH)
        with database.session() as db_session:
            self.db_session = db_session

            # check for first run
            self.progressbar.set_values(messages.checking_database, 15)
            config_sql = ConfigDal(self.db_session, self.log)
            rs_config = config_sql.get_configs()
            if not rs_config:
                # first run, since database is empty
                self.progressbar.set_values(messages.checking_database, 30)
                if program_utils.download_alembic_dir(self.log):
                    program_utils.run_alembic_migrations()

            self.progressbar.set_values(messages.checking_configs, 45)
            self.set_variables(rs_config)
            self.register_form_events()

            self.progressbar.set_values(messages.checking_reshade_updates, 75)
            reshade_utils.check_reshade_updates(self)

            self.progressbar.set_values(messages.checking_files, 80)
            file_utils.check_reshade_config_files(self)
            file_utils.check_reshade_executable_file(self)

            self.progressbar.set_values(messages.checking_program_updates, 90)
            self.qtobj.update_button.setVisible(False)
            new_version = program_utils.check_program_updates(self.log, db_session)
            if new_version:
                self.qtobj.updateAvail_label.clear()
                self.qtobj.updateAvail_label.setText(messages.new_version_available_download.format(new_version))
                self.qtobj.update_button.setVisible(True)

            self.progressbar.close()
            self.qtobj.main_tabWidget.setCurrentIndex(0)
            self.qtobj.programs_tableWidget.setColumnWidth(2, 130)
            self.qtobj.programs_tableWidget.horizontalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignLeft)
            self.populate_table_widget()
            self.enable_widgets(False)

    def set_variables(self, rs_config):
        if rs_config:
            self.check_program_updates = rs_config[0]["check_program_updates"]
            self.check_reshade_updates = rs_config[0]["check_reshade_updates"]
            self.create_screenshots_folder = rs_config[0]["create_screenshots_folder"]
            self.show_info_messages = rs_config[0]["show_info_messages"]
            self.use_dark_theme = rs_config[0]["use_dark_theme"]
            self.reshade_version = rs_config[0]["reshade_version"]

        self.qtobj.yes_dark_theme_radioButton.setChecked(self.use_dark_theme)
        self.qtobj.no_dark_theme_radioButton.setChecked(not self.use_dark_theme)
        self.set_style_sheet()

        self.qtobj.yes_check_program_updates_radioButton.setChecked(self.check_program_updates)
        self.qtobj.no_check_program_updates_radioButton.setChecked(not self.check_program_updates)

        self.qtobj.yes_show_info_messages_radioButton.setChecked(self.show_info_messages)
        self.qtobj.no_show_info_messages_radioButton.setChecked(not self.show_info_messages)

        self.qtobj.yes_check_reshade_updates_radioButton.setChecked(self.check_reshade_updates)
        self.qtobj.no_check_reshade_updates_radioButton.setChecked(not self.check_reshade_updates)

        self.qtobj.yes_screenshots_folder_radioButton.setChecked(self.create_screenshots_folder)
        self.qtobj.no_screenshots_folder_radioButton.setChecked(not self.create_screenshots_folder)

    def register_form_events(self):
        # TAB 1 - grid
        self.qtobj.programs_tableWidget.clicked.connect(self._table_widget_clicked)
        self.qtobj.programs_tableWidget.itemDoubleClicked.connect(self._table_widget_double_clicked)

        # TAB 1 - selected games
        self.qtobj.edit_game_button.clicked.connect(self._table_widget_double_clicked)
        self.qtobj.edit_plugin_button.clicked.connect(lambda: events.edit_selected_game_plugin_config_file(self))
        self.qtobj.reset_files_button.clicked.connect(lambda: events.reset_selected_game_files_button(self))
        self.qtobj.edit_path_button.clicked.connect(lambda: events.edit_selected_game_path(self))
        self.qtobj.open_game_path_button.clicked.connect(lambda: events.open_selected_game_location(self))
        self.qtobj.remove_button.clicked.connect(lambda: events.delete_game(self))

        # TAB 1 - all games
        self.qtobj.add_button.clicked.connect(lambda: events.add_game(self))
        self.qtobj.apply_button.clicked.connect(lambda: events.apply_all(self))
        self.qtobj.update_button.clicked.connect(lambda: events.update_program_clicked())

        # TAB 2 - configs
        self.qtobj.yes_dark_theme_radioButton.clicked.connect(lambda: events.dark_theme_clicked(self, "YES"))
        self.qtobj.no_dark_theme_radioButton.clicked.connect(lambda: events.dark_theme_clicked(self, "NO"))

        self.qtobj.yes_check_program_updates_radioButton.clicked.connect(lambda: events.check_program_updates_clicked(self, "YES"))
        self.qtobj.no_check_program_updates_radioButton.clicked.connect(lambda: events.check_program_updates_clicked(self, "NO"))

        self.qtobj.yes_show_info_messages_radioButton.clicked.connect(lambda: events.show_info_messages_clicked(self, "YES"))
        self.qtobj.no_show_info_messages_radioButton.clicked.connect(lambda: events.show_info_messages_clicked(self, "NO"))

        self.qtobj.yes_check_reshade_updates_radioButton.clicked.connect(lambda: events.check_reshade_updates_clicked(self, "YES"))
        self.qtobj.no_check_reshade_updates_radioButton.clicked.connect(lambda: events.check_reshade_updates_clicked(self, "NO"))

        self.qtobj.yes_screenshots_folder_radioButton.clicked.connect(lambda: events.create_screenshots_folder_clicked(self, "YES"))
        self.qtobj.no_screenshots_folder_radioButton.clicked.connect(lambda: events.create_screenshots_folder_clicked(self, "NO"))

        self.qtobj.edit_default_preset_plugin_button.clicked.connect(lambda: events.edit_global_plugins_button(self))
        self.qtobj.update_shaders_button.clicked.connect(lambda: events.update_shaders_button(self))
        self.qtobj.reset_all_button.clicked.connect(lambda: events.reset_all_game_files_button(self))

        # TAB 3 - about
        self.qtobj.donate_button.clicked.connect(lambda: events.donate_clicked())

    def set_style_sheet(self):
        try:
            if self.use_dark_theme:
                self.form.setStyleSheet(open(variables.QSS_PATH, "r").read())
            else:
                self.form.setStyleSheet("")
        except FileNotFoundError:
            self.form.setStyleSheet("")
            events.dark_theme_clicked(self, "NO")
            qt_utils.show_message_window(self.log, "error", messages.error_rss_file_not_found)

    def populate_table_widget(self):
        self.qtobj.programs_tableWidget.horizontalHeader().setStretchLastSection(False)
        self.qtobj.programs_tableWidget.setRowCount(0)  # cleanning datagrid
        games_sql = GamesDal(self.db_session, self.log)
        rs_all_games = games_sql.get_all_games()
        if rs_all_games is not None and len(rs_all_games) > 0:
            for i in range(len(rs_all_games)):
                self.qtobj.programs_tableWidget.insertRow(i)
                self.qtobj.programs_tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(rs_all_games[i]["name"]))
                self.qtobj.programs_tableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem(rs_all_games[i]["architecture"]))
                self.qtobj.programs_tableWidget.setItem(i, 2, QtWidgets.QTableWidgetItem(rs_all_games[i]["api"]))
                self.qtobj.programs_tableWidget.setItem(i, 3, QtWidgets.QTableWidgetItem(rs_all_games[i]["path"]))

        self.qtobj.programs_tableWidget.resizeColumnsToContents()
        highest_column_width = self.qtobj.programs_tableWidget.columnWidth(3)
        if highest_column_width < 600:
            self.qtobj.programs_tableWidget.horizontalHeader().setStretchLastSection(True)
        else:
            self.qtobj.programs_tableWidget.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)

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
        self.qtobj.remove_button.setEnabled(status)
        self.qtobj.reset_files_button.setEnabled(status)
        self.qtobj.edit_plugin_button.setEnabled(status)
        self.qtobj.edit_path_button.setEnabled(status)
        self.qtobj.open_game_path_button.setEnabled(status)
        self.qtobj.main_tabWidget.setCurrentIndex(0)

    def _set_state_apply_button(self):
        len_games = self.qtobj.programs_tableWidget.rowCount()
        status = False if len_games == 0 else True
        self.qtobj.apply_button.setEnabled(status)

    def _table_widget_clicked(self, item):
        events.programs_tableWidget_clicked(self, item)

    def _table_widget_double_clicked(self):
        if self.selected_game is not None:
            qt_utils.show_game_config_form(self, self.selected_game.name, self.selected_game.architecture)

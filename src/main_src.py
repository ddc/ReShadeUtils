# -*- coding: utf-8 -*-
from ddcUtils import FileUtils, TimedRotatingLog
from ddcUtils.databases import DBSqlite
from PyQt6.QtCore import Qt
from src.constants import messages, variables
from src.database.dal.config_dal import ConfigDal
from src.events import about_tab_events, edit_form_events, games_tab_events, settings_tab_events
from src.tools import program_utils, reshade_utils
from src.tools.qt import qt_utils
from src.tools.qt.progressbar import ProgressBar


class MainSrc:
    def __init__(self, qtobj, form):
        self.qtobj = qtobj
        self.form = form
        self.log = TimedRotatingLog(
            directory=variables.LOGS_DIR,
            filename=variables.LOG_FILE_NAME,
            days_to_keep=int(variables.DAYS_TO_KEEP_LOGS),
            level="debug" if variables.DEBUG else "info",
        ).init()

    def start(self):
        self.log.info(f"STARTING {variables.FULL_PROGRAM_NAME}")
        progressbar = ProgressBar(log=self.log)

        database = DBSqlite(variables.DATABASE_PATH)
        with database.session() as db_session:
            self.log.debug("checking for first run")
            config_sql = ConfigDal(db_session, self.log)
            rs_config = config_sql.get_configs()
            alembic_files = FileUtils.list_files(variables.ALEMBIC_MIGRATIONS_DIR)
            if not rs_config or not alembic_files:
                progressbar.set_values(messages.checking_database, 15)
                program_utils.run_alembic_migrations(self.log)
                rs_config = config_sql.get_configs()

            progressbar.set_values(messages.checking_configs, 30)
            self.set_variables(db_session, rs_config)
            self.register_form_events(db_session)
            qt_utils.populate_games_tab(db_session, self.log, self.qtobj)
            self.qtobj.main_tab_widget.setCurrentIndex(0)
            self.qtobj.programs_table_widget.setColumnHidden(0, True)
            self.qtobj.programs_table_widget.horizontalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignLeft)

            progressbar.set_values(messages.checking_reshade_updates, 45)
            if rs_config[0]["check_reshade_updates"]:
                db_reshade_version = tuple(int(x) for x in rs_config[0]["reshade_version"].split("."))
                new_reshade_version = reshade_utils.check_and_download_new_reshade_version(db_session, self.log, self.qtobj, db_reshade_version)
                if new_reshade_version:
                    self.qtobj.reshade_version_label.clear()
                    self.qtobj.reshade_version_label.setText(f"{messages.info_reshade_version} {new_reshade_version}")

            progressbar.set_values(messages.checking_files, 60)
            reshade_utils.check_reshade_config_files(self.log)
            reshade_utils.check_reshade_executable_file(db_session, self.log, self.qtobj)

            progressbar.set_values(messages.checking_program_updates, 75)
            self.qtobj.update_button.setVisible(False)
            new_version = program_utils.check_program_updates(self.log, db_session)
            if new_version:
                progressbar.set_values(messages.checking_database, 90)
                program_utils.run_alembic_migrations(self.log)
                self.qtobj.update_avail_label.clear()
                self.qtobj.update_avail_label.setText(messages.new_version_available_download.format(new_version))
                self.qtobj.update_button.setVisible(True)

            progressbar.close()
            qt_utils.enable_widgets(self.qtobj, False)

    def set_variables(self, db_session, rs_config):
        check_program_updates = rs_config[0]["check_program_updates"] if rs_config else True
        check_reshade_updates = rs_config[0]["check_reshade_updates"] if rs_config else True
        create_screenshots_folder = rs_config[0]["create_screenshots_folder"] if rs_config else True
        show_info_messages = rs_config[0]["show_info_messages"] if rs_config else True
        use_dark_theme = rs_config[0]["use_dark_theme"] if rs_config else False

        self.qtobj.yes_dark_theme_radio_button.setChecked(use_dark_theme)
        self.qtobj.no_dark_theme_radio_button.setChecked(not use_dark_theme)
        qt_utils.set_style_sheet(db_session, self.form, self.log, use_dark_theme)

        self.qtobj.yes_check_program_updates_radio_button.setChecked(check_program_updates)
        self.qtobj.no_check_program_updates_radio_button.setChecked(not check_program_updates)

        self.qtobj.yes_show_info_messages_radio_button.setChecked(show_info_messages)
        self.qtobj.no_show_info_messages_radio_button.setChecked(not show_info_messages)

        self.qtobj.yes_check_reshade_updates_radio_button.setChecked(check_reshade_updates)
        self.qtobj.no_check_reshade_updates_radio_button.setChecked(not check_reshade_updates)

        self.qtobj.yes_screenshots_folder_radio_button.setChecked(create_screenshots_folder)
        self.qtobj.no_screenshots_folder_radio_button.setChecked(not create_screenshots_folder)

    def register_form_events(self, db_session):
        # TAB 1 - edit_form_events
        self.qtobj.programs_table_widget.clicked.connect(lambda item: games_tab_events.game_clicked(db_session, self.log, self.qtobj, item))
        self.qtobj.programs_table_widget.itemDoubleClicked.connect(lambda item: edit_form_events.show_game_config_form_update(db_session, self.log, self.qtobj, item))

        # TAB 1 - selected games
        self.qtobj.edit_game_button.clicked.connect(lambda item: edit_form_events.show_game_config_form_update(db_session, self.log, self.qtobj, item))
        self.qtobj.edit_plugin_button.clicked.connect(lambda item: games_tab_events.edit_selected_game_plugin_config_file(db_session, self.log, self.qtobj, item))
        self.qtobj.reset_files_button.clicked.connect(lambda item: games_tab_events.reset_selected_game_files_button(db_session, self.log, self.qtobj, item))
        self.qtobj.edit_path_button.clicked.connect(lambda item: games_tab_events.edit_selected_game_path(db_session, self.log, self.qtobj, item))
        self.qtobj.open_game_path_button.clicked.connect(lambda item: games_tab_events.open_selected_game_location(db_session, self.log, self.qtobj, item))
        self.qtobj.remove_button.clicked.connect(lambda item: games_tab_events.delete_game(db_session, self.log, self.qtobj, item))

        # TAB 1 - all games
        self.qtobj.add_button.clicked.connect(lambda: games_tab_events.add_game(db_session, self.log, self.qtobj))
        self.qtobj.apply_button.clicked.connect(lambda: games_tab_events.apply_all_clicked(db_session, self.log, self.qtobj))
        self.qtobj.update_button.clicked.connect(lambda: games_tab_events.update_program_clicked())

        # TAB 2 - settings
        self.qtobj.yes_dark_theme_radio_button.clicked.connect(lambda: settings_tab_events.dark_theme_clicked(db_session, self.form, self.log, True))
        self.qtobj.no_dark_theme_radio_button.clicked.connect(lambda: settings_tab_events.dark_theme_clicked(db_session, self.form, self.log, False))

        self.qtobj.yes_check_program_updates_radio_button.clicked.connect(lambda: settings_tab_events.check_program_updates_clicked(db_session, self.log, True))
        self.qtobj.no_check_program_updates_radio_button.clicked.connect(lambda: settings_tab_events.check_program_updates_clicked(db_session, self.log, False))

        self.qtobj.yes_show_info_messages_radio_button.clicked.connect(lambda: settings_tab_events.show_info_messages_clicked(db_session, self.log, True))
        self.qtobj.no_show_info_messages_radio_button.clicked.connect(lambda: settings_tab_events.show_info_messages_clicked(db_session, self.log, False))

        self.qtobj.yes_check_reshade_updates_radio_button.clicked.connect(lambda: settings_tab_events.check_reshade_updates_clicked(db_session, self.log, True))
        self.qtobj.no_check_reshade_updates_radio_button.clicked.connect(lambda: settings_tab_events.check_reshade_updates_clicked(db_session, self.log, False))

        self.qtobj.yes_screenshots_folder_radio_button.clicked.connect(lambda: settings_tab_events.create_screenshots_folder_clicked(db_session, self.log, True))
        self.qtobj.no_screenshots_folder_radio_button.clicked.connect(lambda: settings_tab_events.create_screenshots_folder_clicked(db_session, self.log, False))

        self.qtobj.edit_global_plugins_button.clicked.connect(lambda: settings_tab_events.edit_global_plugins_button(self.log))
        self.qtobj.update_shaders_button.clicked.connect(lambda: settings_tab_events.update_shaders_button(self.log))
        self.qtobj.reset_all_button.clicked.connect(lambda: settings_tab_events.reset_all_game_files_button(db_session, self.log, self.qtobj))

        # TAB 3 - about
        self.qtobj.donate_button.clicked.connect(lambda: about_tab_events.donate_clicked())

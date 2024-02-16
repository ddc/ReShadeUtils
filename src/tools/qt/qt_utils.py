# -*- coding: utf-8 -*-
import os
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QFileDialog
from src import events
from src.constants import messages, variables
from src.database.dal.games_dal import GamesDal


def open_exe_file_dialog():
    qfd = QFileDialog()
    title = "Open file"
    path = "C:"
    _filter = "exe(*.exe)"
    filepath, _ = QFileDialog.getOpenFileName(parent=qfd, caption=title, directory=path, filter=_filter)
    return None if filepath == "" else os.path.normpath(filepath)


def show_message_window(log, window_type, msg):
    msg_box = QtWidgets.QMessageBox()

    match window_type.lower():
        case "error":
            icon = QtWidgets.QMessageBox.Icon.Critical
            button = QtWidgets.QMessageBox.StandardButton.Ok
            log.error(msg.replace("\n", ":")) if log else None
        case "warning":
            icon = QtWidgets.QMessageBox.Icon.Warning
            button = QtWidgets.QMessageBox.StandardButton.Ok
            log.warning(msg.replace("\n", ":")) if log else None
        case "info":
            icon = QtWidgets.QMessageBox.Icon.Information
            button = QtWidgets.QMessageBox.StandardButton.Ok
            log.info(msg.replace("\n", ":")) if log else None
        case _:
            icon = QtWidgets.QMessageBox.Icon.Question
            button = QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No
            msg_box.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Yes)

    msg_box.setWindowTitle(variables.FULL_PROGRAM_NAME)
    msg_box.setIcon(icon)
    msg_box.setText(msg)
    msg_box.setStandardButtons(button)

    user_answer = msg_box.exec()
    return user_answer


def set_style_sheet(db_session, form, log, use_dark_theme):
    try:
        if use_dark_theme:
            form.setStyleSheet(open(variables.QSS_PATH, "r").read())
        else:
            form.setStyleSheet("")
    except FileNotFoundError:
        form.setStyleSheet("")
        events.dark_theme_clicked(db_session, log, "NO")
        show_message_window(log, "error", messages.error_rss_file_not_found)


def populate_games_tab(db_session, log, qtobj):
    qtobj.programs_table_widget.horizontalHeader().setStretchLastSection(False)
    qtobj.programs_table_widget.setRowCount(0)  # cleanning datagrid
    games_sql = GamesDal(db_session, log)
    rs_all_games = games_sql.get_all_games()
    if rs_all_games is not None and len(rs_all_games) > 0:
        for i in range(len(rs_all_games)):
            qtobj.programs_table_widget.insertRow(i)
            qtobj.programs_table_widget.setItem(i, 0, QtWidgets.QTableWidgetItem(rs_all_games[i]["name"]))
            qtobj.programs_table_widget.setItem(i, 1, QtWidgets.QTableWidgetItem(rs_all_games[i]["architecture"]))
            qtobj.programs_table_widget.setItem(i, 2, QtWidgets.QTableWidgetItem(rs_all_games[i]["api"]))
            qtobj.programs_table_widget.setItem(i, 3, QtWidgets.QTableWidgetItem(rs_all_games[i]["dll"]))
            qtobj.programs_table_widget.setItem(i, 4, QtWidgets.QTableWidgetItem(rs_all_games[i]["path"]))

    qtobj.programs_table_widget.resizeColumnsToContents()
    highest_column_width = qtobj.programs_table_widget.columnWidth(3)
    if highest_column_width < 600:
        qtobj.programs_table_widget.horizontalHeader().setStretchLastSection(True)
    else:
        qtobj.programs_table_widget.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)


def enable_form(qtobj, status: bool):
    qtobj.add_button.setEnabled(status)
    for i in range(0, qtobj.main_tab_widget.count()):
        qtobj.main_tab_widget.setTabEnabled(i, status)
    qtobj.main_tab_widget.setCurrentIndex(0)


def enable_widgets(qtobj, status: bool):
    _set_state_apply_button(qtobj)
    qtobj.edit_game_button.setEnabled(status)
    qtobj.edit_plugin_button.setEnabled(status)
    qtobj.reset_files_button.setEnabled(status)
    qtobj.edit_path_button.setEnabled(status)
    qtobj.open_game_path_button.setEnabled(status)
    qtobj.remove_button.setEnabled(status)
    qtobj.main_tab_widget.setCurrentIndex(0)


def _set_state_apply_button(qtobj):
    len_games = qtobj.programs_table_widget.rowCount()
    status = False if len_games == 0 else True
    qtobj.apply_button.setEnabled(status)

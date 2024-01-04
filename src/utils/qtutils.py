# -*- coding: utf-8 -*-
import os
from PyQt6 import QtWidgets
from src.config import Ui_config
from PyQt6.QtWidgets import QFileDialog
from src import constants, events, messages, utils


def open_exe_file_dialog():
    qfd = QFileDialog()
    title = "Open file"
    path = "C:"
    _filter = "exe(*.exe)"
    filepath, _ = QFileDialog.getOpenFileName(parent=qfd,
                                              caption=title,
                                              directory=path,
                                              filter=_filter)
    if filepath == "":
        return None
    else:
        return os.path.normpath(filepath)


def show_message_window(log, window_type, msg):
    msg_box = QtWidgets.QMessageBox()

    if window_type.lower() == "error":
        icon = QtWidgets.QMessageBox.Icon.Critical
        button = QtWidgets.QMessageBox.StandardButton.Ok
        log.error(msg.replace("\n", ":")) if log else None
    elif window_type.lower() == "warning":
        icon = QtWidgets.QMessageBox.Icon.Warning
        button = QtWidgets.QMessageBox.StandardButton.Ok
        log.warning(msg.replace("\n", ":")) if log else None
    elif window_type.lower() == "info":
        icon = QtWidgets.QMessageBox.Icon.Information
        button = QtWidgets.QMessageBox.StandardButton.Ok
        log.info(msg.replace("\n", ":")) if log else None
    else:
        icon = QtWidgets.QMessageBox.Icon.Question
        button = QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No
        msg_box.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Yes)

    msg_box.setWindowTitle(constants.FULL_PROGRAM_NAME)
    msg_box.setIcon(icon)
    msg_box.setText(msg)
    msg_box.setStandardButtons(button)

    user_answer = msg_box.exec()
    return user_answer


def show_game_config_form(self, game_name, architecture):
    if not utils.check_game_file(self):
        show_message_window(self.log, "error", messages.error_game_not_found)
        return

    self.game_config_form = QtWidgets.QWidget()
    qt_obj = Ui_config()
    qt_obj.setupUi(self.game_config_form)
    self.game_config_form.qtObj = qt_obj

    if self.use_dark_theme:
        self.game_config_form.setStyleSheet(
            open(constants.QSS_PATH, "r").read()
        )

    self.game_config_form.qtObj.game_name_lineEdit.setFocus()
    self.game_config_form.show()
    QtWidgets.QApplication.processEvents()

    self.game_config_form.qtObj.ok_pushButton.clicked.connect(
        lambda: events.game_config_form_result(self, architecture, "OK"))
    self.game_config_form.qtObj.cancel_pushButton.clicked.connect(
        lambda: events.game_config_form_result(self, architecture, "CANCEL"))

    if self.selected_game is not None:
        self.game_config_form.qtObj.game_name_lineEdit.setText(
            self.selected_game.name
        )
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

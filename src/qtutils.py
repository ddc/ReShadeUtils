# |*****************************************************
# * Copyright         : Copyright (C) 2019
# * Author            : ddc
# * License           : GPL v3
# |*****************************************************
# # -*- coding: utf-8 -*-

import os
from src import constants
from PyQt5.QtWidgets import QFileDialog
from PyQt5 import QtWidgets


def open_qt_file_dialog():
    qfd = QFileDialog()
    title = "Open file"
    path = "C:"
    _filter = "exe(*.exe)"
    filepath, extension = QFileDialog.getOpenFileName(parent=qfd, caption=title, directory=path, filter=_filter)
    if filepath == "":
        return None
    else:
        return os.path.normpath(filepath)


def show_message_window(log, window_type, msg):
    msg_box = QtWidgets.QMessageBox()

    if window_type.lower() == "error":
        icon = QtWidgets.QMessageBox.Icon.Critical
        button = QtWidgets.QMessageBox.Ok
        log.error(msg.replace("\n", ":")) if log else None
    elif window_type.lower() == "warning":
        icon = QtWidgets.QMessageBox.Icon.Warning
        button = QtWidgets.QMessageBox.Ok
        log.warning(msg.replace("\n", ":")) if log else None
    elif window_type.lower() == "info":
        icon = QtWidgets.QMessageBox.Icon.Information
        button = QtWidgets.QMessageBox.Ok
        log.info(msg.replace("\n", ":")) if log else None
    else:
        icon = QtWidgets.QMessageBox.Icon.Question
        button = QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        msg_box.setDefaultButton(QtWidgets.QMessageBox.Yes)

    msg_box.setWindowTitle(constants.FULL_PROGRAM_NAME)
    msg_box.setIcon(icon)
    msg_box.setText(msg)
    msg_box.setStandardButtons(button)

    user_answer = msg_box.exec()
    return user_answer

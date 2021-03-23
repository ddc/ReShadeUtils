#! /usr/bin/env python3
# |*****************************************************
# * Copyright         : Copyright (C) 2019
# * Author            : ddc
# * License           : GPL v3
# |*****************************************************
# # -*- coding: utf-8 -*-

import os
from src import utils
from PyQt6.QtWidgets import QFileDialog
from PyQt6 import QtCore, QtGui, QtWidgets


class ProgressBar:
    def __init__(self):
        _width = 350
        _height = 25
        self.progressBar = QtWidgets.QProgressBar()
        self.progressBar.setObjectName("progressBar")
        self.progressBar.setMinimumSize(QtCore.QSize(_width, _height))
        self.progressBar.setMaximumSize(QtCore.QSize(_width, _height))
        self.progressBar.setSizeIncrement(QtCore.QSize(_width, _height))
        self.progressBar.setBaseSize(QtCore.QSize(_width, _height))
        # self.progressBar.setGeometry(QtCore.QRect(960, 540, width, height))
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(100)
        self.progressBar.setWindowFlags(QtCore.Qt.WindowFlags.FramelessWindowHint)
        self.progressBar.setAlignment(QtCore.Qt.Alignment.AlignCenter)

    def set_values(self, message="", value=0):
        _translate = QtCore.QCoreApplication.translate
        self.progressBar.setFormat(_translate("Main", f"{message}  %p%"))
        self.progressBar.show()
        QtWidgets.QApplication.processEvents()
        self.progressBar.setValue(value)
        if value == 100:
            self.progressBar.close()

    def close(self):
        self.progressBar.close()


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


def show_message_window(window_type: str, window_title: str, msg: str):
    if window_type.lower() == "error":
        icon = QtWidgets.QMessageBox.Icon.Critical
    elif window_type.lower() == "warning":
        icon = QtWidgets.QMessageBox.Icon.Warning
    elif window_type.lower() == "question":
        icon = QtWidgets.QMessageBox.Icon.Question
    else:
        icon = QtWidgets.QMessageBox.Icon.Information

    msg_box = QtWidgets.QMessageBox()
    msg_box.setIcon(icon)
    msg_box.setWindowTitle(window_title)
    msg_box.setInformativeText(msg)

    if window_type.lower() == "question":
        msg_box.setStandardButtons(QtWidgets.QMessageBox.StandardButtons.Yes | QtWidgets.QMessageBox.StandardButtons.No)
        msg_box.setDefaultButton(QtWidgets.QMessageBox.StandardButtons.Yes)
    else:
        msg_box.setStandardButtons(QtWidgets.QMessageBox.StandardButtons.Ok)
        msg_box.setDefaultButton(QtWidgets.QMessageBox.StandardButtons.Ok)

    user_answer = msg_box.exec()
    return user_answer


def set_icons(self):
    icon_add = QtGui.QIcon()
    icon_add_pixmap = QtGui.QPixmap(utils.resource_path("images/add.png"))
    icon_add.addPixmap(icon_add_pixmap, QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)

    icon_arrow = QtGui.QIcon()
    icon_arrow_pixmap = QtGui.QPixmap(utils.resource_path("images/arrow.png"))
    icon_arrow.addPixmap(icon_arrow_pixmap, QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)

    icon_delete = QtGui.QIcon()
    icon_delete_pixmap = QtGui.QPixmap(utils.resource_path("images/delete.png"))
    icon_delete.addPixmap(icon_delete_pixmap, QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)

    icon_apply = QtGui.QIcon()
    icon_apply_pixmap = QtGui.QPixmap(utils.resource_path("images/apply.png"))
    icon_apply.addPixmap(icon_apply_pixmap, QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)

    icon_edit = QtGui.QIcon()
    icon_edit_pixmap = QtGui.QPixmap(utils.resource_path("images/edit.png"))
    icon_edit.addPixmap(icon_edit_pixmap, QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)

    icon_controller = QtGui.QIcon()
    icon_controller_pixmap = QtGui.QPixmap(utils.resource_path("images/controller.png"))
    icon_controller.addPixmap(icon_controller_pixmap, QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)

    icon_plugin = QtGui.QIcon()
    icon_plugin_pixmap = QtGui.QPixmap(utils.resource_path("images/plugin.png"))
    icon_plugin.addPixmap(icon_plugin_pixmap, QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)

    icon_gear = QtGui.QIcon()
    icon_gear_pixmap = QtGui.QPixmap(utils.resource_path("images/gear.png"))
    icon_gear.addPixmap(icon_gear_pixmap, QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)

    icon_paypal = QtGui.QIcon()
    icon_paypal_pixmap = QtGui.QPixmap(utils.resource_path("images/paypal.png"))
    icon_paypal.addPixmap(icon_paypal_pixmap, QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)

    icon_help = QtGui.QIcon()
    icon_help_pixmap = QtGui.QPixmap(utils.resource_path("images/help.png"))
    icon_help.addPixmap(icon_help_pixmap, QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)

    icon_update = QtGui.QIcon()
    icon_update_pixmap = QtGui.QPixmap(utils.resource_path("images/update.png"))
    icon_update.addPixmap(icon_update_pixmap, QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)

    self.qtobj.add_button.setIcon(icon_add)
    self.qtobj.edit_path_button.setIcon(icon_arrow)
    self.qtobj.delete_button.setIcon(icon_delete)
    self.qtobj.apply_button.setIcon(icon_apply)
    self.qtobj.apply_all_games_custom_config_button.setIcon(icon_apply)
    self.qtobj.edit_config_button.setIcon(icon_edit)
    self.qtobj.main_tabWidget.addTab(self.qtobj.games_tab, icon_controller, "GAMES")
    self.qtobj.edit_all_games_custom_config_button.setIcon(icon_plugin)
    self.qtobj.main_tabWidget.addTab(self.qtobj.settings_tab, icon_gear, "SETTINGS")
    self.qtobj.paypal_button.setIcon(icon_paypal)
    self.qtobj.main_tabWidget.addTab(self.qtobj.about_tab, icon_help, "ABOUT")
    self.qtobj.update_button.setIcon(icon_update)

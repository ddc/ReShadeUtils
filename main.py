#! /usr/bin/env python3
# |*****************************************************
# * Copyright         : Copyright (C) 2019
# * Author            : ddc
# * License           : GPL v3
# * Python            : 3.6
# |*****************************************************
# # -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets

from src.main_src import MainSrc
from src.utils import constants


class Ui_Main(object):
    def setupUi(self, Main):
        Main.setObjectName("Main")
        Main.resize(950, 700)
        Main.setMinimumSize(QtCore.QSize(950, 700))
        Main.setMaximumSize(QtCore.QSize(950, 700))
        Main.setSizeIncrement(QtCore.QSize(950, 700))
        Main.setBaseSize(QtCore.QSize(950, 700))
        self.reshade_version_label = QtWidgets.QLabel(Main)
        self.reshade_version_label.setGeometry(QtCore.QRect(380, 10, 191, 20))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.reshade_version_label.setFont(font)
        self.reshade_version_label.setText("")
        self.reshade_version_label.setAlignment(QtCore.Qt.AlignCenter)
        self.reshade_version_label.setObjectName("reshade_version_label")
        self.main_tabWidget = QtWidgets.QTabWidget(Main)
        self.main_tabWidget.setGeometry(QtCore.QRect(20, 40, 911, 611))
        self.main_tabWidget.setUsesScrollButtons(False)
        self.main_tabWidget.setObjectName("main_tabWidget")
        self.games_tab = QtWidgets.QWidget()
        self.games_tab.setObjectName("games_tab")
        self.architecture_groupBox = QtWidgets.QGroupBox(self.games_tab)
        self.architecture_groupBox.setGeometry(QtCore.QRect(550, 470, 90, 100))
        self.architecture_groupBox.setObjectName("architecture_groupBox")
        self.radioButton_32bits = QtWidgets.QRadioButton(self.architecture_groupBox)
        self.radioButton_32bits.setGeometry(QtCore.QRect(10, 30, 70, 20))
        self.radioButton_32bits.setObjectName("radioButton_32bits")
        self.radioButton_64bits = QtWidgets.QRadioButton(self.architecture_groupBox)
        self.radioButton_64bits.setGeometry(QtCore.QRect(10, 70, 70, 20))
        self.radioButton_64bits.setObjectName("radioButton_64bits")
        self.api_groupBox = QtWidgets.QGroupBox(self.games_tab)
        self.api_groupBox.setGeometry(QtCore.QRect(660, 470, 90, 100))
        self.api_groupBox.setObjectName("api_groupBox")
        self.dx9_radioButton = QtWidgets.QRadioButton(self.api_groupBox)
        self.dx9_radioButton.setGeometry(QtCore.QRect(10, 30, 70, 20))
        self.dx9_radioButton.setObjectName("dx9_radioButton")
        self.dx11_radioButton = QtWidgets.QRadioButton(self.api_groupBox)
        self.dx11_radioButton.setGeometry(QtCore.QRect(10, 70, 70, 20))
        self.dx11_radioButton.setObjectName("dx11_radioButton")
        self.add_button = QtWidgets.QPushButton(self.games_tab)
        self.add_button.setGeometry(QtCore.QRect(20, 510, 120, 30))
        self.add_button.setMinimumSize(QtCore.QSize(120, 30))
        self.add_button.setMaximumSize(QtCore.QSize(120, 30))
        self.add_button.setObjectName("add_button")
        self.edit_path_button = QtWidgets.QPushButton(self.games_tab)
        self.edit_path_button.setGeometry(QtCore.QRect(280, 510, 120, 30))
        self.edit_path_button.setMinimumSize(QtCore.QSize(120, 30))
        self.edit_path_button.setMaximumSize(QtCore.QSize(120, 30))
        self.edit_path_button.setObjectName("edit_path_button")
        self.delete_button = QtWidgets.QPushButton(self.games_tab)
        self.delete_button.setGeometry(QtCore.QRect(150, 510, 120, 30))
        self.delete_button.setMinimumSize(QtCore.QSize(120, 30))
        self.delete_button.setMaximumSize(QtCore.QSize(120, 30))
        self.delete_button.setObjectName("delete_button")
        self.apply_button = QtWidgets.QPushButton(self.games_tab)
        self.apply_button.setGeometry(QtCore.QRect(770, 470, 120, 100))
        self.apply_button.setMinimumSize(QtCore.QSize(120, 100))
        self.apply_button.setMaximumSize(QtCore.QSize(120, 100))
        self.apply_button.setObjectName("apply_button")
        self.programs_tableWidget = QtWidgets.QTableWidget(self.games_tab)
        self.programs_tableWidget.setGeometry(QtCore.QRect(0, 0, 901, 461))
        self.programs_tableWidget.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.programs_tableWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.programs_tableWidget.setAutoScroll(False)
        self.programs_tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.programs_tableWidget.setDragDropOverwriteMode(False)
        self.programs_tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.programs_tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.programs_tableWidget.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.programs_tableWidget.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.programs_tableWidget.setWordWrap(False)
        self.programs_tableWidget.setColumnCount(2)
        self.programs_tableWidget.setObjectName("programs_tableWidget")
        self.programs_tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.programs_tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.programs_tableWidget.setHorizontalHeaderItem(1, item)
        self.programs_tableWidget.horizontalHeader().setVisible(True)
        self.programs_tableWidget.horizontalHeader().setDefaultSectionSize(150)
        self.programs_tableWidget.horizontalHeader().setHighlightSections(False)
        self.programs_tableWidget.horizontalHeader().setMinimumSectionSize(100)
        self.programs_tableWidget.horizontalHeader().setStretchLastSection(True)
        self.programs_tableWidget.verticalHeader().setVisible(True)
        self.programs_tableWidget.verticalHeader().setDefaultSectionSize(30)
        self.programs_tableWidget.verticalHeader().setMinimumSectionSize(30)
        self.edit_config_button = QtWidgets.QPushButton(self.games_tab)
        self.edit_config_button.setGeometry(QtCore.QRect(410, 510, 120, 30))
        self.edit_config_button.setMinimumSize(QtCore.QSize(120, 30))
        self.edit_config_button.setMaximumSize(QtCore.QSize(120, 30))
        self.edit_config_button.setObjectName("edit_config_button")
        self.main_tabWidget.addTab(self.games_tab, "")
        self.configs_tab = QtWidgets.QWidget()
        self.configs_tab.setObjectName("configs_tab")
        self.update_shaders_groupBox = QtWidgets.QGroupBox(self.configs_tab)
        self.update_shaders_groupBox.setGeometry(QtCore.QRect(210, 300, 175, 60))
        self.update_shaders_groupBox.setObjectName("update_shaders_groupBox")
        self.yes_update_shaders_radioButton = QtWidgets.QRadioButton(self.update_shaders_groupBox)
        self.yes_update_shaders_radioButton.setGeometry(QtCore.QRect(10, 30, 50, 20))
        self.yes_update_shaders_radioButton.setObjectName("yes_update_shaders_radioButton")
        self.no_update_shaders_radioButton = QtWidgets.QRadioButton(self.update_shaders_groupBox)
        self.no_update_shaders_radioButton.setGeometry(QtCore.QRect(120, 30, 50, 20))
        self.no_update_shaders_radioButton.setObjectName("no_update_shaders_radioButton")
        self.check_program_updates_groupBox = QtWidgets.QGroupBox(self.configs_tab)
        self.check_program_updates_groupBox.setGeometry(QtCore.QRect(520, 180, 175, 60))
        self.check_program_updates_groupBox.setObjectName("check_program_updates_groupBox")
        self.yes_check_program_updates_radioButton = QtWidgets.QRadioButton(self.check_program_updates_groupBox)
        self.yes_check_program_updates_radioButton.setGeometry(QtCore.QRect(10, 30, 50, 20))
        self.yes_check_program_updates_radioButton.setObjectName("yes_check_program_updates_radioButton")
        self.no_check_program_updates_radioButton = QtWidgets.QRadioButton(self.check_program_updates_groupBox)
        self.no_check_program_updates_radioButton.setGeometry(QtCore.QRect(120, 30, 50, 20))
        self.no_check_program_updates_radioButton.setObjectName("no_check_program_updates_radioButton")
        self.use_dark_theme_groupBox = QtWidgets.QGroupBox(self.configs_tab)
        self.use_dark_theme_groupBox.setGeometry(QtCore.QRect(360, 90, 175, 60))
        self.use_dark_theme_groupBox.setObjectName("use_dark_theme_groupBox")
        self.yes_dark_theme_radioButton = QtWidgets.QRadioButton(self.use_dark_theme_groupBox)
        self.yes_dark_theme_radioButton.setGeometry(QtCore.QRect(10, 30, 50, 20))
        self.yes_dark_theme_radioButton.setObjectName("yes_dark_theme_radioButton")
        self.no_dark_theme_radioButton = QtWidgets.QRadioButton(self.use_dark_theme_groupBox)
        self.no_dark_theme_radioButton.setGeometry(QtCore.QRect(120, 30, 50, 20))
        self.no_dark_theme_radioButton.setObjectName("no_dark_theme_radioButton")
        self.create_screenshots_folder_groupBox = QtWidgets.QGroupBox(self.configs_tab)
        self.create_screenshots_folder_groupBox.setGeometry(QtCore.QRect(520, 300, 175, 60))
        self.create_screenshots_folder_groupBox.setObjectName("create_screenshots_folder_groupBox")
        self.yes_screenshots_folder_radioButton = QtWidgets.QRadioButton(self.create_screenshots_folder_groupBox)
        self.yes_screenshots_folder_radioButton.setGeometry(QtCore.QRect(10, 30, 50, 20))
        self.yes_screenshots_folder_radioButton.setObjectName("yes_screenshots_folder_radioButton")
        self.no_screenshots_folder_radioButton = QtWidgets.QRadioButton(self.create_screenshots_folder_groupBox)
        self.no_screenshots_folder_radioButton.setGeometry(QtCore.QRect(120, 30, 50, 20))
        self.no_screenshots_folder_radioButton.setObjectName("no_screenshots_folder_radioButton")
        self.reset_all_reshade_config_groupBox = QtWidgets.QGroupBox(self.configs_tab)
        self.reset_all_reshade_config_groupBox.setGeometry(QtCore.QRect(350, 380, 210, 60))
        self.reset_all_reshade_config_groupBox.setObjectName("reset_all_reshade_config_groupBox")
        self.yes_reset_reshade_radioButton = QtWidgets.QRadioButton(self.reset_all_reshade_config_groupBox)
        self.yes_reset_reshade_radioButton.setGeometry(QtCore.QRect(10, 30, 50, 20))
        self.yes_reset_reshade_radioButton.setObjectName("yes_reset_reshade_radioButton")
        self.no_reset_reshade_radioButton = QtWidgets.QRadioButton(self.reset_all_reshade_config_groupBox)
        self.no_reset_reshade_radioButton.setGeometry(QtCore.QRect(150, 30, 50, 20))
        self.no_reset_reshade_radioButton.setObjectName("no_reset_reshade_radioButton")
        self.check_reshade_updates_groupBox = QtWidgets.QGroupBox(self.configs_tab)
        self.check_reshade_updates_groupBox.setGeometry(QtCore.QRect(210, 180, 175, 60))
        self.check_reshade_updates_groupBox.setObjectName("check_reshade_updates_groupBox")
        self.yes_check_reshade_updates_radioButton = QtWidgets.QRadioButton(self.check_reshade_updates_groupBox)
        self.yes_check_reshade_updates_radioButton.setGeometry(QtCore.QRect(10, 30, 50, 20))
        self.yes_check_reshade_updates_radioButton.setObjectName("yes_check_reshade_updates_radioButton")
        self.no_check_reshade_updates_radioButton = QtWidgets.QRadioButton(self.check_reshade_updates_groupBox)
        self.no_check_reshade_updates_radioButton.setGeometry(QtCore.QRect(120, 30, 50, 20))
        self.no_check_reshade_updates_radioButton.setObjectName("no_check_reshade_updates_radioButton")
        self.edit_default_config_button = QtWidgets.QPushButton(self.configs_tab)
        self.edit_default_config_button.setGeometry(QtCore.QRect(380, 450, 150, 30))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edit_default_config_button.sizePolicy().hasHeightForWidth())
        self.edit_default_config_button.setSizePolicy(sizePolicy)
        self.edit_default_config_button.setMinimumSize(QtCore.QSize(150, 30))
        self.edit_default_config_button.setMaximumSize(QtCore.QSize(150, 30))
        self.edit_default_config_button.setObjectName("edit_default_config_button")
        self.silent_reshade_updates_groupBox = QtWidgets.QGroupBox(self.configs_tab)
        self.silent_reshade_updates_groupBox.setGeometry(QtCore.QRect(210, 240, 175, 45))
        self.silent_reshade_updates_groupBox.setObjectName("silent_reshade_updates_groupBox")
        self.yes_silent_reshade_updates_radioButton = QtWidgets.QRadioButton(self.silent_reshade_updates_groupBox)
        self.yes_silent_reshade_updates_radioButton.setGeometry(QtCore.QRect(10, 20, 50, 18))
        self.yes_silent_reshade_updates_radioButton.setObjectName("yes_silent_reshade_updates_radioButton")
        self.no_silent_reshade_updates_radioButton = QtWidgets.QRadioButton(self.silent_reshade_updates_groupBox)
        self.no_silent_reshade_updates_radioButton.setGeometry(QtCore.QRect(120, 20, 45, 18))
        self.no_silent_reshade_updates_radioButton.setObjectName("no_silent_reshade_updates_radioButton")
        self.main_tabWidget.addTab(self.configs_tab, "")
        self.about_tab = QtWidgets.QWidget()
        self.about_tab.setObjectName("about_tab")
        self.about_textBrowser = QtWidgets.QTextBrowser(self.about_tab)
        self.about_textBrowser.setGeometry(QtCore.QRect(0, 0, 921, 581))
        self.about_textBrowser.setAcceptDrops(False)
        self.about_textBrowser.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.about_textBrowser.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.about_textBrowser.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.about_textBrowser.setUndoRedoEnabled(False)
        self.about_textBrowser.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse)
        self.about_textBrowser.setOpenExternalLinks(True)
        self.about_textBrowser.setObjectName("about_textBrowser")
        self.paypal_button = QtWidgets.QPushButton(self.about_tab)
        self.paypal_button.setGeometry(QtCore.QRect(420, 435, 80, 30))
        self.paypal_button.setMinimumSize(QtCore.QSize(80, 30))
        self.paypal_button.setMaximumSize(QtCore.QSize(80, 30))
        self.paypal_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.paypal_button.setToolTip("")
        self.paypal_button.setAutoFillBackground(False)
        self.paypal_button.setStyleSheet("#paypal_button {\n"
"    background-color: transparent;\n"
"    background: none;\n"
"    border: none;\n"
"    background-repeat: none;\n"
"}")
        self.paypal_button.setIconSize(QtCore.QSize(100, 100))
        self.paypal_button.setObjectName("paypal_button")
        self.main_tabWidget.addTab(self.about_tab, "")
        self.updateAvail_label = QtWidgets.QLabel(Main)
        self.updateAvail_label.setGeometry(QtCore.QRect(30, 655, 741, 40))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.updateAvail_label.setFont(font)
        self.updateAvail_label.setText("")
        self.updateAvail_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.updateAvail_label.setObjectName("updateAvail_label")
        self.update_button = QtWidgets.QPushButton(Main)
        self.update_button.setGeometry(QtCore.QRect(790, 660, 120, 30))
        self.update_button.setMinimumSize(QtCore.QSize(120, 30))
        self.update_button.setMaximumSize(QtCore.QSize(120, 30))
        self.update_button.setObjectName("update_button")

        self.retranslateUi(Main)
        self.main_tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Main)

        mainSrc = MainSrc(self, Main)
        mainSrc.init()

    def retranslateUi(self, Main):
        _translate = QtCore.QCoreApplication.translate
        Main.setWindowTitle(_translate("Main", constants.FULL_PROGRAM_NAME))
        self.architecture_groupBox.setTitle(_translate("Main", "Architecture"))
        self.radioButton_32bits.setText(_translate("Main", "32bits"))
        self.radioButton_64bits.setText(_translate("Main", "64bits"))
        self.api_groupBox.setTitle(_translate("Main", "API"))
        self.dx9_radioButton.setText(_translate("Main", "DX9"))
        self.dx11_radioButton.setText(_translate("Main", "DX11"))
        self.add_button.setToolTip(_translate("Main", "Click to add a game"))
        self.add_button.setText(_translate("Main", "ADD"))
        self.edit_path_button.setToolTip(_translate("Main", "Click to edit the game path"))
        self.edit_path_button.setText(_translate("Main", "EDIT PATH"))
        self.delete_button.setToolTip(_translate("Main", "Click to delete the selected game"))
        self.delete_button.setText(_translate("Main", "DELETE"))
        self.apply_button.setToolTip(_translate("Main", "APPLY"))
        self.apply_button.setText(_translate("Main", "APPLY"))
        self.programs_tableWidget.setSortingEnabled(True)
        item = self.programs_tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Main", "Name"))
        item = self.programs_tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Main", "Path"))
        self.edit_config_button.setToolTip(_translate("Main", "Click to edit the game path"))
        self.edit_config_button.setText(_translate("Main", "EDIT CONFIG"))
        self.main_tabWidget.setTabText(self.main_tabWidget.indexOf(self.games_tab), _translate("Main", "Games"))
        self.update_shaders_groupBox.setTitle(_translate("Main", "Update Shader Files"))
        self.yes_update_shaders_radioButton.setText(_translate("Main", "YES"))
        self.no_update_shaders_radioButton.setText(_translate("Main", "NO"))
        self.check_program_updates_groupBox.setTitle(_translate("Main", "Check for Program Updates"))
        self.yes_check_program_updates_radioButton.setText(_translate("Main", "YES"))
        self.no_check_program_updates_radioButton.setText(_translate("Main", "NO"))
        self.use_dark_theme_groupBox.setTitle(_translate("Main", "Use Dark Theme"))
        self.yes_dark_theme_radioButton.setText(_translate("Main", "YES"))
        self.no_dark_theme_radioButton.setText(_translate("Main", "NO"))
        self.create_screenshots_folder_groupBox.setTitle(_translate("Main", "Create Screenshot Folders"))
        self.yes_screenshots_folder_radioButton.setText(_translate("Main", "YES"))
        self.no_screenshots_folder_radioButton.setText(_translate("Main", "NO"))
        self.reset_all_reshade_config_groupBox.setTitle(_translate("Main", "Reset All Reshade Config Files"))
        self.yes_reset_reshade_radioButton.setText(_translate("Main", "YES"))
        self.no_reset_reshade_radioButton.setText(_translate("Main", "NO"))
        self.check_reshade_updates_groupBox.setTitle(_translate("Main", "Check for Reshade Updates"))
        self.yes_check_reshade_updates_radioButton.setText(_translate("Main", "YES"))
        self.no_check_reshade_updates_radioButton.setText(_translate("Main", "NO"))
        self.edit_default_config_button.setToolTip(_translate("Main", "Click to edit the game path"))
        self.edit_default_config_button.setText(_translate("Main", "EDIT DEFAULT CONFIGS"))
        self.silent_reshade_updates_groupBox.setTitle(_translate("Main", "Silent update on startup"))
        self.yes_silent_reshade_updates_radioButton.setText(_translate("Main", "YES"))
        self.no_silent_reshade_updates_radioButton.setText(_translate("Main", "NO"))
        self.main_tabWidget.setTabText(self.main_tabWidget.indexOf(self.configs_tab), _translate("Main", "Configs"))
        self.about_textBrowser.setHtml(_translate("Main", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:12pt; font-weight:600;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600;\">Reshade Utilities</span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt;\">Program to copy reshade DLLs, shaders and config fiies to several games.</span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt;\">Developed as an open source project and hosted on GitHub.</span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt;\">Implemented using Python3 and QT5.</span></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt; text-decoration: underline; color:#0000ff;\"><br /></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt; text-decoration: underline; color:#0000ff;\"><br /></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt; text-decoration: underline; color:#0000ff;\"><br /></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt; text-decoration: underline; color:#0000ff;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600;\">Acknowledgements</span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"https://www.qt.io\"><span style=\" font-size:9pt; text-decoration: underline; color:#8b0000;\">QT5</span></a></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"https://www.python.org\"><span style=\" font-size:9pt; text-decoration: underline; color:#8b0000;\">Python3</span></a></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"https://reshade.me/\"><span style=\" font-size:9pt; text-decoration: underline; color:#8b0000;\">Reshade</span></a></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"https://pyinstaller.readthedocs.io\"><span style=\" font-size:9pt; text-decoration: underline; color:#8b0000;\">PyInstaller</span></a></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:9pt; text-decoration: underline; color:#0000ff;\"><br /></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:9pt; text-decoration: underline; color:#0000ff;\"><br /></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:9pt; text-decoration: underline; color:#0000ff;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600;\">Developed by</span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt;\">Discord: Hadesz#1223</span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"mailto:hadesz456@gmail.com\"><span style=\" font-size:9pt; text-decoration: underline; color:#8b0000;\">Email</span></a></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"https://github.com/ddc/ReshadeUtils/releases/latest\"><span style=\" font-size:9pt; text-decoration: underline; color:#8b0000;\">Download</span></a></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.main_tabWidget.setTabText(self.main_tabWidget.indexOf(self.about_tab), _translate("Main", "About"))
        self.update_button.setText(_translate("Main", "UPDATE"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Main = QtWidgets.QWidget()
    ui = Ui_Main()
    ui.setupUi(Main)
    Main.show()
    sys.exit(app.exec_())

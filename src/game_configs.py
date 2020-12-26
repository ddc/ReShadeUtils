#! /usr/bin/env python3
# |*****************************************************
# * Copyright         : Copyright (C) 2019
# * Author            : ddc
# * License           : GPL v3
# * Python            : 3.6
# |*****************************************************
# # -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_game_config_Form(object):
    def setupUi(self, game_config_Form):
        game_config_Form.setObjectName("game_config_Form")
        game_config_Form.resize(325, 280)
        game_config_Form.setMinimumSize(QtCore.QSize(325, 280))
        game_config_Form.setMaximumSize(QtCore.QSize(325, 280))
        game_config_Form.setSizeIncrement(QtCore.QSize(270, 185))
        game_config_Form.setBaseSize(QtCore.QSize(270, 185))
        self.cancel_pushButton = QtWidgets.QPushButton(game_config_Form)
        self.cancel_pushButton.setGeometry(QtCore.QRect(20, 240, 93, 28))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("src\\ui\\../images/cancel.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cancel_pushButton.setIcon(icon)
        self.cancel_pushButton.setObjectName("cancel_pushButton")
        self.game_name_lineEdit = QtWidgets.QLineEdit(game_config_Form)
        self.game_name_lineEdit.setGeometry(QtCore.QRect(10, 30, 291, 22))
        self.game_name_lineEdit.setText("")
        self.game_name_lineEdit.setObjectName("game_name_lineEdit")
        self.game_label = QtWidgets.QLabel(game_config_Form)
        self.game_label.setGeometry(QtCore.QRect(10, 10, 291, 16))
        self.game_label.setObjectName("game_label")
        self.ok_pushButton = QtWidgets.QPushButton(game_config_Form)
        self.ok_pushButton.setGeometry(QtCore.QRect(200, 240, 93, 28))
        self.ok_pushButton.setFocusPolicy(QtCore.Qt.WheelFocus)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("src\\ui\\../images/apply.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ok_pushButton.setIcon(icon1)
        self.ok_pushButton.setObjectName("ok_pushButton")
        self.architecture_groupBox = QtWidgets.QGroupBox(game_config_Form)
        self.architecture_groupBox.setGeometry(QtCore.QRect(10, 60, 291, 61))
        self.architecture_groupBox.setObjectName("architecture_groupBox")
        self.radioButton_32bits = QtWidgets.QRadioButton(self.architecture_groupBox)
        self.radioButton_32bits.setGeometry(QtCore.QRect(10, 30, 95, 20))
        self.radioButton_32bits.setObjectName("radioButton_32bits")
        self.radioButton_64bits = QtWidgets.QRadioButton(self.architecture_groupBox)
        self.radioButton_64bits.setGeometry(QtCore.QRect(150, 30, 95, 20))
        self.radioButton_64bits.setObjectName("radioButton_64bits")
        self.api_groupBox = QtWidgets.QGroupBox(game_config_Form)
        self.api_groupBox.setGeometry(QtCore.QRect(10, 130, 291, 91))
        self.api_groupBox.setObjectName("api_groupBox")
        self.dx9_radioButton = QtWidgets.QRadioButton(self.api_groupBox)
        self.dx9_radioButton.setGeometry(QtCore.QRect(10, 30, 100, 20))
        self.dx9_radioButton.setObjectName("dx9_radioButton")
        self.dx_radioButton = QtWidgets.QRadioButton(self.api_groupBox)
        self.dx_radioButton.setGeometry(QtCore.QRect(150, 30, 131, 20))
        self.dx_radioButton.setObjectName("dx_radioButton")
        self.opengl_radioButton = QtWidgets.QRadioButton(self.api_groupBox)
        self.opengl_radioButton.setGeometry(QtCore.QRect(10, 60, 95, 20))
        self.opengl_radioButton.setObjectName("opengl_radioButton")
        self.vulkan_radioButton = QtWidgets.QRadioButton(self.api_groupBox)
        self.vulkan_radioButton.setGeometry(QtCore.QRect(150, 60, 95, 20))
        self.vulkan_radioButton.setObjectName("vulkan_radioButton")

        self.retranslateUi(game_config_Form)
        QtCore.QMetaObject.connectSlotsByName(game_config_Form)

    def retranslateUi(self, game_config_Form):
        _translate = QtCore.QCoreApplication.translate
        game_config_Form.setWindowTitle(_translate("game_config_Form", "Configuration"))
        self.cancel_pushButton.setText(_translate("game_config_Form", "Cancel"))
        self.game_label.setText(_translate("game_config_Form", "Name of the game:"))
        self.ok_pushButton.setText(_translate("game_config_Form", "OK"))
        self.architecture_groupBox.setTitle(_translate("game_config_Form", "Architecture"))
        self.radioButton_32bits.setText(_translate("game_config_Form", "32bits"))
        self.radioButton_64bits.setText(_translate("game_config_Form", "64bits"))
        self.api_groupBox.setTitle(_translate("game_config_Form", "API"))
        self.dx9_radioButton.setText(_translate("game_config_Form", "DX9"))
        self.dx_radioButton.setText(_translate("game_config_Form", "DX10 / 11 / 12"))
        self.opengl_radioButton.setText(_translate("game_config_Form", "OpenGL"))
        self.vulkan_radioButton.setText(_translate("game_config_Form", "Vulkan"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    game_config_Form = QtWidgets.QWidget()
    ui = Ui_game_config_Form()
    ui.setupUi(game_config_Form)
    game_config_Form.show()
    sys.exit(app.exec_())

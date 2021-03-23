#! /usr/bin/env python3
# |*****************************************************
# * Copyright         : Copyright (C) 2019
# * Author            : ddc
# * License           : GPL v3
# |*****************************************************
# # -*- coding: utf-8 -*-

from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_game_config_Form(object):
    def setupUi(self, game_config_Form):
        game_config_Form.setObjectName("game_config_Form")
        game_config_Form.resize(360, 195)
        game_config_Form.setMinimumSize(QtCore.QSize(360, 195))
        game_config_Form.setMaximumSize(QtCore.QSize(360, 195))
        self.cancel_pushButton = QtWidgets.QPushButton(game_config_Form)
        self.cancel_pushButton.setGeometry(QtCore.QRect(20, 150, 93, 28))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/src/media/cancel.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.cancel_pushButton.setIcon(icon)
        self.cancel_pushButton.setObjectName("cancel_pushButton")
        self.game_name_lineEdit = QtWidgets.QLineEdit(game_config_Form)
        self.game_name_lineEdit.setGeometry(QtCore.QRect(10, 30, 341, 22))
        self.game_name_lineEdit.setText("")
        self.game_name_lineEdit.setObjectName("game_name_lineEdit")
        self.game_label = QtWidgets.QLabel(game_config_Form)
        self.game_label.setGeometry(QtCore.QRect(10, 10, 71, 16))
        self.game_label.setObjectName("game_label")
        self.ok_pushButton = QtWidgets.QPushButton(game_config_Form)
        self.ok_pushButton.setGeometry(QtCore.QRect(250, 150, 93, 28))
        self.ok_pushButton.setFocusPolicy(QtCore.Qt.FocusPolicy.WheelFocus)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/src/media/apply.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.ok_pushButton.setIcon(icon1)
        self.ok_pushButton.setObjectName("ok_pushButton")
        self.api_groupBox = QtWidgets.QGroupBox(game_config_Form)
        self.api_groupBox.setGeometry(QtCore.QRect(10, 60, 341, 71))
        self.api_groupBox.setObjectName("api_groupBox")
        self.dx9_radioButton = QtWidgets.QRadioButton(self.api_groupBox)
        self.dx9_radioButton.setGeometry(QtCore.QRect(110, 30, 91, 20))
        self.dx9_radioButton.setObjectName("dx9_radioButton")
        self.dx_radioButton = QtWidgets.QRadioButton(self.api_groupBox)
        self.dx_radioButton.setGeometry(QtCore.QRect(200, 30, 131, 20))
        self.dx_radioButton.setObjectName("dx_radioButton")
        self.opengl_radioButton = QtWidgets.QRadioButton(self.api_groupBox)
        self.opengl_radioButton.setGeometry(QtCore.QRect(10, 30, 81, 20))
        self.opengl_radioButton.setObjectName("opengl_radioButton")

        self.retranslateUi(game_config_Form)
        QtCore.QMetaObject.connectSlotsByName(game_config_Form)


    def retranslateUi(self, game_config_Form):
        _translate = QtCore.QCoreApplication.translate
        game_config_Form.setWindowTitle(_translate("game_config_Form", "Configuration"))
        self.cancel_pushButton.setText(_translate("game_config_Form", "Cancel"))
        self.game_label.setText(_translate("game_config_Form", "Name:"))
        self.ok_pushButton.setText(_translate("game_config_Form", "OK"))
        self.api_groupBox.setTitle(_translate("game_config_Form", "API"))
        self.dx9_radioButton.setText(_translate("game_config_Form", "DirectX 9"))
        self.dx_radioButton.setText(_translate("game_config_Form", "DirectX (10,11,12)"))
        self.opengl_radioButton.setText(_translate("game_config_Form", "OpenGL"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    game_config_Form = QtWidgets.QWidget()
    ui = Ui_game_config_Form()
    ui.setupUi(game_config_Form)
    game_config_Form.show()
    app.exec()

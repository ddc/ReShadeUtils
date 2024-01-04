# -*- coding: utf-8 -*-
import sys
from src.utils import resources_rc
from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_config(object):
    def setupUi(self, config):
        config.setObjectName("config")
        config.resize(360, 195)
        config.setMinimumSize(QtCore.QSize(360, 195))
        config.setMaximumSize(QtCore.QSize(360, 195))
        self.cancel_pushButton = QtWidgets.QPushButton(config)
        self.cancel_pushButton.setGeometry(QtCore.QRect(20, 150, 93, 28))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/resources/images/cancel.png"),
                       QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.cancel_pushButton.setIcon(icon)
        self.cancel_pushButton.setObjectName("cancel_pushButton")
        self.game_name_lineEdit = QtWidgets.QLineEdit(config)
        self.game_name_lineEdit.setGeometry(QtCore.QRect(10, 30, 341, 22))
        self.game_name_lineEdit.setText("")
        self.game_name_lineEdit.setObjectName("game_name_lineEdit")
        self.game_label = QtWidgets.QLabel(config)
        self.game_label.setGeometry(QtCore.QRect(10, 10, 71, 16))
        self.game_label.setObjectName("game_label")
        self.ok_pushButton = QtWidgets.QPushButton(config)
        self.ok_pushButton.setGeometry(QtCore.QRect(250, 150, 93, 28))
        self.ok_pushButton.setFocusPolicy(QtCore.Qt.FocusPolicy.WheelFocus)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/resources/images/apply.png"),
                        QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.ok_pushButton.setIcon(icon1)
        self.ok_pushButton.setObjectName("ok_pushButton")
        self.api_groupBox = QtWidgets.QGroupBox(config)
        self.api_groupBox.setGeometry(QtCore.QRect(10, 60, 341, 71))
        self.api_groupBox.setObjectName("api_groupBox")
        self.dx9_radioButton = QtWidgets.QRadioButton(self.api_groupBox)
        self.dx9_radioButton.setGeometry(QtCore.QRect(100, 30, 91, 20))
        self.dx9_radioButton.setObjectName("dx9_radioButton")
        self.dx_radioButton = QtWidgets.QRadioButton(self.api_groupBox)
        self.dx_radioButton.setGeometry(QtCore.QRect(200, 30, 131, 20))
        self.dx_radioButton.setObjectName("dx_radioButton")
        self.opengl_radioButton = QtWidgets.QRadioButton(self.api_groupBox)
        self.opengl_radioButton.setGeometry(QtCore.QRect(10, 30, 81, 20))
        self.opengl_radioButton.setObjectName("opengl_radioButton")

        self.retranslateUi(config)
        QtCore.QMetaObject.connectSlotsByName(config)

    def retranslateUi(self, config):
        _translate = QtCore.QCoreApplication.translate
        config.setWindowTitle(_translate("config", "Configuration"))
        self.cancel_pushButton.setText(_translate("config", "Cancel"))
        self.game_label.setText(_translate("config", "Name:"))
        self.ok_pushButton.setText(_translate("config", "OK"))
        self.api_groupBox.setTitle(_translate("config", "API"))
        self.dx9_radioButton.setText(_translate("config", "DirectX 9"))
        self.dx_radioButton.setText(_translate("config", "DirectX (10,11,12)"))
        self.opengl_radioButton.setText(_translate("config", "OpenGL"))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    config = QtWidgets.QWidget()
    ui = Ui_config()
    ui.setupUi(config)
    config.show()
    sys.exit(app.exec())

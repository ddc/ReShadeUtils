# -*- coding: utf-8 -*-
import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from src.constants import variables


class UiEditForm(object):
    def __init__(self):
        self.cancel_push_button = None
        self.game_name_line_edit = None
        self.game_label = None
        self.ok_push_button = None
        self.api_group_box = None
        self.dx9_radio_button = None
        self.dxgi_radio_button = None
        self.opengl_radio_button = None

    def setup_ui(self, cfg):
        cfg.setObjectName("edit_config_form")
        cfg.resize(360, 195)
        cfg.setMinimumSize(QtCore.QSize(360, 195))
        cfg.setMaximumSize(QtCore.QSize(360, 195))
        self.cancel_push_button = QtWidgets.QPushButton(cfg)
        self.cancel_push_button.setGeometry(QtCore.QRect(20, 150, 93, 28))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/resources/images/cancel.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.cancel_push_button.setIcon(icon)
        self.cancel_push_button.setObjectName("cancel_push_button")
        self.game_name_line_edit = QtWidgets.QLineEdit(cfg)
        self.game_name_line_edit.setGeometry(QtCore.QRect(10, 30, 341, 22))
        self.game_name_line_edit.setText("")
        self.game_name_line_edit.setObjectName("game_name_line_edit")
        self.game_label = QtWidgets.QLabel(cfg)
        self.game_label.setGeometry(QtCore.QRect(10, 10, 71, 16))
        self.game_label.setObjectName("game_label")
        self.ok_push_button = QtWidgets.QPushButton(cfg)
        self.ok_push_button.setGeometry(QtCore.QRect(250, 150, 93, 28))
        self.ok_push_button.setFocusPolicy(QtCore.Qt.FocusPolicy.WheelFocus)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/resources/images/apply.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.ok_push_button.setIcon(icon1)
        self.ok_push_button.setObjectName("ok_push_button")
        self.api_group_box = QtWidgets.QGroupBox(cfg)
        self.api_group_box.setGeometry(QtCore.QRect(10, 60, 341, 71))
        self.api_group_box.setObjectName("api_group_box")
        self.dx9_radio_button = QtWidgets.QRadioButton(self.api_group_box)
        self.dx9_radio_button.setGeometry(QtCore.QRect(100, 30, 91, 20))
        self.dx9_radio_button.setObjectName("dx9_radio_button")
        self.dxgi_radio_button = QtWidgets.QRadioButton(self.api_group_box)
        self.dxgi_radio_button.setGeometry(QtCore.QRect(200, 30, 131, 20))
        self.dxgi_radio_button.setObjectName("dxgi_radio_button")
        self.opengl_radio_button = QtWidgets.QRadioButton(self.api_group_box)
        self.opengl_radio_button.setGeometry(QtCore.QRect(10, 30, 81, 20))
        self.opengl_radio_button.setObjectName("opengl_radio_button")

        self.retranslate_ui(cfg)
        QtCore.QMetaObject.connectSlotsByName(cfg)

    def retranslate_ui(self, cfg):
        _translate = QtCore.QCoreApplication.translate
        cfg.setWindowTitle(_translate("cfg", "Configuration"))
        self.cancel_push_button.setText(_translate("cfg", "Cancel"))
        self.game_label.setText(_translate("cfg", "Name:"))
        self.ok_push_button.setText(_translate("cfg", "OK"))
        self.api_group_box.setTitle(_translate("cfg", "API"))
        self.dx9_radio_button.setText(_translate("cfg", variables.DX9_DISPLAY_NAME))
        self.dxgi_radio_button.setText(_translate("cfg", variables.DXGI_DISPLAY_NAME))
        self.opengl_radio_button.setText(_translate("cfg", variables.OPENGL_DISPLAY_NAME))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    edit_form = QtWidgets.QWidget()
    ui = UiEditForm()
    ui.setup_ui(edit_form)
    edit_form.show()
    sys.exit(app.exec())

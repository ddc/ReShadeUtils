#! /usr/bin/env python3
# |*****************************************************
# * Copyright         : Copyright (C) 2019
# * Author            : ddc
# * License           : GPL v3
# |*****************************************************
# # -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtWidgets


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
        self.progressBar.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.progressBar.setAlignment(QtCore.Qt.AlignCenter)

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

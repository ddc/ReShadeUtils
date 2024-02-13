# -*- coding: utf-8 -*-
from PyQt6 import QtCore, QtWidgets


STYLE = """
QProgressBar,
QProgressBar:horizontal {
    border: 1px transparent white;
    border-radius: 1px;
    text-align: center;
    font-size: 9pt;
    font-weight: bold;
}

QProgressBar::chunk,
QProgressBar::chunk:horizontal {
    background-color: green;
}    
"""


class ProgressBar:
    def __init__(self, width=350, height=25, log=None):
        self.log = log
        self.pbar = QtWidgets.QProgressBar()
        self.pbar.setObjectName("progressBar")
        self.pbar.setMinimumSize(QtCore.QSize(width, height))
        self.pbar.setMaximumSize(QtCore.QSize(width, height))
        self.pbar.setSizeIncrement(QtCore.QSize(width, height))
        self.pbar.setBaseSize(QtCore.QSize(width, height))
        self.pbar.setMinimum(0)
        self.pbar.setMaximum(100)
        self.pbar.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        self.pbar.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.pbar.setStyleSheet(STYLE)

    def set_values(self, message="", value=0):
        if self.log:
            self.log.info(message)
        _translate = QtCore.QCoreApplication.translate
        self.pbar.setFormat(_translate("Main", f"{message}  %p%"))
        self.pbar.setValue(value)
        if value >= 100:
            self.pbar.close()
        else:
            self.pbar.show()
            QtWidgets.QApplication.processEvents()

    def close(self):
        self.pbar.close()

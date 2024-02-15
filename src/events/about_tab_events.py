# -*- coding: utf-8 -*-
from PyQt6 import QtCore
from PyQt6.QtGui import QDesktopServices
from src.constants import variables


def donate_clicked():
    href = QtCore.QUrl(variables.PAYPAL_URL)
    QDesktopServices.openUrl(href)

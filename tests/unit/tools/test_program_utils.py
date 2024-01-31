# -*- coding: utf-8 -*-
from datetime import datetime
from unittest.mock import patch
import pytest
from PyQt6.QtWidgets import QLabel, QPushButton, QRadioButton
from src.tools import program_utils


@pytest.fixture
def qtbutton(qtbot):
    qbutton = QPushButton()
    qbutton.setVisible(True)
    qtbot.addWidget(qbutton)
    return qbutton


@pytest.fixture
def qtlabel(qtbot):
    qlabel = QLabel()
    qlabel.setText("Hello World")
    qtbot.addWidget(qlabel)
    return qlabel


@pytest.fixture
def qtradiobutton(qtbot):
    qradiobutton = QRadioButton()
    qradiobutton.setChecked(True)
    qtbot.addWidget(qradiobutton)
    return qradiobutton


class Object:
    def __init__(self):
        self._created = datetime.now().isoformat()


class TestProgramUtils:
    @patch("src.tools.program_utils.get_new_program_version")
    def test_check_program_updates(self, get_new_program_version_mock, qtbutton, qtlabel):
        obj = Object()
        obj.qtobj = Object()
        obj.qtobj.update_button = qtbutton
        obj.qtobj.updateAvail_label = qtlabel

        # check no new version available
        get_new_program_version_mock.return_value = {
            "client_version": 1.0,
            "remote_version": 1.0,
        }
        obj.check_program_updates = True
        result = program_utils.check_program_updates(obj)
        assert result is False

        # check new version available
        get_new_program_version_mock.return_value = {
            "client_version": 1.0,
            "remote_version": 2.1,
        }
        obj.check_program_updates = True
        result = program_utils.check_program_updates(obj)
        assert result is True

        # check for updates is disabled
        get_new_program_version_mock.return_value = {
            "client_version": 1.0,
            "remote_version": 2.1,
        }
        obj.check_program_updates = False
        result = program_utils.check_program_updates(obj)
        assert result is None
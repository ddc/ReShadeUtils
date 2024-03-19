# -*- coding: utf-8 -*-
import logging.handlers
import os
import tempfile
import pytest
from PyQt6 import QtCore, QtWidgets
from sqlalchemy.orm import Session
from tests.data.base_data import database_engine, Object
from src.constants import variables


@pytest.fixture(name="program_path", autouse=True)
def temp_program_path():
    for k, v in variables.__dict__.items():
        if any(x in k for x in ("PATH", "DIR")):
            # setting all path to dirs to /tmp/name
            setattr(variables, k, os.path.join(tempfile.gettempdir(), variables.SHORT_PROGRAM_NAME, os.path.basename(v)))


@pytest.fixture(name="db_session")
def db_session():
    with Session(database_engine) as session:
        yield session


@pytest.fixture
def log():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.NullHandler())
    return logger


@pytest.fixture
def qpushbutton(qtbot):
    qwb = QtWidgets.QPushButton()
    qwb.setVisible(True)
    qtbot.addWidget(qwb)
    return qwb


@pytest.fixture
def qlabel(qtbot):
    qwl = QtWidgets.QLabel()
    qwl.setText("Hello World")
    qtbot.addWidget(qwl)
    return qwl


@pytest.fixture
def qradiobutton(qtbot):
    qwr = QtWidgets.QRadioButton()
    qwr.setChecked(True)
    qtbot.addWidget(qwr)
    return qwr


@pytest.fixture
def qgroupbox(qtbot):
    qwgb = QtWidgets.QGroupBox()
    qwgb.setGeometry(QtCore.QRect(100, 140, 330, 60))
    qwgb.setMinimumSize(QtCore.QSize(330, 60))
    qwgb.setMaximumSize(QtCore.QSize(330, 60))
    qtbot.addWidget(qwgb)
    return qwgb


@pytest.fixture
def qtabwidget(qtbot):
    qtt = QtWidgets.QTabWidget()
    qtt.setGeometry(QtCore.QRect(20, 10, 960, 691))
    qtt.setMinimumSize(QtCore.QSize(960, 640))
    qtt.setIconSize(QtCore.QSize(20, 20))
    qtt.setUsesScrollButtons(False)
    qtt.setObjectName("main_tab_widget")
    qtbot.addWidget(qtt)
    return qtt


@pytest.fixture
def qtextbrowser(qtbot):
    qwtb = QtWidgets.QTextBrowser()
    qwtb.setGeometry(QtCore.QRect(0, 0, 960, 610))
    qwtb.setMinimumSize(QtCore.QSize(960, 610))
    qwtb.setMaximumSize(QtCore.QSize(960, 610))
    qwtb.setAcceptDrops(False)
    qwtb.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
    qwtb.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    qwtb.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    qwtb.setUndoRedoEnabled(False)
    qwtb.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.LinksAccessibleByMouse)
    qwtb.setOpenExternalLinks(True)
    qwtb.setObjectName("about_text_browser")
    qtbot.addWidget(qwtb)
    return qwtb


@pytest.fixture
def qtablewidget(qtbot):
    qtw = QtWidgets.QTableWidget()
    qtw.setGeometry(QtCore.QRect(0, 0, 960, 520))
    qtw.setMinimumSize(QtCore.QSize(960, 520))
    qtw.setMaximumSize(QtCore.QSize(960, 520))
    qtw.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
    qtw.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
    qtw.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
    qtw.setLineWidth(0)
    qtw.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
    qtw.setAutoScroll(False)
    qtw.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
    qtw.setDragDropOverwriteMode(False)
    qtw.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
    qtw.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
    qtw.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollMode.ScrollPerPixel)
    qtw.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollMode.ScrollPerPixel)
    qtw.setWordWrap(False)
    qtw.setCornerButtonEnabled(False)
    qtw.setColumnCount(4)
    qtw.setObjectName("programs_table_widget")
    qtw.setRowCount(0)
    qtbot.addWidget(qtw)
    return qtw


@pytest.fixture
def qtobj(qpushbutton, qlabel, qradiobutton, qgroupbox, qtabwidget, qtextbrowser, qtablewidget):
    qtobj = Object()
    qtobj.apply_button = qpushbutton
    qtobj.selected_game_group_box = qgroupbox
    qtobj.edit_plugin_button = qpushbutton
    qtobj.reset_files_button = qpushbutton
    qtobj.edit_path_button = qpushbutton
    qtobj.open_game_path_button = qpushbutton
    qtobj.remove_button = qpushbutton
    qtobj.edit_game_button = qpushbutton
    qtobj.all_games_group_box = qgroupbox
    qtobj.apply_button = qpushbutton
    qtobj.add_button = qpushbutton
    qtobj.check_program_updates_group_box = qgroupbox
    qtobj.yes_check_program_updates_radio_button = qradiobutton
    qtobj.no_check_program_updates_radio_button = qradiobutton
    qtobj.use_dark_theme_group_box = qgroupbox
    qtobj.yes_dark_theme_radio_button = qradiobutton
    qtobj.no_dark_theme_radio_button = qradiobutton
    qtobj.create_screenshots_folder_group_box = qgroupbox
    qtobj.yes_screenshots_folder_radio_button = qradiobutton
    qtobj.no_screenshots_folder_radio_button = qradiobutton
    qtobj.check_reshade_updates_group_box = qgroupbox
    qtobj.yes_check_reshade_updates_radio_button = qradiobutton
    qtobj.no_check_reshade_updates_radio_button = qradiobutton
    qtobj.show_info_messages_groupBox = qgroupbox
    qtobj.no_show_info_messages_radio_button = qradiobutton
    qtobj.yes_show_info_messages_radio_button = qradiobutton
    qtobj.reset_all_button = qpushbutton
    qtobj.update_shaders_button = qpushbutton
    qtobj.edit_global_plugins_button = qpushbutton
    qtobj.main_tab_widget = qtabwidget
    qtobj.about_text_browser = qtextbrowser
    qtobj.programs_table_widget = qtablewidget
    return qtobj

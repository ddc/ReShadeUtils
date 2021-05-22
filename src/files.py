# |*****************************************************
# * Copyright         : Copyright (C) 2019
# * Author            : ddc
# * License           : GPL v3
# |*****************************************************
# # -*- coding: utf-8 -*-

import os
import requests
from src import constants, utils


class Files:
    def __init__(self, main):
        self.main = main
        self.log = main.log


    def create_reshade_ini_file(self, local_file_path, screenshot_path):
        remote_file = constants.RESHADE_REMOTE_FILENAME
        self._download_file(remote_file, local_file_path, _ini_file_contents)

        effect_search_paths = os.path.join(constants.PROGRAM_PATH, "Reshade-shaders", "Shaders")
        texture_search_paths = os.path.join(constants.PROGRAM_PATH, "Reshade-shaders", "Textures")
        intermediate_cache_path = os.getenv("TEMP")
        preset_path = f".\\{constants.RESHADE_PRESET_INI}"

        utils.set_file_settings(local_file_path, "GENERAL", "EffectSearchPaths", effect_search_paths)
        utils.set_file_settings(local_file_path, "GENERAL", "TextureSearchPaths", texture_search_paths)
        utils.set_file_settings(local_file_path, "GENERAL", "IntermediateCachePath", intermediate_cache_path)
        utils.set_file_settings(local_file_path, "GENERAL", "PresetPath", preset_path)
        utils.set_file_settings(local_file_path, "SCREENSHOT", "SavePath", screenshot_path)


    def create_reshade_preset_ini_file(self):
        local_file_path = constants.RESHADE_PRESET_FILENAME
        remote_file = constants.PRESET_REMOTE_FILENAME
        self._download_file(remote_file, local_file_path, _preset_file_contents)


    def create_qss_file(self):
        local_file_path = constants.QSS_FILENAME
        remote_file = constants.QSS_REMOTE_FILENAME
        self._download_file(remote_file, local_file_path, _qss_file_contents)


    def _download_file(self, remote_file, local_file_path, contents):
        try:
            req = requests.get(remote_file)
            if req.status_code == 200:
                with open(local_file_path, "wb") as outfile:
                    outfile.write(req.content)
            else:
                self._write_contents_local_file(local_file_path, contents)
        except requests.HTTPError:
            self._write_contents_local_file(local_file_path, contents)


    @staticmethod
    def _write_contents_local_file(local_file_path, contents):
        file = open(local_file_path, encoding="UTF-8", mode="w")
        file.write(contents)
        file.close()


_ini_file_contents = (
f"""[D3D9]
DepthCopyAtClearIndex=0
DepthCopyBeforeClears=0
DisableINTZ=0
UseAspectRatioHeuristics=1

[D3D11]
DepthCopyAtClearIndex=0
DepthCopyBeforeClears=0
UseAspectRatioHeuristics=1

[D3D12]
DepthCopyAtClearIndex=0
DepthCopyBeforeClears=0
UseAspectRatioHeuristics=1

[DEPTH]
DepthCopyAtClearIndex=0
DepthCopyBeforeClears=0
DisableINTZ=0
UseAspectRatioHeuristics=1

[GENERAL]
PerformanceMode=1
PreprocessorDefinitions=
PresetTransitionDelay=1000
SkipLoadingDisabledEffects=1

[INPUT]
ForceShortcutModifiers=1
InputProcessing=2
KeyEffects=145,0,0,0
KeyNextPreset=0,0,0,0
KeyOverlay=119,0,1,0
KeyPerformanceMode=0,0,0,0
KeyPreviousPreset=0,0,0,0
KeyReload=0,0,0,0
KeyScreenshot=44,0,0,0

[OVERLAY]
ClockFormat=0
FPSPosition=3
NoFontScaling=1
SaveWindowState=1
ShowClock=0
ShowForceLoadEffectsButton=1
ShowFPS=1
ShowFrameTime=0
ShowScreenshotMessage=1
TutorialProgress=4
VariableListHeight=336.000000
VariableListUseTabs=1

[SCREENSHOT]
ClearAlpha=1
FileFormat=1
FileNamingFormat=0
JPEGQuality=90
SaveBeforeShot=1
SaveOverlayShot=1
SavePresetFile=1

[STYLE]
Alpha=1.000000
ChildRounding=12.000000
ColFPSText=1.000000,1.000000,0.784314,1.000000
EditorFont=ProggyClean.ttf
EditorFontSize=13
EditorStyleIndex=0
Font=ProggyClean.ttf
FontSize=13
FPSScale=1.300000
FrameRounding=12.000000
GrabRounding=12.000000
PopupRounding=12.000000
ScrollbarRounding=12.000000
StyleIndex=0
TabRounding=12.000000
WindowRounding=12.000000
""")


_preset_file_contents = (
"""PreprocessorDefinitions=
Techniques=LumaSharpen@LumaSharpen.fx,DPX@DPX.fx,Levels@Levels.fx,Clarity@Clarity.fx
TechniqueSorting=LumaSharpen@LumaSharpen.fx,DPX@DPX.fx,Levels@Levels.fx,Clarity@Clarity.fx

[Clarity.fx]
ClarityBlendIfDark=50
ClarityBlendIfLight=205
ClarityBlendMode=2
ClarityDarkIntensity=0.400000
ClarityLightIntensity=0.000000
ClarityOffset=2.000000
ClarityRadius=3
ClarityStrength=0.400000
ClarityViewBlendIfMask=0
ClarityViewMask=0

[DPX.fx]
Colorfulness=2.500000
Contrast=0.000000
RGB_C=0.360000,0.360000,0.340000
RGB_Curve=8.000000,8.000000,8.000000
Saturation=2.200001
Strength=0.200000

[Levels.fx]
BlackPoint=5
HighlightClipping=0
WhitePoint=235

[LumaSharpen.fx]
offset_bias=1.000000
pattern=1
sharp_clamp=0.035000
sharp_strength=0.500000
show_sharpen=0
""")


_qss_file_contents = (
"""QWidget {
   background-color: #222222;
}

QWidget:disabled {
    color: #f5f5f5;
    background-color: #222222;
}

QLabel:disabled,
QCheckBox:disabled,
QRadioButton:disabled,
QGroupBox:disabled,
QTabBar:disabled
{
    color: #828282;
    padding: 3px;
    outline: none;
    background-color: transparent;
}

QLineEdit,
QLabel,
QCheckBox,
QRadioButton,
QGroupBox,
QtWidgets  {
    color: #FFFFFF;
}

QDialogButtonBox {
    button-layout: 0;
}

QTextEdit {
    color: #FFFFFF;
    background-color: #222222;
    border: 1px transparent #FFFFFF;
    padding: 0px;
    margin: 0px;
}

QPlainTextEdit {
    color: #FFFFFF;
    background-color: #222222;
    border-radius: 2px;
    border: 1px solid #b6b6b6;
    padding: 0px;
    margin: 0px;
}

/* QPushButton */

QPushButton {
   background-color: #8b0000;
   color: #000000;
   border-radius: 5px;
   border-style: none;
   height: 25px;
   font-weight: bold;
}

QPushButton:hover {
   background-color: #8b0000;
   color: #ffffff;
}

QPushButton:pressed {
   background-color: #000000;
   color: #8b0000;
   border-radius: 5px;
   border-style: none;
   height: 25px;
   font-weight: bold;
}

/* QTabWidget */

QTabWidget::pane {
    border: 1px transparent #222222;
}

QTabWidget:focus {
    border: 1px transparent #000000;
}

QTabWidget::tab-bar {
    alignment: left;
    border: 1px transparent #000000;
}

/* QTabBar */

QTabBar::tab {
    background-color:qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #cccccc, stop: 1.0 #FFFFFF);
    border: 1px transparent #000000;
    border-top-left-radius: 12px;
    border-top-right-radius: 12px;
    padding:4px;
}

QTabBar::tab:selected {
    border-bottom: 1px transparent #FFFFFF;
    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #8b0000, stop: 1.0 #FFFFFF);
}

/* QRadioButton */

QRadioButton::indicator:checked {
    background-color:#8b0000;
    border:1px solid black;
    border-radius: 8px;
}

QRadioButton::indicator:unchecked {
    background-color:#ffffff;
    border:1px solid black;
    border-radius: 8px;
}

/* QCheckBox */

QCheckBox::indicator:checked {
    background-color:#8b0000;
    border:1px solid black;
}

QCheckBox::indicator:unchecked {
    background-color:#ffffff;
    border:1px solid black;
}

/* QScrollBar */

QScrollBar:horizontal {
    height: 15px;
    margin: 3px 15px 3px 15px;
    border: 1px transparent #3A3939;
    border-radius: 4px;
    background-color: #3A3939;
}

QScrollBar::handle:horizontal {
    background-color: #b6b6b6;
    min-width: 5px;
    border-radius: 4px;
}

QScrollBar::add-line:horizontal {
    margin: 1px 3px 0px 3px;
    width: 6px;
    height: 10px;
    subcontrol-position: right;
    subcontrol-origin: margin;
}

QScrollBar::sub-line:horizontal {
    margin: 1px 3px 0px 3px;
    height: 10px;
    width: 6px;
    subcontrol-position: left;
    subcontrol-origin: margin;
}

QScrollBar::add-line:horizontal:hover,
QScrollBar::sub-line:horizontal:hover,
QScrollBar::up-arrow:horizontal,
QScrollBar::down-arrow:horizontal {
    background: none;
}

QScrollBar::add-page:horizontal,
QScrollBar::sub-page:horizontal {
    background: none;
}

QScrollBar:vertical {
    background-color: #3A3939;
    width: 15px;
    margin: 15px 3px 15px 3px;
    border: 1px transparent #3A3939;
    border-radius: 4px;
}

QScrollBar::handle:vertical {
    background-color: #b6b6b6;
    min-height: 5px;
    border-radius: 4px;
}

QScrollBar::sub-line:vertical {
    margin: 3px 0px 3px 1px;
    height: 6px;
    width: 10px;
    subcontrol-position: top;
    subcontrol-origin: margin;
}

QScrollBar::add-line:vertical {
    margin: 3px 0px 3px 1px;
    height: 6px;
    width: 10px;
    subcontrol-position: bottom;
    subcontrol-origin: margin;
}

QScrollBar::sub-line:vertical:hover,
QScrollBar::add-line:vertical:hover,
QScrollBar::up-arrow:vertical,
QScrollBar::down-arrow:vertical {
    background: none;
}

QScrollBar::add-page:vertical,
QScrollBar::sub-page:vertical {
    background: none;
}

/* QProgressBar */

QProgressBar,
QProgressBar:horizontal {  
    border: 1px solid #b6b6b6;
    border-radius: 4px;
    text-align: center;
    padding: 1px;
    background: #bdc1c9;
    background-color: #8b0000;
}

QProgressBar::chunk,
QProgressBar::chunk:horizontal {
    background-color: qlineargradient(spread:pad, x1:1, y1:0.545, x2:1, y2:0, stop:0 #3874f2, stop:1 #5e90fa);
    border-radius: 3px;
}

/* QTableWidget */

QTableWidget::item {
    background-color: #8b0000;
}

QHeaderView::section {
    background-color: rgba(128, 128, 128, 128);
}

QTableCornerButton::section {
    background: rgba(128, 128, 128, 128);
    border: 1px transparent rgba(128, 128, 128, 128);
}
""")

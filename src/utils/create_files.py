#! /usr/bin/env python3
#|*****************************************************
# * Copyright         : Copyright (C) 2019
# * Author            : ddc
# * License           : GPL v3
# * Python            : 3.6
#|*****************************************************
# # -*- coding: utf-8 -*-

from src.utils import constants


class CreateFiles:
    def __init__(self, main):
        self.main = main
        self.log = main.log

    ################################################################################
    def create_settings_file(self):
        file = open(constants.DB_SETTINGS_FILENAME, encoding="utf-8", mode="w")
        file.write(
"""; DO NOT OPEN THIS FILE WITH NOTEPAD.
; Use Notepad++ or any other modern text editor.

[Configs]
; sqlite or postgres
DatabaseInUse="sqlite"

[Database]
Host="127.0.0.1"
Port="5432"
DBname="reshadeUtils"
Username="postgres"
Password="postgres"
""")
        file.close()

    ################################################################################
    def create_reshade_plugins_ini_file(self):
        file = open(constants.RESHADE_PLUGINS_FILENAME, encoding="utf-8", mode="w")
        file.write(
"""Effects=Clarity.fx,Curves.fx,DPX.fx,LumaSharpen.fx,Levels.fx
PreprocessorDefinitions=
Techniques=Curves,LumaSharpen,Levels
TechniqueSorting=Clarity,Curves,DPX,LumaSharpen,Levels,MXAO,SMAA,ASCII,AdaptiveFog,AdaptiveSharpen,AdvancedCRT,After,AmbientLight,Before,BloomAndLensFlares,Border,CA,Cartoon,Chromakey,ChromaticAberration,CinematicDOF,ColorMatrix,Colourfulness,Daltonize,Deband,Depth3D,DepthHaze,DisplayDepth,Emphasize,EyeAdaption,FilmGrain,FilmGrain2,FilmicAnamorphSharpen,FilmicPass,FXAA,GP65CJ042DOF,GaussianBlur,GlitchB,HDR,HQ4X,HSLShift,HighPassSharp,KNearestNeighbors,LUT,Layer,LeiFx_Tech,LevelsPlus,LiftGammaGain,LightDoF_AutoFocus,LightDoF_Far,LightDoF_Near,MagicBloom,MagicDOF,MartyMcFlyDOF,MatsoDOF,Mode1,Mode2,Mode3,Monochrome,MotionBlur,MultiLUT,Nightvision,NonLocalMeans,Nostalgia,PPFXBloom,PPFXSSDO,PPFX_Godrays,PerfectPerspective,ReflectiveBumpmapping,RingDOF,StageDepth,SurfaceBlur,Technicolor,Technicolor2,TiltShift,Tint,Tonemap,TriDither,UIDetect,UIDetect_After,UIDetect_Before,UIMask_Bottom,UIMask_Top,Vibrance,Vignette,AspectRatioPS

[Clarity.fx]
ClarityBlendIfDark=50
ClarityBlendIfLight=200
ClarityBlendMode=4
ClarityDarkIntensity=0.400000
ClarityLightIntensity=0.000000
ClarityOffset=5.000000
ClarityRadius=4
ClarityStrength=0.400000
ClarityViewBlendIfMask=0
ClarityViewMask=0

[Curves.fx]
Contrast=0.300000
Formula=4
Mode=0

[DPX.fx]
Colorfulness=2.500000
Contrast=0.100000
RGB_C=0.360000,0.360000,0.340000
RGB_Curve=8.000000,8.000000,8.000000
Saturation=2.000000
Strength=0.200000

[Levels.fx]
BlackPoint=5
HighlightClipping=0
WhitePoint=235

[LumaSharpen.fx]
offset_bias=1.000000
pattern=1
sharp_clamp=0.500000
sharp_strength=1.500000
show_sharpen=0
""")
        file.close()

    ################################################################################
    def create_reshade_ini_file(self, game_path:str, screenshot_path:str):
        file = open(f"{game_path}\\{constants.RESHADE_INI}", encoding="utf-8", mode="w")
        file.write(
f"""[INPUT]
KeyMenu=119,0,1,0
KeyScreenshot=44,0,0,0
InputProcessing=2
KeyEffects=145,0,0,0
KeyReload=0,0,0,0

[GENERAL]
TextureSearchPaths={constants.PROGRAM_PATH}\\Reshade-shaders\\Textures
EffectSearchPaths={constants.PROGRAM_PATH}\\Reshade-shaders\\Shaders
ScreenshotPath={screenshot_path}
CurrentPresetPath={game_path}\\{constants.RESHADE_PLUGINS_INI}
PresetFiles=.\\{constants.RESHADE_PLUGINS_INI}
ScreenshotIncludePreset=0
NoFontScaling=0
ClockFormat=1
CurrentPreset=0
PerformanceMode=1
PreprocessorDefinitions=RESHADE_DEPTH_LINEARIZATION_FAR_PLANE=1000.0,RESHADE_DEPTH_INPUT_IS_UPSIDE_DOWN=0,RESHADE_DEPTH_INPUT_IS_REVERSED=0,RESHADE_DEPTH_INPUT_IS_LOGARITHMIC=0
TutorialProgress=5
ScreenshotFormat=0
ShowClock=0
ShowFPS=0
FontGlobalScale=1.000000
ShowFrameTime=0
NoReloadOnInit=0
SaveWindowState=0
PresetSearchPaths=.NewVariableUI=1
ShowScreenshotMessage=1
NewVariableUI=1

[STYLE]
GrabRounding=12.000000
Alpha=1.000000
ColActive=0.200000,0.500000,0.600000
EditorStyleIndex=0
ColFPSText=1.000000,1.000000,0.000000,1.000000
ColBackground=0.275000,0.275000,0.275000
FrameRounding=12.000000
FPSScale=1.000000
ColItemBackground=0.447000,0.447000,0.447000
ColText=0.800000,0.900000,0.900000
PopupRounding=12.000000
ChildRounding=12.000000
WindowRounding=12.000000
ScrollbarRounding=12.000000
TabRounding=12.000000
Font=
FontSize=13
EditorFont=
EditorFontSize=13
StyleIndex=0

[DX9_BUFFER_DETECTION]
DisableINTZ=0

[DX11_BUFFER_DETECTION]
DepthBufferRetrievalMode=0
DepthBufferTextureFormat=0
ExtendedDepthBufferDetection=0
DepthBufferClearingNumber=0
""")
        file.close()

    ################################################################################
    def create_style_file(self):
        file = open(constants.STYLE_QSS_FILENAME, encoding="utf-8", mode="w")
        file.write(
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
        file.close()

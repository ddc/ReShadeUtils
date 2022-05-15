# Reshade Utilities
### Program to copy/update [Reshade](https://reshade.me/) DLLs and shaders

[<img src="https://img.shields.io/badge/Donate-PayPal-green.svg?style=plastic">](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=ENK474GPJMVTE)
[<img src="https://img.shields.io/github/license/ddc/ReshadeUtils.svg?style=plastic">](https://github.com/ddc/ReshadeUtils/blob/master/LICENSE)
[<img src="https://img.shields.io/badge/Python-3-blue.svg?style=plastic">](https://www.python.org/)
[<img src="https://img.shields.io/badge/PyQt-5-brightgreen.svg?style=plastic">](https://riverbankcomputing.com/software/pyqt)
[<img src="https://img.shields.io/github/release/ddc/ReshadeUtils.svg?style=plastic">](https://github.com/ddc/ReshadeUtils/releases/latest)

![screenshot](resources/images/screenshot.png)
![screenshot](resources/images/screenshot_settings.png)

## Download
+ [Latest Release](https://github.com/ddc/ReshadeUtils/releases/latest)


## Program Notes
+ Configuration, logs and database files are now being saved in "%LOCALAPPDATA%\ReshadeUtils"
+ This program was compiled with PyInstaller


## To compile
+ Install requirements:
    + pip install -r requirements.txt
+ Compile both launcher and program with PyInstaller:
    + python.exe -O -m PyInstaller -y --clean ./resources/spec/launcher.spec
    + python.exe -O -m PyInstaller -y --clean ./resources/spec/reshadeUtils.spec


## Acknowledgements
+ [PyQt5](https://riverbankcomputing.com/software/pyqt)
+ [Python3](https://www.python.org)
+ [Reshade](https://reshade.me)
+ [PyInstaller](https://www.pyinstaller.org)
+ [Inno Setup](http://www.innosetup.com)


## License
Released under the [GNU GPL v3](LICENSE)


## Buy Me a Cup of Coffee
This program is open source and always will be, even if I don't get donations. That said, I know there are people out there that may still want to donate just to show their appreciation so this is for you guys. Thanks in advance!

[<img src="https://www.paypalobjects.com/en_US/i/btn/btn_donate_SM.gif">](https://www.paypal.com/donate/?cmd=_s-xclick&hosted_button_id=ENK474GPJMVTE)

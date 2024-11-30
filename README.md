# ReShade Utilities
## Program to copy/update [ReShade](https://reshade.me/) DLLs and shaders

[<img src="https://img.shields.io/badge/Donate-PayPal-green.svg?style=plastic">](https://www.paypal.com/donate/?business=MRJ2NVUGSK4EA&no_recurring=0&item_name=Reshade+Utils&currency_code=USD)
[<img src="https://img.shields.io/github/license/ddc/ReshadeUtils.svg?style=plastic">](https://github.com/ddc/ReshadeUtils/blob/master/LICENSE)
[<img src="https://img.shields.io/badge/Python-3-blue.svg?style=plastic">](https://www.python.org/)
[<img src="https://img.shields.io/badge/PyQt-6-brightgreen.svg?style=plastic">](https://riverbankcomputing.com/software/pyqt)
[<img src="https://img.shields.io/github/release/ddc/ReshadeUtils.svg?style=plastic">](https://github.com/ddc/ReshadeUtils/releases/latest)

![screenshot](src/resources/images/screenshot.png)
![screenshot](src/resources/images/screenshot_settings.png)


# Download
+ [Latest Release](https://github.com/ddc/ReshadeUtils/releases/latest)


# Program Notes
+ Configuration, logs and database files are now being saved in "%LOCALAPPDATA%\ReShadeUtils"
+ This program was compiled with PyInstaller


# Run tests
+ poe test


# Get coverage report
+ poe coverage


# To compile using PyInstaller
+ Compile both launcher and program with PyInstaller:
    + python -O -m PyInstaller -y --clean --log-level INFO --workpath ./dist/build --distpath ./dist ./src/data/spec/launcher.spec
    + python -O -m PyInstaller -y --clean --log-level INFO --workpath ./dist/build --distpath ./dist ./src/data/spec/reshadeUtils.spec


# Acknowledgements
+ [PyQt6](https://riverbankcomputing.com/software/pyqt)
+ [Python3](https://www.python.org)
+ [Reshade](https://reshade.me)
+ [PyInstaller](https://www.pyinstaller.org)
+ [Inno Setup](http://www.innosetup.com)


# License
Released under the [GNU GPL v3](LICENSE)



# Buy me a cup of coffee
+ [GitHub Sponsor](https://github.com/sponsors/ddc)
+ [ko-fi](https://ko-fi.com/ddcsta)
+ [Paypal](https://www.paypal.com/ncp/payment/6G9Z78QHUD4RJ)

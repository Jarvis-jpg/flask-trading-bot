@echo off
echo Installing TA-Lib for Windows...

:: Check if Python is installed
python --version > nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed
    exit /b 1
)

:: Download TA-Lib
echo Downloading TA-Lib...
curl -L https://download.lfd.uci.edu/pythonlibs/archived/TA_Lib-0.4.24-cp39-cp39-win_amd64.whl -o talib.whl

:: Install TA-Lib
echo Installing TA-Lib...
pip install talib.whl

:: Install other requirements
echo Installing other requirements...
pip install -r requirements.txt

:: Clean up
del talib.whl

echo Setup completed successfully!

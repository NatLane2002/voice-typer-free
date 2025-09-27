@echo off
echo Voice Typer - Alternative Dependency Installation
echo ================================================
echo This script handles common Windows installation issues
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo Python found. Checking version...
python --version

REM Upgrade pip first
echo.
echo Upgrading pip...
python -m pip install --upgrade pip

echo.
echo Installing dependencies with alternative methods...

REM Try installing with --user flag to avoid permission issues
echo.
echo Method 1: Installing with --user flag...
pip install --user -r requirements.txt
if %errorlevel% equ 0 (
    echo Success! Dependencies installed with --user flag.
    goto :success
)

echo.
echo Method 1 failed. Trying Method 2: Installing without version constraints...
pip install --user google-cloud-speech pyaudio pynput keyboard pyautogui configparser pyinstaller
if %errorlevel% equ 0 (
    echo Success! Dependencies installed without version constraints.
    goto :success
)

echo.
echo Method 2 failed. Trying Method 3: Installing PyAudio separately with pipwin...
pip install --user pipwin
if %errorlevel% equ 0 (
    pipwin install pyaudio
    pip install --user google-cloud-speech pynput keyboard pyautogui configparser pyinstaller
    if %errorlevel% equ 0 (
        echo Success! Dependencies installed with pipwin for PyAudio.
        goto :success
    )
)

echo.
echo Method 3 failed. Trying Method 4: Manual PyAudio installation...
echo.
echo Please download PyAudio manually:
echo 1. Go to: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
echo 2. Download the wheel file for your Python version and Windows architecture
echo 3. Install it with: pip install --user [downloaded_wheel_file]
echo.
echo Then run this command to install the remaining dependencies:
echo pip install --user google-cloud-speech pynput keyboard pyautogui configparser pyinstaller
echo.
pause
exit /b 1

:success
echo.
echo =====================================
echo Dependencies installed successfully!
echo =====================================
echo.
echo Next steps:
echo 1. Set up Google Cloud Speech-to-Text (see SETUP_GUIDE.md)
echo 2. Place your credentials.json file in this directory
echo 3. Run: python voice_typer.py
echo.
echo To test the installation, run: python test_voice_typer.py
echo.
pause

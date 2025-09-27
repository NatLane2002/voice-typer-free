@echo off
echo Voice Typer - Dependency Installation
echo =====================================

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

REM Install dependencies one by one with better error handling
echo.
echo Installing Python dependencies...

echo Installing google-cloud-speech...
pip install google-cloud-speech==2.21.0
if %errorlevel% neq 0 (
    echo Error: Failed to install google-cloud-speech
    echo This might be due to network issues or Google Cloud SDK conflicts
    pause
    exit /b 1
)

echo Installing pyaudio...
pip install pyaudio==0.2.11
if %errorlevel% neq 0 (
    echo Error: Failed to install pyaudio
    echo.
    echo PyAudio installation failed. This is common on Windows.
    echo Trying alternative installation methods...
    echo.
    
    REM Try installing pipwin first
    echo Installing pipwin for easier PyAudio installation...
    pip install pipwin
    if %errorlevel% equ 0 (
        echo Using pipwin to install pyaudio...
        pipwin install pyaudio
        if %errorlevel% neq 0 (
            echo pipwin method also failed.
            echo.
            echo Manual installation required:
            echo 1. Download PyAudio wheel from: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
            echo 2. Choose the correct version for your Python and Windows architecture
            echo 3. Install with: pip install PyAudio-0.2.11-cp[PYTHON_VERSION]-cp[PYTHON_VERSION]-win_[ARCH].whl
            echo.
            echo Or install Visual C++ Build Tools and try again.
            pause
            exit /b 1
        )
    ) else (
        echo pipwin installation failed. Please install Visual C++ Build Tools.
        echo Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
        pause
        exit /b 1
    )
)

echo Installing pynput...
pip install pynput==1.7.6
if %errorlevel% neq 0 (
    echo Error: Failed to install pynput
    pause
    exit /b 1
)

echo Installing keyboard...
pip install keyboard==0.13.5
if %errorlevel% neq 0 (
    echo Error: Failed to install keyboard
    pause
    exit /b 1
)

echo Installing pyautogui...
pip install pyautogui==0.9.54
if %errorlevel% neq 0 (
    echo Error: Failed to install pyautogui
    pause
    exit /b 1
)

echo Installing configparser...
pip install configparser==5.3.0
if %errorlevel% neq 0 (
    echo Error: Failed to install configparser
    pause
    exit /b 1
)

echo Installing pyinstaller...
pip install pyinstaller==5.13.2
if %errorlevel% neq 0 (
    echo Error: Failed to install pyinstaller
    pause
    exit /b 1
)

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

@echo off
echo Creating Voice Typer shortcuts...
echo =================================

REM Get the current directory
set "CURRENT_DIR=%~dp0"
set "PYTHON_PATH=python"
set "APP_NAME=Voice Typer"
set "APP_FILE=voice_typer.py"

REM Create desktop shortcut
echo Creating desktop shortcut...
powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%PUBLIC%\Desktop\Voice Typer.lnk'); $Shortcut.TargetPath = 'cmd.exe'; $Shortcut.WorkingDirectory = '%CURRENT_DIR%'; $Shortcut.Arguments = '/k python voice_typer.py'; $Shortcut.Description = 'Voice Typer - Voice to Text Application'; $Shortcut.IconLocation = 'python.exe,0'; $Shortcut.Save()"

if exist "%PUBLIC%\Desktop\Voice Typer.lnk" (
    echo ✓ Desktop shortcut created successfully!
) else (
    echo ✗ Failed to create desktop shortcut
)

REM Create Start Menu shortcut
echo Creating Start Menu shortcut...
if not exist "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Voice Typer" (
    mkdir "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Voice Typer"
)

powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%APPDATA%\Microsoft\Windows\Start Menu\Programs\Voice Typer\Voice Typer.lnk'); $Shortcut.TargetPath = 'cmd.exe'; $Shortcut.WorkingDirectory = '%CURRENT_DIR%'; $Shortcut.Arguments = '/k python voice_typer.py'; $Shortcut.Description = 'Voice Typer - Voice to Text Application'; $Shortcut.IconLocation = 'python.exe,0'; $Shortcut.Save()"

if exist "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Voice Typer\Voice Typer.lnk" (
    echo ✓ Start Menu shortcut created successfully!
) else (
    echo ✗ Failed to create Start Menu shortcut
)

echo.
echo =================================
echo Shortcuts created successfully!
echo =================================
echo.
echo Desktop shortcut: %PUBLIC%\Desktop\Voice Typer.lnk
echo Start Menu shortcut: %APPDATA%\Microsoft\Windows\Start Menu\Programs\Voice Typer\Voice Typer.lnk
echo.
echo To pin to taskbar:
echo 1. Right-click the desktop shortcut
echo 2. Select "Pin to taskbar"
echo.
echo Or:
echo 1. Open Start Menu
echo 2. Search for "Voice Typer"
echo 3. Right-click and select "Pin to taskbar"
echo.
pause

# Installation Troubleshooting Guide

This guide helps you resolve common installation issues with Voice Typer on Windows.

## Common Error Messages and Solutions

### 1. "Python is not installed or not in PATH"

**Error**: `'python' is not recognized as an internal or external command`

**Solution**:
1. Download Python from [python.org](https://python.org)
2. During installation, **check "Add Python to PATH"**
3. Restart Command Prompt after installation
4. Verify with: `python --version`

### 2. PyAudio Installation Errors

**Error**: `Microsoft Visual C++ 14.0 is required`

**Solutions** (try in order):

#### Option A: Use pipwin (Recommended)
```cmd
pip install pipwin
pipwin install pyaudio
```

#### Option B: Download Pre-compiled Wheel
1. Go to [Python Extension Packages](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio)
2. Download the correct wheel for your Python version and Windows architecture
3. Install with: `pip install PyAudio-0.2.11-cp39-cp39-win_amd64.whl`

#### Option C: Install Visual C++ Build Tools
1. Download [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
2. Install with "C++ build tools" workload
3. Restart Command Prompt and try again

### 3. Permission Errors

**Error**: `Permission denied` or `Access is denied`

**Solutions**:

#### Option A: Use --user flag
```cmd
pip install --user -r requirements.txt
```

#### Option B: Run as Administrator
1. Right-click Command Prompt
2. Select "Run as administrator"
3. Try installation again

#### Option C: Use Virtual Environment
```cmd
python -m venv voice_typer_env
voice_typer_env\Scripts\activate
pip install -r requirements.txt
```

### 4. Network/Proxy Issues

**Error**: `Could not find a version that satisfies the requirement`

**Solutions**:

#### Option A: Use Different Index
```cmd
pip install -i https://pypi.org/simple/ -r requirements.txt
```

#### Option B: Configure Proxy
```cmd
pip install --proxy http://proxy.company.com:8080 -r requirements.txt
```

#### Option C: Offline Installation
1. Download packages on another computer with internet
2. Transfer to target computer
3. Install with: `pip install --no-index --find-links . -r requirements.txt`

### 5. Google Cloud Speech Installation Issues

**Error**: `google-cloud-speech` installation fails

**Solutions**:

#### Option A: Install Google Cloud SDK First
1. Download [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)
2. Install and authenticate
3. Try installing the Python package again

#### Option B: Install Dependencies Separately
```cmd
pip install google-auth google-auth-oauthlib google-auth-httplib2
pip install google-cloud-speech
```

### 6. Keyboard/PyAutoGUI Permission Issues

**Error**: `Access denied` when trying to use global hotkeys

**Solutions**:

#### Option A: Run as Administrator
- Right-click Command Prompt → "Run as administrator"
- Run the application from elevated prompt

#### Option B: Grant Permissions
1. Go to Windows Settings → Privacy & Security
2. Allow apps to access microphone
3. Allow apps to run in background

### 7. Microphone Access Issues

**Error**: `Failed to initialize audio`

**Solutions**:

#### Check Microphone Permissions
1. Windows Settings → Privacy & Security → Microphone
2. Allow desktop apps to access microphone
3. Ensure Voice Typer is in the allowed list

#### Test Microphone
1. Windows Settings → System → Sound
2. Test your microphone
3. Ensure it's set as default recording device

## Step-by-Step Recovery Process

If you're still having issues, follow this recovery process:

### Step 1: Clean Installation
```cmd
pip uninstall google-cloud-speech pyaudio pynput keyboard pyautogui configparser pyinstaller
pip cache purge
```

### Step 2: Use Alternative Installation Script
```cmd
install_dependencies_alternative.bat
```

### Step 3: Manual Installation
If automated scripts fail, install manually:

```cmd
# Install each package individually
pip install --user google-cloud-speech
pip install --user pynput
pip install --user keyboard
pip install --user pyautogui
pip install --user configparser
pip install --user pyinstaller

# For PyAudio, use pipwin
pip install --user pipwin
pipwin install pyaudio
```

### Step 4: Test Installation
```cmd
python test_voice_typer.py
```

## System Requirements Check

Before installation, verify your system meets requirements:

### Python Version
```cmd
python --version
```
**Required**: Python 3.8 or later

### Windows Version
```cmd
winver
```
**Required**: Windows 10 or later

### Architecture
```cmd
echo %PROCESSOR_ARCHITECTURE%
```
**Note**: Download correct PyAudio wheel for your architecture (x64 or x86)

## Getting Help

If you're still experiencing issues:

1. **Check the log file**: Look at `voice_typer.log` for detailed error messages
2. **Run the test suite**: `python test_voice_typer.py` to identify specific issues
3. **Check Windows Event Viewer**: Look for system-level errors
4. **Try a different Python version**: Some packages work better with specific Python versions

## Alternative Installation Methods

### Using Conda
```cmd
conda install -c conda-forge pyaudio
pip install google-cloud-speech pynput keyboard pyautogui configparser pyinstaller
```

### Using Chocolatey
```cmd
choco install python
pip install -r requirements.txt
```

### Using Windows Subsystem for Linux (WSL)
```bash
sudo apt update
sudo apt install python3-pip portaudio19-dev
pip3 install -r requirements.txt
```

## Prevention Tips

1. **Always run Command Prompt as Administrator** for system-wide installations
2. **Use virtual environments** to avoid conflicts
3. **Keep pip updated**: `python -m pip install --upgrade pip`
4. **Install Visual C++ Build Tools** before installing packages that need compilation
5. **Check Windows Defender** - it might block some installations

## Still Having Issues?

If none of these solutions work:

1. Try installing on a different computer to isolate the issue
2. Use a different Python version (3.8, 3.9, or 3.10)
3. Check if your antivirus is blocking the installation
4. Try installing in a clean Windows user account
5. Consider using a virtual machine with a fresh Windows installation

# Voice Typer - Complete Setup Guide

Voice Typer is a desktop application that allows you to use voice input to type text into any application on Windows. Simply press a global hotkey and start speaking - your words will be transcribed and typed automatically.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Google Cloud Setup](#google-cloud-setup)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Usage](#usage)
6. [Building Executable](#building-executable)
7. [Troubleshooting](#troubleshooting)
8. [Advanced Configuration](#advanced-configuration)

## Prerequisites

### System Requirements
- Windows 10 or later
- Python 3.8 or later
- Microphone (built-in or external)
- Internet connection (for Google Cloud Speech-to-Text)

### Software Requirements
- Python 3.8+ installed from [python.org](https://python.org)
- Git (optional, for cloning the repository)

## Google Cloud Setup

### Step 1: Create a Google Cloud Project

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Sign in with your Google account
3. Click "Select a project" → "New Project"
4. Enter a project name (e.g., "voice-typer")
5. Click "Create"

### Step 2: Enable Speech-to-Text API

1. In the Google Cloud Console, go to "APIs & Services" → "Library"
2. Search for "Speech-to-Text API"
3. Click on "Cloud Speech-to-Text API"
4. Click "Enable"

### Step 3: Create Service Account

1. Go to "IAM & Admin" → "Service Accounts"
2. Click "Create Service Account"
3. Enter a name (e.g., "voice-typer-service")
4. Click "Create and Continue"
5. For roles, select "Cloud Speech-to-Text Client"
6. Click "Continue" → "Done"

### Step 4: Download Credentials

1. Find your service account in the list
2. Click on the service account email
3. Go to the "Keys" tab
4. Click "Add Key" → "Create new key"
5. Select "JSON" format
6. Click "Create"
7. Save the downloaded file as `credentials.json` in your Voice Typer directory

### Step 5: Set Up Billing (Required)

⚠️ **Important**: Google Cloud Speech-to-Text requires billing to be enabled, even for the free tier.

1. Go to "Billing" in the Google Cloud Console
2. Link a billing account to your project
3. The free tier includes 60 minutes of audio per month

## Installation

### Method 1: Automatic Installation (Recommended)

1. Download or clone this repository
2. Open Command Prompt as Administrator
3. Navigate to the Voice Typer directory
4. Run the installation script:
   ```cmd
   install_dependencies.bat
   ```

### Method 2: Manual Installation

1. Open Command Prompt as Administrator
2. Navigate to the Voice Typer directory
3. Install dependencies:
   ```cmd
   pip install -r requirements.txt
   ```

### Troubleshooting Installation Issues

#### PyAudio Installation Issues
If you encounter errors installing PyAudio:

1. **Option 1**: Install pre-compiled wheel:
   ```cmd
   pip install pipwin
   pipwin install pyaudio
   ```

2. **Option 2**: Download wheel from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio)
   ```cmd
   pip install PyAudio-0.2.11-cp39-cp39-win_amd64.whl
   ```

#### Visual C++ Build Tools
If you get compilation errors:
1. Download and install [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
2. Restart Command Prompt and try again

## Configuration

### Basic Configuration

The application will create a `config.ini` file on first run. You can edit this file to customize settings:

```ini
[General]
hotkey = `
language = en-US
google_credentials_file = credentials.json

[Audio]
microphone_device = 
sample_rate = 16000
chunk_size = 1024

[Google]
project_id = your-project-id
region = us-central1
```

### Configuration Options

#### Hotkey Configuration
- **hotkey**: Global keyboard shortcut (default: `)
- Common alternatives: `ctrl+shift+v`, `f9`, `ctrl+alt+space`

#### Language Settings
- **language**: Speech recognition language code
- Examples: `en-US`, `en-GB`, `es-ES`, `fr-FR`, `de-DE`, `ja-JP`

#### Audio Settings
- **microphone_device**: Leave empty for default microphone
- **sample_rate**: Audio sample rate (16000 recommended)
- **chunk_size**: Audio buffer size (1024 recommended)

## Usage

### Starting the Application

1. Place your `credentials.json` file in the Voice Typer directory
2. Run the application:
   ```cmd
   python voice_typer.py
   ```

### Using Voice Recognition

1. **Start Recognition**: Press the backtick key (`) or your configured hotkey
2. **Speak**: Start speaking clearly into your microphone
3. **Stop Recognition**: Press the hotkey again or wait for silence
4. **Text Input**: The transcribed text will be typed into the currently focused input field

### Supported Applications

Voice Typer works with any application that accepts text input:
- Web browsers (Chrome, Firefox, Edge)
- Microsoft Word, Notepad, WordPad
- Chat applications (Discord, Slack, Teams)
- Code editors (VS Code, Notepad++)
- Email clients
- And many more!

### Tips for Best Results

1. **Speak Clearly**: Enunciate words clearly and speak at a moderate pace
2. **Reduce Background Noise**: Use a quiet environment or noise-canceling microphone
3. **Pause Between Sentences**: Allow brief pauses for better recognition
4. **Use Punctuation Commands**: Say "period", "comma", "question mark" for punctuation

## Building Executable

### Automatic Build

Run the build script to create a standalone executable:

```cmd
python build.py
```

This will create:
- `dist/VoiceTyper.exe` - Standalone executable
- `installer/` directory - Installation package

### Manual Build with PyInstaller

```cmd
pyinstaller --onefile --windowed --name=VoiceTyper voice_typer.py
```

### Distributing the Application

1. Copy the `installer/` directory to the target computer
2. Ensure the user has `credentials.json` in the same directory
3. Run `VoiceTyper.exe`

## Troubleshooting

### Common Issues

#### "Google Cloud credentials file not found"
- Ensure `credentials.json` is in the same directory as the application
- Check that the file is not corrupted

#### "Failed to initialize audio"
- Check that your microphone is connected and working
- Try running as Administrator
- Check Windows microphone permissions

#### "Failed to register hotkey"
- Try a different hotkey in the configuration
- Ensure no other application is using the same hotkey
- Run as Administrator

#### "Recognition not working"
- Check your internet connection
- Verify Google Cloud billing is enabled
- Check the language setting matches your speech

#### "Text not being typed"
- Ensure the target application is focused
- Try clicking in the text field before using voice recognition
- Some applications may block automated input

### Debug Mode

Run with debug logging:
```cmd
python voice_typer.py
```

Check the `voice_typer.log` file for detailed error information.

### Audio Device Issues

1. **List Available Devices**: The application will show available microphones on startup
2. **Change Device**: Edit `config.ini` and set `microphone_device` to the desired index
3. **Test Microphone**: Use Windows Sound settings to test your microphone

### Performance Issues

1. **High CPU Usage**: Reduce `chunk_size` in configuration
2. **Audio Lag**: Increase `chunk_size` in configuration
3. **Recognition Delay**: Check internet connection speed

## Advanced Configuration

### Custom Language Models

For better accuracy with specific terminology:

1. Go to Google Cloud Console → Speech-to-Text → Custom Classes
2. Create custom classes for domain-specific terms
3. Update the recognition configuration in the code

### Multiple Microphone Support

To use a specific microphone:

1. Run the application to see available devices
2. Note the device index number
3. Set `microphone_device` in `config.ini` to that number

### Network Configuration

For corporate networks with proxies:

1. Set environment variables:
   ```cmd
   set HTTP_PROXY=http://proxy.company.com:8080
   set HTTPS_PROXY=http://proxy.company.com:8080
   ```

### Security Considerations

1. **Credentials**: Never share your `credentials.json` file
2. **Permissions**: The service account only needs Speech-to-Text access
3. **Billing**: Monitor your Google Cloud usage to avoid unexpected charges

## Support

### Getting Help

1. Check the `voice_typer.log` file for error details
2. Verify all prerequisites are met
3. Test with a simple application like Notepad first

### Reporting Issues

When reporting issues, please include:
- Windows version
- Python version
- Error messages from the log file
- Steps to reproduce the problem

### Contributing

This is an open-source project. Contributions are welcome:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License

This project is provided as-is for educational and personal use. Please ensure compliance with Google Cloud terms of service and local regulations regarding voice recording and data processing.

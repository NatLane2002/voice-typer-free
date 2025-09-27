# Voice Typer

A powerful desktop application for Windows that enables voice-to-text input in any application using Google Cloud Speech-to-Text API.

## Features

- 🎤 **Real-time Speech Recognition**: Uses Google Cloud Speech-to-Text for accurate transcription
- ⌨️ **Global Hotkey Support**: Press ` (backtick) to start/stop voice recognition from anywhere
- 🎯 **Universal Text Input**: Works with any application that accepts text input
- 🔧 **Configurable Settings**: Customize hotkey, language, microphone, and more
- 📦 **Standalone Executable**: Build a single .exe file for easy distribution
- 🛡️ **Error Handling**: Comprehensive error handling and logging

## Quick Start

1. **Install Dependencies**:
   ```cmd
   install_dependencies.bat
   ```

2. **Set up Google Cloud** (see [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed instructions):
   - Create a Google Cloud project
   - Enable Speech-to-Text API
   - Download service account credentials as `credentials.json`

3. **Run the Application**:
   ```cmd
   python voice_typer.py
   ```

4. **Use Voice Recognition**:
   - Press ` (backtick) to start voice recognition
   - Speak clearly into your microphone
   - Press ` again to stop
   - Text will be automatically typed into the focused input field

## Supported Applications

Voice Typer works with any Windows application that accepts text input:

- **Web Browsers**: Chrome, Firefox, Edge, Safari
- **Office Applications**: Microsoft Word, Excel, PowerPoint, Notepad
- **Code Editors**: VS Code, Notepad++, Sublime Text
- **Chat Applications**: Discord, Slack, Microsoft Teams, WhatsApp
- **Email Clients**: Outlook, Thunderbird, Gmail
- **And many more!**

## Configuration

Edit `config.ini` to customize:

```ini
[General]
hotkey = `                    # Global keyboard shortcut
language = en-US             # Speech recognition language
google_credentials_file = credentials.json

[Audio]
microphone_device =          # Leave empty for default
sample_rate = 16000         # Audio quality
chunk_size = 1024          # Buffer size
```

### Supported Languages

- English (US, UK, AU, CA, IN)
- Spanish (ES, MX, AR, CO)
- French (FR, CA)
- German (DE)
- Italian (IT)
- Portuguese (BR, PT)
- Japanese (JP)
- Korean (KR)
- Chinese (CN, TW)
- And many more!

## Building Executable

Create a standalone executable:

```cmd
python build.py
```

This creates:
- `dist/VoiceTyper.exe` - Standalone executable
- `installer/` directory - Ready-to-distribute package

## Requirements

- **Windows 10 or later**
- **Python 3.8+** (for development)
- **Microphone** (built-in or external)
- **Internet connection** (for Google Cloud API)
- **Google Cloud account** (with Speech-to-Text API enabled)

## Installation

### Automatic Installation
```cmd
install_dependencies.bat
```

### Manual Installation
```cmd
pip install -r requirements.txt
```

## Usage Examples

### Basic Usage
1. Open any text application (Notepad, Word, browser)
2. Click in the text field
3. Press ` (backtick) to start voice recognition
4. Speak your text
5. Press ` again to stop
6. Text appears automatically!

### Advanced Usage
- **Punctuation**: Say "period", "comma", "question mark"
- **Numbers**: "one", "two", "three" or "1", "2", "3"
- **Special Characters**: "at symbol", "hash", "dollar sign"
- **Text Shortcuts**: Create custom shortcuts for frequently used text

### Text Shortcuts
Create custom shortcuts for frequently used text:

1. **Manage shortcuts**: `python manage_shortcuts.py`
2. **Add shortcut**: `add email myemail@example.com`
3. **Use shortcut**: Say "email" to insert your email address
4. **List shortcuts**: `list` to see all configured shortcuts
5. **Remove shortcut**: `remove email` to delete a shortcut

**Example shortcuts:**
- `email` → "myemail@example.com"
- `signature` → "Best regards, John"
- `address` → "123 Main Street, City, State 12345"

## Audio Input Selection

### How Audio Input is Selected

The Voice Typer application automatically detects and lists all available audio input devices when it starts. Here's how it works:

1. **Automatic Detection**: The app scans for all audio devices with input capabilities
2. **Device Listing**: All available microphones are displayed with their index numbers
3. **Default Selection**: If no specific device is configured, the system default microphone is used
4. **Manual Selection**: You can specify a device by editing `config.ini` and setting the `microphone_device` value

**Example device list:**
```
Available audio devices:
  0: Microsoft Sound Mapper - Input (inputs: 2)
  1: Microphone (MR02 Audio) (inputs: 1)
  2: Headset Microphone (Oculus Virtual Audio Device) (inputs: 1)
  3: CABLE Output (VB-Audio Virtual Cable) (inputs: 16)
```

**To use a specific microphone:**
1. Note the device index number from the list
2. Edit `config.ini` and set `microphone_device = 1` (for example)
3. Restart the application

## Troubleshooting

### Common Issues

**"Credentials file not found"**
- Ensure `credentials.json` is in the same directory as the application

**"Audio initialization failed"**
- Check microphone permissions in Windows Settings
- Try running as Administrator
- Verify microphone is working in other applications

**"Hotkey not working"**
- Try a different hotkey in `config.ini`
- Ensure no other application is using the same hotkey
- Run as Administrator

**"Text not being typed"**
- Click in the target text field before using voice recognition
- Some applications may block automated input

### Debug Mode
Check `voice_typer.log` for detailed error information.

## Security & Privacy

- **Local Processing**: Audio is streamed to Google Cloud for transcription
- **No Storage**: Audio is not stored locally or on Google's servers
- **Secure Credentials**: Service account credentials are stored locally only
- **Minimal Permissions**: Only requires Speech-to-Text API access

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is provided as-is for educational and personal use. Please ensure compliance with Google Cloud terms of service and local regulations.

## Support

For detailed setup instructions, troubleshooting, and advanced configuration, see [SETUP_GUIDE.md](SETUP_GUIDE.md).

## Changelog

### Version 1.0.0
- Initial release
- Google Cloud Speech-to-Text integration
- Global hotkey support
- Universal text input
- Configuration system
- Standalone executable build
- Comprehensive error handling

---

**Made with ❤️ for productivity and accessibility**

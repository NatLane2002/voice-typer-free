#!/usr/bin/env python3
"""
Voice Typer - A desktop application for voice-to-text input using Google Cloud Speech-to-Text
"""

import configparser
import json
import logging
import os
import select
import sys
import threading
import time
from typing import Any, Dict, Optional

import keyboard
# Third-party imports
import pyaudio
import pyautogui
from google.cloud import speech
from google.oauth2 import service_account

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('voice_typer.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class VoiceTyper:
    def __init__(self, config_file: str = "config.ini"):
        """Initialize the Voice Typer application"""
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        self.load_config()
        
        # Audio settings
        self.audio_format = pyaudio.paInt16
        self.channels = 1
        self.rate = 16000
        self.chunk_size = 1024
        self.audio = None
        self.stream = None
        
        # Speech recognition
        self.speech_client = None
        self.recognizing = False
        self.recognition_thread = None
        self.accumulated_text = ""  # Store accumulated text for continuous typing
        
        # Stream restart mechanism to bypass 305-second limit
        self.stream_start_time = None
        self.max_stream_duration = 300  # Restart stream 5 seconds before the 305-second limit
        self.stream_restart_in_progress = False
        
        # Hotkey settings
        self.hotkey = self.config.get('General', 'hotkey', fallback='`')
        self.hotkey_registered = False
        
        # Language settings
        self.language_code = self.config.get('General', 'language', fallback='en-US')
        
        # Microphone device
        mic_device_str = self.config.get('Audio', 'microphone_device', fallback='')
        self.microphone_device = int(mic_device_str) if mic_device_str.strip() else None
        
        # Text shortcuts
        self.text_shortcuts = self._load_text_shortcuts()
        
        # Interactive command system
        self.command_mode = False
        self.running = True
        
        # Voice Typer initialized
    
    def load_config(self):
        """Load configuration from file"""
        if os.path.exists(self.config_file):
            self.config.read(self.config_file)
        else:
            self.create_default_config()
    
    def create_default_config(self):
        """Create default configuration file"""
        self.config['General'] = {
            'hotkey': '`',
            'language': 'en-US',
            'google_credentials_file': 'credentials.json'
        }
        self.config['Audio'] = {
            'microphone_device': '',
            'sample_rate': '16000',
            'chunk_size': '1024'
        }
        self.config['Google'] = {
            'project_id': '',
            'region': 'us-central1'
        }
        
        with open(self.config_file, 'w') as f:
            self.config.write(f)
        
        logger.info(f"Created default configuration file: {self.config_file}")
    
    def _load_text_shortcuts(self):
        """Load text shortcuts from configuration file"""
        shortcuts = {}
        try:
            if 'Shortcuts' in self.config:
                for key, value in self.config['Shortcuts'].items():
                    shortcuts[key.lower()] = value
        except Exception as e:
            logger.error(f"Error loading text shortcuts: {e}")
        return shortcuts
    
    def _save_text_shortcuts(self):
        """Save text shortcuts to configuration file"""
        try:
            if 'Shortcuts' not in self.config:
                self.config.add_section('Shortcuts')
            
            # Clear existing shortcuts
            self.config.remove_section('Shortcuts')
            self.config.add_section('Shortcuts')
            
            # Add current shortcuts
            for key, value in self.text_shortcuts.items():
                self.config.set('Shortcuts', key, value)
            
            with open(self.config_file, 'w') as f:
                self.config.write(f)
            
            logger.info("Text shortcuts saved to configuration")
        except Exception as e:
            logger.error(f"Error saving text shortcuts: {e}")
    
    def add_text_shortcut(self, trigger_word: str, replacement_text: str):
        """Add a new text shortcut"""
        try:
            self.text_shortcuts[trigger_word.lower()] = replacement_text
            self._save_text_shortcuts()
            logger.info(f"Added shortcut: '{trigger_word}' -> '{replacement_text}'")
            return True
        except Exception as e:
            logger.error(f"Error adding text shortcut: {e}")
            return False
    
    def remove_text_shortcut(self, trigger_word: str):
        """Remove a text shortcut"""
        try:
            if trigger_word.lower() in self.text_shortcuts:
                del self.text_shortcuts[trigger_word.lower()]
                self._save_text_shortcuts()
                logger.info(f"Removed shortcut: '{trigger_word}'")
                return True
            else:
                logger.warning(f"Shortcut '{trigger_word}' not found")
                return False
        except Exception as e:
            logger.error(f"Error removing text shortcut: {e}")
            return False
    
    def list_text_shortcuts(self):
        """List all current text shortcuts"""
        if not self.text_shortcuts:
            return "No text shortcuts configured."
        
        result = "Current text shortcuts:\n"
        for trigger, replacement in self.text_shortcuts.items():
            result += f"  '{trigger}' -> '{replacement}'\n"
        return result
    
    def setup_google_cloud(self):
        """Setup Google Cloud Speech-to-Text client"""
        # First try to use embedded credentials
        embedded_credentials = self._get_embedded_credentials()
        if embedded_credentials:
            try:
                credentials = service_account.Credentials.from_service_account_info(
                    embedded_credentials,
                    scopes=['https://www.googleapis.com/auth/cloud-platform']
                )
                
                self.speech_client = speech.SpeechClient(credentials=credentials)
                # Google Cloud Speech-to-Text client initialized
                return True
                
            except Exception as e:
                logger.error(f"Failed to initialize Google Cloud client with embedded credentials: {e}")
                logger.info("Falling back to external credentials file...")
        
        # Fallback to external credentials file
        credentials_file = self.config.get('General', 'google_credentials_file', fallback='credentials.json')
        
        if not os.path.exists(credentials_file):
            logger.error(f"Google Cloud credentials file not found: {credentials_file}")
            logger.error("Please download your service account JSON key and save it as 'credentials.json'")
            return False
        
        try:
            credentials = service_account.Credentials.from_service_account_file(
                credentials_file,
                scopes=['https://www.googleapis.com/auth/cloud-platform']
            )
            
            self.speech_client = speech.SpeechClient(credentials=credentials)
            # Google Cloud Speech-to-Text client initialized
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize Google Cloud client: {e}")
            return False
    
    def _get_embedded_credentials(self):
        """Get embedded Google Cloud credentials"""
        try:
            # Import the embedded credentials module
            import embedded_credentials
            return embedded_credentials.GOOGLE_CLOUD_CREDENTIALS
        except ImportError:
            logger.debug("No embedded credentials module found")
            return None
        except Exception as e:
            logger.debug(f"Error loading embedded credentials: {e}")
            return None
    
    def setup_audio(self):
        """Setup audio input"""
        try:
            self.audio = pyaudio.PyAudio()
            
            # Show only the device being used
            device_index = self.microphone_device if self.microphone_device is not None else None
            if device_index is not None:
                info = self.audio.get_device_info_by_index(device_index)
                logger.info(f"Using microphone: {info['name']}")
            else:
                # Find default microphone
                for i in range(self.audio.get_device_count()):
                    info = self.audio.get_device_info_by_index(i)
                    if info['maxInputChannels'] > 0:
                        logger.info(f"Using default microphone: {info['name']}")
                        break
            
            # Use specified device or default
            device_index = self.microphone_device if self.microphone_device is not None else None
            
            # Create stream without callback - we'll read manually
            self.stream = self.audio.open(
                format=self.audio_format,
                channels=self.channels,
                rate=self.rate,
                input=True,
                input_device_index=device_index,
                frames_per_buffer=self.chunk_size
            )
            
            # Audio input initialized
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize audio: {e}")
            return False
    
    
    def start_recognition(self):
        """Start speech recognition"""
        if self.recognizing:
            return
        
        if not self.speech_client:
            logger.error("Google Cloud client not initialized")
            return
        
        # Reset accumulated text for new recognition session
        self.accumulated_text = ""
        
        # Initialize stream timing
        self.stream_start_time = time.time()
        self.stream_restart_in_progress = False
        
        self.recognizing = True
        self.recognition_thread = threading.Thread(target=self._recognition_loop)
        self.recognition_thread.daemon = True
        self.recognition_thread.start()
        
        print("🎤 ACTIVE")
    
    def stop_recognition(self):
        """Pause speech recognition (don't stop the application)"""
        if not self.recognizing:
            return
        
        self.recognizing = False
        if self.recognition_thread:
            self.recognition_thread.join(timeout=2)
        
        print("⏸️  INACTIVE")
    
    def _recognition_loop(self):
        """Main recognition loop with automatic stream restart to bypass 305-second limit"""
        while self.recognizing:
            try:
                # Check if we need to restart the stream due to duration limit
                if (self.stream_start_time and 
                    time.time() - self.stream_start_time >= self.max_stream_duration):
                    logger.info("Stream duration limit approaching, restarting stream...")
                    self._restart_stream()
                    continue
                
                # Configure recognition
                config = speech.RecognitionConfig(
                    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                    sample_rate_hertz=self.rate,
                    language_code=self.language_code,
                    enable_automatic_punctuation=False,
                    model='latest_long'
                )
                
                streaming_config = speech.StreamingRecognitionConfig(
                    config=config,
                    interim_results=True,
                    single_utterance=False  # Changed to False to allow continuous streaming
                )
                
                # Start streaming recognition
                audio_generator = self._audio_generator()
                requests = (speech.StreamingRecognizeRequest(audio_content=chunk) 
                           for chunk in audio_generator)
                
                responses = self.speech_client.streaming_recognize(streaming_config, requests)
                
                for response in responses:
                    if not self.recognizing:
                        break
                    
                    # Check if we need to restart stream during processing
                    if (self.stream_start_time and 
                        time.time() - self.stream_start_time >= self.max_stream_duration):
                        logger.info("Stream duration limit reached during processing, restarting...")
                        break  # Exit this loop to restart the stream
                    
                    for result in response.results:
                        if result.is_final:
                            transcript = result.alternatives[0].transcript
                            
                            # Type each final result immediately with continuous typing
                            if transcript.strip():
                                self._type_text(transcript.strip(), is_continuous=True)
                        # Removed interim transcript logging to reduce clutter
                
                # If we exit the response loop due to duration limit, restart
                if (self.stream_start_time and 
                    time.time() - self.stream_start_time >= self.max_stream_duration):
                    self._restart_stream()
                    continue
                
                # If we exit normally (not due to duration limit), break the main loop
                break
                
            except Exception as e:
                error_msg = str(e)
                if "305 seconds" in error_msg or "maximum allowed stream duration" in error_msg:
                    logger.info("Hit 305-second limit, restarting stream automatically...")
                    self._restart_stream()
                    continue
                else:
                    logger.error(f"Recognition error: {e}")
                    break
        
        # Only set recognizing to False if we're not restarting
        if not self.stream_restart_in_progress:
            self.recognizing = False
    
    def _restart_stream(self):
        """Restart the speech recognition stream to bypass 305-second limit"""
        self.stream_restart_in_progress = True
        
        # Reset the stream start time for the new stream
        self.stream_start_time = time.time()
        
        # Log the restart
        logger.info("Restarting speech recognition stream to bypass duration limit")
        
        # Reset the restart flag
        self.stream_restart_in_progress = False
        
        # Continue with the main recognition loop
        return
    
    def _audio_generator(self):
        """Generate audio chunks for streaming"""
        while self.recognizing and self.stream:
            try:
                # Read audio data from the stream
                data = self.stream.read(self.chunk_size, exception_on_overflow=False)
                if data:
                    yield data
                else:
                    # No data available, small delay to prevent busy waiting
                    time.sleep(0.01)
            except Exception as e:
                logger.error(f"Audio generation error: {e}")
                break
    
    def _process_text(self, text: str):
        """Process text to handle punctuation commands and spacing"""
        # Replace punctuation commands with actual punctuation
        processed_text = text
        
        # Handle period command
        processed_text = processed_text.replace(" period", ".")
        processed_text = processed_text.replace("period", ".")
        
        # Handle comma command
        processed_text = processed_text.replace(" comma", ",")
        processed_text = processed_text.replace("comma", ",")
        
        # Handle other common punctuation commands
        processed_text = processed_text.replace(" question mark", "?")
        processed_text = processed_text.replace("question mark", "?")
        processed_text = processed_text.replace(" exclamation mark", "!")
        processed_text = processed_text.replace("exclamation mark", "!")
        processed_text = processed_text.replace(" slash", "/")
        processed_text = processed_text.replace("slash", "/")
        
        # Clean up any double spaces
        processed_text = " ".join(processed_text.split())
        
        return processed_text
    
    
    def _type_text(self, text: str, is_continuous: bool = True):
        """Type text into the active input field"""
        try:
            # Initialize variables
            is_punctuation_command = False
            is_text_shortcut = False
            
            # Check if this is a text shortcut BEFORE processing
            if text.strip().lower() in self.text_shortcuts:
                # Replace with shortcut text
                processed_text = self.text_shortcuts[text.strip().lower()]
                is_text_shortcut = True
            else:
                # Check if this is a punctuation command BEFORE processing
                punctuation_commands = ["period", "comma", "question mark", "exclamation mark", "slash"]
                is_punctuation_command = any(text.strip().lower() == cmd for cmd in punctuation_commands)
                
                # Process the text to handle punctuation commands
                processed_text = self._process_text(text)
            
            # Handle spacing and capitalization if this is continuous typing
            if is_continuous:
                # Apply spacing logic
                if is_punctuation_command:
                    # Punctuation commands must be appended directly to the last word
                    # Don't add any space before punctuation commands
                    pass
                elif is_text_shortcut:
                    # Text shortcuts should have proper spacing
                    if (self.accumulated_text and 
                        (self.accumulated_text[-1].isalnum() or self.accumulated_text[-1] in ".,!?;:/") and
                        not processed_text.startswith(" ") and 
                        not self.accumulated_text.endswith(" ")):
                        processed_text = " " + processed_text
                else:
                    # Only add space if there's already text and the last character is a letter or punctuation
                    if (self.accumulated_text and 
                        (self.accumulated_text[-1].isalnum() or self.accumulated_text[-1] in ".,!?;:/") and
                        not processed_text.startswith(" ") and 
                        not self.accumulated_text.endswith(" ")):
                        processed_text = " " + processed_text
                
                # Apply capitalization after sentence endings
                if processed_text and processed_text[0].isalpha():
                    # Check if we're after sentence-ending punctuation
                    should_capitalize = False
                    
                    if self.accumulated_text:
                        # Check if we're after sentence-ending punctuation
                        if (len(self.accumulated_text) >= 2 and 
                            self.accumulated_text[-2:] in [". ", "! ", "? "]) or \
                           (len(self.accumulated_text) >= 1 and 
                            self.accumulated_text[-1] in ".!?"):
                            should_capitalize = True
                    else:
                        # This is the very first word, capitalize it
                        should_capitalize = True
                    
                    if should_capitalize:
                        processed_text = processed_text[0].upper() + processed_text[1:]
                
                # Update accumulated text
                self.accumulated_text += processed_text
            
            # No delay for maximum speed
            # Ensure we have focus on the current window
            current_window = pyautogui.getActiveWindow()
            if current_window:
                current_window.activate()
            
            # Type the processed text with no interval for maximum speed
            pyautogui.typewrite(processed_text, interval=0)
            
        except Exception as e:
            logger.error(f"Failed to type text: {e}")
            # Try alternative method
            try:
                import pyperclip

                # Initialize variables for alternative method
                is_punctuation_command = False
                is_text_shortcut = False
                
                # Check if this is a text shortcut BEFORE processing
                if text.strip().lower() in self.text_shortcuts:
                    processed_text = self.text_shortcuts[text.strip().lower()]
                    is_text_shortcut = True
                else:
                    # Check if this is a punctuation command BEFORE processing
                    punctuation_commands = ["period", "comma", "question mark", "exclamation mark", "slash"]
                    is_punctuation_command = any(text.strip().lower() == cmd for cmd in punctuation_commands)
                    processed_text = self._process_text(text)
                
                if is_continuous:
                    # Apply the same logic as above
                    if not is_punctuation_command:
                        # Only add space if there's already text and the last character is a letter or punctuation
                        if (self.accumulated_text and 
                            (self.accumulated_text[-1].isalnum() or self.accumulated_text[-1] in ".,!?;:/") and
                            not processed_text.startswith(" ") and 
                            not self.accumulated_text.endswith(" ")):
                            processed_text = " " + processed_text
                    
                    if processed_text and processed_text[0].isalpha():
                        should_capitalize = False
                        
                        if self.accumulated_text:
                            if (len(self.accumulated_text) >= 2 and 
                                self.accumulated_text[-2:] in [". ", "! ", "? "]) or \
                               (len(self.accumulated_text) >= 1 and 
                                self.accumulated_text[-1] in ".!?"):
                                should_capitalize = True
                        else:
                            should_capitalize = True
                        
                        if should_capitalize:
                            processed_text = processed_text[0].upper() + processed_text[1:]
                    
                    self.accumulated_text += processed_text
                pyperclip.copy(processed_text)
                pyautogui.hotkey('ctrl', 'v')
            except Exception as e2:
                logger.error(f"Alternative typing method also failed: {e2}")
    
    def toggle_recognition(self):
        """Toggle speech recognition on/off"""
        if self.recognizing:
            self.stop_recognition()
        else:
            self.start_recognition()
    
    def register_hotkey(self):
        """Register global hotkey"""
        try:
            # Use suppress=True to prevent the backtick from appearing in input
            keyboard.add_hotkey(self.hotkey, self.toggle_recognition, suppress=True)
            self.hotkey_registered = True
            # Global hotkey registered
        except Exception as e:
            logger.error(f"Failed to register hotkey: {e}")
    
    def unregister_hotkey(self):
        """Unregister global hotkey"""
        try:
            keyboard.unhook_all_hotkeys()
            self.hotkey_registered = False
            # Global hotkey unregistered
        except Exception as e:
            logger.error(f"Failed to unregister hotkey: {e}")
    
    def show_menu(self):
        """Show the main application menu"""
        print("\n" + "="*50)
        print("🎤 VOICE TYPER")
        print("="*50)
        print("Press ` (backtick) to start/stop voice recognition")
        print("Type 'shortcuts' to manage text shortcuts")
        print("Type 'devices' to list audio devices")
        print("Type 'help' for all commands")
        print("Type 'exit' or press Ctrl+C to quit")
        print("="*50)
    
    def show_help(self):
        """Show help information"""
        print("\n" + "="*50)
        print("📖 VOICE TYPER HELP")
        print("="*50)
        print("Voice Commands:")
        print("  ` (backtick)     - Start/stop voice recognition")
        print("")
        print("Terminal Commands:")
        print("  shortcuts        - Manage text shortcuts")
        print("  devices          - List available audio devices")
        print("  help             - Show this help")
        print("  exit             - Exit application")
        print("")
        print("Shortcut Commands (when in shortcuts mode):")
        print("  add <word> <text>    - Add new shortcut")
        print("  remove <word>        - Remove shortcut")
        print("  list                 - List all shortcuts")
        print("  back                 - Return to main menu")
        print("="*50)
    
    def handle_command(self, command):
        """Handle user commands"""
        cmd = command.strip().lower()
        
        if cmd == "help":
            self.show_help()
        elif cmd == "shortcuts":
            self.manage_shortcuts()
        elif cmd == "devices":
            self.list_audio_devices()
        elif cmd == "exit" or cmd == "quit":
            print("👋 Goodbye!")
            self.running = False
        elif cmd == "":
            # Empty command, do nothing
            pass
        else:
            print(f"❌ Unknown command: '{cmd}'")
            print("💡 Type 'help' for available commands")
    
    def manage_shortcuts(self):
        """Interactive shortcut management"""
        print("\n" + "="*50)
        print("📝 TEXT SHORTCUTS")
        print("="*50)
        print("Commands:")
        print("  add <trigger> <text>  - Add new shortcut")
        print("  remove <trigger>      - Remove shortcut")
        print("  list                  - List all shortcuts")
        print("  back                  - Return to main menu")
        print("="*50)
        
        while True:
            try:
                command = input("Shortcuts> ").strip()
                
                if not command:
                    continue
                
                parts = command.split(' ', 2)
                cmd = parts[0].lower()
                
                if cmd == "back":
                    break
                elif cmd == "list":
                    print(self.list_text_shortcuts())
                elif cmd == "add":
                    if len(parts) < 3:
                        print("❌ Usage: add <trigger> <text>")
                        print("💡 Example: add email john@example.com")
                    else:
                        trigger = parts[1]
                        text = parts[2]
                        if self.add_text_shortcut(trigger, text):
                            print(f"✅ Added: '{trigger}' -> '{text}'")
                        else:
                            print(f"❌ Failed to add: '{trigger}'")
                elif cmd == "remove":
                    if len(parts) < 2:
                        print("❌ Usage: remove <trigger>")
                        print("💡 Example: remove email")
                    else:
                        trigger = parts[1]
                        if self.remove_text_shortcut(trigger):
                            print(f"✅ Removed: '{trigger}'")
                        else:
                            print(f"❌ Failed to remove: '{trigger}'")
                else:
                    print(f"❌ Unknown command: '{cmd}'")
                    print("💡 Type 'back' to return to main menu")
                    
            except KeyboardInterrupt:
                print("\n💡 Type 'back' to return to main menu")
            except EOFError:
                break
    
    def list_audio_devices(self):
        """List all available audio devices"""
        print("\n" + "="*50)
        print("🎧 AUDIO DEVICES")
        print("="*50)
        
        try:
            if not self.audio:
                self.audio = pyaudio.PyAudio()
            
            device_count = 0
            for i in range(self.audio.get_device_count()):
                info = self.audio.get_device_info_by_index(i)
                if info['maxInputChannels'] > 0:
                    current = " (CURRENT)" if i == self.microphone_device else ""
                    print(f"  {i}: {info['name']}{current}")
                    device_count += 1
            
            if device_count == 0:
                print("❌ No audio input devices found")
            else:
                print(f"\n📊 Found {device_count} audio input device(s)")
                print("💡 To change device, edit config.ini and set microphone_device = <number>")
            
        except Exception as e:
            print(f"❌ Error listing devices: {e}")
        
        print("="*50)
    
    
    def run(self):
        """Run the application with interactive command system"""
        print("🎤 Voice Typer Starting...")
        
        # Setup Google Cloud
        if not self.setup_google_cloud():
            print("❌ Failed to setup Google Cloud. Please check your credentials.")
            return False
        
        # Setup audio
        if not self.setup_audio():
            print("❌ Failed to setup audio. Please check your microphone.")
            return False
        
        # Register hotkey
        self.register_hotkey()
        
        print("✅ Voice Typer ready!")
        self.show_menu()
        
        try:
            # Interactive command loop
            while self.running:
                try:
                    # Check for user input (non-blocking)
                    if select.select([sys.stdin], [], [], 0.1)[0]:
                        command = input().strip()
                        if command:
                            self.handle_command(command)
                except (OSError, AttributeError):
                    # select not available on Windows, use alternative method
                    try:
                        import msvcrt
                        if msvcrt.kbhit():
                            command = input().strip()
                            if command:
                                self.handle_command(command)
                    except ImportError:
                        # Fallback for systems without msvcrt
                        time.sleep(0.1)
                except KeyboardInterrupt:
                    print("\n👋 Shutting down...")
                    self.running = False
                except EOFError:
                    print("\n👋 Goodbye!")
                    self.running = False
                    
        except KeyboardInterrupt:
            print("\n👋 Shutting down...")
        finally:
            self.cleanup()
        
        return True
    
    def cleanup(self):
        """Cleanup resources"""
        self.stop_recognition()
        self.unregister_hotkey()
        
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        
        if self.audio:
            self.audio.terminate()
        
        print("✅ Cleanup completed")

def main():
    """Main entry point"""
    app = VoiceTyper()
    success = app.run()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()

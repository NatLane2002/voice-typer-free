#!/usr/bin/env python3
"""
Test script for Voice Typer application
"""

import os
import sys
import threading
import time
from unittest.mock import Mock, patch


def test_imports():
    """Test that all required modules can be imported"""
    print("Testing imports...")
    
    try:
        import pyaudio
        print("✓ PyAudio imported successfully")
    except ImportError as e:
        print(f"✗ PyAudio import failed: {e}")
        return False
    
    try:
        import keyboard
        print("✓ Keyboard imported successfully")
    except ImportError as e:
        print(f"✗ Keyboard import failed: {e}")
        return False
    
    try:
        import pyautogui
        print("✓ PyAutoGUI imported successfully")
    except ImportError as e:
        print(f"✗ PyAutoGUI import failed: {e}")
        return False
    
    try:
        from google.cloud import speech
        print("✓ Google Cloud Speech imported successfully")
    except ImportError as e:
        print(f"✗ Google Cloud Speech import failed: {e}")
        return False
    
    return True

def test_audio_devices():
    """Test audio device enumeration"""
    print("\nTesting audio devices...")
    
    try:
        import pyaudio
        audio = pyaudio.PyAudio()
        
        print(f"Found {audio.get_device_count()} audio devices:")
        input_devices = []
        
        for i in range(audio.get_device_count()):
            info = audio.get_device_info_by_index(i)
            if info['maxInputChannels'] > 0:
                input_devices.append((i, info['name']))
                print(f"  {i}: {info['name']} (inputs: {info['maxInputChannels']})")
        
        audio.terminate()
        
        if input_devices:
            print(f"✓ Found {len(input_devices)} input devices")
            return True
        else:
            print("✗ No input devices found")
            return False
            
    except Exception as e:
        print(f"✗ Audio device test failed: {e}")
        return False

def test_config_creation():
    """Test configuration file creation"""
    print("\nTesting configuration creation...")
    
    try:
        from voice_typer import VoiceTyper

        # Create a test instance
        app = VoiceTyper("test_config.ini")
        
        if os.path.exists("test_config.ini"):
            print("✓ Configuration file created successfully")
            
            # Clean up
            os.remove("test_config.ini")
            return True
        else:
            print("✗ Configuration file not created")
            return False
            
    except Exception as e:
        print(f"✗ Configuration test failed: {e}")
        return False

def test_google_cloud_setup():
    """Test Google Cloud setup (without actual credentials)"""
    print("\nTesting Google Cloud setup...")
    
    try:
        from voice_typer import VoiceTyper
        
        app = VoiceTyper("test_config.ini")
        
        # Test without credentials file
        result = app.setup_google_cloud()
        
        if not result:
            print("✓ Google Cloud setup correctly failed without credentials")
            return True
        else:
            print("✗ Google Cloud setup should have failed without credentials")
            return False
            
    except Exception as e:
        print(f"✗ Google Cloud test failed: {e}")
        return False
    finally:
        # Clean up
        if os.path.exists("test_config.ini"):
            os.remove("test_config.ini")

def test_hotkey_registration():
    """Test hotkey registration (mock)"""
    print("\nTesting hotkey registration...")
    
    try:
        with patch('keyboard.add_hotkey') as mock_hotkey:
            from voice_typer import VoiceTyper
            
            app = VoiceTyper("test_config.ini")
            app.register_hotkey()
            
            mock_hotkey.assert_called_once()
            print("✓ Hotkey registration test passed")
            return True
            
    except Exception as e:
        print(f"✗ Hotkey test failed: {e}")
        return False
    finally:
        # Clean up
        if os.path.exists("test_config.ini"):
            os.remove("test_config.ini")

def test_text_typing():
    """Test text typing functionality (mock)"""
    print("\nTesting text typing...")
    
    try:
        with patch('pyautogui.typewrite') as mock_typewrite:
            from voice_typer import VoiceTyper
            
            app = VoiceTyper("test_config.ini")
            app._type_text("Hello World")
            
            mock_typewrite.assert_called_once_with("Hello World", interval=0.01)
            print("✓ Text typing test passed")
            return True
            
    except Exception as e:
        print(f"✗ Text typing test failed: {e}")
        return False
    finally:
        # Clean up
        if os.path.exists("test_config.ini"):
            os.remove("test_config.ini")

def run_all_tests():
    """Run all tests"""
    print("Voice Typer - Test Suite")
    print("=" * 40)
    
    tests = [
        test_imports,
        test_audio_devices,
        test_config_creation,
        test_google_cloud_setup,
        test_hotkey_registration,
        test_text_typing
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"✗ Test {test.__name__} crashed: {e}")
    
    print("\n" + "=" * 40)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✓ All tests passed!")
        return True
    else:
        print("✗ Some tests failed!")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

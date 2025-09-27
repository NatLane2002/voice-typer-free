#!/usr/bin/env python3
"""
Test Voice Typer with embedded credentials
==========================================

This script tests the Voice Typer application to ensure
the embedded credentials work correctly.
"""

import os
import sys
import threading
import time
from unittest.mock import patch


def test_embedded_credentials():
    """Test embedded credentials loading"""
    print("Testing embedded credentials...")
    
    try:
        from voice_typer import VoiceTyper

        # Create app instance
        app = VoiceTyper("test_config.ini")
        
        # Test credentials loading
        credentials = app._get_embedded_credentials()
        
        if credentials:
            print("✓ Embedded credentials loaded successfully")
            print(f"  Project ID: {credentials.get('project_id', 'Not found')}")
            print(f"  Client Email: {credentials.get('client_email', 'Not found')}")
            return True
        else:
            print("✗ No embedded credentials found")
            print("  Run setup_credentials.py to embed your credentials")
            return False
            
    except Exception as e:
        print(f"✗ Error testing embedded credentials: {e}")
        return False
    finally:
        # Clean up test config
        if os.path.exists("test_config.ini"):
            os.remove("test_config.ini")

def test_google_cloud_setup():
    """Test Google Cloud client setup"""
    print("\nTesting Google Cloud setup...")
    
    try:
        from voice_typer import VoiceTyper
        
        app = VoiceTyper("test_config.ini")
        
        # Test Google Cloud setup
        success = app.setup_google_cloud()
        
        if success:
            print("✓ Google Cloud client initialized successfully")
            return True
        else:
            print("✗ Google Cloud client initialization failed")
            return False
            
    except Exception as e:
        print(f"✗ Error testing Google Cloud setup: {e}")
        return False
    finally:
        # Clean up test config
        if os.path.exists("test_config.ini"):
            os.remove("test_config.ini")

def test_audio_setup():
    """Test audio setup"""
    print("\nTesting audio setup...")
    
    try:
        from voice_typer import VoiceTyper
        
        app = VoiceTyper("test_config.ini")
        
        # Test audio setup
        success = app.setup_audio()
        
        if success:
            print("✓ Audio system initialized successfully")
            # Clean up audio resources
            if app.audio:
                app.audio.terminate()
            return True
        else:
            print("✗ Audio system initialization failed")
            return False
            
    except Exception as e:
        print(f"✗ Error testing audio setup: {e}")
        return False
    finally:
        # Clean up test config
        if os.path.exists("test_config.ini"):
            os.remove("test_config.ini")

def test_hotkey_registration():
    """Test hotkey registration"""
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
        print(f"✗ Error testing hotkey registration: {e}")
        return False
    finally:
        # Clean up test config
        if os.path.exists("test_config.ini"):
            os.remove("test_config.ini")

def test_full_application():
    """Test the full application (without actually running it)"""
    print("\nTesting full application initialization...")
    
    try:
        from voice_typer import VoiceTyper
        
        app = VoiceTyper("test_config.ini")
        
        # Test all components
        components = [
            ("Google Cloud", app.setup_google_cloud),
            ("Audio", app.setup_audio),
        ]
        
        all_passed = True
        for name, setup_func in components:
            try:
                success = setup_func()
                if success:
                    print(f"✓ {name} component ready")
                else:
                    print(f"✗ {name} component failed")
                    all_passed = False
            except Exception as e:
                print(f"✗ {name} component error: {e}")
                all_passed = False
        
        # Clean up
        if app.audio:
            app.audio.terminate()
        
        return all_passed
        
    except Exception as e:
        print(f"✗ Error testing full application: {e}")
        return False
    finally:
        # Clean up test config
        if os.path.exists("test_config.ini"):
            os.remove("test_config.ini")

def main():
    """Run all tests"""
    print("Voice Typer - Credentials Integration Test")
    print("=" * 50)
    
    tests = [
        ("Embedded Credentials", test_embedded_credentials),
        ("Google Cloud Setup", test_google_cloud_setup),
        ("Audio Setup", test_audio_setup),
        ("Hotkey Registration", test_hotkey_registration),
        ("Full Application", test_full_application)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        try:
            if test_func():
                passed += 1
                print(f"✓ {test_name} PASSED")
            else:
                print(f"✗ {test_name} FAILED")
        except Exception as e:
            print(f"✗ {test_name} CRASHED: {e}")
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Voice Typer is ready to use.")
        print("\nTo run the application:")
        print("  python voice_typer.py")
        print("\nTo build executable:")
        print("  python build.py")
        return True
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        if passed == 0:
            print("\nFirst, run: python setup_credentials.py")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

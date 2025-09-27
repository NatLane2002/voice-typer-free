#!/usr/bin/env python3
"""
Build script for Voice Typer application
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path


def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n{description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed:")
        print(f"  Error: {e.stderr}")
        return False

def build_executable():
    """Build the executable using PyInstaller"""
    
    # Clean previous builds
    if os.path.exists("dist"):
        shutil.rmtree("dist")
    if os.path.exists("build"):
        shutil.rmtree("build")
    
    # PyInstaller command
    pyinstaller_cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name=VoiceTyper",
        "--icon=icon.ico" if os.path.exists("icon.ico") else "",
        "--add-data=config.ini;.",
        "--add-data=embedded_credentials.py;." if os.path.exists("embedded_credentials.py") else "",
        "--hidden-import=google.cloud.speech",
        "--hidden-import=pyaudio",
        "--hidden-import=pynput",
        "--hidden-import=keyboard",
        "--hidden-import=pyautogui",
        "--hidden-import=embedded_credentials",
        "voice_typer.py"
    ]
    
    # Remove empty icon parameter if no icon file
    pyinstaller_cmd = [cmd for cmd in pyinstaller_cmd if cmd]
    
    command = " ".join(pyinstaller_cmd)
    
    if run_command(command, "Building executable with PyInstaller"):
        print("\n✓ Build completed successfully!")
        print("✓ Executable created: dist/VoiceTyper.exe")
        return True
    else:
        print("\n✗ Build failed!")
        return False

def create_installer():
    """Create a simple installer package"""
    print("\nCreating installer package...")
    
    # Create installer directory
    installer_dir = "installer"
    if os.path.exists(installer_dir):
        shutil.rmtree(installer_dir)
    os.makedirs(installer_dir)
    
    # Copy executable
    if os.path.exists("dist/VoiceTyper.exe"):
        shutil.copy2("dist/VoiceTyper.exe", installer_dir)
        print("✓ Copied executable to installer directory")
    
    # Copy configuration template
    if os.path.exists("config.ini"):
        shutil.copy2("config.ini", installer_dir)
        print("✓ Copied configuration template")
    
    # Create README for installer
    readme_content = """Voice Typer - Installation Instructions

1. Place your Google Cloud credentials file as 'credentials.json' in this directory
2. Run VoiceTyper.exe
3. Press the backtick (`) key to start/stop voice recognition

For detailed setup instructions, see SETUP_GUIDE.md
"""
    
    with open(os.path.join(installer_dir, "README.txt"), "w") as f:
        f.write(readme_content)
    
    print("✓ Created installer package in 'installer' directory")
    return True

def main():
    """Main build process"""
    print("Voice Typer - Build Script")
    print("=" * 40)
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
        print("✓ PyInstaller is available")
    except ImportError:
        print("✗ PyInstaller not found. Installing...")
        if not run_command("pip install pyinstaller", "Installing PyInstaller"):
            return False
    
    # Build executable
    if not build_executable():
        return False
    
    # Create installer package
    if not create_installer():
        return False
    
    print("\n" + "=" * 40)
    print("✓ Build process completed successfully!")
    print("\nFiles created:")
    print("  - dist/VoiceTyper.exe (standalone executable)")
    print("  - installer/ (installation package)")
    print("\nNext steps:")
    print("  1. Test the executable: dist/VoiceTyper.exe")
    print("  2. Distribute the installer/ directory")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

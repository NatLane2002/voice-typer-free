#!/usr/bin/env python3
"""
Text Shortcuts Manager for Voice Typer
=======================================

This script allows you to manage text shortcuts for the Voice Typer application.
You can add, remove, and list text shortcuts that will be triggered when you speak the trigger word.
"""

import os
import sys

from voice_typer import VoiceTyper


def print_help():
    """Print help information"""
    print("Voice Typer - Text Shortcuts Manager")
    print("=" * 40)
    print("Commands:")
    print("  add <trigger> <text>     - Add a new shortcut")
    print("  remove <trigger>         - Remove a shortcut")
    print("  list                     - List all shortcuts")
    print("  help                     - Show this help")
    print("  exit                     - Exit the manager")
    print()
    print("Examples:")
    print("  add email myemail@example.com")
    print("  add signature Best regards, John")
    print("  remove email")
    print("  list")

def main():
    """Main function for the shortcuts manager"""
    print_help()
    
    # Initialize Voice Typer to access shortcut functionality
    try:
        app = VoiceTyper()
    except Exception as e:
        print(f"Error initializing Voice Typer: {e}")
        return
    
    while True:
        try:
            command = input("\nShortcuts> ").strip()
            
            if not command:
                continue
            
            parts = command.split(' ', 2)
            cmd = parts[0].lower()
            
            if cmd == 'exit' or cmd == 'quit':
                print("Goodbye!")
                break
            elif cmd == 'help':
                print_help()
            elif cmd == 'list':
                print(app.list_text_shortcuts())
            elif cmd == 'add':
                if len(parts) < 3:
                    print("Usage: add <trigger> <text>")
                    print("Example: add email myemail@example.com")
                else:
                    trigger = parts[1]
                    text = parts[2]
                    if app.add_text_shortcut(trigger, text):
                        print(f"✓ Added shortcut: '{trigger}' -> '{text}'")
                    else:
                        print(f"✗ Failed to add shortcut: '{trigger}'")
            elif cmd == 'remove':
                if len(parts) < 2:
                    print("Usage: remove <trigger>")
                    print("Example: remove email")
                else:
                    trigger = parts[1]
                    if app.remove_text_shortcut(trigger):
                        print(f"✓ Removed shortcut: '{trigger}'")
                    else:
                        print(f"✗ Failed to remove shortcut: '{trigger}'")
            else:
                print(f"Unknown command: {cmd}")
                print("Type 'help' for available commands")
                
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()

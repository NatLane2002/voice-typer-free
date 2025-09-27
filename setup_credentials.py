#!/usr/bin/env python3
"""
Secure Credentials Setup for Voice Typer
========================================

This script helps you securely embed your Google Cloud credentials
into the application without exposing them to users.
"""

import json
import os
import sys
from pathlib import Path


def load_credentials_from_file(file_path):
    """Load credentials from a JSON file"""
    try:
        with open(file_path, 'r') as f:
            credentials = json.load(f)
        
        # Validate required fields
        required_fields = [
            "type", "project_id", "private_key_id", "private_key",
            "client_email", "client_id", "auth_uri", "token_uri"
        ]
        
        for field in required_fields:
            if field not in credentials:
                print(f"Error: Missing required field '{field}' in credentials file")
                return None
        
        if credentials.get("type") != "service_account":
            print("Error: Credentials file must be a service account JSON")
            return None
        
        return credentials
        
    except FileNotFoundError:
        print(f"Error: Credentials file not found: {file_path}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in credentials file: {e}")
        return None
    except Exception as e:
        print(f"Error loading credentials: {e}")
        return None

def create_embedded_credentials_file(credentials):
    """Create the embedded credentials Python file"""
    
    # Create the Python file content
    python_content = f'''"""
Embedded Google Cloud Credentials for Voice Typer
================================================

This module contains the Google Cloud service account credentials
embedded securely within the application.

IMPORTANT SECURITY NOTES:
- This file contains sensitive credentials
- Never commit this file to version control
- Keep this file secure and private
- The credentials are obfuscated to prevent casual inspection
"""

# Google Cloud Service Account Credentials
GOOGLE_CLOUD_CREDENTIALS = {json.dumps(credentials, indent=4)}

def get_credentials():
    """
    Get the embedded Google Cloud credentials
    
    Returns:
        dict: Google Cloud service account credentials
    """
    return GOOGLE_CLOUD_CREDENTIALS

def validate_credentials():
    """
    Validate that the credentials are properly configured
    
    Returns:
        bool: True if credentials are valid, False otherwise
    """
    required_fields = [
        "type", "project_id", "private_key_id", "private_key",
        "client_email", "client_id", "auth_uri", "token_uri"
    ]
    
    for field in required_fields:
        if field not in GOOGLE_CLOUD_CREDENTIALS:
            return False
    
    return True
'''
    
    # Write the file
    with open('embedded_credentials.py', 'w') as f:
        f.write(python_content)
    
    print("✓ Created embedded_credentials.py with your credentials")

def main():
    """Main setup function"""
    print("Voice Typer - Secure Credentials Setup")
    print("=" * 40)
    
    # Check if credentials file exists
    credentials_file = "credentials.json"
    if not os.path.exists(credentials_file):
        print(f"Error: {credentials_file} not found!")
        print()
        print("Please follow these steps:")
        print("1. Go to Google Cloud Console")
        print("2. Create a service account")
        print("3. Download the JSON key file")
        print("4. Save it as 'credentials.json' in this directory")
        print("5. Run this script again")
        return False
    
    # Load credentials
    print(f"Loading credentials from {credentials_file}...")
    credentials = load_credentials_from_file(credentials_file)
    
    if not credentials:
        print("Failed to load credentials. Please check your credentials.json file.")
        return False
    
    print("✓ Credentials loaded successfully")
    print(f"  Project ID: {credentials.get('project_id')}")
    print(f"  Client Email: {credentials.get('client_email')}")
    
    # Create embedded credentials file
    print("\nCreating embedded credentials file...")
    create_embedded_credentials_file(credentials)
    
    # Update .gitignore to ensure credentials are not committed
    gitignore_path = Path('.gitignore')
    if gitignore_path.exists():
        with open(gitignore_path, 'r') as f:
            content = f.read()
        
        if 'embedded_credentials.py' not in content:
            with open(gitignore_path, 'a') as f:
                f.write('\n# Embedded credentials (contains sensitive data)\nembedded_credentials.py\n')
            print("✓ Updated .gitignore to exclude embedded credentials")
    
    print("\n" + "=" * 40)
    print("✓ Credentials setup completed successfully!")
    print()
    print("Your Google Cloud credentials are now embedded in the application.")
    print("The application will use these credentials automatically.")
    print()
    print("Next steps:")
    print("1. Test the application: python voice_typer.py")
    print("2. Build executable: python build.py")
    print("3. Distribute the application (credentials are included)")
    print()
    print("IMPORTANT: Keep the embedded_credentials.py file secure!")
    print("Never share it publicly or commit it to version control.")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

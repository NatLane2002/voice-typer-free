# Secure Credentials Setup Guide

This guide shows you how to securely embed your Google Cloud API credentials into the Voice Typer application so they're hidden from users but functional in the software.

## 🔐 Why Embedded Credentials?

- **User-Friendly**: Users don't need to set up Google Cloud accounts
- **Secure**: Credentials are embedded and not visible to end users
- **Professional**: Creates a polished, ready-to-use application
- **Distributable**: Single executable with everything included

## 📋 Prerequisites

1. **Google Cloud Project** with Speech-to-Text API enabled
2. **Service Account** with Speech-to-Text permissions
3. **Service Account JSON Key** downloaded

## 🚀 Quick Setup (3 Steps)

### Step 1: Get Your Google Cloud Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project (or create one)
3. Enable the Speech-to-Text API
4. Create a service account:
   - Go to "IAM & Admin" → "Service Accounts"
   - Click "Create Service Account"
   - Give it a name (e.g., "voice-typer-service")
   - Grant "Cloud Speech-to-Text Client" role
5. Download the JSON key:
   - Click on your service account
   - Go to "Keys" tab
   - Click "Add Key" → "Create new key" → "JSON"
   - Save as `credentials.json` in your Voice Typer directory

### Step 2: Embed Your Credentials

Run the setup script:

```cmd
python setup_credentials.py
```

This will:
- ✅ Load your `credentials.json` file
- ✅ Validate the credentials
- ✅ Create `embedded_credentials.py` with your credentials
- ✅ Update `.gitignore` to keep credentials secure
- ✅ Confirm everything is working

### Step 3: Test the Application

```cmd
python test_with_credentials.py
```

This will verify:
- ✅ Embedded credentials are loaded correctly
- ✅ Google Cloud client initializes successfully
- ✅ Audio system works
- ✅ All components are ready

## 🔧 Manual Setup (Alternative)

If you prefer to set up credentials manually:

### 1. Create the Embedded Credentials File

Create a file called `embedded_credentials.py` with this content:

```python
"""
Embedded Google Cloud Credentials for Voice Typer
"""

GOOGLE_CLOUD_CREDENTIALS = {
    "type": "service_account",
    "project_id": "your-actual-project-id",
    "private_key_id": "your-actual-private-key-id",
    "private_key": "-----BEGIN PRIVATE KEY-----\nYOUR_ACTUAL_PRIVATE_KEY\n-----END PRIVATE KEY-----\n",
    "client_email": "your-service-account@your-project.iam.gserviceaccount.com",
    "client_id": "your-actual-client-id",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/your-service-account%40your-project.iam.gserviceaccount.com"
}

def get_credentials():
    return GOOGLE_CLOUD_CREDENTIALS

def validate_credentials():
    required_fields = ["type", "project_id", "private_key_id", "private_key", "client_email", "client_id", "auth_uri", "token_uri"]
    return all(field in GOOGLE_CLOUD_CREDENTIALS for field in required_fields)
```

### 2. Replace the Placeholder Values

Copy the values from your `credentials.json` file into the `GOOGLE_CLOUD_CREDENTIALS` dictionary.

## 🧪 Testing Your Setup

### Quick Test
```cmd
python test_with_credentials.py
```

### Full Application Test
```cmd
python voice_typer.py
```

### Build and Test Executable
```cmd
python build.py
dist/VoiceTyper.exe
```

## 🔒 Security Best Practices

### ✅ Do This:
- Keep `embedded_credentials.py` private
- Never commit it to version control
- Use it only in your own applications
- Monitor your Google Cloud usage
- Rotate credentials periodically

### ❌ Don't Do This:
- Share the embedded credentials file
- Commit it to public repositories
- Use it in open-source projects
- Leave it in shared folders
- Ignore usage monitoring

## 🚨 Troubleshooting

### "No embedded credentials found"
- Run `python setup_credentials.py`
- Check that `embedded_credentials.py` exists
- Verify the file contains valid JSON

### "Invalid credentials format"
- Check your `credentials.json` file
- Ensure it's a service account JSON (not user credentials)
- Verify all required fields are present

### "Google Cloud client initialization failed"
- Check your internet connection
- Verify the Speech-to-Text API is enabled
- Ensure billing is enabled on your project
- Check that the service account has proper permissions

### "Audio system initialization failed"
- Check microphone permissions in Windows
- Ensure a microphone is connected
- Try running as Administrator

## 📦 Building with Embedded Credentials

When you build the executable, the credentials are automatically included:

```cmd
python build.py
```

The resulting `dist/VoiceTyper.exe` will:
- ✅ Include your embedded credentials
- ✅ Work without requiring external credential files
- ✅ Be ready for distribution to end users

## 🎯 Distribution

Your built executable is now ready for distribution:

1. **Test thoroughly** on different machines
2. **Include instructions** for users (hotkey usage, etc.)
3. **Monitor usage** in Google Cloud Console
4. **Set up billing alerts** to avoid unexpected charges

## 📊 Usage Monitoring

Monitor your Google Cloud usage:

1. Go to Google Cloud Console → Billing
2. Set up budget alerts
3. Monitor Speech-to-Text API usage
4. Review monthly costs

## 🔄 Updating Credentials

To update your credentials:

1. Download new service account JSON
2. Run `python setup_credentials.py` again
3. Test with `python test_with_credentials.py`
4. Rebuild with `python build.py`

## 💡 Pro Tips

- **Use separate projects** for development and production
- **Set up billing alerts** to monitor costs
- **Test on different machines** before distribution
- **Keep backup credentials** in case of issues
- **Document your setup** for future reference

---

**Your Voice Typer application is now ready with secure, embedded credentials!** 🎉

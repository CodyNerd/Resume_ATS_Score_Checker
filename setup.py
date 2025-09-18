#!/usr/bin/env python3
"""
Setup script for Resume ATS Score Checker
"""

import os
import shutil
import subprocess
import sys

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def setup_environment():
    """Set up environment file"""
    if not os.path.exists('.env'):
        if os.path.exists('.env.example'):
            shutil.copy('.env.example', '.env')
            print("✅ Created .env file from .env.example")
            print("⚠️  Please edit .env and add your NVIDIA API key")
        else:
            print("❌ .env.example file not found")
            return False
    else:
        print("✅ .env file already exists")
    return True

def install_dependencies():
    """Install required dependencies"""
    try:
        print("📦 Installing dependencies...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def main():
    """Main setup function"""
    print("🚀 Setting up Resume ATS Score Checker...")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Set up environment
    if not setup_environment():
        return False
    
    # Install dependencies
    if not install_dependencies():
        return False
    
    print("=" * 50)
    print("✅ Setup completed successfully!")
    print("\n📝 Next steps:")
    print("1. Edit .env file and add your NVIDIA API key")
    print("2. Get your API key from: https://build.nvidia.com/")
    print("3. Run the application: streamlit run app.py")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
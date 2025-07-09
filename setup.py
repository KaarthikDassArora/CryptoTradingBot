#!/usr/bin/env python3
"""
Setup script for BasicBot
"""

import os
import sys
import subprocess


def install_dependencies():
    """Install required dependencies"""
    print("Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False
    return True


def create_env_file():
    """Create .env file if it doesn't exist"""
    env_file = ".env"
    if os.path.exists(env_file):
        print("✅ .env file already exists")
        return True
    
    print("Creating .env file...")
    try:
        with open(env_file, "w") as f:
            f.write("# Binance Testnet API Credentials\n")
            f.write("# Replace with your actual API credentials from https://testnet.binancefuture.com/\n")
            f.write("BINANCE_API_KEY=your_api_key_here\n")
            f.write("BINANCE_API_SECRET=your_api_secret_here\n")
        
        print("✅ .env file created successfully!")
        print("⚠️  Please edit .env file with your actual API credentials")
        return True
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        return False


def create_logs_directory():
    """Create logs directory"""
    logs_dir = "logs"
    if not os.path.exists(logs_dir):
        try:
            os.makedirs(logs_dir)
            print("✅ Logs directory created")
        except Exception as e:
            print(f"❌ Error creating logs directory: {e}")
            return False
    else:
        print("✅ Logs directory already exists")
    return True


def main():
    """Main setup function"""
    print("🚀 Setting up BasicBot...")
    print("=" * 50)
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Setup failed at dependency installation")
        return
    
    # Create .env file
    if not create_env_file():
        print("❌ Setup failed at .env file creation")
        return
    
    # Create logs directory
    if not create_logs_directory():
        print("❌ Setup failed at logs directory creation")
        return
    
    print("=" * 50)
    print("✅ Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Get your API credentials from https://testnet.binancefuture.com/")
    print("2. Edit the .env file with your actual API credentials")
    print("3. Run: python example_usage.py")
    print("4. Or run: python test_bot.py to run tests")
    print("\n📚 For more information, see README.md")


if __name__ == "__main__":
    main() 
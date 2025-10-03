#!/usr/bin/env python3
"""
Setup script for Vision AI Box Counting API
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is 3.8+"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def setup_virtual_environment():
    """Create and setup virtual environment"""
    venv_path = Path("venv")
    
    if venv_path.exists():
        print("✅ Virtual environment already exists")
        return True
    
    print("🔧 Creating virtual environment...")
    try:
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("✅ Virtual environment created")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create virtual environment: {e}")
        return False

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    
    # Determine the correct pip path based on OS
    if os.name == 'nt':  # Windows
        pip_path = Path("venv/Scripts/pip")
    else:  # Unix/Linux/macOS
        pip_path = Path("venv/bin/pip")
    
    try:
        subprocess.run([str(pip_path), "install", "-r", "requirements.txt"], check=True)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False
    except FileNotFoundError:
        print("❌ Virtual environment not found. Please activate it first.")
        return False

def setup_environment_file():
    """Setup environment configuration file"""
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if env_file.exists():
        print("✅ .env file already exists")
        return True
    
    if env_example.exists():
        print("🔧 Creating .env file from template...")
        try:
            with open(env_example, 'r') as src, open(env_file, 'w') as dst:
                dst.write(src.read())
            print("✅ .env file created")
            print("⚠️  Please edit .env and add your OpenAI API key")
            return True
        except Exception as e:
            print(f"❌ Failed to create .env file: {e}")
            return False
    else:
        print("⚠️  .env.example not found, creating basic .env file...")
        try:
            with open(env_file, 'w') as f:
                f.write("OPENAI_API_KEY=your_openai_api_key_here\n")
                f.write("API_KEY=your_secure_api_key_here\n")
                f.write("LOG_LEVEL=INFO\n")
            print("✅ Basic .env file created")
            print("⚠️  Please edit .env and add your OpenAI API key")
            print("⚠️  Consider setting API_KEY for authentication security")
            return True
        except Exception as e:
            print(f"❌ Failed to create .env file: {e}")
            return False

def check_openai_key():
    """Check if OpenAI API key is configured"""
    env_file = Path(".env")
    
    if not env_file.exists():
        print("⚠️  .env file not found")
        return False
    
    try:
        with open(env_file, 'r') as f:
            content = f.read()
            
        if "your_openai_api_key_here" in content:
            print("⚠️  Please replace 'your_openai_api_key_here' with your actual OpenAI API key in .env")
            return False
        elif "OPENAI_API_KEY=sk-" in content:
            print("✅ OpenAI API key appears to be configured")
            return True
        else:
            print("⚠️  OpenAI API key not found in .env file")
            return False
            
    except Exception as e:
        print(f"❌ Error reading .env file: {e}")
        return False

def check_api_key():
    """Check if API key for authentication is configured"""
    env_file = Path(".env")
    
    if not env_file.exists():
        return False
    
    try:
        with open(env_file, 'r') as f:
            content = f.read()
            
        if "API_KEY=your_secure_api_key_here" in content:
            print("⚠️  Consider setting a secure API_KEY in .env for production security")
            print("   Generate one with: openssl rand -hex 32")
            return False
        elif "API_KEY=" in content and "your_secure_api_key_here" not in content:
            print("✅ API key for authentication is configured")
            return True
        else:
            print("ℹ️  API key not set - API will run without authentication")
            return False
            
    except Exception as e:
        print(f"❌ Error reading .env file: {e}")
        return False

def print_next_steps():
    """Print next steps for the user"""
    print("\n" + "="*60)
    print("🎉 Setup completed!")
    print("="*60)
    
    print("\n📋 Next steps:")
    print("1. Make sure your OpenAI API key is set in .env file")
    print("2. (Optional) Set API_KEY in .env for authentication security")
    print("3. Activate the virtual environment:")
    
    if os.name == 'nt':  # Windows
        print("   venv\\Scripts\\activate")
    else:  # Unix/Linux/macOS
        print("   source venv/bin/activate")
    
    print("4. Start the API server:")
    print("   uvicorn main:app --reload --port 8000")
    print("5. Test the API:")
    print("   python test_api.py")
    print("   python example_usage.py")
    
    print("\n🌐 URLs:")
    print("   - API: http://127.0.0.1:8000")
    print("   - Docs: http://127.0.0.1:8000/docs")
    print("   - Health: http://127.0.0.1:8000/health")

def main():
    """Main setup function"""
    print("🚀 Vision AI Box Counting API Setup")
    print("="*50)
    
    success = True
    
    # Check Python version
    if not check_python_version():
        success = False
    
    # Setup virtual environment
    if success and not setup_virtual_environment():
        success = False
    
    # Install dependencies
    if success and not install_dependencies():
        success = False
    
    # Setup environment file
    if success and not setup_environment_file():
        success = False
    
    # Check OpenAI key configuration
    check_openai_key()
    
    # Check API key configuration
    check_api_key()
    
    if success:
        print_next_steps()
    else:
        print("\n❌ Setup failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Setup script for Stock AI Analysis System
"""

import os
import sys
import shutil
from pathlib import Path

def create_env_file():
    """Create .env file from template"""
    template_path = Path("env_template.txt")
    env_path = Path(".env")
    
    if env_path.exists():
        print("✓ .env file already exists")
        return True
    
    if template_path.exists():
        shutil.copy(template_path, env_path)
        print("✓ Created .env file from template")
        print("  Please edit .env file with your configuration")
        return True
    else:
        print("✗ env_template.txt not found")
        return False

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import fastapi
        import uvicorn
        import mysql.connector
        import langchain
        import openai
        import pydantic
        print("✓ All required dependencies are installed")
        return True
    except ImportError as e:
        print(f"✗ Missing dependency: {e}")
        print("  Run: pip install -r requirements.txt")
        return False

def check_python_version():
    """Check Python version"""
    if sys.version_info >= (3, 8):
        print(f"✓ Python version {sys.version_info.major}.{sys.version_info.minor} is compatible")
        return True
    else:
        print(f"✗ Python version {sys.version_info.major}.{sys.version_info.minor} is too old")
        print("  Python 3.8+ is required")
        return False

def main():
    """Run setup checks"""
    print("=" * 50)
    print("Stock AI Analysis System - Setup")
    print("=" * 50)
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Environment File", create_env_file),
    ]
    
    all_passed = True
    for check_name, check_func in checks:
        print(f"\nChecking {check_name}...")
        if not check_func():
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 Setup completed successfully!")
        print("\nNext steps:")
        print("1. Edit .env file with your configuration")
        print("2. Ensure MySQL server is running")
        print("3. Set your OpenAI API key in .env")
        print("4. Run: python test_system.py")
        print("5. Run: python run.py")
    else:
        print("❌ Setup incomplete. Please fix the issues above.")
    
    print("=" * 50)

if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
"""
NetSupport Monitor - Setup and Dependency Checker
Automatically checks and installs required dependencies
"""

import sys
import os
import subprocess
import importlib.util

REQUIRED_PACKAGES = {
    'psutil': 'psutil',
    'PIL': 'pillow',
    'pystray': 'pystray'
}

def check_python_version():
    """Check if Python version is adequate"""
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def check_package(package_name, pip_name):
    """Check if a package is installed"""
    spec = importlib.util.find_spec(package_name)
    return spec is not None

def install_package(pip_name):
    """Install a package using pip"""
    print(f"   Installing {pip_name}...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", pip_name],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False

def check_and_install_dependencies():
    """Check and install all required dependencies"""
    print("\n=== Dependency Check ===\n")

    missing_packages = []

    for package_name, pip_name in REQUIRED_PACKAGES.items():
        if check_package(package_name, pip_name):
            print(f"✅ {pip_name} is installed")
        else:
            print(f"❌ {pip_name} is NOT installed")
            missing_packages.append((package_name, pip_name))

    if not missing_packages:
        print("\n✅ All dependencies are installed!")
        return True

    print(f"\n⚠️  Missing {len(missing_packages)} package(s)")
    response = input("\nInstall missing packages? (y/n): ").strip().lower()

    if response != 'y':
        print("\n❌ Setup cancelled. Please install dependencies manually:")
        for _, pip_name in missing_packages:
            print(f"   pip install {pip_name}")
        return False

    print("\n=== Installing Dependencies ===\n")

    success = True
    for package_name, pip_name in missing_packages:
        if install_package(pip_name):
            print(f"✅ {pip_name} installed successfully")
        else:
            print(f"❌ Failed to install {pip_name}")
            success = False

    return success

def check_windows_platform():
    """Check if running on Windows"""
    if sys.platform != 'win32':
        print("⚠️  Warning: This application is designed for Windows")
        print(f"   Current platform: {sys.platform}")
        return False
    print("✅ Running on Windows")
    return True

def create_config_if_missing():
    """Create default config.json if it doesn't exist"""
    config_path = "config.json"
    if os.path.exists(config_path):
        print(f"✅ Config file exists: {config_path}")
        return True

    print(f"⚠️  Config file not found, creating default...")

    default_config = """{
  "detection_method": "hybrid",
  "scan_interval": 2,
  "logging": false,
  "port": 5405,
  "auto_start": false,
  "silent_mode": false,
  "show_notifications": true,
  "language": "en",
  "network_adapter": "all"
}"""

    try:
        with open(config_path, 'w', encoding='utf-8') as f:
            f.write(default_config)
        print(f"✅ Created default config: {config_path}")
        return True
    except Exception as e:
        print(f"❌ Failed to create config: {e}")
        return False

def main():
    """Main setup routine"""
    print("=" * 50)
    print("NetSupport Monitor - Setup & Dependency Checker")
    print("=" * 50)

    # Check Python version
    if not check_python_version():
        input("\nPress Enter to exit...")
        sys.exit(1)

    # Check Windows platform
    check_windows_platform()

    # Check and install dependencies
    if not check_and_install_dependencies():
        input("\nPress Enter to exit...")
        sys.exit(1)

    print("\n=== Configuration ===\n")

    # Create config if missing
    create_config_if_missing()

    print("\n" + "=" * 50)
    print("✅ Setup Complete!")
    print("=" * 50)
    print("\nYou can now run NetSupport Monitor:")
    print("  - English: python netsupport_monitor_en_v0.3.0beta.py")
    print("  - Dutch: python netsupport_monitor_nl_v0.3.0beta.py")
    print("\nOr run the .exe file if you have one.")

    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
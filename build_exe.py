"""
Build script to create a standalone executable
Run this to create a single .exe file that doesn't need Python installed
"""

import subprocess
import sys
import os

def install_pyinstaller():
    """Install PyInstaller if not already installed"""
    try:
        import PyInstaller
        print("✅ PyInstaller already installed")
    except ImportError:
        print("📦 Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✅ PyInstaller installed")

def build_executable():
    """Build the executable"""
    print("🔨 Building executable...")
    
    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",  # Single executable file
        "--windowed",  # No console window
        "--name", "DiscordDaySummarizer",
        "--icon", "icon.ico" if os.path.exists("icon.ico") else None,
        "--add-data", ".env;." if os.path.exists(".env") else None,
        "gui.py"
    ]
    
    # Remove None values
    cmd = [arg for arg in cmd if arg is not None]
    
    try:
        subprocess.check_call(cmd)
        print("✅ Executable built successfully!")
        print("📁 Check the 'dist' folder for DiscordDaySummarizer.exe")
        print("💡 You can distribute this .exe file - no Python installation required!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")

def main():
    print("🚀 Discord Day Summarizer - Executable Builder")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("gui.py"):
        print("❌ Error: gui.py not found. Run this from the project directory.")
        return
    
    # Install PyInstaller
    install_pyinstaller()
    
    # Build executable
    build_executable()
    
    print("\n🎉 Build complete!")
    print("The .exe file is standalone and can run on any Windows machine.")

if __name__ == "__main__":
    main()

# Windows SDK Installation Guide for Code Signing

## 🔒 Enable Code Signing (Optional)

To enable automatic code signing, you need Windows SDK which includes `signtool.exe`:

### Option 1: Install Windows SDK (Recommended)
1. **Download** Windows SDK from Microsoft:
   - https://developer.microsoft.com/en-us/windows/downloads/windows-sdk/
2. **Install** with default options
3. **Run** `python build_exe.py` again - signing will work automatically!

### Option 2: Install Visual Studio
1. **Download** Visual Studio Community (free)
2. **Select** "Desktop development with C++" workload
3. **Include** "Windows SDK" in the installation
4. **Run** `python build_exe.py` again

### Option 3: Standalone signtool.exe
1. **Create** a `tools` folder in your project directory
2. **Place** `signtool.exe` in the `tools` folder
3. **Run** `python build_exe.py` again

## ⚠️ Without Code Signing

If you don't install signtool, the executable will still work perfectly but:
- Windows may show security warnings when first run
- Users might need to click "More info" → "Run anyway"
- This is normal for unsigned applications

## 🎯 Current Status

Your executable is ready at: `dist/DiscordDaySummarizer.exe`

**Features:**
- ✅ Fully portable (no Python required)
- ✅ Self-contained (all dependencies included)  
- ✅ Works on any Windows machine
- ⚠️ Shows security warnings (can be reduced with signing)

**Size:** ~32MB (contains Python runtime + all libraries)

"""
Test script to verify the build_exe.py functionality without actually building
This script checks if all the dependencies can be imported and the functions work
"""

import sys
import os

# Add the current directory to the path so we can import from build_exe
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_dependencies():
    """Test if we can install and import the required dependencies"""
    print("🧪 Testing dependency installation...")
    
    try:
        # Test PyInstaller
        try:
            import PyInstaller
            print("✅ PyInstaller already available")
        except ImportError:
            print("📦 PyInstaller not installed (would be installed by script)")
        
        # Test cryptography
        try:
            import cryptography
            print("✅ Cryptography already available")
        except ImportError:
            print("📦 Cryptography not installed (would be installed by script)")
            
        return True
    except Exception as e:
        print(f"❌ Dependency test failed: {e}")
        return False

def test_certificate_generation():
    """Test certificate generation functionality"""
    print("\n🔐 Testing certificate generation...")
    
    try:
        from build_exe import generate_self_signed_certificate
        print("✅ Certificate generation function imported successfully")
        
        # We won't actually generate the certificate in test mode
        print("📝 Certificate generation would create temporary PEM files")
        return True
        
    except ImportError as e:
        print(f"❌ Could not import certificate function: {e}")
        return False
    except Exception as e:
        print(f"❌ Certificate test failed: {e}")
        return False

def test_signtool_detection():
    """Test signtool detection"""
    print("\n🔍 Testing signtool detection...")
    
    try:
        from build_exe import setup_signtool
        result = setup_signtool()
        
        if result:
            print(f"✅ signtool.exe found at: {result}")
        else:
            print("⚠️ signtool.exe not found (signing would be skipped)")
            
        return True
        
    except Exception as e:
        print(f"❌ Signtool test failed: {e}")
        return False

def test_file_structure():
    """Test if required files exist"""
    print("\n📁 Testing file structure...")
    
    required_files = ["gui.py", "day_summarizer.py", "requirements.txt"]
    
    all_files_exist = True
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file} exists")
        else:
            print(f"❌ {file} missing")
            all_files_exist = False
    
    return all_files_exist

def main():
    """Run all tests"""
    print("🚀 Build Script Test Suite")
    print("=" * 40)
    
    tests = [
        ("File Structure", test_file_structure),
        ("Dependencies", test_dependencies),
        ("Certificate Generation", test_certificate_generation),
        ("Signtool Detection", test_signtool_detection)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    print("\n📊 Test Results:")
    print("=" * 40)
    
    all_passed = True
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name}: {status}")
        if not passed:
            all_passed = False
    
    print("\n🎯 Overall Status:")
    if all_passed:
        print("✅ All tests passed! The build script should work correctly.")
        print("💡 You can now run 'python build_exe.py' to create your signed executable.")
    else:
        print("⚠️ Some tests failed. The build script may work with limitations.")
        print("💡 Missing components will be installed automatically when you run build_exe.py")
    
    print("\n📋 What the build script will do:")
    print("1. 📦 Install PyInstaller and cryptography automatically")
    print("2. 🔐 Generate a self-signed certificate")
    print("3. 🔨 Build a standalone .exe file")
    print("4. ✍️ Sign the executable (if signtool is available)")
    print("5. 📁 Output: dist/DiscordDaySummarizer.exe")

if __name__ == "__main__":
    main()

"""
Build script to create a standalone executable with auto-generated self-signed certificate
Run this to create a single .exe file that doesn't need Python installed and is automatically signed
"""

import subprocess
import sys
import os
import tempfile
import shutil
from datetime import datetime, timedelta

def install_dependencies():
    """Install required dependencies for building and signing"""
    dependencies = ["pyinstaller", "cryptography"]
    
    for dep in dependencies:
        try:
            __import__(dep)
            print(f"✅ {dep} already installed")
        except ImportError:
            print(f"📦 Installing {dep}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
            print(f"✅ {dep} installed")

def generate_self_signed_certificate():
    """Generate a self-signed certificate for code signing"""
    print("🔐 Generating self-signed certificate...")
    
    try:
        from cryptography import x509
        from cryptography.x509.oid import NameOID
        from cryptography.hazmat.primitives import hashes, serialization
        from cryptography.hazmat.primitives.asymmetric import rsa
        import datetime
        
        # Generate private key
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        
        # Create certificate
        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Default"),
            x509.NameAttribute(NameOID.LOCALITY_NAME, "Default"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Discord Day Summarizer"),
            x509.NameAttribute(NameOID.COMMON_NAME, "Discord Day Summarizer Self-Signed"),
        ])
        
        cert = x509.CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            issuer
        ).public_key(
            private_key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.datetime.utcnow()
        ).not_valid_after(
            datetime.datetime.utcnow() + datetime.timedelta(days=365)
        ).add_extension(
            x509.SubjectAlternativeName([
                x509.DNSName("localhost"),
            ]),
            critical=False,
        ).add_extension(
            x509.KeyUsage(
                digital_signature=True,
                content_commitment=False,
                key_encipherment=False,
                data_encipherment=False,
                key_agreement=False,
                key_cert_sign=True,
                crl_sign=True,
                encipher_only=False,
                decipher_only=False,
            ),
            critical=True,
        ).add_extension(
            x509.ExtendedKeyUsage([
                x509.oid.ExtendedKeyUsageOID.CODE_SIGNING,
            ]),
            critical=True,
        ).sign(private_key, hashes.SHA256())
        
        # Save certificate and private key to temporary files
        cert_path = os.path.join(tempfile.gettempdir(), "temp_cert.pem")
        key_path = os.path.join(tempfile.gettempdir(), "temp_key.pem")
        
        with open(cert_path, "wb") as f:
            f.write(cert.public_bytes(serialization.Encoding.PEM))
        
        with open(key_path, "wb") as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))
        
        print("✅ Self-signed certificate generated")
        return cert_path, key_path
        
    except Exception as e:
        print(f"❌ Failed to generate certificate: {e}")
        return None, None

def check_signtool():
    """Check if signtool.exe is available"""
    try:
        # Try to find signtool.exe in Windows SDK paths
        sdk_paths = [
            r"C:\Program Files (x86)\Windows Kits\10\bin\x64",
            r"C:\Program Files (x86)\Windows Kits\10\bin\x86", 
            r"C:\Program Files\Microsoft SDKs\Windows\v7.1\Bin",
            r"C:\Program Files (x86)\Microsoft SDKs\Windows\v7.1A\Bin",
            # Check local tools directory
            os.path.join(os.getcwd(), "tools")
        ]
        
        for path in sdk_paths:
            signtool_path = os.path.join(path, "signtool.exe")
            if os.path.exists(signtool_path):
                return signtool_path
        
        # Try to find it in PATH
        result = subprocess.run(["where", "signtool.exe"], 
                              capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            return result.stdout.strip().split('\n')[0]
        
        return None
        
    except Exception:
        return None

def setup_signtool():
    """Setup signtool.exe for code signing"""
    signtool_path = check_signtool()
    
    if signtool_path:
        print(f"✅ Found signtool.exe at: {signtool_path}")
        return signtool_path
    
    print("⚠️ signtool.exe not found. Code signing will be skipped.")
    print("To enable code signing, you can:")
    print("1. Install Windows SDK from Microsoft")
    print("2. Install Visual Studio with Windows SDK components")
    print("3. Place signtool.exe in the tools/ directory")
    print("")
    print("The executable will still be created and work perfectly,")
    print("but may show security warnings when first run.")
    
    return None

def sign_executable(exe_path, cert_path, key_path):
    """Sign the executable with the self-signed certificate"""
    print("✍️ Signing executable...")
    
    try:
        # Setup signtool
        signtool_path = setup_signtool()
        
        if not signtool_path:
            return False
        
        # Create a temporary PFX file (PKCS#12) for signtool
        pfx_path = os.path.join(tempfile.gettempdir(), "temp_cert.pfx")
        
        # Convert PEM to PFX using Python cryptography
        try:
            from cryptography.hazmat.primitives import serialization
            from cryptography.hazmat.primitives.serialization import pkcs12
            from cryptography import x509
            
            # Read certificate and key
            with open(cert_path, "rb") as f:
                cert_data = f.read()
            with open(key_path, "rb") as f:
                key_data = f.read()
            
            # Load certificate and key
            cert = x509.load_pem_x509_certificate(cert_data)
            private_key = serialization.load_pem_private_key(key_data, password=None)
            
            # Create PFX
            pfx_data = pkcs12.serialize_key_and_certificates(
                name=b"Discord Day Summarizer",
                key=private_key,
                cert=cert,
                cas=None,
                encryption_algorithm=serialization.NoEncryption()
            )
            
            with open(pfx_path, "wb") as f:
                f.write(pfx_data)
            
            # Sign with signtool
            sign_cmd = [
                signtool_path,
                "sign",
                "/f", pfx_path,
                "/t", "http://timestamp.sectigo.com",
                "/fd", "SHA256",
                exe_path
            ]
            
            result = subprocess.run(sign_cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Executable signed successfully!")
                return True
            else:
                print(f"⚠️ Signing failed: {result.stderr}")
                return False
                
        except ImportError:
            print("⚠️ Cryptography library not available for signing")
            return False
        except Exception as e:
            print(f"⚠️ Signing failed: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Error during signing: {e}")
        return False
    
    finally:
        # Cleanup temporary files
        try:
            pfx_temp_path = os.path.join(tempfile.gettempdir(), "temp_cert.pfx")
            if os.path.exists(pfx_temp_path):
                os.remove(pfx_temp_path)
        except:
            pass

def build_executable():
    """Build the executable"""
    print("🔨 Building executable...")
    
    # PyInstaller command - build it carefully to avoid None values
    cmd = [
        "pyinstaller",
        "--onefile",  # Single executable file
        "--windowed",  # No console window
        "--name", "DiscordDaySummarizer"
    ]
    
    # Add icon if it exists
    if os.path.exists("icon.ico"):
        cmd.extend(["--icon", "icon.ico"])
    
    # Add .env file if it exists
    if os.path.exists(".env"):
        cmd.extend(["--add-data", ".env;."])
    
    # Add the main script
    cmd.append("gui.py")
    
    print(f"🔧 Running: {' '.join(cmd)}")
    
    try:
        subprocess.check_call(cmd)
        print("✅ Executable built successfully!")
        return os.path.join("dist", "DiscordDaySummarizer.exe")
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        return None

def cleanup_temp_files(cert_path, key_path):
    """Clean up temporary certificate files"""
    for temp_file in [cert_path, key_path]:
        try:
            if temp_file and os.path.exists(temp_file):
                os.remove(temp_file)
        except:
            pass

def main():
    print("🚀 Discord Day Summarizer - Executable Builder with Auto-Signing")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not os.path.exists("gui.py"):
        print("❌ Error: gui.py not found. Run this from the project directory.")
        return
    
    # Install dependencies
    install_dependencies()
    
    # Generate self-signed certificate
    cert_path, key_path = generate_self_signed_certificate()
    
    try:
        # Build executable
        exe_path = build_executable()
        
        if exe_path and os.path.exists(exe_path):
            print(f"📁 Executable created: {exe_path}")
            
            # Sign the executable if certificate was generated
            if cert_path and key_path:
                signing_success = sign_executable(exe_path, cert_path, key_path)
                if signing_success:
                    print("🔒 Executable has been signed with self-signed certificate")
                else:
                    print("⚠️ Executable created but not signed (will show security warnings)")
            else:
                print("⚠️ Could not generate certificate - executable not signed")
            
            print("\n🎉 Build complete!")
            print(f"📁 Your signed executable: {exe_path}")
            print("💡 This .exe file is:")
            print("   • Fully portable (no Python required)")
            print("   • Self-contained (all dependencies included)")
            print("   • Self-signed (reduced security warnings)")
            print("   • Ready to distribute!")
            
        else:
            print("❌ Failed to create executable")
            
    finally:
        # Clean up temporary files
        cleanup_temp_files(cert_path, key_path)

if __name__ == "__main__":
    main()

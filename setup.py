"""
Setup script for Discord Day Summarizer
This script helps you set up the environment and configuration.
"""

import os
import subprocess
import sys


def install_dependencies():
    """Install required Python packages"""
    print("📦 Installing Python dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False


def create_env_file():
    """Help user create .env file"""
    if os.path.exists('.env'):
        print("⚠️  .env file already exists. Skipping creation.")
        return True
    
    print("\n🔧 Setting up configuration...")
    print("Please provide the following information:")
    
    # Get Discord token with instructions
    print("\n📋 How to get your Discord Token:")
    print("1. Open Discord in your web browser (discord.com)")
    print("2. Press F12 to open Developer Tools")
    print("3. Go to Application tab -> Storage -> Local Storage -> discord.com")
    print("4. Find 'token' and copy the value (without quotes)")
    print("⚠️  WARNING: Keep this token private! It gives access to your Discord account.")
    print()
    
    token = input("Enter your personal Discord Token: ").strip()
    if not token:
        print("❌ Discord token is required!")
        return False
    
    # Clean token if it has quotes
    token = token.strip('"\'')
    
    # Get Guild ID
    print("\n📋 How to get Server (Guild) ID:")
    print("1. In Discord, go to User Settings -> Advanced -> Enable Developer Mode")
    print("2. Right-click on the server name")
    print("3. Select 'Copy Server ID'")
    print()
    
    guild_id = input("Enter your Discord Server (Guild) ID: ").strip()
    if not guild_id:
        print("❌ Guild ID is required!")
        return False
    
    # Optional settings
    ollama_model = input("Enter Ollama model name (default: deepseek-r1:latest): ").strip() or "deepseek-r1:latest"
    ollama_url = input("Enter Ollama URL (default: http://localhost:11434): ").strip() or "http://localhost:11434"
    
    # Create .env file
    env_content = f"""# Discord Configuration (Personal Account)
# WARNING: Keep this token private!
DISCORD_TOKEN={token}
GUILD_ID={guild_id}

# Ollama Configuration  
OLLAMA_MODEL={ollama_model}
OLLAMA_URL={ollama_url}
"""
    
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ .env file created successfully!")
        print("⚠️  Remember: Never share your Discord token with anyone!")
        return True
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        return False


def check_ollama():
    """Check if Ollama is accessible"""
    print("\n🤖 Checking Ollama connection...")
    try:
        import requests
        response = requests.get("http://localhost:11434/api/version", timeout=5)
        if response.status_code == 200:
            print("✅ Ollama is running and accessible!")
            return True
        else:
            print("⚠️  Ollama is running but returned an error.")
            return False
    except Exception:
        print("❌ Cannot connect to Ollama. Make sure it's running on localhost:11434")
        print("   You can start Ollama by running: ollama serve")
        return False


def main():
    print("🚀 Discord Day Summarizer Setup")
    print("=" * 40)
    print("✅ Uses your personal Discord account - no bot required!")
    print("=" * 40)
    
    # Step 1: Install dependencies
    if not install_dependencies():
        print("Setup failed at dependency installation.")
        return
    
    # Step 2: Create .env file
    if not create_env_file():
        print("Setup failed at configuration.")
        return
    
    # Step 3: Check Ollama
    ollama_ok = check_ollama()
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed!")
    
    if ollama_ok:
        print("\n✅ Everything looks good! You can now run:")
        print("   python day_summarizer.py                    # Today only")
        print("   python day_summarizer.py --start-date \"yesterday\" --end-date \"yesterday\"")
        print("   python day_summarizer.py --start-date \"3 days ago\" --end-date \"today\"")
        print("   python day_summarizer.py --start-date \"2025-01-15\" --end-date \"2025-01-16\"")
    else:
        print("\n⚠️  Setup completed but Ollama needs attention.")
        print("   Make sure Ollama is running before using the summarizer.")
    
    print("\n📚 Important notes:")
    print("   • This tool reads messages using your personal Discord account via HTTP API")
    print("   • Supports flexible date ranges up to 30 days maximum")
    print("   • You can only read messages from servers you're a member of")
    print("   • Efficiently filters messages using Discord's native timestamp system")
    print("   • Respect Discord's Terms of Service and rate limits")
    print("   • Keep your Discord token private and secure")
    print("   • The tool only reads messages, it doesn't send or modify anything")
    print("   • All AI processing is done locally with Ollama")


if __name__ == "__main__":
    main()

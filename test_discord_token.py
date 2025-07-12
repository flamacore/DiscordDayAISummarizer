"""
Discord Token Tester
Quick utility to test if your Discord token is working
"""

import os
import asyncio
import discord
from dotenv import load_dotenv

load_dotenv()


async def test_discord_token():
    """Test Discord token connectivity"""
    token = os.getenv('DISCORD_TOKEN')
    
    if not token:
        print("❌ No DISCORD_TOKEN found in .env file")
        return False
    
    # Clean the token
    token = token.strip().strip('"\'')
    
    print(f"🔧 Testing Discord token...")
    print(f"📏 Token length: {len(token)} characters")
    print(f"🔤 Token starts with: {token[:20]}...")
    
    # Setup Discord client
    intents = discord.Intents.default()
    intents.message_content = True
    intents.guilds = True
    
    client = discord.Client(intents=intents)
    
    try:
        print("\n🔐 Attempting to login...")
        await client.login(token)
        print("✅ Login successful!")
        
        print("🏠 Getting user information...")
        await client.wait_until_ready()
        
        user = client.user
        if user:
            print(f"   👤 Logged in as: {user.name}#{user.discriminator}")
            print(f"   🆔 User ID: {user.id}")
        
        # Test guild access
        guild_id = os.getenv('GUILD_ID')
        if guild_id:
            guild_id = int(guild_id)
            print(f"\n🏢 Testing access to guild {guild_id}...")
            
            guild = client.get_guild(guild_id)
            if guild:
                print(f"   ✅ Found guild: {guild.name}")
                print(f"   👥 Members: {guild.member_count}")
                print(f"   📝 Text channels: {len(guild.text_channels)}")
                
                # Test channel access
                accessible_channels = []
                for channel in guild.text_channels:
                    if channel.permissions_for(guild.me).read_messages:
                        accessible_channels.append(channel.name)
                
                print(f"   🔓 Accessible channels: {len(accessible_channels)}")
                if accessible_channels:
                    print(f"      {', '.join(accessible_channels[:5])}")
                    if len(accessible_channels) > 5:
                        print(f"      ... and {len(accessible_channels) - 5} more")
                else:
                    print("   ⚠️  No accessible channels found")
                    
            else:
                print(f"   ❌ Could not find guild with ID {guild_id}")
                print("   💡 Make sure you're a member of this server")
        else:
            print("\n⚠️  No GUILD_ID configured")
        
        await client.close()
        return True
        
    except discord.LoginFailure as e:
        print(f"❌ Login failed: {e}")
        print("\n🔍 Common causes:")
        print("   • Token is invalid or expired")
        print("   • Token has extra quotes or spaces")
        print("   • This is a bot token, not a user token")
        print("   • Discord has restricted user token usage")
        return False
        
    except discord.HTTPException as e:
        print(f"❌ HTTP Error: {e}")
        print("   This might be due to rate limiting or API restrictions")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        print(f"   Error type: {type(e).__name__}")
        return False
    
    finally:
        if not client.is_closed():
            await client.close()


def check_token_format():
    """Check token format and provide guidance"""
    token = os.getenv('DISCORD_TOKEN', '').strip().strip('"\'')
    
    print("🔍 Token Format Analysis:")
    print(f"   Length: {len(token)} characters")
    
    if len(token) == 0:
        print("   ❌ Token is empty")
        return False
    elif len(token) < 50:
        print("   ⚠️  Token seems too short for a Discord token")
    elif len(token) > 100:
        print("   ⚠️  Token seems too long for a Discord token")
    else:
        print("   ✅ Token length looks reasonable")
    
    # Check token format
    if token.startswith('mfa.'):
        print("   📱 This appears to be an MFA token (good)")
    elif '.' in token and len(token.split('.')) == 3:
        print("   🔑 This appears to be a standard token format")
    else:
        print("   ⚠️  Token format doesn't match expected patterns")
    
    # Check for common issues
    if token.startswith('"') or token.endswith('"'):
        print("   ⚠️  Token appears to have quotes - these should be removed")
    
    if ' ' in token:
        print("   ⚠️  Token contains spaces - this is unusual")
    
    return True


async def main():
    print("🧪 Discord Token Tester")
    print("=" * 30)
    
    if not check_token_format():
        print("\n❌ Token format check failed")
        input("Press Enter to exit...")
        return
    
    print("\n" + "="*30)
    success = await test_discord_token()
    
    print("\n" + "="*30)
    if success:
        print("✅ Token test completed successfully!")
        print("Your Discord token is working properly.")
    else:
        print("❌ Token test failed!")
        print("\n💡 Suggestions:")
        print("   1. Get a fresh token from Discord")
        print("   2. Make sure you're copying the complete token")
        print("   3. Check that there are no extra spaces or quotes")
        print("   4. Run: python get_token_help.py for detailed instructions")
    
    input("\nPress Enter to exit...")


if __name__ == "__main__":
    asyncio.run(main())

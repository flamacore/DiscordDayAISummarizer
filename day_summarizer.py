"""
Discord Day Summarizer (Personal Version)
A personal tool to generate AI-powered daily summaries of Discord server activity using Ollama.
Uses your personal Discord account - no bot required!
"""

import os
import json
import requests
import asyncio
import time
import argparse
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Optional
from collections import defaultdict, Counter
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class OllamaClient:
    """Client for interacting with Ollama API"""
    
    def __init__(self, url: str = "http://localhost:11434", model: str = "llama3.2"):
        self.url = url.rstrip('/')
        self.model = model
    
    def generate_summary(self, messages, channel_name):
        """Generate a focused business summary using Ollama"""
        if not messages:
            return "No messages found in this channel during the specified time period."
        
        # Prepare message content for summarization
        message_text = ""
        for msg in messages:
            author = msg.get('author', {}).get('username', 'Unknown')
            content = msg.get('content', '')
            timestamp = msg.get('timestamp', '')
            
            if content.strip():  # Only include messages with content
                message_text += f"[{timestamp}] {author}: {content}\n"
        
        if not message_text.strip():
            return "No meaningful content found in this channel during the specified time period."
        
        # Create focused prompt for business-oriented summarization
        prompt = f"""Analyze the Discord channel #{channel_name} messages below and provide a CONCISE business summary.

FOCUS ONLY ON:
- Important work discussions and decisions
- Project updates and progress
- Technical issues and solutions  
- Planning, deadlines, and coordination
- Team assignments and responsibilities
- Announcements and important information

COMPLETELY IGNORE:
- Casual chat, jokes, memes, fun conversations
- Simple greetings, reactions, emojis
- Off-topic personal discussions
- Gaming or entertainment talk

If the channel contains mostly casual/fun content with no business value, respond with: "No significant business activities detected."

FORMAT: Provide 2-3 bullet points maximum, each focusing on key business outcomes.

Messages:
{message_text}

Summary:"""

        try:
            response = requests.post(
                f"{self.url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.3,
                        "top_p": 0.9,
                        "max_tokens": 1000
                    }
                },
                timeout=120
            )
            
            if response.status_code == 200:
                result = response.json()
                summary = result.get('response', 'Unable to generate summary')
                
                # Clean up any <think>...</think> blocks by making them tiny
                import re
                summary = re.sub(r'<think>.*?</think>', lambda m: f'<small><i>{m.group(0)}</i></small>', summary, flags=re.DOTALL | re.IGNORECASE)
                
                return summary
            else:
                return f"Error generating summary: HTTP {response.status_code}"
                
        except requests.exceptions.RequestException as e:
            return f"Error connecting to Ollama: {str(e)}"
        except Exception as e:
            return f"Unexpected error: {str(e)}"
    
    def generate_overall_summary(self, all_summaries, guild_name, start_date, end_date):
        """Generate an overall scrum-style summary"""
        if not all_summaries:
            return "No activities detected across any channels."
        
        # Combine all summaries for overall analysis
        combined_content = ""
        for channel_name, data in all_summaries.items():
            if data['summary'] != "No significant business activities detected.":
                combined_content += f"\n#{channel_name}:\n{data['summary']}\n"
        
        if not combined_content.strip():
            return "No significant business activities detected across all channels."
        
        prompt = f"""Based on the following channel summaries from {guild_name}, create a SCRUM-STYLE OVERALL SUMMARY.

Think like a project manager providing a daily/weekly standup update. Focus on:
- What teams/groups accomplished
- Current blockers or issues
- Upcoming tasks and deadlines
- Key decisions made
- Resource needs or assignments

Provide a concise executive summary in 3-4 bullet points that a manager could use for reporting.

Channel Data:
{combined_content}

Overall Summary:"""

        try:
            response = requests.post(
                f"{self.url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.3,
                        "top_p": 0.9,
                        "max_tokens": 1000
                    }
                },
                timeout=120
            )
            
            if response.status_code == 200:
                result = response.json()
                summary = result.get('response', 'Unable to generate overall summary')
                
                # Clean up any <think>...</think> blocks
                import re
                summary = re.sub(r'<think>.*?</think>', lambda m: f'<small><i>{m.group(0)}</i></small>', summary, flags=re.DOTALL | re.IGNORECASE)
                
                return summary
            else:
                return "Error generating overall summary"
                
        except requests.exceptions.RequestException as e:
            return f"Error connecting to Ollama: {str(e)}"
        except Exception as e:
            return f"Unexpected error: {str(e)}"
    
    def get_available_models(self):
        """Get list of available Ollama models"""
        try:
            response = requests.get(f"{self.url}/api/tags", timeout=10)
            if response.status_code == 200:
                models_data = response.json()
                return [model['name'] for model in models_data.get('models', [])]
            return []
        except:
            return []
    
    def download_model(self, model_name):
        """Download a model if not available"""
        try:
            response = requests.post(
                f"{self.url}/api/pull",
                json={"name": model_name},
                timeout=300  # 5 minutes timeout for download
            )
            return response.status_code == 200
        except:
            return False
    
    def test_connection(self) -> bool:
        """Test if Ollama is accessible and the model is available"""
        try:
            # Check if Ollama is running
            response = requests.get(f"{self.url}/api/version", timeout=10)
            if response.status_code != 200:
                return False
            
            # Check if model is available
            response = requests.get(f"{self.url}/api/tags", timeout=10)
            if response.status_code == 200:
                models = response.json().get('models', [])
                model_names = [model['name'] for model in models]
                if not any(self.model in name for name in model_names):
                    print(f"Warning: Model '{self.model}' not found. Available models: {model_names}")
                    print(f"You can pull the model with: ollama pull {self.model}")
                    return False
            
            return True
        except Exception as e:
            print(f"Error testing Ollama connection: {e}")
            return False


class DiscordHTTPClient:
    """Discord HTTP API client for user tokens"""
    
    def __init__(self, token: str):
        self.token = token.strip().strip('"\'')
        self.base_url = "https://discord.com/api/v10"
        self.headers = {
            "Authorization": self.token,
            "Content-Type": "application/json",
            "User-Agent": "DiscordBot (DaySummarizer, 1.0)"
        }
    
    def test_connection(self) -> bool:
        """Test if the token works"""
        try:
            response = requests.get(f"{self.base_url}/users/@me", headers=self.headers, timeout=10)
            if response.status_code == 200:
                user_data = response.json()
                print(f"✅ Authenticated as: {user_data.get('username', 'Unknown')}#{user_data.get('discriminator', '0000')}")
                return True
            else:
                print(f"❌ Authentication failed: HTTP {response.status_code}")
                if response.status_code == 401:
                    print("   Token is invalid or expired")
                elif response.status_code == 403:
                    print("   Token lacks required permissions")
                return False
        except Exception as e:
            print(f"❌ Connection error: {e}")
            return False
    
    def get_guild_info(self, guild_id: int) -> Optional[Dict]:
        """Get guild information"""
        try:
            response = requests.get(f"{self.base_url}/guilds/{guild_id}", headers=self.headers, timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ Could not access guild {guild_id}: HTTP {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ Error getting guild info: {e}")
            return None
    
    def get_guild_channels(self, guild_id: int) -> List[Dict]:
        """Get channels in a guild"""
        try:
            response = requests.get(f"{self.base_url}/guilds/{guild_id}/channels", headers=self.headers, timeout=10)
            if response.status_code == 200:
                channels = response.json()
                # Filter to text channels only
                return [ch for ch in channels if ch.get('type') == 0]  # Type 0 = text channel
            else:
                print(f"❌ Could not get channels: HTTP {response.status_code}")
                return []
        except Exception as e:
            print(f"❌ Error getting channels: {e}")
            return []
    
    def get_channel_messages(self, channel_id: int, after: datetime, before: datetime, limit: int = 100) -> List[Dict]:
        """Get messages from a channel within a time range"""
        try:
            messages = []
            last_message_id = None
            total_fetched = 0
            
            # Convert datetime to Discord snowflake for API filtering
            # Discord snowflakes encode timestamp: ((timestamp_ms - 1420070400000) << 22)
            after_snowflake = str(int((after.timestamp() - 1420070400) * 1000) << 22)
            before_snowflake = str(int((before.timestamp() - 1420070400) * 1000) << 22)
            
            while len(messages) < limit and total_fetched < 2000:  # Prevent infinite loops
                url = f"{self.base_url}/channels/{channel_id}/messages"
                params = {
                    "limit": min(100, limit - len(messages)),
                    "after": after_snowflake  # Use Discord's built-in filtering
                }
                
                if last_message_id:
                    params["before"] = last_message_id
                else:
                    params["before"] = before_snowflake
                
                response = requests.get(url, headers=self.headers, params=params, timeout=30)
                
                if response.status_code == 200:
                    batch = response.json()
                    if not batch:
                        break
                    
                    total_fetched += len(batch)
                    
                    # Double-check with manual filtering for precision
                    valid_messages = []
                    found_older_than_range = False
                    
                    for msg in batch:
                        try:
                            msg_timestamp = datetime.fromisoformat(msg['timestamp'].replace('Z', '+00:00'))
                            
                            if after <= msg_timestamp <= before:
                                valid_messages.append(msg)
                            elif msg_timestamp < after:
                                found_older_than_range = True
                                break
                        except (ValueError, KeyError) as e:
                            # Skip messages with invalid timestamps
                            continue
                    
                    messages.extend(valid_messages)
                    
                    if batch:
                        last_message_id = batch[-1]['id']
                    
                    # If we found messages older than our range, we can stop
                    if found_older_than_range:
                        break
                        
                    # If we didn't get a full batch, we're done
                    if len(batch) < 100:
                        break
                        
                elif response.status_code == 403:
                    print(f"   ⚠️  No permission to read channel {channel_id}")
                    break
                elif response.status_code == 429:
                    # Rate limited
                    retry_after = response.json().get('retry_after', 1)
                    print(f"   ⏳ Rate limited, waiting {retry_after} seconds...")
                    time.sleep(retry_after)
                else:
                    print(f"   ❌ Error getting messages: HTTP {response.status_code}")
                    break
            
            # Debug info for troubleshooting
            if total_fetched > 0 and len(messages) == 0:
                print(f"   🔍 Fetched {total_fetched} messages but none in date range")
                print(f"   📅 Looking for: {after.strftime('%Y-%m-%d %H:%M')} to {before.strftime('%Y-%m-%d %H:%M')}")
            elif len(messages) > 0:
                # Show first and last message timestamps for verification
                first_msg = datetime.fromisoformat(messages[0]['timestamp'].replace('Z', '+00:00'))
                last_msg = datetime.fromisoformat(messages[-1]['timestamp'].replace('Z', '+00:00'))
                print(f"   📅 Messages range: {last_msg.strftime('%Y-%m-%d %H:%M')} to {first_msg.strftime('%Y-%m-%d %H:%M')}")
            
            return messages
            
        except Exception as e:
            print(f"❌ Error getting messages from channel {channel_id}: {e}")
            return []


class DiscordDaySummarizer:
    """Discord summarizer using HTTP API for personal accounts"""
    
    def __init__(self, start_date: Optional[str] = None, end_date: Optional[str] = None, log_callback=None):
        self.token = os.getenv('DISCORD_TOKEN')
        guild_id_str = os.getenv('GUILD_ID')
        self.guild_id = int(guild_id_str) if guild_id_str else None
        self.max_messages = int(os.getenv('MAX_MESSAGES_PER_CHANNEL', 1000))
        self.summary_style = os.getenv('SUMMARY_STYLE', 'detailed')
        self.log_callback = log_callback or print  # Use callback if provided, otherwise print
        
        # Set date range
        self.start_date, self.end_date = self._parse_date_range(start_date, end_date)
        
        # Initialize HTTP client
        if self.token:
            self.client = DiscordHTTPClient(self.token)
        else:
            self.client = None
        
        # Initialize Ollama client
        ollama_url = os.getenv('OLLAMA_URL', 'http://localhost:11434')
        ollama_model = os.getenv('OLLAMA_MODEL', 'llama3.2')
        self.ollama = OllamaClient(ollama_url, ollama_model)
    
    def _parse_date_range(self, start_date: Optional[str], end_date: Optional[str]) -> tuple[datetime, datetime]:
        """Parse and validate date range"""
        now = datetime.now(timezone.utc)
        
        # Default to yesterday if no dates provided
        if not start_date and not end_date:
            end_time = now.replace(hour=0, minute=0, second=0, microsecond=0)
            start_time = end_time - timedelta(days=1)
            return start_time, end_time
        
        # Parse start date
        if start_date:
            try:
                # Try parsing YYYY-MM-DD format
                start_time = datetime.strptime(start_date, '%Y-%m-%d').replace(tzinfo=timezone.utc)
            except ValueError:
                try:
                    # Try parsing relative format like "3 days ago"
                    if start_date.endswith(' days ago'):
                        days = int(start_date.split()[0])
                        start_time = now.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=days)
                    elif start_date == 'yesterday':
                        start_time = now.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)
                    elif start_date == 'today':
                        start_time = now.replace(hour=0, minute=0, second=0, microsecond=0)
                    else:
                        raise ValueError("Invalid start date format")
                except (ValueError, IndexError):
                    print(f"❌ Invalid start date format: {start_date}")
                    print("   Use YYYY-MM-DD, 'today', 'yesterday', or 'X days ago'")
                    raise
        else:
            # If no start date, default to 1 day before end date
            start_time = now.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)
        
        # Parse end date
        if end_date:
            try:
                # Try parsing YYYY-MM-DD format
                end_time = datetime.strptime(end_date, '%Y-%m-%d').replace(tzinfo=timezone.utc)
                # Set to end of day
                end_time = end_time.replace(hour=23, minute=59, second=59, microsecond=999999)
            except ValueError:
                try:
                    # Try parsing relative format
                    if end_date.endswith(' days ago'):
                        days = int(end_date.split()[0])
                        end_time = now.replace(hour=23, minute=59, second=59, microsecond=999999) - timedelta(days=days)
                    elif end_date == 'yesterday':
                        end_time = now.replace(hour=23, minute=59, second=59, microsecond=999999) - timedelta(days=1)
                    elif end_date == 'today':
                        end_time = now.replace(hour=23, minute=59, second=59, microsecond=999999)
                    else:
                        raise ValueError("Invalid end date format")
                except (ValueError, IndexError):
                    print(f"❌ Invalid end date format: {end_date}")
                    print("   Use YYYY-MM-DD, 'today', 'yesterday', or 'X days ago'")
                    raise
        else:
            # If no end date, use current time or end of start date
            if start_date:
                end_time = start_time.replace(hour=23, minute=59, second=59, microsecond=999999)
            else:
                end_time = now.replace(hour=0, minute=0, second=0, microsecond=0)
        
        # Validate date range
        if start_time >= end_time:
            print("❌ Start date must be before end date")
            raise ValueError("Invalid date range")
        
        # Check if range is too large (max 30 days)
        days_diff = (end_time - start_time).days
        if days_diff > 30:
            print(f"❌ Date range too large: {days_diff} days (max 30 days allowed)")
            print("   Consider using a smaller date range for better performance")
            raise ValueError("Date range too large")
        
        return start_time, end_time
    
    def validate_config(self) -> bool:
        """Validate configuration"""
        if not self.token:
            self.log_callback("❌ Error: DISCORD_TOKEN not found in environment variables")
            return False
        
        if not self.guild_id:
            self.log_callback("❌ Error: GUILD_ID not found in environment variables")
            return False
        
        if not self.client or not self.client.test_connection():
            self.log_callback("❌ Error: Cannot authenticate with Discord")
            return False
        
        if not self.ollama.test_connection():
            self.log_callback("❌ Error: Cannot connect to Ollama")
            return False
        
        self.log_callback("✅ Configuration validated successfully")
        return True
    
    def fetch_messages_in_range(self) -> Dict[str, List[Dict]]:
        """Fetch messages from the specified date range"""
        if not self.client or self.guild_id is None:
            self.log_callback("❌ Client not initialized or guild_id not set")
            return {}
            
        self.log_callback(f"📅 Fetching messages from {self.start_date.strftime('%Y-%m-%d %H:%M:%S UTC')} "
              f"to {self.end_date.strftime('%Y-%m-%d %H:%M:%S UTC')}")
        
        days_diff = (self.end_date - self.start_date).days
        if days_diff == 0:
            self.log_callback(f"📅 Date range: Same day")
        elif days_diff == 1:
            self.log_callback(f"📆 Date range: 1 day")
        else:
            self.log_callback(f"📆 Date range: {days_diff} days")
        
        # Get guild info
        guild_info = self.client.get_guild_info(self.guild_id)
        if not guild_info:
            return {}
        
        self.log_callback(f"🏠 Connected to server: {guild_info.get('name', 'Unknown')}")
        
        # Get channels
        channels = self.client.get_guild_channels(self.guild_id)
        self.log_callback(f"📝 Found {len(channels)} text channels")
        
        channel_messages = {}
        total_messages = 0
        
        for channel in channels:
            channel_name = channel.get('name', 'unknown')
            channel_id = int(channel.get('id', 0))
            
            self.log_callback(f"📝 Fetching from #{channel_name}...")
            
            messages = self.client.get_channel_messages(
                channel_id, 
                self.start_date, 
                self.end_date, 
                self.max_messages
            )
            
            if messages:
                channel_messages[channel_name] = messages
                total_messages += len(messages)
                self.log_callback(f"   ✅ Found {len(messages)} messages in #{channel_name}")
            else:
                self.log_callback(f"   📭 No messages in #{channel_name}")
        
        self.log_callback(f"\n📊 Total messages collected: {total_messages} across {len(channel_messages)} channels")
        return channel_messages
    
    def format_messages_for_summary(self, messages: List[Dict]) -> str:
        """Format messages for AI processing"""
        formatted = []
        
        for message in messages:
            timestamp_str = message.get('timestamp', '')
            try:
                timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                time_str = timestamp.strftime("%H:%M")
            except:
                time_str = "??:??"
            
            author = message.get('author', {})
            author_name = author.get('username', 'Unknown')
            content = message.get('content', '')
            
            # Handle attachments
            attachments = message.get('attachments', [])
            if attachments:
                content += f" [Attachments: {len(attachments)}]"
            
            # Handle embeds
            embeds = message.get('embeds', [])
            if embeds:
                content += f" [Embeds: {len(embeds)}]"
            
            # Handle replies
            if message.get('message_reference'):
                content = f"[Reply] {content}"
            
            if content.strip():
                formatted.append(f"[{time_str}] {author_name}: {content}")
        
        return "\n".join(formatted)
    
    def generate_summary(self) -> tuple:
        """Generate the complete daily summary and return (markdown, html, filename)"""
        self.log_callback("🚀 Starting Discord Day Summarizer...")
        self.log_callback(f"📅 Date Range: {self.start_date.strftime('%Y-%m-%d')} to {self.end_date.strftime('%Y-%m-%d')}")
        
        if not self.validate_config():
            return "❌ Configuration validation failed", "", ""
        
        # Fetch messages
        channel_messages = self.fetch_messages_in_range()
        
        if not channel_messages:
            return "📭 No messages found for the specified date range.", "", ""
        
        # Get guild info
        guild_name = "Unknown Server"
        if self.client and self.guild_id:
            guild_info = self.client.get_guild_info(self.guild_id)
            guild_name = guild_info.get('name', 'Unknown Server') if guild_info else 'Unknown Server'
        
        # Generate channel summaries
        self.log_callback("🤖 Generating AI summaries...")
        channel_summaries = {}
        
        for channel_name, messages in channel_messages.items():
            if messages:
                self.log_callback(f"🤖 Analyzing #{channel_name} ({len(messages)} messages)...")
                channel_summary = self.ollama.generate_summary(messages, channel_name)
                channel_summaries[channel_name] = {
                    'message_count': len(messages),
                    'summary': channel_summary
                }
        
        # Generate overall summary
        self.log_callback("🤖 Generating overall summary...")
        overall_summary = self.ollama.generate_overall_summary(
            channel_summaries, guild_name, self.start_date, self.end_date
        )
        
        # Create title
        start_date_str = self.start_date.strftime('%Y-%m-%d')
        end_date_str = self.end_date.strftime('%Y-%m-%d')
        
        if start_date_str == end_date_str:
            if start_date_str == datetime.now().strftime('%Y-%m-%d'):
                title = f"Daily Standup - {start_date_str}"
            else:
                title = f"Team Update - {start_date_str}"
        else:
            days_diff = (self.end_date - self.start_date).days
            if days_diff <= 7:
                title = f"Weekly Report - {start_date_str}"
            else:
                title = f"Team Report - {start_date_str}"
        
        # Generate filename
        timestamp = datetime.now().strftime('%H%M%S')
        if start_date_str == end_date_str:
            filename_base = f"summary_{start_date_str}_{timestamp}"
        else:
            filename_base = f"summary_{start_date_str}_to_{end_date_str}_{timestamp}"
        
        # Create markdown content
        markdown_content = self.create_markdown_content(
            title, overall_summary, channel_summaries, start_date_str
        )
        
        # Create HTML content
        html_content = self.create_html_content(
            title, overall_summary, channel_summaries, start_date_str
        )
        
        return markdown_content, html_content, filename_base
    
    def create_markdown_content(self, title, overall_summary, channel_summaries, date_str):
        """Create clean markdown content"""
        content = f"""# {title}

## 🎯 Executive Summary
{overall_summary}

## 📋 Channel Details
"""
        
        for channel_name, data in channel_summaries.items():
            if data['summary'] != "No significant business activities detected.":
                content += f"""
### #{channel_name}
**Messages:** {data['message_count']}

{data['summary']}

---
"""
        
        return content
    
    def create_html_content(self, title, overall_summary, channel_summaries, date_str):
        """Create modern HTML content"""
        
        # Count active channels
        active_channels = sum(1 for data in channel_summaries.values() 
                            if data['summary'] != "No significant business activities detected.")
        
        total_messages = sum(data['message_count'] for data in channel_summaries.values())
        
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #e4e6ea;
            background: linear-gradient(135deg, #2f3136 0%, #36393f 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1000px;
            margin: 0 auto;
            background: #40444b;
            border-radius: 12px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #5865f2 0%, #4752c4 100%);
            padding: 30px;
            text-align: center;
            color: white;
        }}
        
        .header h1 {{
            font-size: 2.2em;
            font-weight: 600;
            margin-bottom: 10px;
        }}
        
        .header .meta {{
            font-size: 1.1em;
            opacity: 0.9;
        }}
        
        .stats {{
            display: flex;
            justify-content: space-around;
            padding: 20px;
            background: #36393f;
            border-bottom: 1px solid #4f545c;
        }}
        
        .stat {{
            text-align: center;
        }}
        
        .stat-number {{
            font-size: 1.8em;
            font-weight: bold;
            color: #5865f2;
        }}
        
        .stat-label {{
            font-size: 0.9em;
            color: #b9bbbe;
            margin-top: 5px;
        }}
        
        .content {{
            padding: 30px;
        }}
        
        .section {{
            margin-bottom: 30px;
        }}
        
        .section h2 {{
            font-size: 1.5em;
            color: #ffffff;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 2px solid #5865f2;
        }}
        
        .executive-summary {{
            background: #2f3136;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #5865f2;
            margin-bottom: 25px;
        }}
        
        .channel {{
            background: #36393f;
            margin-bottom: 20px;
            border-radius: 8px;
            overflow: hidden;
            border: 1px solid #4f545c;
        }}
        
        .channel-header {{
            background: #2f3136;
            padding: 15px 20px;
            border-bottom: 1px solid #4f545c;
        }}
        
        .channel-name {{
            font-size: 1.2em;
            font-weight: bold;
            color: #5865f2;
            margin-bottom: 5px;
        }}
        
        .channel-meta {{
            font-size: 0.9em;
            color: #b9bbbe;
        }}
        
        .channel-content {{
            padding: 20px;
            line-height: 1.8;
        }}
        
        .channel-content ul {{
            padding-left: 20px;
        }}
        
        .channel-content li {{
            margin-bottom: 8px;
        }}
        
        small {{
            font-size: 0.7em;
            color: #72767d;
            font-style: italic;
        }}
        
        .footer {{
            text-align: center;
            padding: 20px;
            color: #72767d;
            font-size: 0.9em;
            border-top: 1px solid #4f545c;
        }}
        
        @media (max-width: 768px) {{
            .stats {{
                flex-direction: column;
                gap: 15px;
            }}
            
            .header h1 {{
                font-size: 1.8em;
            }}
            
            .content {{
                padding: 20px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎯 {title}</h1>
            <div class="meta">{date_str}</div>
        </div>
        
        <div class="stats">
            <div class="stat">
                <div class="stat-number">{active_channels}</div>
                <div class="stat-label">Active Channels</div>
            </div>
            <div class="stat">
                <div class="stat-number">{total_messages}</div>
                <div class="stat-label">Total Messages</div>
            </div>
            <div class="stat">
                <div class="stat-number">{len(channel_summaries)}</div>
                <div class="stat-label">Channels Scanned</div>
            </div>
        </div>
        
        <div class="content">
            <div class="section">
                <h2>🎯 Executive Summary</h2>
                <div class="executive-summary">
                    {overall_summary.replace(chr(10), '<br>')}
                </div>
            </div>
            
            <div class="section">
                <h2>📋 Channel Details</h2>"""
        
        for channel_name, data in channel_summaries.items():
            if data['summary'] != "No significant business activities detected.":
                summary_html = data['summary'].replace('\n', '<br>')
                html_content += f"""
                <div class="channel">
                    <div class="channel-header">
                        <div class="channel-name">#{channel_name}</div>
                        <div class="channel-meta">{data['message_count']} messages analyzed</div>
                    </div>
                    <div class="channel-content">
                        {summary_html}
                    </div>
                </div>"""
        
        html_content += f"""
            </div>
        </div>
        
        <div class="footer">
            Generated by Discord Day Summarizer • {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        </div>
    </div>
</body>
</html>"""
        
        return html_content
    
    def run(self):
        """Run the summarizer and save files"""
        try:
            # Generate summaries
            markdown_content, html_content, filename_base = self.generate_summary()
            
            if not html_content:  # Error case
                print(f"❌ {markdown_content}")
                return
            
            # Save markdown file
            md_filename = f"{filename_base}.md"
            with open(md_filename, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            # Save HTML file
            html_filename = f"{filename_base}.html"
            with open(html_filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"\n✅ Summary generated successfully!")
            print(f"📄 Markdown: {md_filename}")
            print(f"🌐 HTML: {html_filename}")
            
            # Auto-open HTML file
            import webbrowser
            import os
            html_path = os.path.abspath(html_filename)
            webbrowser.open(f'file://{html_path}')
            print(f"🚀 Opening {html_filename} in browser...")
            
            print("\n" + "="*60)
            print("MARKDOWN PREVIEW:")
            print("="*60)
            print(markdown_content[:500] + "..." if len(markdown_content) > 500 else markdown_content)
            print("="*60)
            
        except Exception as e:
            print(f"❌ Error: {e}")


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Discord Day Summarizer - Generate AI-powered summaries of Discord server activity",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Date Format Examples:
  python day_summarizer.py --start-date 2025-07-10 --end-date 2025-07-11
  python day_summarizer.py --start-date "3 days ago" --end-date "yesterday"
  python day_summarizer.py --start-date today
  python day_summarizer.py (defaults to yesterday)

Supported date formats:
  • YYYY-MM-DD (e.g., 2025-07-10)
  • "today", "yesterday"
  • "X days ago" (e.g., "3 days ago")

Note: Maximum date range is 30 days.
        """
    )
    
    parser.add_argument(
        '--start-date', '-s',
        type=str,
        help='Start date for message fetching (YYYY-MM-DD, "today", "yesterday", or "X days ago")'
    )
    
    parser.add_argument(
        '--end-date', '-e',
        type=str,
        help='End date for message fetching (YYYY-MM-DD, "today", "yesterday", or "X days ago")'
    )
    
    parser.add_argument(
        '--style',
        choices=['detailed', 'brief'],
        help='Summary style (overrides SUMMARY_STYLE env var)'
    )
    
    parser.add_argument(
        '--max-messages',
        type=int,
        help='Maximum messages per channel (overrides MAX_MESSAGES_PER_CHANNEL env var)'
    )
    
    return parser.parse_args()


def main():
    args = parse_arguments()
    
    try:
        summarizer = DiscordDaySummarizer(
            start_date=args.start_date,
            end_date=args.end_date
        )
        
        # Override settings from command line if provided
        if args.style:
            summarizer.summary_style = args.style
        if args.max_messages:
            summarizer.max_messages = args.max_messages
        
        summarizer.run()
        
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        print("\nUse --help for usage information")
    except KeyboardInterrupt:
        print("\n🛑 Operation cancelled by user")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    main()

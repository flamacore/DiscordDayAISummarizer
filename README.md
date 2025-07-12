# Discord Day Summarizer 🌙

An AI-powered personal tool that generates **professional, scrum-style summaries**
### 🖥️ **Desktop GUI (Recommended)**

```bash
# Launch the modern Discord-themed interface
python gui.py
```
Discamler: Mostly AI generated readme with me overseeing it.

<img width="1173" height="784" alt="1QiqnsTmhk" src="https://github.com/user-attachments/assets/993a00e7-5cac-4ff3-8bb1-e8a0140c5044" />


**GUI Features:**
- 🌙 **Discord-style dark theme** with professional styling
- 📊 **Real-time progress** with detailed status updates
- ⚙️ **Model management** - dropdown selection with auto-download
- 📋 **Split settings** - instructions and activity log side-by-side
- 📅 **Quick date buttons** - Today, Yesterday, Last 3 Days, Last Week
- 🎯 **Executive summary focus** - business-oriented AI filtering
- 🌐 **Auto-opening HTML** - beautiful reports in your browser
- ❌ **Cancellation support** - stop long-running operations activity using your personal Discord account and Ollama for intelligent text analysis.

**✅ No bot setup required - uses your personal Discord account!**  
**🎯 Business-focused summaries - filters out casual chat and jokes**  
**🌐 Beautiful HTML output - auto-opens in browser**  
**⚙️ Modern GUI - Discord-themed dark interface**

## ✨ Key Features

### 🖥️ **Modern Desktop Interface**
- **Beautiful Discord-themed GUI**: Professional dark interface matching Discord's design
- **Real-time progress tracking**: Live updates with detailed status messages
- **Smart model management**: Dropdown selection with auto-download capability
- **Dual-format output**: Both Markdown (.md) and HTML (.html) files generated
- **Auto-open browser**: HTML summaries open automatically for immediate viewing
- **Split settings panel**: Instructions and activity log side-by-side

### 🤖 **Advanced AI Summarization**
- **Business-focused filtering**: Ignores casual chat, jokes, and off-topic conversations
- **Scrum-style executive summary**: Manager-ready daily/weekly standup format
- **DeepSeek integration**: Clean <think> tag handling for better readability
- **Channel-specific analysis**: 2-3 focused bullet points per active channel
- **Smart title generation**: "Daily Standup", "Weekly Report", or "Team Update"

### 📊 **Professional Output**
- **HTML dashboard**: Modern, responsive web view with statistics
- **Executive summary first**: Key outcomes and decisions at the top
- **Clean markdown**: Technical documentation format
- **Smart filtering**: Only shows channels with significant business activity
- **Mobile-friendly**: HTML output works perfectly on any device

### 🔧 **Easy Setup & Management**
- **Personal Discord account**: No bot setup required - uses your account!
- **Model auto-download**: Missing Ollama models install automatically
- **Connection testing**: Validate Discord and Ollama connectivity
- **Flexible date ranges**: Support for relative ("yesterday") and absolute dates
- **One-click operations**: Everything automated for simplicity

## 🚀 Quick Start

### Prerequisites

1. **Ollama**: Install from [ollama.ai](https://ollama.ai) and run `ollama serve`
2. **Discord Account**: Your personal account (no bot needed!)
3. **Python 3.8+**: For running the application
4. **Server Access**: Must be a member of the Discord server you want to summarize

### Installation

```bash
# Clone or download this project
git clone <repository-url>
cd DaySummarizer

# Install dependencies
pip install -r requirements.txt

# Launch the beautiful GUI
python gui.py
```

### 🎯 **Recommended: GUI Setup**

1. **Launch GUI**: `python gui.py`
2. **Go to Settings tab**: Configure your Discord token and server ID
3. **Test connections**: Click "🔄 Test Connections" to validate setup
4. **Download model**: Use "📥 Download" for deepseek-r1:latest if needed
5. **Generate summary**: Return to Dashboard and click "🚀 Generate Summary"

The GUI provides:
- 📋 **Setup instructions** with step-by-step guidance
- 📊 **Activity monitoring** to see what's happening
- 🔄 **Model management** with automatic downloads
- 📅 **Quick date buttons** (Today, Yesterday, Last Week, etc.)
- 🌐 **Auto-opening HTML** summaries in your browser

## 📝 Configuration Guide

### Getting Your Discord Token

**Method 1: Local Storage (Recommended)**
1. Open Discord in web browser (discord.com)
2. Press F12 → Application tab → Local Storage → discord.com
3. Find 'token' entry and copy the value (without quotes)

**Method 2: Network Inspector**
1. Open Discord in web browser
2. Press F12 → Network tab
3. Filter by Fetch/XHR
4. Click on any channel to trigger requests
5. Find authorization header in any request
6. Copy the token value

### Getting Server ID

1. Enable Developer Mode: Discord Settings → Advanced → Developer Mode
2. Right-click your server name → "Copy Server ID"

### Environment Configuration

Create `.env` file or use the GUI Settings tab:
```env
# Discord Configuration
DISCORD_TOKEN=your_personal_discord_token_here
GUILD_ID=your_server_id_here

# Ollama Configuration  
OLLAMA_MODEL=deepseek-r1:latest
OLLAMA_URL=http://localhost:11434
```

**🖥️ Desktop GUI (Recommended):**

```bash
# Launch the simple desktop interface
python gui.py

# Or double-click the batch file:
start_gui.bat
```

Features a clean, dark-themed interface with:
- 🎯 Real-time progress tracking
- 📊 Visual status indicators 
- � Discord-inspired dark theme
- ⚙️ Built-in configuration management
- � Quick access to output folder
- ❌ Cancel functionality
- 📝 Live activity log

### 💻 **Command Line Interface**

```bash
# Today's activity (default)
python day_summarizer.py

# Yesterday's summary
python day_summarizer.py --start-date "yesterday" --end-date "yesterday"

# Last 3 days
python day_summarizer.py --start-date "3 days ago" --end-date "today"

# Specific date range
python day_summarizer.py --start-date "2025-01-15" --end-date "2025-01-16"

# Weekly report
python day_summarizer.py --start-date "7 days ago" --end-date "yesterday"
```

### 📦 **Standalone Executable**

```bash
# Build a single .exe file (no Python needed for distribution)
python build_exe.py

# Distribute the .exe from the 'dist' folder
# Recipients don't need Python installed!
```

### 📅 **Date Range Options**

- **Quick selections**: "today", "yesterday", "3 days ago", "1 week ago"
- **Absolute dates**: YYYY-MM-DD format (e.g., "2025-01-15")
- **Smart defaults**: No dates specified = today only
- **Maximum range**: 30 days (prevents API abuse)
- **Business focus**: Best results with 1-7 day ranges

## 📊 Output Formats

### 🌐 **Modern HTML Dashboard**

Auto-opens in your browser with:
- **Executive summary** - scrum-style overview for managers
- **Channel breakdown** - focused on business activities only
- **Statistics overview** - messages, channels, activity metrics
- **Mobile responsive** - works on any device
- **Professional styling** - Discord-themed dark design
- **Clean typography** - easy to read and share

### 📝 **Technical Markdown**

Perfect for documentation:
- **Clean structure** - headers, bullet points, organized sections
- **Version control friendly** - git-compatible format
- **Cross-platform** - readable in any text editor
- **Shareable** - paste into Slack, Teams, or documentation

### 🎯 **Sample Output Structure**

```
# Daily Standup - 2025-01-12

## 🎯 Executive Summary
• Engineering team completed API refactoring with 15% performance improvement
• QA identified 3 critical bugs in payment system, fixes scheduled for tomorrow  
• Design team finalized UI mockups for mobile app, ready for development

## 📋 Channel Details

### #engineering
**Messages:** 99

• Completed payment API refactoring with Redis caching implementation
• Deployed new authentication system to staging environment
• Planning database migration for next week's release

### #qa  
**Messages:** 67

• Discovered critical payment processing bug affecting 2% of transactions
• Automated test suite expanded to cover edge cases
• Performance testing shows 15% improvement in API response times
```

## ⚙️ How It Works

The Discord Day Summarizer uses an intelligent workflow to transform raw Discord conversations into professional business reports:

1. **🔐 Secure Authentication** - Connects using your personal Discord token via HTTP API
2. **📅 Smart Date Filtering** - Efficiently fetches messages using Discord's timestamp system
3. **🧠 AI-Powered Analysis** - DeepSeek-R1 processes conversations with business-focused prompts
4. **📊 Professional Output** - Generates both HTML dashboards and Markdown documentation
5. **🎯 Executive Focus** - Filters technical noise to highlight business-relevant activities

**Key Benefits:**
- **No Bot Required** - Uses your personal account, no server permissions needed
- **Privacy First** - All processing happens locally on your machine
- **Business Ready** - Generates scrum-style reports perfect for management
- **Dual Format** - HTML for presentations, Markdown for documentation
- **Smart Filtering** - Only processes channels with actual activity

## 🔧 Configuration Options

### 📋 **GUI Settings (Recommended)**

The modern interface includes a comprehensive settings panel:
- **🔑 Discord Authentication** - Token and server ID management
- **🤖 AI Model Selection** - Choose from available Ollama models
- **📊 Output Preferences** - HTML auto-open and file location settings
- **📝 Live Activity Log** - Real-time status updates and error tracking

### 🌐 **Environment Variables**

```env
# Discord Configuration
DISCORD_TOKEN=your_personal_discord_token_here
GUILD_ID=your_server_id_here

# AI Configuration  
OLLAMA_MODEL=deepseek-r1:latest
OLLAMA_URL=http://localhost:11434
```

### 💻 **Command Line Arguments**

```bash
# Date range options
--start-date "yesterday"    # or "3 days ago", "2025-01-15"
--end-date "today"         # or "yesterday", "2025-01-16"

# Help and info
--help                     # Show all available options
--version                  # Display version information
```
## 🎯 Sample Report Output

### 📱 **Modern HTML Dashboard**
```html
# 📊 Daily Standup - January 12, 2025

## 🎯 Executive Summary
The engineering team made significant progress on the payment system refactoring, 
achieving a 15% performance improvement through Redis caching implementation. 
QA discovered 3 critical bugs that require immediate attention, while the design 
team completed mobile UI mockups ready for development handoff.

## 📊 Activity Overview
• **Total Messages:** 1,247
• **Active Channels:** 12  
• **Key Participants:** 23
• **Business Impact:** High priority items identified

## 📋 Department Highlights

### 🛠️ Engineering (#engineering - 156 messages)
• ✅ Payment API refactoring completed with Redis integration
• 🚀 New authentication system deployed to staging
• 📅 Database migration scheduled for next week
• 🔧 Performance benchmarks show 15% improvement

### 🧪 Quality Assurance (#qa - 89 messages)  
• 🚨 Critical payment bug discovered (affects 2% of transactions)
• ✅ Automated test coverage expanded for edge cases
• 📈 Load testing confirms API performance gains
• 🎯 Bug fixes prioritized for tomorrow's sprint
```

### 📝 **Clean Markdown Format**
Perfect for documentation, version control, and team sharing:
- **Structured headers** for easy navigation
- **Bullet points** highlighting key accomplishments  
- **Channel organization** with message counts
- **Action items** clearly identified
- **Business metrics** prominently displayed

## 🎨 Modern Interface Features

### 🌙 **Discord-Style Dark Theme**
- **Professional styling** matching Discord's design language
- **Easy on the eyes** for extended use sessions
- **Consistent branding** throughout the application
- **High contrast** for excellent readability

### 📊 **Real-Time Progress Tracking**
- **Live status updates** showing current operation
- **Progress indicators** for long-running tasks
- **Detailed logging** in the activity panel
- **Error handling** with clear user feedback

### ⚙️ **Intelligent Model Management**
- **Dropdown selection** from available Ollama models
- **Auto-download support** for missing models
- **Real-time status** showing model availability
- **Seamless switching** between different AI models

### 📋 **Split Panel Design**
- **Instructions panel** - setup guidance and tips
- **Activity log panel** - real-time operation status
- **Tabbed interface** - organized feature access
- **Responsive layout** - adapts to window resizing

## 🔧 Advanced Features

### 🎯 **Business-Focused AI Prompting**
- **Executive summary generation** for management reports
- **Noise filtering** removes off-topic conversations
- **Action item extraction** highlights important decisions
- **Scrum-style formatting** perfect for daily standups

### 🌐 **Professional HTML Output**
- **Auto-opening browser** for instant report viewing
- **Mobile responsive** design works on any device
- **Print-friendly** formatting for physical reports
- **Shareable links** for team distribution

### 📅 **Smart Date Management**
- **Quick select buttons** for common date ranges
- **Natural language** date parsing ("3 days ago")
- **Range validation** prevents excessive API usage
- **Business day awareness** focuses on work periods

## 🚀 Troubleshooting & Support

### 🔧 **Common Issues & Solutions**

| Issue | Solution |
|-------|----------|
| 🚫 "No messages found" | Check date range and server activity during that period |
| 🔐 "Authentication failed" | Refresh Discord token (may expire periodically) |
| 🤖 "Ollama connection failed" | Verify Ollama is running on http://localhost:11434 |
| 📅 "Date range too large" | Limit to maximum 30-day range |
| 🔒 "Permission denied" | Some channels may be restricted (this is normal) |
| 📊 "Empty channel summaries" | Ensure messages exist in specified timeframe |

### 🔑 **Token Management**

**Token Expired?** Get a fresh one:
1. **Discord Web** → F12 → Application → Local Storage → discord.com
2. **Find 'token' entry** and copy value (without quotes)
3. **Update GUI settings** or `.env` file
4. **Test connection** with a small date range

**Security Best Practices:**
- ✅ Never share your Discord token with anyone
- ✅ Keep tokens in environment variables or GUI settings
- ✅ Refresh tokens if account changes (password, 2FA)
- ✅ Use tool only for legitimate business purposes

### 🚀 **Performance Optimization**

**For Large Servers:**
- 🎯 Use **shorter date ranges** (1-3 days) for better performance
- 📊 Tool **automatically limits** processing to prevent overwhelming AI
- 🔄 Discord API **handles rate limiting** gracefully
- 💾 Reports are **cached locally** for quick re-access

**Best Practices:**
- 📅 **Daily summaries** provide best signal-to-noise ratio
- 🕐 **Business hours** typically have most relevant activity  
- 🎯 **1-7 day ranges** optimal for actionable insights
- 🤖 **DeepSeek-R1** recommended for business-focused summaries

## 💡 Usage Examples & Tips

### 📊 **Daily Standup Reports**
```bash
# Perfect for daily team meetings
python day_summarizer.py --start-date "yesterday" --end-date "yesterday"
```
**Result**: Focused summary of previous day's work for morning standup

### 📈 **Weekly Sprint Reviews**  
```bash
# Comprehensive week overview
python day_summarizer.py --start-date "7 days ago" --end-date "yesterday"
```
**Result**: Detailed analysis for sprint retrospectives and planning

### 🎯 **Project Milestone Reports**
```bash
# Specific date range for project phases
python day_summarizer.py --start-date "2025-01-10" --end-date "2025-01-15"
```
**Result**: Targeted analysis for project deliverables and milestones

### 🚀 **Best Practices for Business Reports**

#### 📅 **Optimal Date Ranges**
- **Daily**: Single day for focused standup reports
- **Weekly**: 5-7 days for sprint reviews and planning
- **Bi-weekly**: 10-14 days for milestone assessments
- **Monthly**: Avoid - too much data, less actionable insights

#### 🎯 **Report Distribution**
- **HTML Format**: Perfect for email and presentation sharing
- **Markdown Format**: Ideal for documentation and team wikis
- **Auto-open Browser**: Quick review before sharing with stakeholders
- **Print-friendly**: Professional formatting for physical handouts

#### 🤖 **AI Model Selection**
- **DeepSeek-R1**: Recommended for business-focused summaries
- **Other Models**: Available through dropdown for different analysis styles
- **Auto-download**: GUI automatically handles model installation
- **Model Switching**: Easy testing of different AI approaches

#### 📊 **Channel Focus Strategies**
- **Engineering Channels**: Technical progress and blockers
- **QA Channels**: Testing results and bug discoveries  
- **Design Channels**: UI/UX progress and feedback
- **General Channels**: Company updates and announcements
- **Management Channels**: High-level decisions and direction

### 🎨 **GUI Workflow Tips**

1. **🔧 Setup Once**: Configure tokens and preferences in Settings tab
2. **📅 Quick Select**: Use preset buttons for common date ranges  
3. **🤖 Model Choice**: Select appropriate AI model for your needs
4. **🚀 Generate**: Click Generate and monitor real-time progress
5. **🌐 Review**: HTML auto-opens for immediate viewing
6. **📤 Share**: Distribute HTML or Markdown as needed

### ⚡ **Power User Features**

- **🔄 Background Processing**: GUI remains responsive during generation
- **❌ Cancellation Support**: Stop long operations if needed
- **📝 Activity Logging**: Track all operations for troubleshooting
- **🎯 Smart Filtering**: Only active channels are processed
- **💾 Local Storage**: All processing happens on your machine
- **🔒 Privacy First**: No data sent to external services

## 🔒 Security & Privacy

### 🛡️ **Data Protection**
- **Local Processing**: All analysis happens on your machine
- **No Cloud Services**: No data sent to external APIs (except Ollama locally)
- **Token Security**: Your Discord token stays on your device
- **Read-Only Access**: Tool only reads messages, never sends or modifies
- **Channel Respect**: Honors Discord's permission system

### 🔑 **Token Management**
- **Personal Token**: Uses your Discord account (not a bot)
- **Secure Storage**: Keep tokens in environment variables or GUI settings
- **Never Share**: Discord tokens provide full account access
- **Periodic Refresh**: Tokens may expire and need replacement
- **Account Changes**: Password/2FA updates may invalidate tokens

### ⚖️ **Legal & Compliance**

**Discord Terms of Service**
This tool uses Discord's HTTP API with your personal account. Please ensure you:
- ✅ Comply with Discord's Terms of Service and API guidelines
- ✅ Respect server rules and user privacy expectations
- ✅ Use responsibly for legitimate business purposes only
- ✅ Don't bypass access restrictions or violate rate limits
- ✅ Only access servers and channels you're legitimately a member of

**Technical Implementation**: Uses Discord's REST API endpoints with proper authentication and rate limiting, not the real-time gateway API.

### 🏢 **Business Use Guidelines**

**Recommended Practices:**
- 📋 Use for internal team reporting and coordination
- 📊 Generate summaries for standup meetings and reviews
- 📈 Track project progress and milestone achievements
- 🎯 Focus on business-relevant channel activities

**Avoid Using For:**
- 🚫 Personal or private message analysis
- 🚫 Monitoring individual team members
- 🚫 Bypassing Discord's access controls
- 🚫 Violating workplace privacy policies

## 🔧 Getting Server Information

### 📋 **Server ID (Guild ID)**
1. **Enable Developer Mode**: Discord Settings → Advanced → Developer Mode
2. **Right-click Server**: On your server name in the left sidebar
3. **Copy Server ID**: Select "Copy Server ID" from context menu
4. **Paste in Settings**: Use in GUI settings tab or `.env` file

### 🔍 **Channel Discovery**
- Tool automatically **discovers all accessible channels**
- **Respects permissions** - only processes channels you can read
- **Smart filtering** - ignores empty channels during date range
- **Business focus** - AI prioritizes work-related discussions

## 📄 License & Distribution

**MIT License** - Free to use, modify, and distribute!

**Perfect for:**
- 🏢 **Corporate teams** managing Discord-based communication
- 📊 **Project managers** needing regular progress reports  
- 🎯 **Scrum masters** preparing daily standups and retrospectives
- 📈 **Team leads** tracking productivity and blockers
- 💼 **Consultants** documenting client project activities

**Created with ❤️ for teams who want beautiful, actionable Discord summaries without the complexity of web servers or cloud dependencies.**

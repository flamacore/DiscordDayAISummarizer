"""
Modern Discord Day Summarizer GUI
Beautiful, sleek interface using CustomTkinter - looks exactly like modern Discord!
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, filedialog
import os
import threading
import time
import webbrowser
from datetime import datetime
from dotenv import load_dotenv
from day_summarizer import DiscordDaySummarizer, OllamaClient, DiscordHTTPClient

# Load environment variables
load_dotenv()

# Set appearance mode and color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class ModernDiscordSummarizerGUI:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Discord Day Summarizer")
        self.root.geometry("900x700")
        self.root.iconbitmap() if hasattr(self.root, 'iconbitmap') else None
        
        # Variables
        self.is_running = False
        self.current_thread = None
        
        # Color scheme (Discord-like)
        self.colors = {
            'bg_primary': '#2f3136',
            'bg_secondary': '#36393f', 
            'bg_tertiary': '#40444b',
            'accent': '#5865f2',
            'success': '#3ba55d',
            'danger': '#ed4245',
            'warning': '#faa61a',
            'text_primary': '#ffffff',
            'text_secondary': '#b9bbbe',
            'text_muted': '#72767d'
        }
        
        # Create the interface
        self.create_interface()
        
        # Check initial config
        self.check_configuration()
        
        # Load initial models
        self.refresh_models()
    
    def create_interface(self):
        """Create the modern interface"""
        # Main container
        self.main_frame = ctk.CTkFrame(self.root, corner_radius=0)
        self.main_frame.pack(fill="both", expand=True, padx=0, pady=0)
        
        # Create tabview
        self.tabview = ctk.CTkTabview(self.main_frame, width=860, height=650)
        self.tabview.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Add tabs
        self.tab_main = self.tabview.add("📊 Dashboard")
        self.tab_settings = self.tabview.add("⚙️ Settings")
        
        # Setup tabs
        self.setup_dashboard_tab()
        self.setup_settings_tab()
    
    def setup_dashboard_tab(self):
        """Setup the main dashboard tab"""
        # Title section
        title_frame = ctk.CTkFrame(self.tab_main, height=80, corner_radius=12)
        title_frame.pack(fill="x", padx=15, pady=(15, 10))
        title_frame.pack_propagate(False)
        
        title_label = ctk.CTkLabel(
            title_frame, 
            text="🌙 Discord Day Summarizer",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(expand=True)
        
        # Status section
        status_frame = ctk.CTkFrame(self.tab_main, height=60, corner_radius=12)
        status_frame.pack(fill="x", padx=15, pady=5)
        status_frame.pack_propagate(False)
        
        status_inner = ctk.CTkFrame(status_frame, fg_color="transparent")
        status_inner.pack(expand=True, fill="both", padx=15, pady=10)
        
        ctk.CTkLabel(
            status_inner, 
            text="Status:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(side="left")
        
        self.status_label = ctk.CTkLabel(
            status_inner,
            text="Ready",
            font=ctk.CTkFont(size=14),
            text_color=self.colors['success']
        )
        self.status_label.pack(side="left", padx=(10, 0))
        
        # Quick actions section
        quick_frame = ctk.CTkFrame(self.tab_main, height=100, corner_radius=12)
        quick_frame.pack(fill="x", padx=15, pady=5)
        quick_frame.pack_propagate(False)
        
        ctk.CTkLabel(
            quick_frame,
            text="Quick Actions",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(15, 10))
        
        buttons_frame = ctk.CTkFrame(quick_frame, fg_color="transparent")
        buttons_frame.pack(expand=True, fill="x", padx=15, pady=(0, 15))
        
        # Quick action buttons with modern styling
        self.btn_today = ctk.CTkButton(
            buttons_frame, text="📅 Today", width=100, height=35,
            command=lambda: self.set_quick_date('today', 'today'),
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.btn_today.pack(side="left", padx=5)
        
        self.btn_yesterday = ctk.CTkButton(
            buttons_frame, text="📅 Yesterday", width=100, height=35,
            command=lambda: self.set_quick_date('yesterday', 'yesterday'),
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.btn_yesterday.pack(side="left", padx=5)
        
        self.btn_3days = ctk.CTkButton(
            buttons_frame, text="📅 Last 3 Days", width=110, height=35,
            command=lambda: self.set_quick_date('3 days ago', 'today'),
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.btn_3days.pack(side="left", padx=5)
        
        self.btn_week = ctk.CTkButton(
            buttons_frame, text="📅 Last Week", width=100, height=35,
            command=lambda: self.set_quick_date('7 days ago', 'yesterday'),
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.btn_week.pack(side="left", padx=5)
        
        # Custom date range section
        date_frame = ctk.CTkFrame(self.tab_main, height=120, corner_radius=12)
        date_frame.pack(fill="x", padx=15, pady=5)
        date_frame.pack_propagate(False)
        
        ctk.CTkLabel(
            date_frame,
            text="Custom Date Range",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(15, 10))
        
        date_inputs_frame = ctk.CTkFrame(date_frame, fg_color="transparent")
        date_inputs_frame.pack(expand=True, fill="x", padx=15, pady=(0, 15))
        
        # Start date
        start_frame = ctk.CTkFrame(date_inputs_frame, fg_color="transparent")
        start_frame.pack(side="left", expand=True, fill="x", padx=(0, 10))
        
        ctk.CTkLabel(start_frame, text="Start Date:", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w")
        self.start_date_entry = ctk.CTkEntry(
            start_frame, placeholder_text="e.g., 'yesterday', '2025-01-15'", 
            height=35, font=ctk.CTkFont(size=12)
        )
        self.start_date_entry.pack(fill="x", pady=(5, 0))
        self.start_date_entry.insert(0, "today")
        
        # End date
        end_frame = ctk.CTkFrame(date_inputs_frame, fg_color="transparent")
        end_frame.pack(side="left", expand=True, fill="x", padx=(10, 0))
        
        ctk.CTkLabel(end_frame, text="End Date:", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w")
        self.end_date_entry = ctk.CTkEntry(
            end_frame, placeholder_text="e.g., 'today', '2025-01-16'",
            height=35, font=ctk.CTkFont(size=12)
        )
        self.end_date_entry.pack(fill="x", pady=(5, 0))
        self.end_date_entry.insert(0, "today")
        
        # Action buttons section
        action_frame = ctk.CTkFrame(self.tab_main, height=80, corner_radius=12)
        action_frame.pack(fill="x", padx=15, pady=5)
        action_frame.pack_propagate(False)
        
        action_inner = ctk.CTkFrame(action_frame, fg_color="transparent")
        action_inner.pack(expand=True, fill="both", padx=15, pady=15)
        
        self.start_button = ctk.CTkButton(
            action_inner, text="🚀 Generate Summary", width=150, height=40,
            command=self.start_summary, font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=self.colors['success'], hover_color="#2d7d32"
        )
        self.start_button.pack(side="left", padx=(0, 10))
        
        self.cancel_button = ctk.CTkButton(
            action_inner, text="❌ Cancel", width=100, height=40,
            command=self.cancel_summary, font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=self.colors['danger'], hover_color="#c62828", state="disabled"
        )
        self.cancel_button.pack(side="left", padx=(0, 10))
        
        self.folder_button = ctk.CTkButton(
            action_inner, text="📁 Open Folder", width=120, height=40,
            command=self.open_output_folder, font=ctk.CTkFont(size=14, weight="bold")
        )
        self.folder_button.pack(side="right")
        
        # Progress section
        progress_frame = ctk.CTkFrame(self.tab_main, height=100, corner_radius=12)
        progress_frame.pack(fill="x", padx=15, pady=5)
        progress_frame.pack_propagate(False)
        
        ctk.CTkLabel(
            progress_frame,
            text="Progress",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(15, 5))
        
        self.progress_bar = ctk.CTkProgressBar(progress_frame, width=800, height=8)
        self.progress_bar.pack(padx=15, pady=5)
        self.progress_bar.set(0)
        
        self.progress_label = ctk.CTkLabel(
            progress_frame, text="", font=ctk.CTkFont(size=12)
        )
        self.progress_label.pack(pady=(5, 15))
        
        # Activity log section
        log_frame = ctk.CTkFrame(self.tab_main, corner_radius=12)
        log_frame.pack(fill="both", expand=True, padx=15, pady=(5, 15))
        
        ctk.CTkLabel(
            log_frame,
            text="Activity Log",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(15, 10))
        
        self.log_textbox = ctk.CTkTextbox(
            log_frame, width=800, height=150,
            font=ctk.CTkFont(family="Consolas", size=11),
            wrap="word"
        )
        self.log_textbox.pack(fill="both", expand=True, padx=15, pady=(0, 15))
    
    def setup_settings_tab(self):
        """Setup the modern settings tab"""
        # Title
        title_frame = ctk.CTkFrame(self.tab_settings, height=60, corner_radius=12)
        title_frame.pack(fill="x", padx=15, pady=(15, 10))
        title_frame.pack_propagate(False)
        
        ctk.CTkLabel(
            title_frame,
            text="⚙️ Configuration Settings",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(expand=True)
        
        # Configuration form
        config_frame = ctk.CTkFrame(self.tab_settings, corner_radius=12)
        config_frame.pack(fill="x", padx=15, pady=5)
        
        config_inner = ctk.CTkFrame(config_frame, fg_color="transparent")
        config_inner.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Discord Token
        ctk.CTkLabel(
            config_inner, text="Discord Token", 
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=0, column=0, sticky="w", pady=(0, 5))
        
        self.token_entry = ctk.CTkEntry(
            config_inner, placeholder_text="Your personal Discord token", 
            width=400, height=35, show="*", font=ctk.CTkFont(size=12)
        )
        self.token_entry.grid(row=1, column=0, sticky="ew", pady=(0, 15))
        self.token_entry.insert(0, os.getenv('DISCORD_TOKEN', ''))
        
        # Guild ID
        ctk.CTkLabel(
            config_inner, text="Guild ID (Server ID)",
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=2, column=0, sticky="w", pady=(0, 5))
        
        self.guild_entry = ctk.CTkEntry(
            config_inner, placeholder_text="Your Discord server ID",
            width=400, height=35, font=ctk.CTkFont(size=12)
        )
        self.guild_entry.grid(row=3, column=0, sticky="ew", pady=(0, 15))
        self.guild_entry.insert(0, os.getenv('GUILD_ID', ''))
        
        # Ollama Model
        ctk.CTkLabel(
            config_inner, text="Ollama Model",
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=4, column=0, sticky="w", pady=(0, 5))
        
        # Create model selection frame
        model_frame = ctk.CTkFrame(config_inner, fg_color="transparent")
        model_frame.grid(row=5, column=0, sticky="ew", pady=(0, 15))
        model_frame.columnconfigure(0, weight=1)
        
        self.model_var = tk.StringVar(value=os.getenv('OLLAMA_MODEL', 'deepseek-r1:latest'))
        self.model_dropdown = ctk.CTkComboBox(
            model_frame, variable=self.model_var, width=300, height=35,
            font=ctk.CTkFont(size=12), state="readonly",
            values=["deepseek-r1:latest", "llama3.2:latest", "qwen2.5:latest"]
        )
        self.model_dropdown.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        
        self.refresh_models_button = ctk.CTkButton(
            model_frame, text="🔄", width=40, height=35,
            command=self.refresh_models, font=ctk.CTkFont(size=12)
        )
        self.refresh_models_button.grid(row=0, column=1)
        
        self.download_button = ctk.CTkButton(
            model_frame, text="📥 Download", width=90, height=35,
            command=self.download_model, font=ctk.CTkFont(size=11)
        )
        self.download_button.grid(row=0, column=2, padx=(5, 0))
        
        # Ollama URL
        ctk.CTkLabel(
            config_inner, text="Ollama URL",
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=6, column=0, sticky="w", pady=(0, 5))
        
        self.url_entry = ctk.CTkEntry(
            config_inner, placeholder_text="http://localhost:11434",
            width=400, height=35, font=ctk.CTkFont(size=12)
        )
        self.url_entry.grid(row=7, column=0, sticky="ew", pady=(0, 20))
        self.url_entry.insert(0, os.getenv('OLLAMA_URL', 'http://localhost:11434'))
        
        config_inner.columnconfigure(0, weight=1)
        
        # Buttons
        button_frame = ctk.CTkFrame(config_inner, fg_color="transparent")
        button_frame.grid(row=8, column=0, sticky="ew", pady=(0, 10))
        
        self.save_button = ctk.CTkButton(
            button_frame, text="💾 Save Settings", width=130, height=40,
            command=self.save_settings, font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=self.colors['success'], hover_color="#2d7d32"
        )
        self.save_button.pack(side="left", padx=(0, 10))
        
        self.test_button = ctk.CTkButton(
            button_frame, text="🔄 Test Connections", width=140, height=40,
            command=self.test_connections, font=ctk.CTkFont(size=13, weight="bold")
        )
        self.test_button.pack(side="left")
        
        # Instructions and Activity sections side by side
        content_frame = ctk.CTkFrame(self.tab_settings, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=15, pady=(5, 15))
        content_frame.columnconfigure(0, weight=1)
        content_frame.columnconfigure(1, weight=1)
        
        # Instructions section (left side)
        instructions_frame = ctk.CTkFrame(content_frame, corner_radius=12)
        instructions_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 7))
        
        ctk.CTkLabel(
            instructions_frame,
            text="📋 Setup Instructions",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(15, 10))
        
        instructions_text = """🔑 Discord Token:
1. Open Discord in web browser (discord.com)
2. Press F12 → Application → Local Storage → discord.com
3. Find 'token' and copy value (without quotes)

🏠 Guild ID:
1. Enable Developer Mode in Discord settings
2. Right-click server name → Copy Server ID

🤖 Ollama Setup:
1. Install from ollama.ai
2. Run: ollama serve  
3. Download model: ollama pull deepseek-r1:latest"""
        
        self.instructions_textbox = ctk.CTkTextbox(
            instructions_frame, width=380, height=250,
            font=ctk.CTkFont(family="Consolas", size=10)
        )
        self.instructions_textbox.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        self.instructions_textbox.insert("0.0", instructions_text)
        self.instructions_textbox.configure(state="disabled")
        
        # Activity log section (right side)
        activity_frame = ctk.CTkFrame(content_frame, corner_radius=12)
        activity_frame.grid(row=0, column=1, sticky="nsew", padx=(7, 0))
        
        ctk.CTkLabel(
            activity_frame,
            text="📊 Test Activity",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(15, 10))
        
        self.settings_log_textbox = ctk.CTkTextbox(
            activity_frame, width=380, height=250,
            font=ctk.CTkFont(family="Consolas", size=10),
            wrap="word"
        )
        self.settings_log_textbox.pack(fill="both", expand=True, padx=15, pady=(0, 15))
    
    def set_quick_date(self, start, end):
        """Set quick date values"""
        self.start_date_entry.delete(0, "end")
        self.start_date_entry.insert(0, start)
        self.end_date_entry.delete(0, "end") 
        self.end_date_entry.insert(0, end)
    
    def check_configuration(self):
        """Check if configuration is complete"""
        token = os.getenv('DISCORD_TOKEN', '')
        guild = os.getenv('GUILD_ID', '')
        
        if not token or not guild:
            self.status_label.configure(
                text="⚠️ Configuration needed - check Settings",
                text_color=self.colors['warning']
            )
            self.start_button.configure(state="disabled")
        else:
            self.status_label.configure(
                text="✅ Ready to generate summaries",
                text_color=self.colors['success']
            )
            self.start_button.configure(state="normal")
    
    def refresh_models(self):
        """Refresh available Ollama models"""
        def refresh():
            self.log_to_settings("🔄 Refreshing model list...")
            try:
                ollama_url = self.url_entry.get().strip()
                ollama_client = OllamaClient(ollama_url)
                models = ollama_client.get_available_models()
                
                if models:
                    # Update dropdown values
                    self.model_dropdown.configure(values=models)
                    self.log_to_settings(f"✅ Found {len(models)} models: {', '.join(models[:3])}{'...' if len(models) > 3 else ''}")
                else:
                    self.log_to_settings("❌ No models found or Ollama not accessible")
            except Exception as e:
                self.log_to_settings(f"❌ Error refreshing models: {str(e)}")
        
        threading.Thread(target=refresh, daemon=True).start()
    
    def download_model(self):
        """Download the selected model"""
        def download():
            model_name = self.model_var.get()
            self.log_to_settings(f"📥 Downloading model: {model_name}")
            
            try:
                ollama_url = self.url_entry.get().strip()
                ollama_client = OllamaClient(ollama_url)
                
                success = ollama_client.download_model(model_name)
                if success:
                    self.log_to_settings(f"✅ Model {model_name} downloaded successfully")
                    self.refresh_models()  # Refresh the list
                else:
                    self.log_to_settings(f"❌ Failed to download {model_name}")
            except Exception as e:
                self.log_to_settings(f"❌ Error downloading model: {str(e)}")
        
        threading.Thread(target=download, daemon=True).start()
    
    def save_settings(self):
        """Save settings to .env file"""
        try:
            env_content = f"""# Discord Configuration
DISCORD_TOKEN={self.token_entry.get().strip()}
GUILD_ID={self.guild_entry.get().strip()}

# Ollama Configuration  
OLLAMA_MODEL={self.model_var.get().strip()}
OLLAMA_URL={self.url_entry.get().strip()}
"""
            
            with open('.env', 'w') as f:
                f.write(env_content)
            
            # Reload environment
            load_dotenv(override=True)
            
            messagebox.showinfo("Success", "Settings saved successfully!")
            self.check_configuration()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {str(e)}")
    
    def log_to_settings(self, message):
        """Add message to settings activity log"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        log_message = f"[{timestamp}] {message}\n"
        self.root.after(0, lambda: self.settings_log_textbox.insert("end", log_message))
        self.root.after(0, lambda: self.settings_log_textbox.see("end"))
    
    def test_connections(self):
        """Test Discord and Ollama connections"""
        def test():
            self.log_to_settings("🔄 Testing connections...")
            
            # Test Discord
            try:
                token = self.token_entry.get().strip()
                guild_id = self.guild_entry.get().strip()
                
                if not token or not guild_id:
                    self.log_to_settings("❌ Discord: Token or Guild ID missing")
                else:
                    client = DiscordHTTPClient(token)
                    guild_info = client.get_guild_info(int(guild_id))
                    if guild_info:
                        self.log_to_settings(f"✅ Discord: Connected to {guild_info.get('name', 'server')}")
                    else:
                        self.log_to_settings("❌ Discord: Could not access server")
            except Exception as e:
                self.log_to_settings(f"❌ Discord: {str(e)}")
            
            # Test Ollama
            try:
                ollama_url = self.url_entry.get().strip()
                
                import requests
                response = requests.get(f"{ollama_url}/api/tags", timeout=5)
                if response.status_code == 200:
                    models = response.json().get('models', [])
                    model_names = [model['name'] for model in models[:3]]
                    self.log_to_settings(f"✅ Ollama: Connected. Models: {', '.join(model_names)}")
                    
                    # Check if selected model is available
                    selected_model = self.model_var.get()
                    available_models = [m['name'] for m in models]
                    if selected_model in available_models:
                        self.log_to_settings(f"✅ Model '{selected_model}' is available")
                    else:
                        self.log_to_settings(f"⚠️ Model '{selected_model}' not found. Click Download to install it.")
                else:
                    self.log_to_settings("❌ Ollama: API error")
            except Exception as e:
                self.log_to_settings(f"❌ Ollama: {str(e)}")
        
        threading.Thread(target=test, daemon=True).start()
    
    def start_summary(self):
        """Start the summarization process"""
        if self.is_running:
            return
        
        start_date = self.start_date_entry.get().strip()
        end_date = self.end_date_entry.get().strip()
        
        if not start_date or not end_date:
            messagebox.showerror("Error", "Please enter both start and end dates")
            return
        
        self.is_running = True
        self.start_button.configure(state="disabled")
        self.cancel_button.configure(state="normal")
        self.progress_bar.set(0)
        
        # Clear log
        self.log_textbox.delete("0.0", "end")
        
        # Start summarizer thread
        self.current_thread = threading.Thread(
            target=self.run_summarizer, 
            args=(start_date, end_date),
            daemon=True
        )
        self.current_thread.start()
    
    def run_summarizer(self, start_date, end_date):
        """Run the summarizer in background thread"""
        try:
            self.log("🚀 Starting Discord Day Summarizer...")
            self.update_progress(0.05, "Initializing...")
            
            # Create summarizer with log callback
            summarizer = DiscordDaySummarizer(start_date, end_date, log_callback=self.log)
            
            if not summarizer.client:
                self.log("❌ Discord token not configured")
                self.finish_with_error("Discord token not configured")
                return
            
            if not summarizer.guild_id:
                self.log("❌ Guild ID not configured")
                self.finish_with_error("Guild ID not configured")
                return
            
            self.update_progress(0.2, "Generating summaries...")
            
            # Generate summaries (this now returns tuple and logs everything)
            markdown_content, html_content, filename_base = summarizer.generate_summary()
            
            if not html_content:  # Error case
                self.log(f"❌ {markdown_content}")
                self.finish_with_error(markdown_content)
                return
            
            self.update_progress(0.95, "Saving files...")
            
            # Save markdown file
            md_filename = f"{filename_base}.md"
            with open(md_filename, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            # Save HTML file
            html_filename = f"{filename_base}.html"
            with open(html_filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            self.log(f"✅ Markdown saved: {md_filename}")
            self.log(f"✅ HTML saved: {html_filename}")
            self.update_progress(1.0, "Summary completed!")
            
            # Auto-open HTML file
            html_path = os.path.abspath(html_filename)
            webbrowser.open(f'file://{html_path}')
            self.log(f"🚀 Opening {html_filename} in browser...")
            
            # Show completion message
            self.root.after(0, lambda: messagebox.showinfo(
                "Summary Complete", 
                f"Summary generated successfully!\n\nMarkdown: {md_filename}\nHTML: {html_filename}\n\nHTML file opened in browser!"
            ))
            
        except Exception as e:
            self.log(f"❌ Error: {str(e)}")
            self.finish_with_error(str(e))
        finally:
            self.root.after(0, self.reset_ui)
    
    def update_progress(self, value, message):
        """Update progress bar and message"""
        self.root.after(0, lambda: self.progress_bar.set(value))
        self.root.after(0, lambda: self.progress_label.configure(text=message))
    
    def log(self, message):
        """Add message to log"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        log_message = f"[{timestamp}] {message}\n"
        self.root.after(0, lambda: self.log_textbox.insert("end", log_message))
        self.root.after(0, lambda: self.log_textbox.see("end"))
    
    def finish_with_error(self, error):
        """Finish with error"""
        self.root.after(0, lambda: messagebox.showerror("Error", error))
    
    def cancel_summary(self):
        """Cancel the running summary"""
        self.is_running = False
        self.log("❌ Summary cancelled by user")
        self.reset_ui()
    
    def reset_ui(self):
        """Reset UI after completion or cancellation"""
        self.is_running = False
        self.start_button.configure(state="normal")
        self.cancel_button.configure(state="disabled")
        self.update_progress(0, "")
    
    def open_output_folder(self):
        """Open the output folder"""
        import subprocess
        import sys
        
        if sys.platform == "win32":
            os.startfile('.')
        elif sys.platform == "darwin":
            subprocess.call(["open", "."])
        else:
            subprocess.call(["xdg-open", "."])
    
    def run(self):
        """Run the application"""
        self.root.mainloop()

def main():
    app = ModernDiscordSummarizerGUI()
    app.run()

if __name__ == "__main__":
    main()

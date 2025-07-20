#!/usr/bin/env python3
"""
Modern TUI Taiga CFD Management System
Enterprise Edition with Beautiful Terminal Interface

A comprehensive interactive tool with modern Terminal User Interface
for managing Taiga CFD analytics with rich formatting and colors.

Created by: Muhammad Zeshan Ayub
GitHub: https://github.com/ydrgzm
Email: zeshanayub.connect@gmail.com
Version: 2.1.0

Usage:
    python3 taiga_cfd_tui.py
"""

import os
import sys
import json
import getpass
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path
import requests

# Rich TUI imports
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.columns import Columns
from rich.text import Text
from rich.prompt import Prompt, Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.layout import Layout
from rich.align import Align
from rich.rule import Rule
from rich import box
from rich.tree import Tree
from rich.status import Status
import time

# Configuration
TAIGA_API_BASE_URL = "https://api.taiga.io"
PROJECT_SLUG = "azeb-admin-empathy"
PROJECT_ID = 1554789
VENV_PYTHON = "/Users/zeshan.ayub/Documents/taiga-stats/.venv/bin/python"

class ModernTaigaCFDManager:
    def __init__(self):
        self.console = Console()
        self.session_data = {}
        self.auth_token = None
        self.user_info = {}
        
        # Color scheme
        self.colors = {
            'primary': '#00D2FF',
            'secondary': '#3F51B5', 
            'success': '#4CAF50',
            'warning': '#FF9800',
            'error': '#F44336',
            'info': '#2196F3',
            'accent': '#E91E63'
        }
        
    def clear_screen(self):
        """Clear terminal screen."""
        self.console.clear()
        
    def show_header(self):
        """Display beautiful header with branding."""
        header_text = Text()
        header_text.append("🎯 TAIGA CFD ANALYTICS\n", style="bold cyan")
        header_text.append("Enterprise Terminal Interface", style="bold white")
        
        header_panel = Panel(
            Align.center(header_text),
            box=box.DOUBLE_EDGE,
            style="cyan",
            padding=(1, 2)
        )
        
        self.console.print("\n")
        self.console.print(header_panel)
        self.console.print()
        
    def show_status_bar(self):
        """Show current system status in a beautiful bar."""
        # Count files
        csv_files = [f for f in os.listdir('.') if f.startswith('cfd_data_') and f.endswith('.csv')]
        viz_dir = Path('cfd_visualizations')
        viz_files = []
        if viz_dir.exists():
            viz_files = list(viz_dir.glob('*.png')) + list(viz_dir.glob('*.pdf'))
            
        # Create status table
        status_table = Table(show_header=False, show_edge=False, pad_edge=False, box=None)
        status_table.add_column("Item", style="cyan", width=20)
        status_table.add_column("Value", style="white", width=30)
        status_table.add_column("Item2", style="cyan", width=20) 
        status_table.add_column("Value2", style="white")
        
        # Authentication status
        if self.auth_token:
            auth_status = f"✅ {self.user_info.get('full_name', 'Unknown')}"
            auth_color = "green"
        else:
            auth_status = "❌ Not authenticated"
            auth_color = "red"
            
        status_table.add_row(
            "🔐 Authentication:", auth_status,
            "📊 CSV Files:", f"{len(csv_files)} files",
        )
        status_table.add_row(
            "🎯 Project:", PROJECT_SLUG,
            "🎨 Visualizations:", f"{len(viz_files)} charts",
        )
        
        status_panel = Panel(
            status_table,
            title="[bold white]System Status[/bold white]",
            border_style="blue",
            padding=(0, 1)
        )
        
        self.console.print(status_panel)
        self.console.print()
        
    def create_menu_table(self):
        """Create beautiful main menu table."""
        menu_table = Table(
            show_header=True,
            header_style="bold magenta",
            border_style="cyan",
            box=box.ROUNDED
        )
        
        menu_table.add_column("Option", style="bold cyan", width=8, justify="center")
        menu_table.add_column("Feature", style="bold white", width=35)
        menu_table.add_column("Description", style="dim white", width=45)
        
        menu_items = [
            ("1", "🔐 Authentication Setup", "Configure Taiga credentials & tokens"),
            ("2", "📈 Generate CFD Data", "Interactive analysis with custom options"),
            ("3", "🎨 Visualization Studio", "Create, view & export beautiful charts"),
            ("4", "⚡ Quick Analysis", "Instant 1-month daily CFD analysis"),
            ("5", "🛠️ System Diagnostics", "Check authentication & file status"),
            ("6", "📚 Help Center", "Built-in documentation & guides"),
            ("7", "🚪 Exit", "Clean shutdown with confirmation")
        ]
        
        for option, feature, description in menu_items:
            menu_table.add_row(option, feature, description)
            
        return menu_table
        
    def show_main_menu(self):
        """Display the main menu with beautiful formatting."""
        self.clear_screen()
        self.show_header()
        self.show_status_bar()
        
        menu_table = self.create_menu_table()
        menu_panel = Panel(
            menu_table,
            title="[bold white]🎮 Main Menu[/bold white]",
            border_style="magenta",
            padding=(1, 2)
        )
        
        self.console.print(menu_panel)
        self.console.print()
        
    def animated_prompt(self, message, choices=None, default=None):
        """Beautiful animated prompt with validation."""
        if choices:
            choice_text = f" [dim]({'/'.join(choices)})[/dim]"
        else:
            choice_text = ""
            
        if default:
            default_text = f" [dim][default: {default}][/dim]"
        else:
            default_text = ""
            
        prompt_text = f"[bold cyan]❯[/bold cyan] {message}{choice_text}{default_text}: "
        
        while True:
            response = Prompt.ask(prompt_text, console=self.console)
            
            if not response and default:
                return default
                
            if not response:
                self.console.print("[red]❌ Input required. Please try again.[/red]")
                continue
                
            if choices and response not in choices:
                self.console.print(f"[red]❌ Invalid choice. Please select from: {', '.join(choices)}[/red]")
                continue
                
            return response
            
    def show_progress_bar(self, task_description, duration=2):
        """Show animated progress bar."""
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console,
        ) as progress:
            task = progress.add_task(task_description, total=100)
            
            for i in range(100):
                time.sleep(duration / 100)
                progress.update(task, advance=1)
                
    def show_success_panel(self, title, message, details=None):
        """Display success message in beautiful panel."""
        success_text = Text()
        success_text.append("✅ ", style="bold green")
        success_text.append(message, style="green")
        
        if details:
            success_text.append(f"\n\n{details}", style="dim green")
            
        panel = Panel(
            success_text,
            title=f"[bold green]{title}[/bold green]",
            border_style="green",
            padding=(1, 2)
        )
        
        self.console.print(panel)
        self.console.print()
        
    def show_error_panel(self, title, message, suggestion=None):
        """Display error message in beautiful panel."""
        error_text = Text()
        error_text.append("❌ ", style="bold red")
        error_text.append(message, style="red")
        
        if suggestion:
            error_text.append(f"\n\n💡 {suggestion}", style="yellow")
            
        panel = Panel(
            error_text,
            title=f"[bold red]{title}[/bold red]",
            border_style="red",
            padding=(1, 2)
        )
        
        self.console.print(panel)
        self.console.print()
        
    def load_existing_auth(self):
        """Load existing authentication with visual feedback."""
        with self.console.status("[cyan]🔍 Checking for existing authentication...", spinner="dots"):
            time.sleep(1)  # Visual delay for effect
            
            token_files = [f for f in os.listdir('.') if f.startswith('taiga_tokens_') and f.endswith('.json')]
            if not token_files:
                return False
                
            latest_token_file = max(token_files, key=os.path.getmtime)
            
            try:
                with open(latest_token_file, 'r') as f:
                    token_data = json.load(f)
                    self.auth_token = token_data.get('auth_token')
                    self.user_info = token_data.get('user_info', {})
                    
                if self.test_auth_token():
                    user_name = self.user_info.get('full_name', 'Unknown User')
                    self.show_success_panel(
                        "Authentication Found", 
                        f"Loaded existing authentication for {user_name}",
                        f"Token file: {latest_token_file}"
                    )
                    return True
            except Exception as e:
                self.show_error_panel("Authentication Error", f"Could not load existing auth: {e}")
                
            return False
            
    def test_auth_token(self):
        """Test if the current auth token is valid."""
        if not self.auth_token:
            return False
            
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        try:
            response = requests.get(f"{TAIGA_API_BASE_URL}/api/v1/users/me", 
                                  headers=headers, timeout=10)
            return response.status_code == 200
        except:
            return False
            
    def authenticate_user(self):
        """Beautiful authentication process."""
        self.clear_screen()
        
        # Header
        auth_header = Panel(
            "[bold cyan]🔐 Taiga Authentication Setup[/bold cyan]\n[dim]Secure your connection to Taiga API",
            box=box.DOUBLE_EDGE,
            border_style="cyan",
            padding=(1, 2)
        )
        self.console.print(auth_header)
        self.console.print()
        
        # Check for existing auth
        if self.load_existing_auth():
            if Confirm.ask("✨ Use existing authentication?", console=self.console, default=True):
                return True
                
        # Credential input
        self.console.print("[bold yellow]📝 Please provide your Taiga credentials:[/bold yellow]")
        self.console.print("[dim]Your password will be hidden for security[/dim]\n")
        
        username = Prompt.ask("👤 Username or Email", console=self.console)
        password = getpass.getpass("🔒 Password: ")
        
        # Authentication process
        self.show_progress_bar("🔄 Authenticating with Taiga API...", 3)
        
        # Authenticate with Taiga
        auth_data = {
            "type": "normal",
            "username": username,
            "password": password
        }
        
        try:
            response = requests.post(f"{TAIGA_API_BASE_URL}/api/v1/auth", 
                                   json=auth_data, timeout=30)
            
            if response.status_code == 200:
                auth_response = response.json()
                self.auth_token = auth_response.get('auth_token')
                
                # Get user info
                headers = {"Authorization": f"Bearer {self.auth_token}"}
                user_response = requests.get(f"{TAIGA_API_BASE_URL}/api/v1/users/me", 
                                           headers=headers, timeout=10)
                
                if user_response.status_code == 200:
                    self.user_info = user_response.json()
                    
                    # Save tokens
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    token_file = f"taiga_tokens_{timestamp}.json"
                    
                    token_data = {
                        'auth_token': self.auth_token,
                        'user_info': self.user_info,
                        'created_at': timestamp
                    }
                    
                    with open(token_file, 'w') as f:
                        json.dump(token_data, f, indent=2)
                        
                    user_name = self.user_info.get('full_name', 'User')
                    self.show_success_panel(
                        "Authentication Successful",
                        f"Welcome, {user_name}!",
                        f"🔑 Tokens saved to: {token_file}"
                    )
                    return True
                    
            self.show_error_panel(
                "Authentication Failed", 
                "Invalid credentials. Please check your username and password.",
                "Make sure you're using the correct Taiga account credentials"
            )
            return False
            
        except Exception as e:
            self.show_error_panel("Connection Error", f"Authentication error: {e}")
            return False
            
    def get_date_range_selection(self):
        """Beautiful date range selection interface."""
        self.clear_screen()
        
        # Header
        date_header = Panel(
            "[bold magenta]📅 Date Range Selection[/bold magenta]\n[dim]Choose your analysis period for CFD generation",
            border_style="magenta",
            padding=(1, 2)
        )
        self.console.print(date_header)
        self.console.print()
        
        # Options table
        options_table = Table(
            show_header=True,
            header_style="bold cyan",
            border_style="blue",
            box=box.ROUNDED
        )
        
        options_table.add_column("Option", style="bold cyan", width=8, justify="center")
        options_table.add_column("Type", style="bold white", width=20)
        options_table.add_column("Description", style="dim white")
        
        options_table.add_row("1", "📊 Preset Ranges", "Quick selection from common periods")
        options_table.add_row("2", "🎯 Custom Range", "Specify exact start and end dates")
        
        options_panel = Panel(
            options_table,
            title="[bold white]Selection Options[/bold white]",
            border_style="blue"
        )
        
        self.console.print(options_panel)
        self.console.print()
        
        choice = self.animated_prompt("Select date range type", ["1", "2"], "1")
        
        if choice == "1":
            return self.get_preset_date_range()
        else:
            return self.get_custom_date_range()
            
    def get_preset_date_range(self):
        """Beautiful preset date range selection."""
        self.console.print()
        
        preset_table = Table(
            show_header=True,
            header_style="bold green",
            border_style="green",
            box=box.ROUNDED
        )
        
        preset_table.add_column("Option", style="bold green", width=8, justify="center")
        preset_table.add_column("Period", style="bold white", width=20)
        preset_table.add_column("Data Points", style="cyan", width=15)
        preset_table.add_column("Best For", style="dim white")
        
        preset_options = [
            ("1", "Last 1 Month", "~30 days", "Sprint analysis, recent trends"),
            ("2", "Last 3 Months", "~90 days", "Quarterly reviews, pattern detection"),
            ("3", "Last 6 Months", "~180 days", "Half-year analysis, long-term trends"),
            ("4", "Last 12 Months", "~365 days", "Annual review, yearly patterns"),
            ("5", "Year to Date", "Jan 1 - Today", "Current year performance")
        ]
        
        for option, period, points, best_for in preset_options:
            preset_table.add_row(option, period, points, best_for)
            
        preset_panel = Panel(
            preset_table,
            title="[bold white]📊 Preset Date Ranges[/bold white]",
            border_style="green"
        )
        
        self.console.print(preset_panel)
        self.console.print()
        
        choice = self.animated_prompt("Select preset range", ["1", "2", "3", "4", "5"], "2")
        
        end_date = datetime.now(timezone.utc)
        
        range_map = {
            "1": (end_date - timedelta(days=30), "Last 1 Month"),
            "2": (end_date - timedelta(days=90), "Last 3 Months"), 
            "3": (end_date - timedelta(days=180), "Last 6 Months"),
            "4": (end_date - timedelta(days=365), "Last 12 Months"),
            "5": (datetime(2025, 1, 1, tzinfo=timezone.utc), "Year to Date 2025")
        }
        
        start_date, period_name = range_map[choice]
        return start_date, end_date, period_name
        
    def get_custom_date_range(self):
        """Beautiful custom date range input."""
        self.console.print()
        
        custom_panel = Panel(
            "[bold yellow]📅 Custom Date Range Entry[/bold yellow]\n" +
            "[dim]Format: YYYY-MM-DD (e.g., 2025-01-15)[/dim]\n" +
            "[dim]Enter your specific analysis period below[/dim]",
            border_style="yellow",
            padding=(1, 2)
        )
        
        self.console.print(custom_panel)
        self.console.print()
        
        while True:
            try:
                start_str = Prompt.ask("📅 Start Date (YYYY-MM-DD)", console=self.console)
                start_date = datetime.strptime(start_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
                break
            except ValueError:
                self.console.print("[red]❌ Invalid date format. Please use YYYY-MM-DD[/red]")
                
        while True:
            try:
                end_str = Prompt.ask(
                    "📅 End Date (YYYY-MM-DD)", 
                    default=datetime.now().strftime("%Y-%m-%d"),
                    console=self.console
                )
                end_date = datetime.strptime(end_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
                
                if end_date < start_date:
                    self.console.print("[red]❌ End date must be after start date[/red]")
                    continue
                    
                break
            except ValueError:
                self.console.print("[red]❌ Invalid date format. Please use YYYY-MM-DD[/red]")
                
        period_name = f"Custom: {start_str} to {end_str}"
        
        # Confirmation with beautiful summary
        summary_table = Table(show_header=False, box=box.MINIMAL_HEAVY_HEAD)
        summary_table.add_column("Field", style="cyan", width=15)
        summary_table.add_column("Value", style="white")
        
        days_diff = (end_date - start_date).days
        summary_table.add_row("📅 Start Date:", start_str)
        summary_table.add_row("📅 End Date:", end_str)
        summary_table.add_row("📊 Duration:", f"{days_diff} days")
        summary_table.add_row("🎯 Period:", period_name)
        
        summary_panel = Panel(
            summary_table,
            title="[bold white]📋 Date Range Summary[/bold white]",
            border_style="cyan"
        )
        
        self.console.print(summary_panel)
        
        return start_date, end_date, period_name
        
    def get_granularity_selection(self):
        """Beautiful granularity selection interface."""
        self.console.print()
        
        granularity_header = Panel(
            "[bold blue]📈 Data Granularity Selection[/bold blue]\n[dim]Choose how detailed your CFD analysis should be",
            border_style="blue",
            padding=(1, 2)
        )
        self.console.print(granularity_header)
        self.console.print()
        
        granularity_table = Table(
            show_header=True,
            header_style="bold blue",
            border_style="blue",
            box=box.ROUNDED
        )
        
        granularity_table.add_column("Option", style="bold blue", width=8, justify="center")
        granularity_table.add_column("Granularity", style="bold white", width=15)
        granularity_table.add_column("Best For", style="cyan", width=25)
        granularity_table.add_column("Typical Points", style="green", width=15)
        granularity_table.add_column("Use Case", style="dim white")
        
        granularity_options = [
            ("1", "🔍 Daily", "< 3 months", "~90 points", "Sprint analysis, detailed workflow"),
            ("2", "📊 Weekly", "3-12 months", "~52 points", "Monthly reports, trend tracking"),
            ("3", "📈 Monthly", "> 6 months", "~12 points", "Quarterly reviews, executive summaries")
        ]
        
        for option, gran, best_for, points, use_case in granularity_options:
            granularity_table.add_row(option, gran, best_for, points, use_case)
            
        granularity_panel = Panel(
            granularity_table,
            title="[bold white]⚡ Granularity Options[/bold white]",
            border_style="blue"
        )
        
        self.console.print(granularity_panel)
        self.console.print()
        
        choice = self.animated_prompt("Select granularity", ["1", "2", "3"], "1")
        
        granularity_map = {"1": "daily", "2": "weekly", "3": "monthly"}
        return granularity_map[choice]
        
    def generate_cfd_with_beautiful_progress(self, start_date, end_date, granularity, period_name):
        """Generate CFD data with beautiful progress display."""
        self.clear_screen()
        
        # Generation header
        gen_header = Panel(
            f"[bold green]📊 CFD Data Generation[/bold green]\n[dim]Creating comprehensive flow analysis",
            border_style="green",
            padding=(1, 2)
        )
        self.console.print(gen_header)
        self.console.print()
        
        # Parameters summary
        params_table = Table(show_header=False, box=box.MINIMAL)
        params_table.add_column("Parameter", style="cyan", width=20)
        params_table.add_column("Value", style="white")
        
        params_table.add_row("📅 Period:", period_name)
        params_table.add_row("📈 Granularity:", granularity.title())
        params_table.add_row("🗓️ Date Range:", f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
        params_table.add_row("🎯 Project:", PROJECT_SLUG)
        
        params_panel = Panel(
            params_table,
            title="[bold white]📋 Generation Parameters[/bold white]",
            border_style="cyan"
        )
        self.console.print(params_panel)
        self.console.print()
        
        try:
            # Command construction
            cmd = [
                VENV_PYTHON,
                "taiga_cfd_generator.py",
                f"--granularity={granularity}",
                f"--start-date={start_date.strftime('%Y-%m-%d')}",
                f"--end-date={end_date.strftime('%Y-%m-%d')}"
            ]
            
            # Beautiful progress display
            with self.console.status("[cyan]🚀 Launching CFD generator...", spinner="dots"):
                time.sleep(1)
                
            self.console.print("[green]🔄 Running CFD generation engine...[/green]")
            self.console.print(f"[dim]Command: {' '.join(cmd[1:])}[/dim]\n")
            
            result = subprocess.run(cmd, cwd=os.getcwd())
            
            if result.returncode == 0:
                self.show_success_panel(
                    "Generation Complete", 
                    "CFD data and visualizations created successfully!",
                    "📄 CSV data file generated\n🎨 Professional charts created\n📊 Ready for analysis"
                )
                return True
            else:
                self.show_error_panel(
                    "Generation Failed",
                    "CFD data generation encountered an error",
                    "Check your authentication and try again"
                )
                return False
                
        except Exception as e:
            self.show_error_panel("System Error", f"Unexpected error during generation: {e}")
            return False
            
    def show_visualization_studio(self):
        """Beautiful visualization management interface."""
        self.clear_screen()
        
        # Studio header
        studio_header = Panel(
            "[bold magenta]🎨 Visualization Studio[/bold magenta]\n[dim]Create, manage and export professional CFD charts",
            border_style="magenta",
            padding=(1, 2)
        )
        self.console.print(studio_header)
        self.console.print()
        
        # Studio menu
        studio_table = Table(
            show_header=True,
            header_style="bold magenta",
            border_style="magenta",
            box=box.ROUNDED
        )
        
        studio_table.add_column("Option", style="bold magenta", width=8, justify="center")
        studio_table.add_column("Action", style="bold white", width=30)
        studio_table.add_column("Description", style="dim white")
        
        studio_options = [
            ("1", "✨ Generate Latest Charts", "Create visualizations from newest data"),
            ("2", "📊 Choose Specific Data", "Generate charts from selected CSV file"),
            ("3", "👀 View Gallery", "Browse existing visualizations"),
            ("4", "📤 Export Studio", "Convert charts to different formats"),
            ("5", "🔙 Return to Main", "Back to main menu")
        ]
        
        for option, action, desc in studio_options:
            studio_table.add_row(option, action, desc)
            
        studio_panel = Panel(
            studio_table,
            title="[bold white]🎭 Studio Actions[/bold white]",
            border_style="magenta"
        )
        
        self.console.print(studio_panel)
        self.console.print()
        
        choice = self.animated_prompt("Select studio action", ["1", "2", "3", "4", "5"], "1")
        
        if choice == "1":
            self.generate_latest_visualizations()
        elif choice == "2":
            self.generate_custom_visualizations()
        elif choice == "3":
            self.view_visualization_gallery()
        elif choice == "4":
            self.export_visualization_studio()
        # Option 5 returns to main menu
        
    def generate_latest_visualizations(self):
        """Generate visualizations with beautiful feedback."""
        self.console.print("\n[cyan]🎨 Generating visualizations from latest data...[/cyan]")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console,
        ) as progress:
            task = progress.add_task("Creating professional charts...", total=100)
            
            try:
                cmd = [VENV_PYTHON, "cfd_visualizer.py", "--latest"]
                
                # Simulate progress during subprocess
                import threading
                result_container = []
                
                def run_command():
                    result = subprocess.run(cmd, capture_output=True, text=True)
                    result_container.append(result)
                
                thread = threading.Thread(target=run_command)
                thread.start()
                
                while thread.is_alive():
                    progress.update(task, advance=2)
                    time.sleep(0.1)
                    
                thread.join()
                progress.update(task, completed=100)
                
                if result_container[0].returncode == 0:
                    self.show_success_panel(
                        "Charts Created",
                        "Beautiful visualizations generated successfully!",
                        "📊 Dashboard, trends, and distribution charts ready"
                    )
                else:
                    self.show_error_panel("Generation Failed", "Could not create visualizations")
                    
            except Exception as e:
                self.show_error_panel("Error", f"Visualization error: {e}")
                
        Prompt.ask("\n[dim]Press Enter to continue...", console=self.console)
        
    def generate_custom_visualizations(self):
        """Generate visualizations from specific CSV file."""
        self.console.print("\n[cyan]📊 Choose specific CSV file for visualization...[/cyan]")
        
        # Find CSV files
        csv_files = [f for f in os.listdir('.') if f.startswith('cfd_data_') and f.endswith('.csv')]
        
        if not csv_files:
            self.show_error_panel(
                "No Data Files",
                "No CFD CSV files found in current directory",
                "Generate some CFD data first using option 2"
            )
            Prompt.ask("\n[dim]Press Enter to continue...", console=self.console)
            return
            
        # Display CSV files
        csv_table = Table(
            show_header=True,
            header_style="bold green",
            border_style="green",
            box=box.ROUNDED
        )
        
        csv_table.add_column("#", style="bold green", width=5)
        csv_table.add_column("CSV File", style="bold white", width=50)
        csv_table.add_column("Size", style="cyan", width=10)
        csv_table.add_column("Modified", style="dim white")
        
        for i, file in enumerate(sorted(csv_files, key=lambda f: os.path.getmtime(f), reverse=True), 1):
            size_kb = os.path.getsize(file) // 1024
            modified = datetime.fromtimestamp(os.path.getmtime(file)).strftime('%m/%d %H:%M')
            csv_table.add_row(str(i), file, f"{size_kb}KB", modified)
            
        csv_panel = Panel(
            csv_table,
            title="[bold white]📄 Available CSV Files[/bold white]",
            border_style="green"
        )
        
        self.console.print(csv_panel)
        
        choice_num = self.animated_prompt(
            "Select CSV file number", 
            [str(i) for i in range(1, len(csv_files) + 1)], 
            "1"
        )
        
        selected_file = sorted(csv_files, key=lambda f: os.path.getmtime(f), reverse=True)[int(choice_num) - 1]
        
        self.console.print(f"\n[green]🎨 Generating charts from: {selected_file}[/green]")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console,
        ) as progress:
            task = progress.add_task("Creating custom visualizations...", total=100)
            
            try:
                cmd = [VENV_PYTHON, "cfd_visualizer.py", selected_file]
                
                import threading
                result_container = []
                
                def run_command():
                    result = subprocess.run(cmd, capture_output=True, text=True)
                    result_container.append(result)
                
                thread = threading.Thread(target=run_command)
                thread.start()
                
                while thread.is_alive():
                    progress.update(task, advance=2)
                    time.sleep(0.1)
                    
                thread.join()
                progress.update(task, completed=100)
                
                if result_container[0].returncode == 0:
                    self.show_success_panel(
                        "Custom Charts Created",
                        f"Visualizations generated from {selected_file}",
                        "📊 All chart types created and saved"
                    )
                else:
                    self.show_error_panel("Generation Failed", "Could not create custom visualizations")
                    
            except Exception as e:
                self.show_error_panel("Error", f"Visualization error: {e}")
                
        Prompt.ask("\n[dim]Press Enter to continue...", console=self.console)
        
    def export_visualization_studio(self):
        """Export visualization studio with format options."""
        self.console.print("\n[cyan]📤 Export Studio - Convert charts to different formats[/cyan]")
        
        viz_dir = Path('cfd_visualizations')
        if not viz_dir.exists():
            self.show_error_panel(
                "No Export Data",
                "Visualization directory doesn't exist",
                "Generate some charts first"
            )
            Prompt.ask("\n[dim]Press Enter to continue...", console=self.console)
            return
            
        png_files = list(viz_dir.glob('*.png'))
        
        if not png_files:
            self.show_error_panel(
                "No Charts Found",
                "No PNG charts found for export",
                "Create some visualizations first"
            )
            Prompt.ask("\n[dim]Press Enter to continue...", console=self.console)
            return
            
        # Export options
        export_table = Table(
            show_header=True,
            header_style="bold blue",
            border_style="blue",
            box=box.ROUNDED
        )
        
        export_table.add_column("Option", style="bold blue", width=8)
        export_table.add_column("Format", style="bold white", width=15)
        export_table.add_column("Best For", style="cyan", width=25)
        export_table.add_column("Quality", style="green")
        
        export_table.add_row("1", "📄 PDF", "Reports, presentations", "Vector (scalable)")
        export_table.add_row("2", "📊 SVG", "Web, design tools", "Vector (editable)")
        export_table.add_row("3", "📂 Open Folder", "Manual management", "Current formats")
        
        export_panel = Panel(
            export_table,
            title="[bold white]📤 Export Options[/bold white]",
            border_style="blue"
        )
        
        self.console.print(export_panel)
        
        choice = self.animated_prompt("Select export option", ["1", "2", "3"], "3")
        
        if choice == "1":
            self.console.print("[yellow]📄 PDF export coming soon![/yellow]")
        elif choice == "2":
            self.console.print("[yellow]📊 SVG export coming soon![/yellow]")
        else:
            # Open folder
            self.console.print("\n[green]📂 Opening visualizations folder...[/green]")
            try:
                subprocess.run(['open', str(viz_dir)], check=False)
                self.console.print("[green]✅ Folder opened in Finder[/green]")
            except:
                self.console.print(f"[yellow]📁 Manual path: {viz_dir.absolute()}[/yellow]")
                
        Prompt.ask("\n[dim]Press Enter to continue...", console=self.console)
        
    def view_visualization_gallery(self):
        """Beautiful visualization gallery interface."""
        viz_dir = Path('cfd_visualizations')
        
        if not viz_dir.exists():
            self.show_error_panel(
                "No Gallery Found",
                "Visualization directory doesn't exist",
                "Generate some charts first using the studio options"
            )
            Prompt.ask("\n[dim]Press Enter to continue...", console=self.console)
            return
            
        viz_files = list(viz_dir.glob('*.png')) + list(viz_dir.glob('*.pdf'))
        
        if not viz_files:
            self.show_error_panel(
                "Empty Gallery", 
                "No visualization files found",
                "Create some charts first using the generation options"
            )
            Prompt.ask("\n[dim]Press Enter to continue...", console=self.console)
            return
            
        # Gallery display
        gallery_table = Table(
            show_header=True,
            header_style="bold cyan",
            border_style="cyan",
            box=box.ROUNDED
        )
        
        gallery_table.add_column("Chart", style="bold white", width=40)
        gallery_table.add_column("Type", style="cyan", width=15)
        gallery_table.add_column("Size", style="green", width=10)
        gallery_table.add_column("Modified", style="dim white")
        
        for file in sorted(viz_files, key=lambda f: f.stat().st_mtime, reverse=True):
            chart_type = "Dashboard" if "dashboard" in file.name else \
                        "Stacked Area" if "stackedarea" in file.name else \
                        "Distribution" if "distribution" in file.name else \
                        "Trends" if "trends" in file.name else "Other"
                        
            size_kb = file.stat().st_size // 1024
            modified = datetime.fromtimestamp(file.stat().st_mtime).strftime('%m/%d %H:%M')
            
            gallery_table.add_row(file.name[:35] + "..." if len(file.name) > 35 else file.name, 
                                chart_type, f"{size_kb}KB", modified)
            
        gallery_panel = Panel(
            gallery_table,
            title=f"[bold white]🖼️ Visualization Gallery ({len(viz_files)} files)[/bold white]",
            border_style="cyan"
        )
        
        self.console.print(gallery_panel)
        
        self.console.print("\n[green]📂 Opening gallery folder...[/green]")
        try:
            subprocess.run(['open', str(viz_dir)], check=False)
            self.console.print("[green]✅ Gallery opened in Finder[/green]")
        except:
            self.console.print(f"[yellow]📁 Manual path: {viz_dir.absolute()}[/yellow]")
            
        Prompt.ask("\n[dim]Press Enter to continue...", console=self.console)
        
    def show_system_diagnostics(self):
        """Beautiful system diagnostics interface."""
        self.clear_screen()
        
        # Diagnostics header
        diag_header = Panel(
            "[bold yellow]🛠️ System Diagnostics[/bold yellow]\n[dim]Complete system health and status report",
            border_style="yellow",
            padding=(1, 2)
        )
        self.console.print(diag_header)
        self.console.print()
        
        # Run diagnostics with progress
        with self.console.status("[yellow]🔍 Running system diagnostics...", spinner="dots"):
            time.sleep(2)  # Simulate diagnostic time
            
        # Authentication status
        auth_table = Table(show_header=False, box=box.MINIMAL)
        auth_table.add_column("Component", style="cyan", width=25)
        auth_table.add_column("Status", style="white", width=40)
        
        if self.auth_token:
            auth_status = f"✅ Active - {self.user_info.get('full_name', 'Unknown')}"
            email_status = f"📧 {self.user_info.get('email', 'Unknown')}"
        else:
            auth_status = "❌ Not configured"
            email_status = "📧 No user data"
            
        auth_table.add_row("🔐 Authentication:", auth_status)
        auth_table.add_row("👤 User Account:", email_status)
        
        auth_panel = Panel(auth_table, title="[bold white]Authentication Status[/bold white]", border_style="green" if self.auth_token else "red")
        
        # System status
        venv_path = Path(VENV_PYTHON)
        csv_files = [f for f in os.listdir('.') if f.startswith('cfd_data_') and f.endswith('.csv')]
        viz_dir = Path('cfd_visualizations')
        viz_files = []
        if viz_dir.exists():
            viz_files = list(viz_dir.glob('*.png')) + list(viz_dir.glob('*.pdf'))
            
        system_table = Table(show_header=False, box=box.MINIMAL)
        system_table.add_column("Component", style="cyan", width=25)
        system_table.add_column("Status", style="white")
        
        system_table.add_row("🐍 Python Environment:", "✅ Configured" if venv_path.exists() else "❌ Not found")
        system_table.add_row("📄 CSV Data Files:", f"📊 {len(csv_files)} files available")
        system_table.add_row("🎨 Visualization Files:", f"🖼️ {len(viz_files)} charts created")
        system_table.add_row("🎯 Target Project:", f"{PROJECT_SLUG} (ID: {PROJECT_ID})")
        system_table.add_row("🌐 API Endpoint:", TAIGA_API_BASE_URL)
        
        if csv_files:
            latest_csv = max(csv_files, key=os.path.getmtime)
            system_table.add_row("📊 Latest Data:", latest_csv)
            
        system_panel = Panel(system_table, title="[bold white]System Components[/bold white]", border_style="blue")
        
        # Display panels
        self.console.print(auth_panel)
        self.console.print()
        self.console.print(system_panel)
        
        Prompt.ask("\n[dim]Press Enter to continue...", console=self.console)
        
    def show_help_center(self):
        """Beautiful help center interface."""
        self.clear_screen()
        
        # Help header
        help_header = Panel(
            "[bold blue]📚 Help Center[/bold blue]\n[dim]Comprehensive guide to CFD analytics system",
            border_style="blue",
            padding=(1, 2)
        )
        self.console.print(help_header)
        self.console.print()
        
        # Create help tree
        help_tree = Tree("🎯 [bold]Taiga CFD System Guide[/bold]")
        
        # Authentication branch
        auth_branch = help_tree.add("🔐 [bold cyan]Authentication[/bold cyan]")
        auth_branch.add("• One-time setup with Taiga credentials")
        auth_branch.add("• Secure token storage and auto-detection")
        auth_branch.add("• Re-authentication when tokens expire")
        
        # CFD Generation branch
        cfd_branch = help_tree.add("📈 [bold green]CFD Data Generation[/bold green]")
        cfd_branch.add("• Choose preset or custom date ranges")
        cfd_branch.add("• Select daily, weekly, or monthly granularity")
        cfd_branch.add("• Automatic CSV export with timestamp")
        cfd_branch.add("• Integrated visualization generation")
        
        # Visualization branch
        viz_branch = help_tree.add("🎨 [bold magenta]Visualization Studio[/bold magenta]")
        viz_branch.add("• 📊 Comprehensive Dashboard (recommended)")
        viz_branch.add("• 📈 Stacked Area Chart (classic CFD)")
        viz_branch.add("• 🥧 Status Distribution Pie Chart")
        viz_branch.add("• 📊 Trend Analysis with Velocity")
        
        # Tips branch
        tips_branch = help_tree.add("💡 [bold yellow]Enterprise Tips[/bold yellow]")
        tips_branch.add("• Use Quick Analysis for daily monitoring")
        tips_branch.add("• Generate monthly reports with custom ranges")
        tips_branch.add("• Export as PDF for presentations")
        tips_branch.add("• Keep CSV files for historical analysis")
        
        # Credits branch
        credits_branch = help_tree.add("👨‍💻 [bold yellow]Credits[/bold yellow]")
        credits_branch.add("• Created by: Muhammad Zeshan Ayub")
        credits_branch.add("• GitHub: https://github.com/ydrgzm")
        credits_branch.add("• Email: zeshanayub.connect@gmail.com")
        credits_branch.add("• Version: 2.1.0 (Enterprise Edition)")
        
        help_panel = Panel(help_tree, title="[bold white]📖 User Guide[/bold white]", border_style="blue")
        self.console.print(help_panel)
        
        # Granularity guide
        self.console.print()
        granularity_guide = Table(
            title="📊 [bold]Granularity Selection Guide[/bold]",
            show_header=True,
            header_style="bold blue",
            border_style="blue",
            box=box.ROUNDED
        )
        
        granularity_guide.add_column("Granularity", style="bold white", width=12)
        granularity_guide.add_column("Best For", style="cyan", width=20)
        granularity_guide.add_column("Data Points", style="green", width=15)
        granularity_guide.add_column("Use Case", style="dim white")
        
        granularity_guide.add_row("Daily", "< 3 months", "~90 points", "Sprint analysis, detailed workflow")
        granularity_guide.add_row("Weekly", "3-12 months", "~52 points", "Monthly reports, trend tracking")
        granularity_guide.add_row("Monthly", "> 6 months", "~12 points", "Quarterly reviews, executive summaries")
        
        self.console.print(granularity_guide)
        
        Prompt.ask("\n[dim]Press Enter to continue...", console=self.console)
        
    def run_interactive_system(self):
        """Main interactive system loop."""
        while True:
            self.show_main_menu()
            
            choice = self.animated_prompt("Select option", ["1", "2", "3", "4", "5", "6", "7"], "2")
            
            if choice == "1":
                # Authentication
                self.authenticate_user()
                Prompt.ask("\n[dim]Press Enter to continue...", console=self.console)
                
            elif choice == "2":
                # Generate CFD Data
                if not self.auth_token:
                    self.show_error_panel(
                        "Authentication Required", 
                        "Please authenticate first before generating CFD data",
                        "Select option 1 to set up authentication"
                    )
                    Prompt.ask("\n[dim]Press Enter to continue...", console=self.console)
                    continue
                    
                start_date, end_date, period_name = self.get_date_range_selection()
                granularity = self.get_granularity_selection()
                self.generate_cfd_with_beautiful_progress(start_date, end_date, granularity, period_name)
                Prompt.ask("\n[dim]Press Enter to continue...", console=self.console)
                
            elif choice == "3":
                # Visualization Studio
                self.show_visualization_studio()
                
            elif choice == "4":
                # Quick Analysis
                if not self.auth_token:
                    self.show_error_panel(
                        "Authentication Required",
                        "Please authenticate first before running analysis",
                        "Select option 1 to set up authentication"
                    )
                    Prompt.ask("\n[dim]Press Enter to continue...", console=self.console)
                    continue
                    
                self.console.print("\n[bold green]⚡ Quick Analysis: Last 1 month with daily granularity[/bold green]")
                end_date = datetime.now(timezone.utc)
                start_date = end_date - timedelta(days=30)
                self.generate_cfd_with_beautiful_progress(start_date, end_date, "daily", "Quick: Last 1 Month")
                Prompt.ask("\n[dim]Press Enter to continue...", console=self.console)
                
            elif choice == "5":
                # System Status
                self.show_system_diagnostics()
                
            elif choice == "6":
                # Help
                self.show_help_center()
                
            elif choice == "7":
                # Exit
                if Confirm.ask("\n[yellow]🚪 Are you sure you want to exit?[/yellow]", console=self.console):
                    self.console.print("\n[bold cyan]👋 Thank you for using Taiga CFD Analytics![/bold cyan]")
                    self.console.print("[dim]Created by Muhammad Zeshan Ayub (https://github.com/ydrgzm)[/dim]")
                    self.console.print("[dim]Your enterprise CFD system is ready for use.[/dim]\n")
                    sys.exit(0)

def main():
    """Main entry point for modern TUI CFD system."""
    try:
        # Dependency check with beautiful error
        console = Console()
        try:
            import requests
            import matplotlib
            import seaborn
            import pandas
        except ImportError as e:
            error_panel = Panel(
                f"[red]❌ Missing required dependency![/red]\n\n" +
                f"[yellow]Error: {e}[/yellow]\n\n" +
                "[cyan]💡 Install dependencies with:[/cyan]\n" +
                "[white]pip install -r requirements.txt[/white]",
                title="[bold red]Dependency Error[/bold red]",
                border_style="red",
                padding=(1, 2)
            )
            console.print(error_panel)
            sys.exit(1)
            
        # Welcome message
        console.print("\n[bold cyan]🚀 Launching Modern TUI CFD System...[/bold cyan]")
        time.sleep(1)
        
        manager = ModernTaigaCFDManager()
        manager.run_interactive_system()
        
    except KeyboardInterrupt:
        console = Console()
        console.print("\n\n[bold yellow]👋 Session interrupted. Goodbye![/bold yellow]")
        sys.exit(0)
    except Exception as e:
        console = Console()
        error_panel = Panel(
            f"[red]❌ Unexpected system error:[/red]\n\n[yellow]{e}[/yellow]\n\n" +
            "[cyan]Please report this issue to the development team.[/cyan]",
            title="[bold red]System Error[/bold red]",
            border_style="red"
        )
        console.print(error_panel)
        sys.exit(1)

if __name__ == "__main__":
    main()

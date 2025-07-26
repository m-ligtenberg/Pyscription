"""
Modern terminal styling and colors for Pyscription CLI
Beautiful syntax highlighting and UI elements
"""

import os
import sys
import time
from typing import Optional


class Colors:
    """ANSI color codes for terminal styling"""
    
    # Reset
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    
    # Background colors
    BG_LIGHT_BLUE = '\033[48;5;153m'    # Light blue background
    BG_DARK_BLUE = '\033[48;5;18m'      # Dark blue background
    BG_WHITE = '\033[48;5;231m'         # White background
    BG_GRAY = '\033[48;5;240m'          # Gray background
    BG_GREEN = '\033[48;5;46m'          # Green background
    BG_RED = '\033[48;5;196m'           # Red background
    BG_YELLOW = '\033[48;5;226m'        # Yellow background
    
    # Foreground colors - Modern syntax highlighting
    BLACK = '\033[38;5;16m'             # Pure black
    WHITE = '\033[38;5;231m'            # Pure white
    DARK_BLUE = '\033[38;5;18m'         # Dark blue for main text
    BRIGHT_BLUE = '\033[38;5;39m'       # Keywords, commands
    CYAN = '\033[38;5;51m'              # Function names, identifiers
    GREEN = '\033[38;5;46m'             # Strings, success messages
    ORANGE = '\033[38;5;208m'           # Numbers, constants
    PURPLE = '\033[38;5;165m'           # Classes, types
    RED = '\033[38;5;196m'              # Errors, warnings
    YELLOW = '\033[38;5;226m'           # Comments, notes
    GRAY = '\033[38;5;240m'             # Dimmed text
    PINK = '\033[38;5;213m'             # Special highlighting
    
    # Gradient colors for fancy effects
    GRADIENT_BLUE = [
        '\033[38;5;18m',   # Dark blue
        '\033[38;5;19m',   # 
        '\033[38;5;20m',   # 
        '\033[38;5;21m',   # 
        '\033[38;5;39m',   # Bright blue
        '\033[38;5;51m',   # Cyan
    ]


class TerminalUI:
    """Modern terminal UI components"""
    
    def __init__(self):
        self.width = self._get_terminal_width()
        self.setup_terminal()
    
    def setup_terminal(self):
        """Setup terminal for optimal display"""
        # Clear screen and set light blue background
        print('\033[2J', end='')  # Clear screen
        print('\033[H', end='')   # Move cursor to top
        
        # Set light blue background for entire terminal
        if os.name != 'nt':  # Unix-like systems
            print(f'{Colors.BG_LIGHT_BLUE}{Colors.DARK_BLUE}', end='')
    
    def _get_terminal_width(self) -> int:
        """Get terminal width, default to 80"""
        try:
            return os.get_terminal_size().columns
        except:
            return 80
    
    def print_header(self, title: str, subtitle: str = ""):
        """Print a beautiful header with gradient effect"""
        self.clear_screen()
        
        # Top border with gradient
        border = "█" * self.width
        print(f"{Colors.BG_DARK_BLUE}{Colors.BRIGHT_BLUE}{border}{Colors.RESET}")
        
        # Title with emoji and styling
        title_line = f"🤖 {title}"
        padding = (self.width - len(title_line)) // 2
        print(f"{Colors.BG_LIGHT_BLUE}{Colors.DARK_BLUE}" + " " * padding + 
              f"{Colors.BOLD}{Colors.BRIGHT_BLUE}{title_line}" + 
              " " * (self.width - len(title_line) - padding) + f"{Colors.RESET}")
        
        if subtitle:
            subtitle_line = f"✨ {subtitle}"
            padding = (self.width - len(subtitle_line)) // 2
            print(f"{Colors.BG_LIGHT_BLUE}{Colors.PURPLE}" + " " * padding + 
                  subtitle_line + " " * (self.width - len(subtitle_line) - padding) + 
                  f"{Colors.RESET}")
        
        # Bottom border
        print(f"{Colors.BG_DARK_BLUE}{Colors.BRIGHT_BLUE}{border}{Colors.RESET}")
        print()
    
    def print_section(self, title: str, emoji: str = "📋"):
        """Print a section header"""
        print(f"{Colors.BG_WHITE}{Colors.DARK_BLUE} {emoji} {Colors.BOLD}{title} {Colors.RESET}")
        print(f"{Colors.BG_LIGHT_BLUE}{Colors.GRAY}{'─' * (len(title) + 4)}{Colors.RESET}")
    
    def print_command_help(self, commands: list):
        """Print command help in a beautiful format"""
        self.print_section("Available Commands", "⚡")
        
        for cmd, desc in commands:
            print(f"{Colors.BG_LIGHT_BLUE}  {Colors.BRIGHT_BLUE}{Colors.BOLD}{cmd:<20}{Colors.RESET}" +
                  f"{Colors.BG_LIGHT_BLUE}{Colors.DARK_BLUE} - {desc}{Colors.RESET}")
        print()
    
    def print_status_box(self, title: str, items: list, status_type: str = "info"):
        """Print a status box with colored indicators"""
        # Choose colors based on status type
        if status_type == "success":
            bg_color = Colors.BG_GREEN
            text_color = Colors.BLACK
            border_char = "✅"
        elif status_type == "error":
            bg_color = Colors.BG_RED
            text_color = Colors.WHITE
            border_char = "❌"
        elif status_type == "warning":
            bg_color = Colors.BG_YELLOW
            text_color = Colors.BLACK
            border_char = "⚠️"
        else:
            bg_color = Colors.BG_LIGHT_BLUE
            text_color = Colors.DARK_BLUE
            border_char = "ℹ️"
        
        # Header
        print(f"{bg_color}{text_color} {border_char} {Colors.BOLD}{title} {Colors.RESET}")
        
        # Items
        for item in items:
            print(f"{Colors.BG_LIGHT_BLUE}{Colors.DARK_BLUE}  • {item}{Colors.RESET}")
        print()
    
    def print_progress_bar(self, progress: float, title: str = "", width: int = 40):
        """Print a beautiful progress bar"""
        filled = int(progress * width)
        bar = "█" * filled + "░" * (width - filled)
        percentage = f"{progress:.0%}"
        
        print(f"{Colors.BG_LIGHT_BLUE}{Colors.DARK_BLUE}{title} " +
              f"{Colors.GREEN}[{bar}]{Colors.RESET} " +
              f"{Colors.BG_LIGHT_BLUE}{Colors.BRIGHT_BLUE}{percentage}{Colors.RESET}")
    
    def print_live_progress(self, progress: float, title: str, details: str = "", show_spinner: bool = True):
        """Print live updating progress with spinner animation"""
        spinner_chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        spinner = spinner_chars[int(time.time() * 4) % len(spinner_chars)] if show_spinner else "🚀"
        
        filled = int(progress * 30)
        bar = "█" * filled + "░" * (30 - filled)
        percentage = f"{progress:.0%}"
        
        # Clear line and print progress
        print(f"\r{Colors.BG_LIGHT_BLUE}{Colors.BRIGHT_BLUE} {spinner} {title} " +
              f"{Colors.GREEN}[{bar}] {percentage}{Colors.RESET} " +
              f"{Colors.BG_LIGHT_BLUE}{Colors.GRAY}{details}{Colors.RESET}", end="", flush=True)
    
    def print_task_progress_dashboard(self, tasks_status: dict, current_task: str = ""):
        """Print a real-time task progress dashboard"""
        import time
        
        self.clear_screen()
        
        # Header
        print(f"{Colors.BG_DARK_BLUE}{Colors.WHITE} 🤖 REAL-TIME AGENT PROGRESS {Colors.RESET}")
        print(f"{Colors.BG_LIGHT_BLUE}{Colors.DARK_BLUE}{'═' * self.width}{Colors.RESET}")
        
        # Current task with animation
        if current_task:
            spinner_chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
            spinner = spinner_chars[int(time.time() * 4) % len(spinner_chars)]
            print(f"{Colors.BG_LIGHT_BLUE}{Colors.BRIGHT_BLUE} {spinner} Current: {Colors.BOLD}{current_task}{Colors.RESET}")
        
        # Progress bars for each status
        total_tasks = sum(tasks_status.values())
        if total_tasks > 0:
            for status, count in tasks_status.items():
                progress = count / total_tasks
                status_emoji = {"completed": "✅", "in_progress": "🚀", "pending": "⏳", "failed": "❌"}
                emoji = status_emoji.get(status, "📋")
                
                self.print_progress_bar(progress, f"  {emoji} {status.title()}:", width=50)
        
        # Overall completion
        completed = tasks_status.get('completed', 0)
        overall_progress = completed / total_tasks if total_tasks > 0 else 0
        print(f"{Colors.BG_LIGHT_BLUE}{Colors.DARK_BLUE}{'─' * self.width}{Colors.RESET}")
        self.print_progress_bar(overall_progress, "  🎯 Overall Progress:", width=60)
        
        print(f"\n{Colors.BG_LIGHT_BLUE}{Colors.GRAY}Press Ctrl+C to stop agent execution{Colors.RESET}")
    
    def animate_thinking(self, message: str = "Agent thinking"):
        """Show animated thinking indicator"""
        import time
        
        thinking_chars = ["🤔", "💭", "🧠", "⚡", "✨", "🔍"]
        char = thinking_chars[int(time.time() * 2) % len(thinking_chars)]
        
        print(f"\r{Colors.BG_LIGHT_BLUE}{Colors.PURPLE} {char} {message}... {Colors.RESET}", end="", flush=True)
    
    def print_code_block(self, code: str, language: str = "python"):
        """Print syntax-highlighted code block"""
        print(f"{Colors.BG_GRAY}{Colors.WHITE} {language.upper()} {Colors.RESET}")
        print(f"{Colors.BG_WHITE}{Colors.BLACK}┌{'─' * (self.width - 2)}┐{Colors.RESET}")
        
        lines = code.split('\n')
        for i, line in enumerate(lines, 1):
            line_num = f"{i:3d}"
            highlighted_line = self._highlight_python_syntax(line)
            print(f"{Colors.BG_WHITE}{Colors.GRAY}│{line_num}│{highlighted_line:<{self.width-6}}│{Colors.RESET}")
        
        print(f"{Colors.BG_WHITE}{Colors.BLACK}└{'─' * (self.width - 2)}┘{Colors.RESET}")
        print()
    
    def _highlight_python_syntax(self, line: str) -> str:
        """Apply syntax highlighting to Python code"""
        if not line.strip():
            return line
        
        # Keywords
        keywords = ['def', 'class', 'if', 'else', 'elif', 'for', 'while', 'try', 'except', 
                   'finally', 'with', 'import', 'from', 'return', 'yield', 'break', 'continue',
                   'pass', 'raise', 'assert', 'del', 'global', 'nonlocal', 'lambda', 'and', 
                   'or', 'not', 'in', 'is', 'True', 'False', 'None']
        
        highlighted = line
        
        # Highlight keywords
        for keyword in keywords:
            highlighted = highlighted.replace(f' {keyword} ', f' {Colors.BRIGHT_BLUE}{keyword}{Colors.BLACK} ')
            if highlighted.startswith(f'{keyword} '):
                highlighted = f'{Colors.BRIGHT_BLUE}{keyword}{Colors.BLACK}' + highlighted[len(keyword):]
        
        # Highlight strings
        highlighted = highlighted.replace('"', f'{Colors.GREEN}"{Colors.BLACK}')
        highlighted = highlighted.replace("'", f'{Colors.GREEN}\'{Colors.BLACK}')
        
        # Highlight comments
        if '#' in highlighted:
            comment_start = highlighted.find('#')
            if comment_start != -1:
                highlighted = (highlighted[:comment_start] + 
                             f'{Colors.GRAY}{highlighted[comment_start:]}{Colors.BLACK}')
        
        # Highlight function names (simple pattern)
        import re
        highlighted = re.sub(r'\bdef\s+(\w+)', f'{Colors.BRIGHT_BLUE}def{Colors.BLACK} {Colors.CYAN}\\1{Colors.BLACK}', highlighted)
        highlighted = re.sub(r'\bclass\s+(\w+)', f'{Colors.BRIGHT_BLUE}class{Colors.BLACK} {Colors.PURPLE}\\1{Colors.BLACK}', highlighted)
        
        return f"{Colors.BLACK}{highlighted}{Colors.RESET}"
    
    def print_task_list(self, tasks: list, show_details: bool = False):
        """Print a beautiful task list"""
        if not tasks:
            print(f"{Colors.BG_LIGHT_BLUE}{Colors.GRAY}  No tasks available{Colors.RESET}")
            return
        
        for i, task in enumerate(tasks, 1):
            # Status emoji and color
            if task.get('status') == 'completed':
                status_emoji = "✅"
                status_color = Colors.GREEN
            elif task.get('status') == 'in_progress':
                status_emoji = "🚀"
                status_color = Colors.ORANGE
            elif task.get('status') == 'failed':
                status_emoji = "❌"
                status_color = Colors.RED
            else:
                status_emoji = "⏳"
                status_color = Colors.GRAY
            
            # Priority emoji
            priority = task.get('priority', 'medium')
            priority_emoji = "🔥" if priority == 'high' else "⚡" if priority == 'medium' else "📌"
            
            # Main task line
            task_title = task.get('title', 'Untitled Task')
            print(f"{Colors.BG_LIGHT_BLUE}{Colors.DARK_BLUE}  {i:2d}. {status_emoji} {priority_emoji} " +
                  f"{Colors.BOLD}{task_title}{Colors.RESET}")
            
            if show_details:
                # Description
                if task.get('description'):
                    print(f"{Colors.BG_LIGHT_BLUE}{Colors.GRAY}      └─ {task['description']}{Colors.RESET}")
                
                # Progress bar if available
                if task.get('progress', 0) > 0:
                    self.print_progress_bar(task['progress'], "     Progress: ", width=30)
    
    def print_agent_status(self, status: dict):
        """Print agent status in a beautiful dashboard format"""
        print(f"{Colors.BG_DARK_BLUE}{Colors.WHITE} 🤖 AGENT STATUS DASHBOARD {Colors.RESET}")
        print(f"{Colors.BG_LIGHT_BLUE}{Colors.DARK_BLUE}{'═' * self.width}{Colors.RESET}")
        
        # Main stats
        stats = [
            ("📋 Total Tasks", status.get('total_tasks', 0)),
            ("⏳ Pending", status.get('pending', 0)),
            ("🚀 In Progress", status.get('in_progress', 0)),
            ("✅ Completed", status.get('completed', 0)),
            ("❌ Failed", status.get('failed', 0)),
        ]
        
        # Print stats in two columns
        for i in range(0, len(stats), 2):
            left_stat = stats[i]
            right_stat = stats[i + 1] if i + 1 < len(stats) else ("", "")
            
            left_text = f"{left_stat[0]}: {Colors.BOLD}{left_stat[1]}{Colors.RESET}{Colors.DARK_BLUE}"
            right_text = f"{right_stat[0]}: {Colors.BOLD}{right_stat[1]}{Colors.RESET}{Colors.DARK_BLUE}" if right_stat[0] else ""
            
            print(f"{Colors.BG_LIGHT_BLUE}{Colors.DARK_BLUE}  {left_text:<30} {right_text}{Colors.RESET}")
        
        # Completion rate
        completion_rate = status.get('completion_rate', 0)
        print(f"{Colors.BG_LIGHT_BLUE}{Colors.DARK_BLUE}{'─' * self.width}{Colors.RESET}")
        self.print_progress_bar(completion_rate, "  📈 Completion Rate:", width=50)
        
        # Next task
        next_task = status.get('next_task', 'None')
        print(f"{Colors.BG_LIGHT_BLUE}{Colors.DARK_BLUE}  🎯 Next Task: {Colors.BOLD}{next_task}{Colors.RESET}")
        print()
    
    def input_prompt(self, prompt: str, prompt_type: str = "normal") -> str:
        """Styled input prompt"""
        if prompt_type == "agent":
            emoji = "🤖"
            color = Colors.BRIGHT_BLUE
        elif prompt_type == "error":
            emoji = "❌"
            color = Colors.RED
        elif prompt_type == "success":
            emoji = "✅"
            color = Colors.GREEN
        else:
            emoji = "💬"
            color = Colors.CYAN
        
        try:
            return input(f"{Colors.BG_LIGHT_BLUE}{color} {emoji} {prompt} {Colors.RESET}")
        except (KeyboardInterrupt, EOFError):
            print(f"\n{Colors.BG_LIGHT_BLUE}{Colors.GRAY}Goodbye! 👋{Colors.RESET}")
            sys.exit(0)
    
    def clear_screen(self):
        """Clear screen while maintaining background"""
        print('\033[2J', end='')  # Clear screen
        print('\033[H', end='')   # Move cursor to top
        print(f'{Colors.BG_LIGHT_BLUE}{Colors.DARK_BLUE}', end='')
    
    def print_success(self, message: str):
        """Print success message"""
        print(f"{Colors.BG_GREEN}{Colors.BLACK} ✅ {message} {Colors.RESET}")
    
    def print_error(self, message: str):
        """Print error message"""
        print(f"{Colors.BG_RED}{Colors.WHITE} ❌ {message} {Colors.RESET}")
    
    def print_warning(self, message: str):
        """Print warning message"""
        print(f"{Colors.BG_YELLOW}{Colors.BLACK} ⚠️  {message} {Colors.RESET}")
    
    def print_info(self, message: str):
        """Print info message"""
        print(f"{Colors.BG_LIGHT_BLUE}{Colors.DARK_BLUE} ℹ️  {message} {Colors.RESET}")
    
    def restore_terminal(self):
        """Restore terminal to default state"""
        print(Colors.RESET, end='')
        if os.name != 'nt':
            print('\033[2J\033[H', end='')  # Clear and reset


# Global UI instance
ui = TerminalUI()
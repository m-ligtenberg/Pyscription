"""
Modern terminal styling and colors for Pyscription CLI
Beautiful syntax highlighting and UI elements
"""

import os
import sys
import time
from typing import Optional


class Colors:
    """ANSI color codes for terminal styling - Calm color palette"""
    
    # Reset
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    
    # Background colors - Calm and subtle
    BG_CONTAINER = '\033[48;5;236m'     # Dark gray container background
    BG_CONTENT = '\033[48;5;234m'       # Slightly darker content area
    BG_HEADER = '\033[48;5;238m'        # Header background
    BG_INPUT = '\033[48;5;235m'         # Input area background
    BG_SUCCESS = '\033[48;5;22m'        # Muted green
    BG_ERROR = '\033[48;5;52m'          # Muted red
    BG_WARNING = '\033[48;5;58m'        # Muted yellow/brown
    BG_INFO = '\033[48;5;24m'           # Muted blue
    
    # Foreground colors - Calm and readable
    BLACK = '\033[38;5;16m'             # Pure black
    WHITE = '\033[38;5;231m'            # Pure white
    LIGHT_GRAY = '\033[38;5;250m'       # Light gray for main text
    GRAY = '\033[38;5;244m'             # Medium gray for secondary text
    DARK_GRAY = '\033[38;5;240m'        # Dark gray for dimmed text
    
    # Calm accent colors
    SOFT_BLUE = '\033[38;5;74m'         # Soft blue for keywords
    SOFT_CYAN = '\033[38;5;80m'         # Soft cyan for functions
    SOFT_GREEN = '\033[38;5;72m'        # Soft green for strings
    SOFT_ORANGE = '\033[38;5;179m'      # Soft orange for numbers
    SOFT_PURPLE = '\033[38;5;140m'      # Soft purple for types
    SOFT_RED = '\033[38;5;167m'         # Soft red for errors
    SOFT_YELLOW = '\033[38;5;186m'      # Soft yellow for warnings
    
    # Container border colors
    BORDER_LIGHT = '\033[38;5;245m'     # Light border
    BORDER_DARK = '\033[38;5;239m'      # Dark border
    
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
        """Setup terminal for containerized display"""
        # Clear screen
        print('\033[2J', end='')  # Clear screen
        print('\033[H', end='')   # Move cursor to top
        
        # Initialize container UI
        self.print_container_frame()
    
    def _get_terminal_width(self) -> int:
        """Get terminal width with responsive design"""
        try:
            width = os.get_terminal_size().columns
            # Responsive width constraints
            if width < 60:
                return 60  # Minimum readable width
            elif width > 120:
                return 120  # Maximum for readability
            else:
                return width
        except:
            return 80  # Safe default
    
    def print_header(self, title: str, subtitle: str = ""):
        """Print a calm containerized header"""
        self.clear_screen()
        self.print_container_frame()
        
        # Container width (leave margin for borders)
        container_width = self.width - 4
        
        # Header section
        print(f"{Colors.BORDER_LIGHT}│ {Colors.BG_HEADER}{Colors.WHITE}" + 
              f" 💊 {title}".ljust(container_width) + 
              f"{Colors.RESET}{Colors.BORDER_LIGHT} │{Colors.RESET}")
        
        if subtitle:
            print(f"{Colors.BORDER_LIGHT}│ {Colors.BG_CONTENT}{Colors.GRAY}" + 
                  f" {subtitle}".ljust(container_width) + 
                  f"{Colors.RESET}{Colors.BORDER_LIGHT} │{Colors.RESET}")
        
        # Separator
        print(f"{Colors.BORDER_LIGHT}├{'─' * container_width}┤{Colors.RESET}")
        print()
    
    def print_section(self, title: str, emoji: str = "📋"):
        """Print a calm section header within container"""
        container_width = self.width - 4
        section_line = f" {emoji} {title}"
        
        print(f"{Colors.BORDER_LIGHT}│ {Colors.BG_CONTENT}{Colors.SOFT_BLUE}" + 
              f"{section_line}".ljust(container_width) + 
              f"{Colors.RESET}{Colors.BORDER_LIGHT} │{Colors.RESET}")
        
        print(f"{Colors.BORDER_LIGHT}│ {Colors.BG_CONTENT}{Colors.DARK_GRAY}" + 
              f"{'─' * (len(section_line) - 1)}".ljust(container_width) + 
              f"{Colors.RESET}{Colors.BORDER_LIGHT} │{Colors.RESET}")
    
    def print_command_help(self, commands: list):
        """Print command help in containerized format"""
        self.print_section("Available Commands", "⚡")
        
        container_width = self.width - 4
        for cmd, desc in commands:
            cmd_line = f"  {cmd:<20} - {desc}"
            if len(cmd_line) > container_width:
                cmd_line = cmd_line[:container_width-3] + "..."
            
            print(f"{Colors.BORDER_LIGHT}│ {Colors.BG_CONTENT}{Colors.SOFT_CYAN}" + 
                  f"{cmd:<20}{Colors.LIGHT_GRAY} - {desc}".ljust(container_width) + 
                  f"{Colors.RESET}{Colors.BORDER_LIGHT} │{Colors.RESET}")
        
        self.print_container_separator()
    
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
    
    def print_code_block_container(self, code: str, language: str = "python"):
        """Print syntax-highlighted code block within container"""
        container_width = self.width - 4
        
        # Code header
        header = f" {language.upper()} "
        print(f"{Colors.BORDER_LIGHT}│ {Colors.BG_HEADER}{Colors.WHITE}" + 
              f"{header}".ljust(container_width) + 
              f"{Colors.RESET}{Colors.BORDER_LIGHT} │{Colors.RESET}")
        
        # Code content with line numbers
        lines = code.split('\n')
        for i, line in enumerate(lines, 1):
            line_num = f"{i:3d}"
            highlighted_line = self._highlight_python_syntax_container(line)
            code_line = f"{line_num}│ {highlighted_line}"
            
            # Truncate if too long
            if len(code_line) > container_width - 4:
                code_line = code_line[:container_width-7] + "..."
            
            print(f"{Colors.BORDER_LIGHT}│ {Colors.BG_CONTENT}{Colors.DARK_GRAY}" + 
                  f"{code_line}".ljust(container_width) + 
                  f"{Colors.RESET}{Colors.BORDER_LIGHT} │{Colors.RESET}")
        
        self.print_container_separator()
    
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
    
    def _highlight_python_syntax_container(self, line: str) -> str:
        """Apply calm syntax highlighting for containerized code"""
        if not line.strip():
            return line
        
        # Keywords
        keywords = ['def', 'class', 'if', 'else', 'elif', 'for', 'while', 'try', 'except', 
                   'finally', 'with', 'import', 'from', 'return', 'yield', 'break', 'continue',
                   'pass', 'raise', 'assert', 'del', 'global', 'nonlocal', 'lambda', 'and', 
                   'or', 'not', 'in', 'is', 'True', 'False', 'None']
        
        highlighted = line
        
        # Highlight keywords with soft colors
        for keyword in keywords:
            highlighted = highlighted.replace(f' {keyword} ', f' {Colors.SOFT_BLUE}{keyword}{Colors.LIGHT_GRAY} ')
            if highlighted.startswith(f'{keyword} '):
                highlighted = f'{Colors.SOFT_BLUE}{keyword}{Colors.LIGHT_GRAY}' + highlighted[len(keyword):]
        
        # Highlight strings with soft green
        highlighted = highlighted.replace('"', f'{Colors.SOFT_GREEN}"{Colors.LIGHT_GRAY}')
        highlighted = highlighted.replace("'", f'{Colors.SOFT_GREEN}\'{Colors.LIGHT_GRAY}')
        
        # Highlight comments with soft gray
        if '#' in highlighted:
            comment_start = highlighted.find('#')
            if comment_start != -1:
                highlighted = (highlighted[:comment_start] + 
                             f'{Colors.DARK_GRAY}{highlighted[comment_start:]}{Colors.LIGHT_GRAY}')
        
        # Highlight function and class names
        import re
        highlighted = re.sub(r'\bdef\s+(\w+)', f'{Colors.SOFT_BLUE}def{Colors.LIGHT_GRAY} {Colors.SOFT_CYAN}\\1{Colors.LIGHT_GRAY}', highlighted)
        highlighted = re.sub(r'\bclass\s+(\w+)', f'{Colors.SOFT_BLUE}class{Colors.LIGHT_GRAY} {Colors.SOFT_PURPLE}\\1{Colors.LIGHT_GRAY}', highlighted)
        
        return f"{Colors.LIGHT_GRAY}{highlighted}{Colors.RESET}"
    
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
        """Fixed position input prompt at bottom of container"""
        if prompt_type == "agent":
            emoji = "🤖"
            color = Colors.SOFT_BLUE
        elif prompt_type == "error":
            emoji = "❌"
            color = Colors.SOFT_RED
        elif prompt_type == "success":
            emoji = "✅"
            color = Colors.SOFT_GREEN
        else:
            emoji = "💬"
            color = Colors.SOFT_CYAN
        
        terminal_height = self.get_terminal_height()
        container_width = self.width - 2
        input_row = terminal_height - 2
        
        # Print input line at fixed position
        input_line = f" {emoji} {prompt}: "
        spaces_needed = container_width - len(input_line) - 1
        print(f"\033[{input_row};1H{Colors.BORDER_LIGHT}│ {color}{input_line}{Colors.RESET}" + 
              " " * spaces_needed + 
              f"{Colors.BORDER_LIGHT}│{Colors.RESET}")
        
        try:
            # Position cursor for input
            print(f"\033[{input_row};{len(input_line) + 2}H", end="")
            print('\033[?25h', end='')  # Show cursor
            user_input = input()
            print('\033[?25l', end='')  # Hide cursor again
            
            # Clear input line and show what was entered
            display_line = f" > {user_input}"
            spaces_needed = container_width - len(display_line) - 1
            print(f"\033[{input_row};1H{Colors.BORDER_LIGHT}│ {Colors.LIGHT_GRAY}{display_line}{Colors.RESET}" + 
                  " " * spaces_needed + 
                  f"{Colors.BORDER_LIGHT}│{Colors.RESET}")
            return user_input
        except (KeyboardInterrupt, EOFError):
            goodbye_line = " Goodbye! 👋"
            spaces_needed = container_width - len(goodbye_line) - 1
            print(f"\033[{input_row};1H{Colors.BORDER_LIGHT}│ {Colors.GRAY}{goodbye_line}{Colors.RESET}" + 
                  " " * spaces_needed + 
                  f"{Colors.BORDER_LIGHT}│{Colors.RESET}")
            print('\033[?25h', end='')  # Show cursor before exit
            sys.exit(0)
    
    def clear_screen(self):
        """Clear screen for containerized display"""
        print('\033[2J', end='')  # Clear screen
        print('\033[H', end='')   # Move cursor to top
    
    def print_success(self, message: str):
        """Print medical-themed success message in container"""
        container_width = self.width - 4
        msg_line = f" ✅ RECOVERY: {message}"
        spaces_needed = container_width - len(msg_line)
        print(f"{Colors.BORDER_LIGHT}│ {Colors.SOFT_GREEN}{msg_line}{Colors.RESET}" + 
              " " * spaces_needed + 
              f"{Colors.BORDER_LIGHT}│{Colors.RESET}")
    
    def print_error(self, message: str):
        """Print medical-themed error message in container"""
        container_width = self.width - 4
        msg_line = f" 🩺 DIAGNOSIS: {message}"
        spaces_needed = container_width - len(msg_line)
        print(f"{Colors.BORDER_LIGHT}│ {Colors.SOFT_RED}{msg_line}{Colors.RESET}" + 
              " " * spaces_needed + 
              f"{Colors.BORDER_LIGHT}│{Colors.RESET}")
    
    def print_warning(self, message: str):
        """Print medical-themed warning message in container"""
        container_width = self.width - 4
        msg_line = f" ⚠️ SYMPTOM: {message}"
        spaces_needed = container_width - len(msg_line)
        print(f"{Colors.BORDER_LIGHT}│ {Colors.SOFT_YELLOW}{msg_line}{Colors.RESET}" + 
              " " * spaces_needed + 
              f"{Colors.BORDER_LIGHT}│{Colors.RESET}")
    
    def print_info(self, message: str):
        """Print medical-themed info message in container"""
        container_width = self.width - 4
        msg_line = f" 💊 TREATMENT: {message}"
        spaces_needed = container_width - len(msg_line)
        print(f"{Colors.BORDER_LIGHT}│ {Colors.SOFT_BLUE}{msg_line}{Colors.RESET}" + 
              " " * spaces_needed + 
              f"{Colors.BORDER_LIGHT}│{Colors.RESET}")
    
    
    def print_critical(self, message: str):
        """Print critical medical emergency message"""
        container_width = self.width - 4
        msg_line = f" 🚨 EMERGENCY: {message}"
        # Flash effect for critical messages
        for _ in range(3):
            print(f"\033[7m{Colors.BORDER_LIGHT}│ {Colors.BG_ERROR}{Colors.WHITE}" + 
                  f"{msg_line}".ljust(container_width) + 
                  f"{Colors.RESET}\033[7m{Colors.BORDER_LIGHT} │{Colors.RESET}")
            time.sleep(0.2)
            print(f"\033[A\033[K", end='')  # Move up and clear line
            time.sleep(0.1)
        # Final display
        print(f"{Colors.BORDER_LIGHT}│ {Colors.BG_ERROR}{Colors.WHITE}" + 
              f"{msg_line}".ljust(container_width) + 
              f"{Colors.RESET}{Colors.BORDER_LIGHT} │{Colors.RESET}")
    
    def print_diagnosis(self, title: str, symptoms: list, treatment: str = None):
        """Print a complete medical diagnosis with symptoms and treatment"""
        container_width = self.width - 4
        
        # Diagnosis header
        header_line = f" 🏥 MEDICAL DIAGNOSIS: {title}"
        print(f"{Colors.BORDER_LIGHT}│ {Colors.BG_HEADER}{Colors.WHITE}" + 
              f"{header_line}".ljust(container_width) + 
              f"{Colors.RESET}{Colors.BORDER_LIGHT} │{Colors.RESET}")
        
        # Symptoms
        if symptoms:
            print(f"{Colors.BORDER_LIGHT}│ {Colors.BG_CONTENT}{Colors.SOFT_RED}" + 
                  f" 🔍 SYMPTOMS DETECTED:".ljust(container_width) + 
                  f"{Colors.RESET}{Colors.BORDER_LIGHT} │{Colors.RESET}")
            
            for symptom in symptoms[:5]:  # Limit to 5 symptoms
                symptom_line = f"   • {symptom}"
                if len(symptom_line) > container_width - 2:
                    symptom_line = symptom_line[:container_width-5] + "..."
                print(f"{Colors.BORDER_LIGHT}│ {Colors.BG_CONTENT}{Colors.LIGHT_GRAY}" + 
                      f"{symptom_line}".ljust(container_width) + 
                      f"{Colors.RESET}{Colors.BORDER_LIGHT} │{Colors.RESET}")
        
        # Treatment recommendation
        if treatment:
            print(f"{Colors.BORDER_LIGHT}│ {Colors.BG_CONTENT}{Colors.SOFT_GREEN}" + 
                  f" 💊 PRESCRIBED TREATMENT:".ljust(container_width) + 
                  f"{Colors.RESET}{Colors.BORDER_LIGHT} │{Colors.RESET}")
            
            treatment_line = f"   {treatment}"
            if len(treatment_line) > container_width - 2:
                treatment_line = treatment_line[:container_width-5] + "..."
            print(f"{Colors.BORDER_LIGHT}│ {Colors.BG_CONTENT}{Colors.LIGHT_GRAY}" + 
                  f"{treatment_line}".ljust(container_width) + 
                  f"{Colors.RESET}{Colors.BORDER_LIGHT} │{Colors.RESET}")
    
    def print_splash_screen(self):
        """Display the main splash screen"""
        self.clear_screen()
        
        # ASCII Art Header
        print(f"{Colors.SOFT_CYAN}")
        print("    ____                      _       _   _             ")
        print("   |  _ \ _   _ ___  ___ _ __(_)_ __ | |_(_) ___  _ __  ")
        print("   | |_) | | | / __|/ __| '__| | '_ \| __| |/ _ \| '_ \ ")
        print("   |  __/| |_| \__ \ (__| |  | | |_) | |_| | (_) | | | |")
        print("   |_|    \__, |___/\___|_|  |_| .__/ \__|_|\___/|_| |_|")
        print("          |___/                |_|                      ")
        print(f"{Colors.RESET}")
        print()
        
        # Version and tagline
        print(f"{Colors.SOFT_YELLOW}           💊 Terminal medication. No prescription needed.{Colors.RESET}")
        print()
        print(f"{Colors.SOFT_GREEN}    🏥 AI-Enhanced Python Development Assistant{Colors.RESET}")
        print(f"{Colors.LIGHT_GRAY}    🔬 Diagnose • 💉 Inject • 💊 Medicate • 🧬 Evolve{Colors.RESET}")
        print()
    
    def print_sticky_container_header(self, title: str, current_dir: str):
        """Print a sticky header with title and current directory"""
        import os
        
        # Clear screen and position cursor at top
        print('\033[2J\033[H', end='')
        
        container_width = self.width - 4
        
        # Top border
        print(f"{Colors.BORDER_LIGHT}┌{'─' * (self.width - 2)}┐{Colors.RESET}")
        
        # Title line
        title_line = f" 💊 {title}"
        spaces_needed = container_width - len(title_line)
        print(f"{Colors.BORDER_LIGHT}│{Colors.SOFT_CYAN}{title_line}{Colors.RESET}" + 
              " " * spaces_needed + 
              f"{Colors.BORDER_LIGHT}│{Colors.RESET}")
        
        # Directory line
        dir_display = os.path.basename(current_dir) or current_dir
        if len(dir_display) > container_width - 10:
            dir_display = "..." + dir_display[-(container_width-13):]
        dir_line = f" 📁 {dir_display}"
        spaces_needed = container_width - len(dir_line)
        print(f"{Colors.BORDER_LIGHT}│{Colors.GRAY}{dir_line}{Colors.RESET}" + 
              " " * spaces_needed + 
              f"{Colors.BORDER_LIGHT}│{Colors.RESET}")
        
        # Separator line
        print(f"{Colors.BORDER_LIGHT}├{'─' * (self.width - 2)}┤{Colors.RESET}")
        
        # Store current position for scrollable content
        self.content_start_row = 5  # Header takes 4 rows + separator
    
    def print_scrollable_content_line(self, content: str, color: str = None):
        """Print a single line of scrollable content inside the container"""
        container_width = self.width - 4
        text_color = color or Colors.LIGHT_GRAY
        
        # Wrap long content
        if len(content) > container_width:
            wrapped_lines = self.wrap_text(content, container_width)
            for line in wrapped_lines:
                # Calculate actual visual length (excluding ANSI codes)
                visual_length = len(line)
                spaces_needed = container_width - visual_length
                print(f"{Colors.BORDER_LIGHT}│ {text_color}{line}{Colors.RESET}" + 
                      " " * spaces_needed + 
                      f"{Colors.BORDER_LIGHT}│{Colors.RESET}")
        else:
            # Calculate actual visual length (excluding ANSI codes)
            visual_length = len(content)
            spaces_needed = container_width - visual_length
            print(f"{Colors.BORDER_LIGHT}│ {text_color}{content}{Colors.RESET}" + 
                  " " * spaces_needed + 
                  f"{Colors.BORDER_LIGHT}│{Colors.RESET}")
    
    def print_sticky_container_footer(self):
        """Print the bottom border of the sticky container"""
        print(f"{Colors.BORDER_LIGHT}└{'─' * (self.width - 2)}┘{Colors.RESET}")
    
    def get_terminal_height(self) -> int:
        """Get terminal height for scrollable content calculation"""
        try:
            return os.get_terminal_size().lines
        except:
            return 24  # Safe default
    
    def get_scrollable_content_height(self) -> int:
        """Calculate available height for scrollable content"""
        total_height = self.get_terminal_height()
        header_height = 4  # Title, dir, separator lines
        footer_height = 1  # Bottom border
        input_height = 2   # Input prompt space
        
        return max(5, total_height - header_height - footer_height - input_height)
    
    def restore_terminal(self):
        """Restore terminal to default state"""
        print('\033[?25h', end='')  # Show cursor
        print(Colors.RESET, end='')
        if os.name != 'nt':
            print('\033[2J\033[H', end='')  # Clear and reset


    def print_container_frame(self):
        """Print the container frame top"""
        print(f"{Colors.BORDER_LIGHT}┌{'─' * (self.width - 2)}┐{Colors.RESET}")
    
    def print_container_bottom(self):
        """Print the container frame bottom"""
        print(f"{Colors.BORDER_LIGHT}└{'─' * (self.width - 2)}┘{Colors.RESET}")
    
    def print_container_separator(self):
        """Print a separator line within container"""
        print(f"{Colors.BORDER_LIGHT}│{' ' * (self.width - 2)}│{Colors.RESET}")
    
    def update_terminal_size(self):
        """Update terminal width for responsive design"""
        self.width = self._get_terminal_width()
    
    def wrap_text(self, text: str, max_width: int) -> list:
        """Intelligently wrap text for better readability"""
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            # Check if adding this word would exceed the width
            test_line = current_line + (" " if current_line else "") + word
            if len(test_line) <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                # If single word is too long, truncate it
                if len(word) > max_width:
                    lines.append(word[:max_width-3] + "...")
                    current_line = ""
                else:
                    current_line = word
        
        if current_line:
            lines.append(current_line)
        
        return lines if lines else [""]
    
    def print_container_content(self, content: str, color: str = None):
        """Print content within the container borders with intelligent wrapping"""
        # Update terminal size for responsive design
        self.update_terminal_size()
        container_width = self.width - 4
        lines = content.split('\n')
        
        text_color = color or Colors.LIGHT_GRAY
        
        for line in lines:
            # Use intelligent wrapping for long lines
            if len(line) > container_width:
                wrapped_lines = self.wrap_text(line, container_width)
                for wrapped_line in wrapped_lines:
                    print(f"{Colors.BORDER_LIGHT}│ {Colors.BG_CONTENT}{text_color}" + 
                          f"{wrapped_line}".ljust(container_width) + 
                          f"{Colors.RESET}{Colors.BORDER_LIGHT} │{Colors.RESET}")
            else:
                # Print lines that fit normally
                print(f"{Colors.BORDER_LIGHT}│ {Colors.BG_CONTENT}{text_color}" + 
                      f"{line}".ljust(container_width) + 
                      f"{Colors.RESET}{Colors.BORDER_LIGHT} │{Colors.RESET}")


# Global UI instance
ui = TerminalUI()
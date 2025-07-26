"""
Conversational CLI interface for Pyscription
Supports natural language Python assistance with local AI
Beautiful terminal UI with light blue theme and syntax highlighting
"""

import argparse
import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

from pyscription.core.doctor_interactive import MLEnhancedPyscription
from pyscription.utils.documentation_downloader import DocumentationDownloader
from pyscription.utils.terminal_styling import ui, Colors


class ConversationalCLI:
    """Conversational command-line interface"""
    
    def __init__(self, project_dir: str = "."):
        """Initialize conversational CLI (project_dir is reserved for future codebase context)."""
        self.project_dir = Path(project_dir)
        self.mentor = MLEnhancedPyscription()
        self.running = True
    
    def run_interactive(self):
        """Run interactive conversational mode with sticky container"""
        import os
        
        # Get current directory for header
        current_dir = os.getcwd()
        
        # Print initial sticky header and content
        ui.print_sticky_container_header("Pyscription - Doctor Mode", current_dir)
        
        # Display welcome content
        welcome_lines = [
            "",
            "💬 Quick Start Examples:",
            "  • 'How do I implement a singleton pattern?'",
            "  • 'Can you analyze this code: [paste code]'", 
            "  • 'What's the best way to handle exceptions?'",
            "",
            "🤖 AI Commands:",
            "  /analyze <file>    - Deep code analysis",
            "  /info             - System info (ESC to exit)",
            "",
            "🔧 Workflow Commands:",
            "  /format <file>    - Format with black/autopep8",
            "  /test [pattern]   - Run tests with pytest",
            "",
            "📚 Help: /help ai, /help workflow, /quit",
            ""
        ]
        
        for line in welcome_lines:
            ui.print_scrollable_content_line(line)
        
        while self.running:
            try:
                # Get input using fixed positioning
                user_input = ui.input_prompt("You", "normal").strip()
                
                if not user_input:
                    continue
                
                # Process the command/conversation and update display
                if user_input.startswith('/'):
                    self._handle_command_with_container(user_input)
                else:
                    self._handle_conversation_with_container(user_input)
                    
            except KeyboardInterrupt:
                ui.print_scrollable_content_line("👋 See you later!")
                ui.print_sticky_container_footer()
                break
            except EOFError:
                ui.print_scrollable_content_line("👋 See you later!")
                ui.print_sticky_container_footer()
                break
            except Exception as e:
                ui.print_scrollable_content_line(f"❌ Error: {e}", Colors.SOFT_RED)
        
        ui.print_sticky_container_footer()
    
    def _handle_command_with_container(self, command: str):
        """Handle commands within container display"""
        ui.print_scrollable_content_line(f"💬 You: {command}", Colors.SOFT_CYAN)
        ui.print_scrollable_content_line("")
        
        # Process the command normally
        self._handle_command(command)
    
    def _handle_conversation_with_container(self, message: str):
        """Handle conversation within container display"""
        ui.print_scrollable_content_line(f"💬 You: {message}", Colors.SOFT_CYAN)
        ui.print_scrollable_content_line("")
        
        # Process the conversation normally
        self._handle_conversation(message)
    
    def _handle_command(self, command: str):
        """Handle special commands"""
        parts = command[1:].split(' ', 1)
        cmd = parts[0].lower()
        arg = parts[1] if len(parts) > 1 else ''
        
        if cmd == 'quit' or cmd == 'exit':
            ui.print_scrollable_content_line("✅ RECOVERY: 👋 Happy coding!", Colors.SOFT_GREEN)
            self.running = False
            
        elif cmd == 'help':
            if arg.lower() == 'ai':
                self._show_ai_help()
            elif arg.lower() == 'workflow':
                self._show_workflow_help()
            else:
                self._show_help()
            
        elif cmd == 'analyze':
            if not arg:
                ui.print_warning("Usage: /analyze <file_path>")
                return
                
            try:
                with open(arg, 'r') as f:
                    code = f.read()
                    
                ui.print_info(f"🔍 Analyzing {arg}...")
                
                # Show code preview
                ui.print_section("Code Preview", "📄")
                preview_lines = code.split('\n')[:10]  # First 10 lines
                ui.print_code_block_container('\n'.join(preview_lines), "python")
                
                response = self.mentor.chat_about_code(code=code)
                
                ui.print_section("AI Analysis", "🤖")
                self._print_ai_response(response)
                
            except FileNotFoundError:
                ui.print_error(f"File not found: {arg}")
            except Exception as e:
                ui.print_error(f"Error analyzing file: {e}")
                
        elif cmd == 'generate':
            if not arg:
                print("Usage: /generate <pattern_type>")
                print("Available patterns: singleton, factory, observer")
                return
                
            print(f"\n🏗️ Generating {arg} pattern...")
            template = self.mentor.generate_code_template(arg)
            print(f"\n```python\n{template}\n```")
            
        elif cmd == 'models':
            models = self.mentor.get_ai_models()
            print(f"\n🤖 Available AI models:")
            for i, model in enumerate(models, 1):
                print(f"  {i}. {model}")
                
        elif cmd == 'switch':
            if not arg:
                print("Usage: /switch <model_name>")
                return
                
            if self.mentor.switch_ai_model(arg):
                print(f"✅ Switched to model: {arg}")
            else:
                print(f"❌ Failed to switch to model: {arg}")
                
        elif cmd == 'clear':
            self.mentor.clear_ai_history()
            print("🧹 Conversation history cleared")
            
        elif cmd == 'stats':
            stats = self.mentor.get_stats()
            print("\n📊 System Statistics:")
            print(f"  📚 Documents: {stats['ml_stats']['processed_documents']}")
            print(f"  🔍 Patterns: {stats['ml_stats']['discovered_patterns']}")
            print(f"  💬 Interactions: {stats['ml_stats']['total_interactions']}")
            print(f"  🤖 AI Backend: {stats['ai_stats']['current_backend']}")
            print(f"  🧠 Conversation: {stats['ai_stats']['conversation_length']} messages")
        
        elif cmd == 'info':
            self._show_info_screen()
            
        elif cmd == 'format':
            self._handle_format_command(arg)
            
        elif cmd == 'test':
            self._handle_test_command(arg)
            
        elif cmd == 'coverage':
            self._handle_coverage_command()
            
        elif cmd == 'lint':
            self._handle_lint_command(arg)
            
        elif cmd == 'deps':
            self._handle_deps_command(arg)
            
        elif cmd == 'env':
            self._handle_env_command(arg)
            
        else:
            print(f"❌ Unknown command: /{cmd}")
            print("Type /help for available commands")
    
    def _handle_conversation(self, message: str):
        """Handle natural language conversation"""
        # Check if message contains code
        if any(keyword in message.lower() for keyword in ['def ', 'class ', 'import ', 'def(', 'class(', '```']):
            # Likely contains code, use code analysis
            if '```python' in message:
                # Extract code from markdown blocks
                import re
                code_blocks = re.findall(r'```python\n(.*?)\n```', message, re.DOTALL)
                if code_blocks:
                    code = code_blocks[0]
                    question = message.replace(f'```python\n{code}\n```', '').strip()
                    
                    # Show extracted code
                    ui.print_section("Code Analysis", "🔍")
                    ui.print_code_block_container(code, "python")
                    
                    response = self.mentor.chat_about_code(code=code, question=question if question else None)
                else:
                    response = self.mentor.chat_about_code(question=message)
            else:
                # Treat entire message as code + question
                response = self.mentor.chat_about_code(question=message)
        else:
            # General Python question
            response = self.mentor.chat_about_code(question=message)
        
        ui.print_section("AI Response", "🤖")
        self._print_ai_response(response)
    
    def _print_ai_response(self, response: str):
        """Print AI response within container with beautiful formatting"""
        # Split response into paragraphs
        paragraphs = response.split('\n\n')
        
        for paragraph in paragraphs:
            if not paragraph.strip():
                continue
                
            # Check if it's a code block
            if '```' in paragraph:
                lines = paragraph.split('\n')
                in_code_block = False
                current_code = []
                
                for line in lines:
                    if line.startswith('```'):
                        if in_code_block:
                            # End of code block
                            if current_code:
                                language = "python"  # Default to python
                                ui.print_code_block_container('\n'.join(current_code), language)
                            current_code = []
                            in_code_block = False
                        else:
                            # Start of code block
                            in_code_block = True
                    elif in_code_block:
                        current_code.append(line)
                    else:
                        # Regular text
                        if line.strip():
                            ui.print_container_content(line, Colors.LIGHT_GRAY)
            else:
                # Regular paragraph
                ui.print_container_content(paragraph, Colors.LIGHT_GRAY)
        
        ui.print_container_separator()  # Add spacing
    
    def _print_categorized_help(self):
        """Display concise categorized help for terminal-friendly display"""
        
        # AI & Analysis Commands
        ui.print_section("🤖 AI & Analysis", "🧠")
        ui.print_container_content(f"  {Colors.SOFT_CYAN}/analyze <file>{Colors.LIGHT_GRAY}     - Deep code analysis with ML", Colors.LIGHT_GRAY)
        ui.print_container_content(f"  {Colors.SOFT_CYAN}/info{Colors.LIGHT_GRAY}             - System info (ESC to exit)", Colors.LIGHT_GRAY)
        ui.print_container_content(f"  {Colors.DIM}/help ai{Colors.LIGHT_GRAY}           - Show all AI commands", Colors.LIGHT_GRAY)
        
        ui.print_container_separator()
        
        # Developer Workflow Commands  
        ui.print_section("🔧 Developer Workflow", "⚡")
        ui.print_container_content(f"  {Colors.SOFT_ORANGE}/format <file>{Colors.LIGHT_GRAY}     - Format code with black/autopep8", Colors.LIGHT_GRAY)
        ui.print_container_content(f"  {Colors.SOFT_ORANGE}/test [pattern]{Colors.LIGHT_GRAY}   - Run tests with pytest", Colors.LIGHT_GRAY)
        ui.print_container_content(f"  {Colors.DIM}/help workflow{Colors.LIGHT_GRAY}     - Show all workflow commands", Colors.LIGHT_GRAY)
        
        ui.print_container_separator()
        
        # System Commands
        ui.print_section("🔄 System & Control", "⚙️")
        ui.print_container_content(f"  {Colors.SOFT_RED}/help{Colors.LIGHT_GRAY}             - Show detailed help", Colors.LIGHT_GRAY)
        ui.print_container_content(f"  {Colors.SOFT_RED}/quit{Colors.LIGHT_GRAY}             - Exit Pyscription", Colors.LIGHT_GRAY)
        
        ui.print_container_separator()
    
    def _handle_format_command(self, arg: str):
        """Handle code formatting commands"""
        import subprocess
        import os
        
        if not arg:
            ui.print_warning("Usage: /format <file.py> [formatter]")
            ui.print_container_content("Available formatters: black, autopep8, yapf")
            return
        
        parts = arg.split()
        file_path = parts[0]
        formatter = parts[1] if len(parts) > 1 else 'black'
        
        if not os.path.exists(file_path):
            ui.print_error(f"File not found: {file_path}")
            return
        
        ui.print_info(f"🎨 Formatting {file_path} with {formatter}...")
        
        try:
            if formatter == 'black':
                result = subprocess.run(['black', file_path], capture_output=True, text=True)
            elif formatter == 'autopep8':
                result = subprocess.run(['autopep8', '--in-place', file_path], capture_output=True, text=True)
            elif formatter == 'yapf':
                result = subprocess.run(['yapf', '--in-place', file_path], capture_output=True, text=True)
            else:
                ui.print_error(f"Unknown formatter: {formatter}")
                return
            
            if result.returncode == 0:
                ui.print_success(f"✅ Formatted {file_path} successfully!")
                if result.stdout:
                    ui.print_container_content(result.stdout)
            else:
                ui.print_error(f"❌ Formatting failed: {result.stderr}")
                
        except FileNotFoundError:
            ui.print_error(f"❌ {formatter} not installed. Install with: pip install {formatter}")
        except Exception as e:
            ui.print_error(f"❌ Formatting error: {e}")
    
    def _handle_test_command(self, arg: str):
        """Handle test execution commands"""
        import subprocess
        import os
        
        ui.print_info("🧪 Running tests...")
        
        # Determine test command
        if os.path.exists('pytest.ini') or os.path.exists('pyproject.toml'):
            cmd = ['pytest']
        elif os.path.exists('setup.py'):
            cmd = ['python', '-m', 'unittest']
        else:
            cmd = ['python', '-m', 'pytest']
        
        # Add pattern if provided
        if arg:
            cmd.append(arg)
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            ui.print_section("Test Results", "🧪")
            if result.stdout:
                ui.print_container_content(result.stdout)
            if result.stderr:
                ui.print_container_content(result.stderr, Colors.SOFT_RED)
            
            if result.returncode == 0:
                ui.print_success("✅ All tests passed!")
            else:
                ui.print_warning(f"⚠️ Tests finished with exit code {result.returncode}")
                
        except FileNotFoundError:
            ui.print_error("❌ Test runner not found. Install with: pip install pytest")
        except Exception as e:
            ui.print_error(f"❌ Test execution error: {e}")
    
    def _handle_coverage_command(self):
        """Handle code coverage analysis"""
        import subprocess
        
        ui.print_info("📊 Analyzing code coverage...")
        
        try:
            # Run coverage
            result = subprocess.run(['coverage', 'run', '-m', 'pytest'], capture_output=True, text=True)
            if result.returncode != 0:
                ui.print_warning("⚠️ Test execution had issues, but generating coverage report...")
            
            # Generate report
            report_result = subprocess.run(['coverage', 'report'], capture_output=True, text=True)
            
            ui.print_section("Coverage Report", "📊")
            if report_result.stdout:
                ui.print_container_content(report_result.stdout)
            
            # Generate HTML report
            html_result = subprocess.run(['coverage', 'html'], capture_output=True, text=True)
            if html_result.returncode == 0:
                ui.print_success("✅ HTML coverage report generated in htmlcov/")
            
        except FileNotFoundError:
            ui.print_error("❌ Coverage not installed. Install with: pip install coverage")
        except Exception as e:
            ui.print_error(f"❌ Coverage analysis error: {e}")
    
    def _handle_lint_command(self, arg: str):
        """Handle code linting commands"""
        import subprocess
        import os
        
        if not arg:
            arg = "."  # Default to current directory
        
        ui.print_info(f"🔍 Linting {arg}...")
        
        linters = [
            ('pylint', ['pylint', arg]),
            ('flake8', ['flake8', arg]),
            ('mypy', ['mypy', arg])
        ]
        
        for linter_name, cmd in linters:
            try:
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                ui.print_section(f"{linter_name.capitalize()} Results", "🔍")
                if result.stdout:
                    lines = result.stdout.split('\n')[:20]  # First 20 lines
                    for line in lines:
                        if line.strip():
                            ui.print_container_content(line)
                    if len(result.stdout.split('\n')) > 20:
                        ui.print_container_content("... (truncated)")
                
                if result.returncode == 0:
                    ui.print_success(f"✅ {linter_name} passed!")
                else:
                    ui.print_warning(f"⚠️ {linter_name} found issues")
                
            except FileNotFoundError:
                ui.print_warning(f"⚠️ {linter_name} not installed. Install with: pip install {linter_name}")
            except Exception as e:
                ui.print_error(f"❌ {linter_name} error: {e}")
    
    def _handle_deps_command(self, arg: str):
        """Handle dependency management commands"""
        import subprocess
        import os
        
        if not arg:
            ui.print_warning("Usage: /deps <command>")
            ui.print_container_content("Commands: install <package>, freeze, outdated, check")
            return
        
        parts = arg.split()
        subcmd = parts[0].lower()
        
        if subcmd == 'install':
            if len(parts) < 2:
                ui.print_warning("Usage: /deps install <package>")
                return
            
            package = parts[1]
            ui.print_info(f"📦 Installing {package}...")
            
            try:
                result = subprocess.run(['pip', 'install', package], capture_output=True, text=True)
                if result.returncode == 0:
                    ui.print_success(f"✅ {package} installed successfully!")
                else:
                    ui.print_error(f"❌ Installation failed: {result.stderr}")
            except Exception as e:
                ui.print_error(f"❌ Installation error: {e}")
        
        elif subcmd == 'freeze':
            ui.print_info("📋 Current dependencies:")
            try:
                result = subprocess.run(['pip', 'freeze'], capture_output=True, text=True)
                ui.print_section("Dependencies", "📦")
                if result.stdout:
                    for line in result.stdout.split('\n')[:15]:  # First 15 packages
                        if line.strip():
                            ui.print_container_content(line)
            except Exception as e:
                ui.print_error(f"❌ Freeze error: {e}")
        
        elif subcmd == 'outdated':
            ui.print_info("🔍 Checking for outdated packages...")
            try:
                result = subprocess.run(['pip', 'list', '--outdated'], capture_output=True, text=True)
                ui.print_section("Outdated Packages", "⚠️")
                if result.stdout:
                    ui.print_container_content(result.stdout)
                else:
                    ui.print_success("✅ All packages are up to date!")
            except Exception as e:
                ui.print_error(f"❌ Outdated check error: {e}")
        
        elif subcmd == 'check':
            ui.print_info("🔍 Checking dependency conflicts...")
            try:
                result = subprocess.run(['pip', 'check'], capture_output=True, text=True)
                if result.returncode == 0:
                    ui.print_success("✅ No dependency conflicts found!")
                else:
                    ui.print_warning("⚠️ Dependency conflicts detected:")
                    ui.print_container_content(result.stdout)
            except Exception as e:
                ui.print_error(f"❌ Dependency check error: {e}")
        
        else:
            ui.print_error(f"❌ Unknown deps command: {subcmd}")
    
    def _handle_env_command(self, arg: str):
        """Handle virtual environment commands"""
        import subprocess
        import os
        
        if not arg:
            ui.print_warning("Usage: /env <command>")
            ui.print_container_content("Commands: create <name>, list, activate <name>, info")
            return
        
        parts = arg.split()
        subcmd = parts[0].lower()
        
        if subcmd == 'create':
            if len(parts) < 2:
                ui.print_warning("Usage: /env create <name>")
                return
            
            env_name = parts[1]
            ui.print_info(f"🏗️ Creating virtual environment: {env_name}")
            
            try:
                result = subprocess.run(['python', '-m', 'venv', env_name], capture_output=True, text=True)
                if result.returncode == 0:
                    ui.print_success(f"✅ Virtual environment '{env_name}' created!")
                    ui.print_container_content(f"Activate with: source {env_name}/bin/activate")
                else:
                    ui.print_error(f"❌ Creation failed: {result.stderr}")
            except Exception as e:
                ui.print_error(f"❌ Environment creation error: {e}")
        
        elif subcmd == 'list':
            ui.print_info("📂 Looking for virtual environments...")
            venvs = []
            for item in os.listdir('.'):
                if os.path.isdir(item) and os.path.exists(os.path.join(item, 'pyvenv.cfg')):
                    venvs.append(item)
            
            if venvs:
                ui.print_section("Virtual Environments", "🏗️")
                for venv in venvs:
                    ui.print_container_content(f"  📁 {venv}")
            else:
                ui.print_warning("No virtual environments found in current directory")
        
        elif subcmd == 'info':
            ui.print_info("ℹ️ Python environment information:")
            ui.print_section("Environment Info", "🐍")
            ui.print_container_content(f"Python executable: {subprocess.sys.executable}")
            ui.print_container_content(f"Virtual env: {os.environ.get('VIRTUAL_ENV', 'None')}")
            ui.print_container_content(f"Python version: {subprocess.sys.version}")
        
        else:
            ui.print_error(f"❌ Unknown env command: {subcmd}")
    
    def _show_ai_help(self):
        """Show detailed AI and analysis commands"""
        ui.print_section("🤖 AI & Analysis Commands", "🧠")
        
        ai_commands = [
            ("/analyze <file>", "Deep analysis of Python file with ML"),
            ("/generate <pattern>", "Generate code templates (singleton, factory, etc)"),
            ("/models", "Show available AI models"),
            ("/switch <model>", "Switch AI model"),
            ("/clear", "Clear conversation history"),
            ("/stats", "Show system statistics"),
            ("/info", "Show system info with indefinite display")
        ]
        
        for cmd, desc in ai_commands:
            ui.print_container_content(f"  {Colors.SOFT_CYAN}{cmd:<20}{Colors.LIGHT_GRAY} - {desc}")
        
        ui.print_container_separator()
    
    def _show_workflow_help(self):
        """Show detailed developer workflow commands"""
        ui.print_section("🔧 Developer Workflow Commands", "⚡")
        
        workflow_commands = [
            ("/format <file> [tool]", "Format code (black, autopep8, yapf)"),
            ("/test [pattern]", "Run tests with pytest/unittest"),
            ("/coverage", "Generate code coverage reports"),
            ("/lint [path]", "Run multiple linters (pylint, flake8, mypy)"),
            ("/deps <command>", "Manage dependencies (install, freeze, outdated, check)"),
            ("/env <command>", "Manage virtual environments (create, list, info)")
        ]
        
        for cmd, desc in workflow_commands:
            ui.print_container_content(f"  {Colors.SOFT_ORANGE}{cmd:<20}{Colors.LIGHT_GRAY} - {desc}")
        
        ui.print_container_separator()
        
        # Show examples
        ui.print_container_content(f"{Colors.SOFT_BLUE}Examples:")
        ui.print_container_content(f"  /format myfile.py black")
        ui.print_container_content(f"  /test tests/test_*.py") 
        ui.print_container_content(f"  /deps install requests")
        ui.print_container_content(f"  /env create myproject")
        ui.print_container_separator()
    
    def _show_info_screen(self):
        """Display ASCII art with version info until ESC pressed"""
        import sys
        import select
        import termios
        import tty
        import time
        
        # Clear screen and show info
        ui.clear_screen()
        
        # Display ASCII art and info indefinitely
        while True:
            # Clear and redraw
            print('\033[2J\033[H', end='')  # Clear screen, move cursor to top
            
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
            
            # Version and system info
            print(f"{Colors.SOFT_YELLOW}💊 Terminal medication. No prescription needed.{Colors.RESET}")
            print()
            print(f"{Colors.SOFT_GREEN}🏥 AI-Enhanced Python Development Assistant{Colors.RESET}")
            print(f"{Colors.LIGHT_GRAY}🔬 Diagnose • 💉 Inject • 💊 Medicate • 🧬 Evolve{Colors.RESET}")
            print()
            
            # System information
            print(f"{Colors.SOFT_BLUE}📊 SYSTEM INFORMATION:{Colors.RESET}")
            print(f"   🐍 Python: {sys.version.split()[0]}")
            print(f"   💻 Platform: {sys.platform}")
            print(f"   📁 Project: {self.project_dir.absolute()}")
            print()
            
            # AI Statistics
            try:
                stats = self.mentor.get_stats()
                print(f"{Colors.SOFT_PURPLE}🤖 AI STATISTICS:{Colors.RESET}")
                print(f"   📚 Documents: {stats['ml_stats']['processed_documents']}")
                print(f"   🔍 Patterns: {stats['ml_stats']['discovered_patterns']}")
                print(f"   💬 Interactions: {stats['ml_stats']['total_interactions']}")
                print(f"   🧠 Backend: {stats['ai_stats']['current_backend']}")
                print()
            except:
                print(f"{Colors.SOFT_PURPLE}🤖 AI: Ready for assistance{Colors.RESET}")
                print()
            
            # Medical Commands Summary
            print(f"{Colors.SOFT_ORANGE}💊 AVAILABLE TREATMENTS:{Colors.RESET}")
            print("   🏥 --checkup      Comprehensive health examination")
            print("   🚨 --emergency    Critical issue detection")  
            print("   🧠 --therapy      Guided improvement session")
            print("   📊 --vitals       Real-time health monitoring")
            print("   📋 --prescription Detailed recommendations")
            print()
            
            # Interactive modes
            print(f"{Colors.SOFT_GREEN}🗣️ INTERACTIVE MODES:{Colors.RESET}")
            print("   💬 --doctor       Conversational AI assistant")
            print("   🔧 --surgeon      Autonomous code improvement")
            print()
            
            # Exit instruction
            print(f"{Colors.DIM}Press ESC to return to conversation, or Ctrl+C to exit{Colors.RESET}")
            
            # Check for ESC key (non-blocking)
            try:
                # Set terminal to raw mode to capture individual keypresses
                old_settings = termios.tcgetattr(sys.stdin)
                tty.setraw(sys.stdin.fileno())
                
                # Non-blocking check for input
                if select.select([sys.stdin], [], [], 0.5) == ([sys.stdin], [], []):
                    char = sys.stdin.read(1)
                    if ord(char) == 27:  # ESC key
                        # Restore terminal settings
                        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
                        ui.clear_screen()
                        print(f"{Colors.SOFT_GREEN}👋 Returning to conversation mode...{Colors.RESET}")
                        return
                
                # Restore terminal settings
                termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
                
            except KeyboardInterrupt:
                # Restore terminal and exit gracefully
                try:
                    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
                except:
                    pass
                ui.clear_screen()
                print(f"{Colors.SOFT_GREEN}👋 Exiting Pyscription...{Colors.RESET}")
                sys.exit(0)
            except:
                # Fallback - just show once and return
                time.sleep(3)
                ui.clear_screen()
                print(f"{Colors.SOFT_GREEN}👋 Returning to conversation mode...{Colors.RESET}")
                return
    
    def _show_help(self):
        """Show help information"""
        print("\n📖 Pyscription Help")
        print("=" * 30)
        print("🗣️  Natural Conversation:")
        print("   Just ask questions naturally about Python!")
        print("   Examples:")
        print("   • 'How do I read a file in Python?'")
        print("   • 'What's wrong with this code: def foo(): pass'")
        print("   • 'Explain list comprehensions to me'")
        print()
        print("🔗 Quick Commands:")
        print("   /analyze <file>     - Deep analysis of Python file")
        print("   /format <file>      - Format code with black/autopep8/yapf")
        print("   /test [pattern]     - Run tests with pytest/unittest")
        print("   /info               - Show system info (ESC to exit)")
        print("   /quit               - Exit Pyscription")
        print()
        print("📚 Detailed Help:")
        print("   /help ai            - Show all AI & analysis commands")
        print("   /help workflow      - Show all developer workflow commands")


def main():
    """Main entry point for conversational CLI"""
    parser = argparse.ArgumentParser(description='Pyscription - Conversational AI Python Assistant')
    parser.add_argument('--setup', action='store_true', help='Setup with Python documentation download')
    parser.add_argument('--download-docs', help='Download Python docs (version: 3.9, 3.10, 3.11)')
    parser.add_argument('--ingest-docs', help='Ingest documentation from path')
    parser.add_argument('--analyze', '-a', help='Analyze Python file')
    parser.add_argument('--interactive', '-i', action='store_true', help='Start interactive conversation mode')
    parser.add_argument('--chat', '-c', help='Ask a single question and exit')
    
    args = parser.parse_args()
    
    # Handle setup
    if args.setup:
        print("🚀 Setting up Pyscription with conversational AI...")
        
        # Download docs
        downloader = DocumentationDownloader()
        docs_path = downloader.download_python_docs("3.11")
        
        if docs_path:
            # Ingest docs
            mentor = MLEnhancedPyscription()
            count = mentor.ingest_docs(docs_path)
            print(f"✅ Setup complete! Processed {count} documentation files.")
            print("🤖 Local AI ready for conversational assistance!")
            print()
            print("💡 Quick start:")
            print("  python -m pyscription.cli.conversational --interactive")
        else:
            print("❌ Setup failed. Try manual documentation ingestion.")
        return
    
    # Handle documentation download
    if args.download_docs:
        downloader = DocumentationDownloader()
        docs_path = downloader.download_python_docs(args.download_docs)
        if docs_path:
            print(f"📚 Use: python -m pyscription.cli.conversational --ingest-docs {docs_path}")
        return
    
    # Handle documentation ingestion
    if args.ingest_docs:
        mentor = MLEnhancedPyscription()
        count = mentor.ingest_docs(args.ingest_docs)
        print(f"✅ Ingested {count} documentation files")
        return
    
    # Handle single file analysis
    if args.analyze:
        mentor = MLEnhancedPyscription()
        try:
            with open(args.analyze, 'r') as f:
                code = f.read()
            
            print(f"🔍 Analyzing {args.analyze}...")
            response = mentor.chat_about_code(code=code)
            print(f"\n🤖 Analysis:\n{response}")
        except FileNotFoundError:
            print(f"❌ File not found: {args.analyze}")
        except Exception as e:
            print(f"❌ Error: {e}")
        return
    
    # Handle single chat question
    if args.chat:
        mentor = MLEnhancedPyscription()
        response = mentor.chat_about_code(question=args.chat)
        print(f"🤖 {response}")
        return
    
    # Default to interactive mode
    if args.interactive or len(sys.argv) == 1:
        cli = ConversationalCLI()
        cli.run_interactive()
    else:
        print("🤖 Pyscription - Conversational AI Python Assistant")
        print("\nQuick start:")
        print("  python -m pyscription.cli.conversational --setup")
        print("  python -m pyscription.cli.conversational --interactive")
        print()
        parser.print_help()


if __name__ == "__main__":
    main()

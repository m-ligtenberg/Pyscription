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

from pyscription.core.mentor import MLEnhancedPyscription
from pyscription.utils.documentation_downloader import DocumentationDownloader
from pyscription.utils.terminal_styling import ui, Colors


class ConversationalCLI:
    """Conversational command-line interface"""
    
    def __init__(self):
        self.mentor = MLEnhancedPyscription()
        self.running = True
    
    def run_interactive(self):
        """Run interactive conversational mode"""
        # Beautiful header
        ui.print_header("Pyscription - Conversational AI Mode", 
                       "Your Local Python Development Assistant")
        
        # Examples section
        ui.print_section("Natural Language Examples", "💬")
        examples = [
            "How do I implement a singleton pattern?",
            "Can you analyze this code: [paste code]",
            "What's the best way to handle exceptions?",
            "Generate a factory pattern for me",
            "Explain list comprehensions with examples"
        ]
        for example in examples:
            print(f"{Colors.BG_LIGHT_BLUE}{Colors.DARK_BLUE}  • {Colors.ITALIC}'{Colors.GREEN}{example}{Colors.DARK_BLUE}'{Colors.RESET}")
        print()
        
        # Commands section
        commands = [
            ("/analyze <file>", "Analyze a Python file with ML"),
            ("/generate <pattern>", "Generate code template"),
            ("/models", "Show available AI models"),
            ("/switch <model>", "Switch AI model"),
            ("/clear", "Clear conversation history"),
            ("/stats", "Show system statistics"),
            ("/help", "Show this help"),
            ("/quit", "Exit Pyscription")
        ]
        ui.print_command_help(commands)
        
        while self.running:
            try:
                user_input = ui.input_prompt("You:", "normal").strip()
                
                if not user_input:
                    continue
                    
                if user_input.startswith('/'):
                    self._handle_command(user_input)
                else:
                    self._handle_conversation(user_input)
                    
            except KeyboardInterrupt:
                ui.print_info("👋 See you later!")
                break
            except EOFError:
                ui.print_info("👋 See you later!")
                break
            except Exception as e:
                ui.print_error(f"Error: {e}")
    
    def _handle_command(self, command: str):
        """Handle special commands"""
        parts = command[1:].split(' ', 1)
        cmd = parts[0].lower()
        arg = parts[1] if len(parts) > 1 else ''
        
        if cmd == 'quit' or cmd == 'exit':
            ui.print_success("👋 Happy coding!")
            self.running = False
            
        elif cmd == 'help':
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
                ui.print_code_block('\n'.join(preview_lines), "python")
                
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
                    ui.print_code_block(code, "python")
                    
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
        """Print AI response with beautiful formatting"""
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
                                ui.print_code_block('\n'.join(current_code), language)
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
                            print(f"{Colors.BG_LIGHT_BLUE}{Colors.DARK_BLUE}{line}{Colors.RESET}")
            else:
                # Regular paragraph
                print(f"{Colors.BG_LIGHT_BLUE}{Colors.DARK_BLUE}{paragraph}{Colors.RESET}")
        
        print()  # Extra spacing
    
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
        print("⚡ Special Commands:")
        print("   /analyze <file>     - Deep analysis of Python file")
        print("   /generate <pattern> - Generate design pattern code")
        print("   /models             - List available AI models")
        print("   /switch <model>     - Change AI model")
        print("   /clear              - Clear conversation memory")
        print("   /stats              - Show system statistics")
        print("   /quit               - Exit Pyscription")


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
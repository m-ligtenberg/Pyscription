#!/usr/bin/env python3
"""
Pyscription CLI Entry Point
Main entry point for the Pyscription CLI system
"""

import argparse
import sys
from pathlib import Path

# Add current directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from pyscription.core.mentor import MLEnhancedPyscription
from pyscription.utils.documentation_downloader import DocumentationDownloader
from pyscription.cli.conversational import ConversationalCLI
from pyscription.cli.agent_mode import AgentCLI


def main():
    """Main entry point with argument parsing"""
    parser = argparse.ArgumentParser(
        description='Pyscription - ML-Enhanced Python Development Assistant',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  pyscription --setup                    # Complete setup with documentation
  pyscription --interactive              # Start conversational mode
  pyscription --agent                    # Start autonomous agent mode
  pyscription --analyze code.py          # Analyze a Python file
  pyscription --search "decorator pattern"  # Search documentation
        """
    )
    
    # Mode selection
    parser.add_argument('--interactive', '-i', action='store_true', 
                       help='Start conversational AI mode')
    parser.add_argument('--agent', '-a', action='store_true',
                       help='Start autonomous agent mode')
    
    # Setup and configuration
    parser.add_argument('--setup', action='store_true',
                       help='Complete setup with Python documentation download')
    parser.add_argument('--download-docs', 
                       help='Download Python docs (version: 3.9, 3.10, 3.11)')
    parser.add_argument('--ingest-docs', 
                       help='Ingest Python documentation from path')
    
    # Analysis and search
    parser.add_argument('--analyze', help='Analyze Python file or code snippet')
    parser.add_argument('--search', '-s', help='Search documentation and patterns')
    parser.add_argument('--discover-patterns', action='store_true',
                       help='Discover patterns from coding history')
    
    # Project options
    parser.add_argument('--project', '-p', default='.',
                       help='Project directory for agent mode')
    
    args = parser.parse_args()
    
    try:
        # Handle setup first
        if args.setup:
            print("🚀 Setting up Pyscription with conversational AI...")
            
            # Download documentation
            downloader = DocumentationDownloader()
            docs_path = downloader.download_python_docs("3.11")
            
            if docs_path:
                # Ingest documentation
                mentor = MLEnhancedPyscription()
                count = mentor.ingest_docs(docs_path)
                print(f"✅ Setup complete! Processed {count} documentation files.")
                print("🤖 Local AI ready for conversational assistance!")
                print("\n💡 Quick start:")
                print("  pyscription --interactive    # Start chatting")
                print("  pyscription --agent          # Start autonomous mode")
            else:
                print("❌ Setup failed. Try manual documentation ingestion.")
            return
        
        # Handle documentation download
        if args.download_docs:
            downloader = DocumentationDownloader()
            docs_path = downloader.download_python_docs(args.download_docs)
            if docs_path:
                print(f"📚 Use: pyscription --ingest-docs {docs_path}")
            return
        
        # Handle documentation ingestion
        if args.ingest_docs:
            mentor = MLEnhancedPyscription()
            count = mentor.ingest_docs(args.ingest_docs)
            print(f"✅ Ingested {count} documentation files")
            return
        
        # Handle pattern discovery
        if args.discover_patterns:
            mentor = MLEnhancedPyscription()
            count = mentor.discover_patterns_from_history()
            print(f"🔍 Analyzed {count} code samples from history")
            print("✅ Pattern discovery complete!")
            return
        
        # Handle single file analysis
        if args.analyze:
            mentor = MLEnhancedPyscription()
            try:
                # Check if it's a file path or code snippet
                if Path(args.analyze).exists():
                    with open(args.analyze, 'r') as f:
                        code = f.read()
                    print(f"🔍 Analyzing {args.analyze}...")
                else:
                    code = args.analyze
                    print("🔍 Analyzing code snippet...")
                
                # Get AI-powered analysis
                response = mentor.chat_about_code(code=code)
                print(f"\n🤖 Pyscription Analysis:\n{response}")
                
            except FileNotFoundError:
                print(f"❌ File not found: {args.analyze}")
            except Exception as e:
                print(f"❌ Error: {e}")
            return
        
        # Handle search
        if args.search:
            mentor = MLEnhancedPyscription()
            results = mentor.smart_search(args.search)
            
            print(f"🔍 Smart Search Results for: '{args.search}'")
            if not results:
                print("No results found. Try running --setup first to ingest documentation.")
                return
            
            for i, result in enumerate(results, 1):
                print(f"\n{i}. {result['title']} ({result['type']})")
                print(f"   Relevance: {result['relevance']:.3f}")
                print(f"   Content: {result['content']}")
                print(f"   Source: {result['source']}")
            return
        
        # Handle interactive conversational mode
        if args.interactive:
            cli = ConversationalCLI()
            cli.run_interactive()
            return
        
        # Handle autonomous agent mode
        if args.agent:
            cli = AgentCLI(args.project)
            cli.run_interactive_agent()
            return
        
        # Default: show help and features
        print("🤖 Pyscription - ML-Enhanced Python Development Assistant")
        print("\n🚀 Key Features:")
        print("  🗣️  Conversational AI - Chat naturally about Python")
        print("  🤖 Autonomous Agent - Self-directed code improvements")
        print("  📚 Documentation Analysis - Semantic search in Python docs")
        print("  🔍 Pattern Discovery - Learn from your coding patterns")
        print("  🛡️  Security Analysis - Detect vulnerabilities and code smells")
        print("  🎨 Beautiful Terminal UI - Light blue theme with syntax highlighting")
        
        print("\n💡 Quick Start:")
        print("  pyscription --setup        # First-time setup")
        print("  pyscription --interactive  # Start conversational mode")
        print("  pyscription --agent        # Start autonomous agent mode")
        
        print("\n📖 For more options:")
        parser.print_help()
        
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
# Pyscription 💊 - Medication for your Python Headaches\n\n## 🚀 **MAJOR UPDATES** (Latest Session)\n\n### ✅ **Enhanced Medical Command Suite** (NEW!)\n- **Comprehensive Diagnostics**: New medical-themed commands for complete codebase health management\n- **Real-time Monitoring**: Live code health vitals and metrics tracking\n- **Treatment Recommendations**: AI-powered improvement prescriptions\n- **Emergency Response**: Critical issue detection and immediate remediation\n- **Interactive Therapy**: Guided code improvement sessions\n\n**New Medical Commands:**\n```bash\n--checkup        # Comprehensive codebase health examination\n--emergency      # Critical issue immediate diagnosis and fix  \n--therapy        # Interactive guided code improvement session\n--vitals         # Real-time code health monitoring and metrics\n--prescription   # Generate detailed improvement recommendations\n```\n\n### ✅ **Enhanced Splash Screen Experience**\n- **Cinematic Startup**: Beautiful ASCII art logo with medical theming\n- **Timed Display**: 2.5-second display with elegant fade-out effect\n- **Color-coded Branding**: Soft cyan logo, yellow tagline, green features\n- **Smooth Transitions**: Fade effect leading into main interface\n\n### ✅ **Developer Workflow Integration** (NEW!)\n- **Complete Development Toolkit**: Integrated formatting, testing, linting, and dependency management\n- **One-Command Operations**: Execute common development tasks without leaving Pyscription\n- **Smart Tool Detection**: Automatically detects and uses available tools (pytest, black, pylint, etc.)\n- **Environment Management**: Virtual environment creation and management\n- **Real-time Feedback**: Beautiful terminal output with progress indicators\n\n**New Workflow Commands:**\n```bash\n/format <file> [tool]  # Format code with black, autopep8, or yapf\n/test [pattern]        # Run tests with pytest or unittest\n/coverage              # Generate code coverage reports\n/lint [path]           # Run pylint, flake8, and mypy\n/deps <command>        # Manage dependencies (install, freeze, outdated, check)\n/env <command>         # Manage virtual environments (create, list, info)\n```\n\n### ✅ **Enhanced Information Display** (NEW!)\n- **Interactive Info Screen**: `/info` command shows indefinite ASCII display\n- **System Statistics**: Real-time Python version, platform, and project info\n- **AI Status**: Current backend, document count, pattern statistics\n- **Medical Commands Summary**: Quick reference for all available treatments\n- **ESC to Exit**: Elegant keyboard control for returning to conversation\n\n### ✅ **Medical-Themed UI/UX Enhancements** (NEW!)\n- **Medical Error Handling**: Diagnostic-themed error messages with treatment suggestions\n- **Clinical Messaging**: DIAGNOSIS, SYMPTOM, TREATMENT, RECOVERY, EMERGENCY themed feedback\n- **Responsive Design**: Adaptive terminal width (60-120 chars) with intelligent text wrapping\n- **Categorized Commands**: Organized help system with AI & Analysis, Developer Workflow, System & Control\n- **Visual Improvements**: Enhanced splash screen function, flashing critical alerts, diagnostic displays\n- **Intelligent Text Wrapping**: Word-aware wrapping for better readability across terminal sizes\n\n### ✅ **Advanced Scrolling Terminal Interface**\n- **Locked Terminal**: Main terminal window stays fixed, content scrolls inside bordered container\n- **Smart Scrolling**: Automatic content scrolling with scroll indicators showing [current-lines/total]\n- **Buffer System**: All commands, responses, and interactions stored in scrollable buffer\n- **Improved Text Wrapping**: Perfect alignment for wrapped text with proper indentation\n- **Input History**: Previous commands and responses accessible via scroll buffer\n- **Auto-scroll to Bottom**: Latest content always visible, input prompt at bottom\n\n### ✅ **Complete Python Documentation Integration**\n- **507 Documentation Files**: Automatic detection and ingestion of local Python .txt documentation\n- **Smart Setup Process**: `--setup` command prioritizes local docs over downloads\n- **Enhanced AI Knowledge**: Doctor now has access to complete Python standard library documentation\n- **Documentation Commands**: \n  - `/find-docs` - Locate and preview available documentation\n  - `/ingest-local-docs` - Import local docs into AI knowledge base\n  - Real-time doc search and semantic analysis\n\n### ✅ **OpenAI API Integration for Premium AI**\n- **Dual AI System**: Local AI by default + optional OpenAI for enhanced analysis\n- **Secure API Key Storage**: Keys stored using keyring or encrypted config files\n- **Premium Code Analysis**: Advanced code feedback when OpenAI is configured\n- **API Management Commands**:\n  - `/set-openai-key <key>` - Configure OpenAI API key securely\n  - `/openai-status` - Check API configuration and test connection\n  - `/remove-openai-key` - Remove API key and return to local-only mode\n\n### ✅ **Extended CLI Features & System Integration**\n- **System Commands**: Full Linux command integration within Pyscription\n  - `/ls [path]`, `/pwd`, `/cd <path>`, `/mkdir <name>`, `/touch <file>`, `/rm <file>`\n- **Git Integration**: Native git commands with beautiful output formatting\n  - `/git <command>`, `/g` (status), `/glog`, `/gdiff`, `/gadd`, `/gcommit <msg>`\n- **Enhanced Help System**: Organized command categories with perfect alignment\n- **Medical Theming**: \"💊 The Doctor\" and \"🔧 The Surgeon\" response titles\n\n### ✅ **UI/UX Improvements**\n- **Perfect Text Alignment**: Fixed-width command columns with proper description wrapping\n- **Color-coded Commands**: Different colors for Python, System, Git, and AI commands\n- **Terminal Features Display**: Shows scrolling capabilities and buffer status\n- **Responsive Layout**: Adapts to different terminal sizes while maintaining formatting\n\n---

*AI-enhanced command-line assistant for Python development - operates like a software physician*

## Overview
Pyscription is an AI-enhanced command-line assistant designed to help you maintain, refactor and analyze Python code. Although it operates like a doctor reviewing a patient file – diagnosing patterns, prescribing fixes and guiding your workflow – it provides intelligent, context-aware assistance for Python development.

## Core Philosophy
- **Production Ready**: Suited for real projects and active codebases
- **Security First**: Includes multiple vulnerability checks mapped to CWE standards
- **AI Powered**: Uses locally hosted language models for intelligent suggestions
- **Privacy Conscious**: All analysis happens on your machine, no external data transmission
- **Learning-Based**: Grows smarter from your coding patterns and interactions
- **Zero Database Anxiety**: File-based storage using JSON and compressed pickle files

## Best Practices and Workflow Tips  
- Edit claude.md after every major task so in a new session he will know what to do next and where he left off
- Always try and work modular, no files exceeding the thousands of lines, if you can make a helper for it or a different file with the function then please do so

## 💊 **MEDICATION-THEMED COMMAND STRUCTURE**

Pyscription operates with a medical metaphor, offering different "treatments" for your code:

### Core Commands:
```bash
python3 -m pyscription [options] [file]

Options:
  --pill             Apply a mild correction (lint, style, syntax)
  --inject           Perform targeted code changes
  --overdose         Apply all available fixes without prompts
  --refill           Repeat the previous operation
  --side-effects     Display a list of recent changes
  --checkup          Comprehensive codebase health examination
  --emergency        Critical issue immediate diagnosis and fix
  --therapy          Interactive guided code improvement session
  --vitals           Real-time code health monitoring and metrics
  --prescription     Generate detailed improvement recommendations
  --doctor           Start conversational session with the AI Doctor
  --surgeon          Run autonomous codebase improvement (Surgeon mode)
  --analyze <file>   Perform static analysis on a single file
  --search <term>    Semantic search in Python documentation
  --setup            Initialize the environment and documentation
```

### Operating Modes:

#### Doctor Mode (`--doctor`)
- Interactive conversational AI assistant
- Natural language queries about Python topics
- Code snippet analysis and explanations
- Real-time syntax highlighting and focused dialogue

#### Surgeon Mode (`--surgeon`)
- Autonomous codebase analysis and improvement
- Comprehensive project review and refactoring
- Automated task execution with backup maintenance
- Progressive improvement plans with time/task limits

#### Security Analysis
- Built-in vulnerability detection (SQL injection, command injection, etc.)
- CWE standard mapping
- OWASP compliance assistance
- Hardcoded credential detection

#### Pattern Discovery
- ML-based design pattern recognition (Singleton, Factory, Observer)
- Code smell identification
- Architecture consistency maintenance
- Template and improvement suggestions

---

## 🚀 **CURRENT DEVELOPMENT STATUS** (2025-07-26)

## Development Memory
- Added reminder to update claude.md with every big update to track project evolution and maintain documentation
- **COMPLETED: Sticky Container Terminal Interface** - Successfully implemented terminal-friendly interface with sticky header showing current directory and scrollable content area within bordered container. Perfect fit for normal terminal windows with responsive width (60-120 chars).
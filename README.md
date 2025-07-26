# Pyscription 🚀

**Your Complete AI-Powered Python Development Assistant**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Code Quality](https://img.shields.io/badge/code%20quality-A-green.svg)](https://github.com/your-username/pyscription)

> 🎯 **Production Ready** • 🛡️ **Security First** • 🤖 **AI-Powered** • 📱 **Beautiful UI** • 🔒 **100% Local**

---

## ✨ What is Pyscription?

Pyscription is a **locally-running, ML-enhanced Python development assistant** that learns from your coding patterns and provides intelligent suggestions. Think of it as having an AI Python mentor that works entirely on your machine.

### 🎥 **Quick Demo**

```bash
# Setup in 30 seconds
curl -fsSL https://ollama.ai/install.sh | sh && ollama pull codellama:7b-instruct
python3 -m pyscription --setup

# Start chatting with your AI Python mentor!
python3 -m pyscription --interactive
```

![Demo GIF](docs/demo.gif)

---

## 🚀 **Key Features**

### 🗣️ **Conversational AI Mode**
- Chat naturally about Python like talking to a mentor
- Get instant code explanations and suggestions
- Beautiful terminal UI with syntax highlighting
- Works offline with intelligent fallback

### 🤖 **Autonomous Agent Mode** 
- Self-directed AI that analyzes your entire codebase
- Creates multi-step improvement plans autonomously
- Real-time progress visualization with animated dashboards
- Intelligently refactors code with automatic backups

### 🛡️ **Advanced Security Analysis**
- Detects 15+ types of vulnerabilities (SQL injection, XSS, etc.)
- Maps issues to CWE (Common Weakness Enumeration) standards
- Identifies hardcoded credentials and secrets
- OWASP compliance checking

### 🔍 **ML-Powered Pattern Discovery**
- Learns from your coding patterns automatically
- Detects design patterns (Singleton, Factory, Observer)
- Identifies code smells and suggests improvements
- Generates code templates based on discovered patterns

### 📚 **Documentation Intelligence**
- Semantic search through entire Python documentation
- Context-aware suggestions during coding
- Automatically finds relevant docs for your functions
- TF-IDF powered similarity matching

---

## 🎯 **Quick Start**

### Prerequisites
- Python 3.8+
- [Ollama](https://ollama.ai/) (for local AI) - *Optional, has fallback mode*

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/pyscription.git
cd pyscription

# Install dependencies
pip install -r requirements.txt

# Setup with Python documentation
python3 -m pyscription --setup
```

### Usage

```bash
# Conversational AI mode - chat naturally about Python
python3 -m pyscription --interactive

# Autonomous agent mode - let AI improve your codebase
python3 -m pyscription --agent

# Quick code analysis
python3 -m pyscription --analyze your_file.py

# Search documentation
python3 -m pyscription --search "decorator patterns"
```

---

## 📖 **Modes Overview**

### 💬 **Conversational Mode**

Chat naturally with your AI Python mentor:

```
💬 You: "How do I implement a singleton pattern?"
🤖 Pyscription: Here's a thread-safe singleton implementation...

💬 You: "What's wrong with this code: [paste code]"
🤖 Pyscription: I can see several issues. Let me explain...
```

**Features:**
- Natural language Python discussions
- Real-time code analysis and suggestions
- Beautiful syntax highlighting
- Context-aware responses using your codebase patterns

### 🤖 **Autonomous Agent Mode**

Let Pyscription analyze and improve your codebase autonomously:

```bash
🤖 Agent> plan refactor codebase for better maintainability
📋 Created execution plan with 23 tasks

🤖 Agent> auto 10 60  # Run 10 tasks or 60 minutes
🚀 Starting autonomous session...
✅ Completed: Add missing docstrings to DataProcessor
✅ Completed: Extract long method in calculate_metrics
✅ Completed: Apply singleton pattern to DatabaseConnection
```

**Features:**
- Multi-step autonomous task planning
- Intelligent code refactoring with backups
- Real-time progress dashboards
- Architecture analysis and recommendations

---

## 🛡️ **Security Analysis**

Pyscription includes enterprise-grade security analysis:

```python
# Example: Detecting security vulnerabilities
password = "hardcoded_secret"  # 🚨 CRITICAL: Hardcoded credentials
query = f"SELECT * FROM users WHERE id = {user_id}"  # 🚨 HIGH: SQL injection
os.system("rm " + filename)  # 🚨 CRITICAL: Command injection
```

**Detects:**
- Hardcoded credentials and API keys
- SQL injection vulnerabilities  
- Command injection risks
- Path traversal attacks
- Unsafe deserialization
- Weak cryptographic practices
- SSL/TLS misconfigurations
- And much more...

---

## 🏗️ **Architecture**

Pyscription follows a clean, modular architecture:

```
pyscription/
├── core/                     # Core ML components
│   ├── mentor.py            # Main orchestrator
│   ├── document_processor.py # Documentation analysis
│   ├── pattern_discovery.py # ML pattern detection
│   ├── local_ai.py         # Local AI integration
│   ├── autonomous_agent.py  # Self-directed agent
│   ├── project_analyzer.py  # Project-wide analysis
│   └── security_analyzer.py # Security vulnerability detection
├── cli/                     # Command-line interfaces
│   ├── conversational.py   # Interactive chat mode
│   └── agent_mode.py       # Autonomous agent interface
├── utils/                   # Utility modules
│   ├── terminal_styling.py # Beautiful UI components
│   └── documentation_downloader.py # Doc management
└── __main__.py             # Entry point
```

---

## 🎨 **Beautiful Terminal UI**

Pyscription features a stunning terminal interface:

- **Light Blue Theme**: Professional, easy-on-the-eyes color scheme
- **Syntax Highlighting**: Python code displayed with beautiful colors
- **Progress Animations**: Spinners, progress bars, and status dashboards
- **Interactive Elements**: Smooth command input and response formatting

---

## 🔒 **Privacy & Security**

- **100% Local Processing**: All analysis happens on your machine
- **No Data Collection**: Zero telemetry or external data transmission
- **Offline Capable**: Works without internet connection
- **Secure by Design**: Input validation and safe code execution
- **Your Code Stays Private**: Nothing ever leaves your computer

---

## 📊 **Performance**

- **Fast Startup**: < 2 seconds to interactive mode
- **Memory Efficient**: < 200MB RAM usage typical
- **Scalable**: Handles codebases with 100k+ lines
- **Responsive**: Real-time analysis and suggestions

---

## 🤝 **Contributing**

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup

```bash
# Clone and setup development environment
git clone https://github.com/your-username/pyscription.git
cd pyscription

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/

# Run linting
flake8 pyscription/
```

### Areas for Contribution

- 🔍 New security vulnerability patterns
- 🎨 Additional terminal themes
- 🤖 Enhanced AI prompts and responses
- 📚 More design pattern templates
- 🌐 Web interface development
- 📖 Documentation improvements

---

## 📝 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 **Acknowledgments**

- **Ollama Team** for excellent local LLM infrastructure
- **Python Community** for comprehensive documentation
- **Claude AI** for development assistance
- **Open Source Contributors** worldwide

---

## 📞 **Support**

- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/your-username/pyscription/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/your-username/pyscription/discussions)  
- 📚 **Documentation**: [Wiki](https://github.com/your-username/pyscription/wiki)
- ⭐ **Feature Requests**: [GitHub Issues](https://github.com/your-username/pyscription/issues/new)

---

<div align="center">

**Made with ❤️ for the Python community**

[⭐ Star this repo](https://github.com/your-username/pyscription) • [🍴 Fork it](https://github.com/your-username/pyscription/fork) • [📝 Contribute](CONTRIBUTING.md)

</div>
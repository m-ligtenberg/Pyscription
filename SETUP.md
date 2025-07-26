# 🚀 PythonMentor Setup Guide

## Quick Start (5 minutes)

### 1. Install Ollama (Local AI)
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Start Ollama service
ollama serve &

# Install a coding model (choose one)
ollama pull codellama:7b-instruct    # Best for code (4GB)
ollama pull phi3:3.8b               # Fast and efficient (2.3GB) 
ollama pull llama3.2:3b             # General purpose (2GB)
ollama pull llama3.2:1b             # Smallest/fastest (1GB)
```

### 2. Setup PythonMentor
```bash
# Complete setup with Python docs
python -m python_mentor --setup

# Or step by step:
python -m python_mentor --download-docs 3.11
python -m python_mentor --ingest-docs ~/.python_mentor/python_docs
```

### 3. Start Conversational Mode
```bash
python -m python_mentor --interactive
```

## Usage Examples

### 💬 Natural Conversation
```
💬 You: How do I implement a singleton pattern in Python?

🤖 PythonMentor: Here's a clean singleton implementation...
```

### 🔍 Code Analysis
```
💬 You: Can you analyze this code:
```python
def calculate(a, b, c, d, e, f, g):
    if a > 0:
        if b > 0:
            if c > 0:
                return a + b + c
```

🤖 PythonMentor: I see several issues with this code:
1. Too many parameters (7) - consider using a data class
2. Deep nesting (3 levels) - can be flattened
3. Missing error handling...
```

### ⚗️ Template Generation
```
/generate singleton
🏗️ Generating singleton pattern...
```

## Advanced Setup

### Custom AI Models
```bash
# Install specialized models
ollama pull deepseek-coder:6.7b     # Excellent for code
ollama pull starcoder2:3b           # GitHub Copilot alternative

# Switch models in conversation
/models
/switch deepseek-coder:6.7b
```

### Documentation Sources
```bash
# Add custom documentation
python -m python_mentor --ingest-docs /path/to/your/docs

# Download different Python versions
python -m python_mentor --download-docs 3.10
```

## System Requirements

### Minimum
- **RAM**: 4GB (for 1B models)
- **Storage**: 2GB for models + docs
- **CPU**: Any modern processor

### Recommended
- **RAM**: 8GB+ (for 7B models)
- **Storage**: 10GB for multiple models
- **CPU**: 8+ cores for faster responses

## Troubleshooting

### "Local AI not available"
```bash
# Check if Ollama is running
ollama list

# Start Ollama service
ollama serve

# Install a model
ollama pull llama3.2:1b
```

### Slow responses
```bash
# Try smaller model
/switch llama3.2:1b

# Or close other applications
```

### Import errors
```bash
# Make sure you're in the right directory
cd /path/to/pythonHelper

# Run with python -m
python -m python_mentor --interactive
```

## Features Overview

- 🤖 **Conversational AI** - Natural language Python help
- 🔍 **Code Analysis** - ML-powered pattern detection  
- 📚 **Documentation Search** - Semantic search of Python docs
- 🏗️ **Code Generation** - Template generation from patterns
- 📊 **Learning System** - Improves from your coding patterns
- 🛡️ **100% Local** - No data leaves your machine

## What Makes This Special?

Unlike ChatGPT or GitHub Copilot:
- ✅ **Completely offline** - works without internet
- ✅ **Learns your style** - adapts to your coding patterns  
- ✅ **Privacy first** - all data stays local
- ✅ **Python focused** - specialized for Python development
- ✅ **Context aware** - uses your project's patterns and docs
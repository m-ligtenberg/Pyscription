"""
Local AI integration for conversational Python assistance
Supports multiple local LLM backends (Ollama, llama.cpp, etc.)
"""

import json
import requests
from typing import Dict, List, Optional, Any
from abc import ABC, abstractmethod


class LocalAIBackend(ABC):
    """Abstract base class for local AI backends"""
    
    @abstractmethod
    def generate_response(self, messages: List[Dict], **kwargs) -> str:
        """Generate response from conversation history"""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if backend is available and running"""
        pass


class OllamaBackend(LocalAIBackend):
    """Ollama local AI backend"""
    
    def __init__(self, model: str = "codellama:7b", base_url: str = "http://localhost:11434"):
        self.model = model
        self.base_url = base_url
        self.api_url = f"{base_url}/api/chat"
    
    def generate_response(self, messages: List[Dict], **kwargs) -> str:
        """Generate response using Ollama API"""
        try:
            payload = {
                "model": self.model,
                "messages": messages,
                "stream": False,
                "options": {
                    "temperature": kwargs.get("temperature", 0.3),
                    "top_p": kwargs.get("top_p", 0.9),
                    "max_tokens": kwargs.get("max_tokens", 1000)
                }
            }
            
            response = requests.post(self.api_url, json=payload, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            return result.get("message", {}).get("content", "Sorry, I couldn't generate a response.")
            
        except requests.exceptions.RequestException as e:
            # Return None to trigger fallback mode
            return None
        except Exception as e:
            # Return None to trigger fallback mode
            return None
    
    def is_available(self) -> bool:
        """Check if Ollama is running"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False


class LlamaCppBackend(LocalAIBackend):
    """llama.cpp Python bindings backend (placeholder)"""
    
    def __init__(self, model_path: str):
        self.model_path = model_path
        # Note: Would need llama-cpp-python package
        # from llama_cpp import Llama
        # self.llm = Llama(model_path=model_path)
    
    def generate_response(self, messages: List[Dict], **kwargs) -> str:
        return "llama.cpp backend not implemented yet. Install llama-cpp-python."
    
    def is_available(self) -> bool:
        return False


class LocalAIInterface:
    """Main interface for local AI interactions"""
    
    def __init__(self, backend: LocalAIBackend = None):
        # Try Ollama by default, with Python-optimized models first
        self.preferred_models = [
            "codellama:7b-python",      # Python-specific CodeLlama
            "codellama:13b-python",     # Larger Python-specific model
            "codellama:7b-instruct",    # General CodeLlama instruct
            "codellama:13b-instruct",   # Larger general CodeLlama
            "deepseek-coder:6.7b",      # Alternative coding model
            "phi3:3.8b",                # Lightweight option
            "llama3.2:3b"               # Fallback option
        ]
        
        self.backend = backend or self._init_default_backend()
        self.conversation_history = []
        self.system_context = self._build_system_context()
    
    def _init_default_backend(self) -> LocalAIBackend:
        """Initialize the best available backend"""
        # Try Ollama first
        for model in self.preferred_models:
            ollama = OllamaBackend(model)
            if ollama.is_available():
                print(f"✅ Using Ollama with model: {model}")
                return ollama
        
        # Fallback to a basic model
        ollama = OllamaBackend("llama3.2:1b")  # Smallest model
        if ollama.is_available():
            print("✅ Using Ollama with basic model: llama3.2:1b")
            return ollama
        
        print("⚠️ No local AI available. Install Ollama: https://ollama.ai/")
        return OllamaBackend()  # Will return error messages
    
    def _build_system_context(self) -> str:
        """Build system context optimized for Python-specific models"""
        current_model = getattr(self.backend, 'model', 'unknown')
        
        if 'python' in current_model.lower():
            # Enhanced context for Python-specific models
            return """You are Pyscription 💊, a specialized Python development assistant using CodeLlama-Python.

Your medical metaphor: You're a Python doctor diagnosing code issues and prescribing fixes.

Core Python specializations:
- Deep Python syntax and semantic analysis
- Pythonic code patterns and idioms
- Standard library expertise and best practices
- Performance optimization and memory management
- Modern Python features (f-strings, type hints, dataclasses, etc.)
- Framework-specific guidance (Django, FastAPI, Flask, etc.)
- Testing strategies (pytest, unittest, mocking)
- Package management and virtual environments

Diagnostic approach:
- Analyze code for bugs, security issues, and performance problems
- Suggest Pythonic refactoring and improvements
- Provide working, tested code examples
- Explain the 'why' behind recommendations
- Focus on readability, maintainability, and performance

Treatment style: Concise, practical, with executable code examples."""
        else:
            # General context for other models
            return """You are Pyscription, a local AI assistant specialized in Python development.

Key capabilities:
- Analyze Python code and suggest improvements
- Explain Python concepts and best practices  
- Help with debugging and problem-solving
- Generate code examples and templates
- Provide guidance on design patterns and architecture

Guidelines:
- Keep responses concise and practical
- Always provide working code examples when relevant
- Focus on best practices and clean code principles
- Suggest alternative approaches when appropriate
- Be encouraging and educational

Context: You have access to ML-discovered patterns, documentation analysis, and code smell detection from the user's codebase."""
    
    def chat(self, user_message: str, ml_context: Dict = None) -> str:
        """Have a conversation with the AI"""
        if not self.backend.is_available():
            return self._fallback_response(user_message, ml_context)
        
        # Build enhanced context with ML insights
        enhanced_message = self._enhance_with_context(user_message, ml_context)
        
        # Add to conversation history
        messages = [{"role": "system", "content": self.system_context}]
        messages.extend(self.conversation_history)
        messages.append({"role": "user", "content": enhanced_message})
        
        # Generate response
        response = self.backend.generate_response(messages)
        
        # If AI failed, use fallback
        if response is None:
            return self._fallback_response(user_message, ml_context)
        
        # Update conversation history (keep last 10 exchanges)
        self.conversation_history.append({"role": "user", "content": user_message})
        self.conversation_history.append({"role": "assistant", "content": response})
        
        if len(self.conversation_history) > 20:  # Keep last 10 exchanges
            self.conversation_history = self.conversation_history[-20:]
        
        return response
    
    def _enhance_with_context(self, message: str, ml_context: Dict = None) -> str:
        """Enhance user message with ML context"""
        if not ml_context:
            return message
        
        context_parts = [message]
        
        # Add discovered patterns
        if ml_context.get('patterns'):
            patterns_info = "\n".join([p['description'] for p in ml_context['patterns'][:3]])
            context_parts.append(f"\nRelevant patterns from my codebase:\n{patterns_info}")
        
        # Add code analysis
        if ml_context.get('analysis'):
            analysis = ml_context['analysis']
            if analysis.get('functions'):
                context_parts.append(f"\nCode contains functions: {', '.join(analysis['functions'])}")
            if analysis.get('complexity', 0) > 5:
                context_parts.append(f"\nCode complexity: {analysis['complexity']} (consider refactoring)")
        
        # Add documentation suggestions
        if ml_context.get('doc_suggestions'):
            docs = [d['doc_file'] for d in ml_context['doc_suggestions'][:2]]
            context_parts.append(f"\nRelated documentation: {', '.join(docs)}")
        
        return "\n".join(context_parts)
    
    def analyze_and_chat(self, code: str, question: str = None) -> str:
        """Analyze code and provide conversational feedback"""
        # This would integrate with the ML analysis pipeline
        base_question = question or "Please analyze this code and provide suggestions for improvement."
        
        # Enhanced prompt for code analysis
        analysis_prompt = f"""Here's some Python code I'm working on:

```python
{code}
```

{base_question}

Please provide specific, actionable feedback focusing on:
1. Code quality and best practices
2. Potential improvements or refactoring opportunities  
3. Design patterns that could be applicable
4. Any code smells or issues you notice
"""
        
        return self.chat(analysis_prompt)
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
    
    def get_available_models(self) -> List[str]:
        """Get list of available models"""
        if isinstance(self.backend, OllamaBackend):
            try:
                response = requests.get(f"{self.backend.base_url}/api/tags", timeout=5)
                if response.status_code == 200:
                    models = response.json().get("models", [])
                    return [model["name"] for model in models]
            except:
                pass
        return ["No models available"]
    
    def switch_model(self, model_name: str) -> bool:
        """Switch to a different model"""
        if isinstance(self.backend, OllamaBackend):
            self.backend.model = model_name
            return True
        return False
    
    def _fallback_response(self, message: str, ml_context: Dict = None) -> str:
        """Provide helpful responses without AI"""
        message_lower = message.lower()
        
        # Pattern-based responses for common Python questions
        if any(word in message_lower for word in ['decorator', 'decorators']):
            return self._explain_decorators(ml_context)
        elif any(word in message_lower for word in ['singleton', 'design pattern']):
            return self._explain_patterns(ml_context)
        elif any(word in message_lower for word in ['exception', 'error', 'try', 'catch']):
            return self._explain_exceptions(ml_context)
        elif any(word in message_lower for word in ['list comprehension', 'comprehension']):
            return self._explain_comprehensions(ml_context)
        elif any(word in message_lower for word in ['class', 'object', 'oop']):
            return self._explain_classes(ml_context)
        elif 'analyze' in message_lower or 'code' in message_lower:
            if ml_context and ml_context.get('analysis'):
                return self._format_analysis_response(ml_context['analysis'])
            return "I can analyze Python code for patterns, complexity, and potential improvements. Paste your code and I'll provide detailed feedback!"
        else:
            return self._general_fallback(message, ml_context)
    
    def _explain_decorators(self, ml_context: Dict = None) -> str:
        """Explain Python decorators"""
        response = """🎯 **Python Decorators Explained**

Decorators are a powerful Python feature that modify or enhance functions/classes without changing their core code.

**Basic Syntax:**
```python
@decorator_name
def function_name():
    pass
```

**Common Examples:**

1. **Simple Decorator:**
```python
def my_decorator(func):
    def wrapper():
        print("Before function")
        func()
        print("After function")
    return wrapper

@my_decorator
def say_hello():
    print("Hello!")
```

2. **With Arguments:**
```python
def repeat(times):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(3)
def greet(name):
    print(f"Hello {name}!")
```

**Built-in Decorators:**
- `@property` - Creates getter/setter methods
- `@staticmethod` - Method doesn't need self
- `@classmethod` - Method gets class as first argument"""
        
        if ml_context and ml_context.get('patterns'):
            decorator_patterns = [p for p in ml_context['patterns'] if 'decorator' in p.get('description', '').lower()]
            if decorator_patterns:
                response += f"\n\n**From Your Codebase:**\nFound {len(decorator_patterns)} decorator-related patterns in your code!"
        
        return response
    
    def _explain_patterns(self, ml_context: Dict = None) -> str:
        """Explain design patterns"""
        response = """🏗️ **Design Patterns in Python**

Design patterns are reusable solutions to common programming problems.

**Popular Python Patterns:**

1. **Singleton Pattern:**
```python
class Singleton:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```

2. **Factory Pattern:**
```python
class HandlerFactory:
    @staticmethod
    def create_handler(handler_type):
        if handler_type == "json":
            return JsonHandler()
        elif handler_type == "xml":
            return XmlHandler()
        return DefaultHandler()
```

3. **Observer Pattern:**
```python
class Subject:
    def __init__(self):
        self._observers = []
    
    def attach(self, observer):
        self._observers.append(observer)
    
    def notify(self):
        for observer in self._observers:
            observer.update(self)
```"""
        
        if ml_context and ml_context.get('patterns'):
            design_patterns = [p for p in ml_context['patterns'] if p.get('type') == 'design_pattern']
            if design_patterns:
                response += f"\n\n**In Your Code:**\nDetected patterns: {', '.join([p['pattern'] for p in design_patterns])}"
        
        return response
    
    def _explain_exceptions(self, ml_context: Dict = None) -> str:
        """Explain exception handling"""
        return """⚠️ **Exception Handling in Python**

Python uses try/except blocks for error handling:

**Basic Structure:**
```python
try:
    # Code that might raise an exception
    result = risky_operation()
except SpecificException as e:
    # Handle specific exception
    print(f"Error: {e}")
except Exception as e:
    # Handle any other exception
    print(f"Unexpected error: {e}")
else:
    # Runs if no exception occurred
    print("Success!")
finally:
    # Always runs, cleanup code
    cleanup_resources()
```

**Best Practices:**
1. Catch specific exceptions, not generic `Exception`
2. Use `finally` for cleanup (close files, connections)
3. Don't ignore exceptions silently
4. Use `raise` to re-raise exceptions when needed

**Custom Exceptions:**
```python
class ValidationError(Exception):
    \"\"\"Custom exception for validation errors\"\"\"
    pass

def validate_age(age):
    if age < 0:
        raise ValidationError("Age cannot be negative")
```"""
    
    def _explain_comprehensions(self, ml_context: Dict = None) -> str:
        """Explain list comprehensions"""
        return """📝 **List Comprehensions in Python**

Comprehensions provide a concise way to create lists, sets, and dictionaries.

**List Comprehension:**
```python
# Basic syntax: [expression for item in iterable if condition]
numbers = [x**2 for x in range(10) if x % 2 == 0]
# Result: [0, 4, 16, 36, 64]

# Equivalent for loop:
numbers = []
for x in range(10):
    if x % 2 == 0:
        numbers.append(x**2)
```

**Dictionary Comprehension:**
```python
# Create dict from two lists
keys = ['a', 'b', 'c']
values = [1, 2, 3]
my_dict = {k: v for k, v in zip(keys, values)}
# Result: {'a': 1, 'b': 2, 'c': 3}
```

**Set Comprehension:**
```python
unique_lengths = {len(word) for word in ['hello', 'world', 'python']}
# Result: {5, 6}
```

**Nested Comprehensions:**
```python
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flattened = [num for row in matrix for num in row]
# Result: [1, 2, 3, 4, 5, 6, 7, 8, 9]
```"""
    
    def _explain_classes(self, ml_context: Dict = None) -> str:
        """Explain Python classes"""
        return """🏛️ **Python Classes and Objects**

Classes define the structure and behavior of objects.

**Basic Class:**
```python
class Person:
    def __init__(self, name, age):
        self.name = name        # Instance variable
        self.age = age
    
    def greet(self):           # Instance method
        return f"Hi, I'm {self.name}!"
    
    @classmethod
    def from_string(cls, person_str):
        name, age = person_str.split('-')
        return cls(name, int(age))
    
    @staticmethod
    def is_adult(age):
        return age >= 18

# Usage
person = Person("Alice", 30)
print(person.greet())  # "Hi, I'm Alice!"
```

**Inheritance:**
```python
class Student(Person):
    def __init__(self, name, age, student_id):
        super().__init__(name, age)
        self.student_id = student_id
    
    def study(self, subject):
        return f"{self.name} is studying {subject}"
```

**Properties:**
```python
class Circle:
    def __init__(self, radius):
        self._radius = radius
    
    @property
    def radius(self):
        return self._radius
    
    @radius.setter
    def radius(self, value):
        if value <= 0:
            raise ValueError("Radius must be positive")
        self._radius = value
    
    @property
    def area(self):
        return 3.14159 * self._radius ** 2
```"""
    
    def _format_analysis_response(self, analysis: Dict) -> str:
        """Format code analysis results"""
        response = "🔍 **Code Analysis Results**\n\n"
        
        if not analysis.get('syntax_valid', True):
            response += f"❌ **Syntax Error:** {analysis.get('error', 'Unknown error')}\n\n"
            return response
        
        response += f"✅ **Syntax:** Valid\n"
        response += f"📊 **Complexity:** {analysis.get('complexity', 1)}\n"
        
        if analysis.get('functions'):
            response += f"🔧 **Functions:** {', '.join(analysis['functions'])}\n"
        
        if analysis.get('classes'):
            response += f"🏛️ **Classes:** {', '.join(analysis['classes'])}\n"
        
        if analysis.get('imports'):
            response += f"📦 **Imports:** {', '.join(analysis['imports'])}\n"
        
        # Add recommendations based on complexity
        if analysis.get('complexity', 1) > 10:
            response += "\n💡 **Suggestions:**\n"
            response += "- High complexity detected - consider breaking into smaller functions\n"
            response += "- Look for opportunities to reduce nested if/for statements\n"
        
        return response
    
    def _general_fallback(self, message: str, ml_context: Dict = None) -> str:
        """General fallback response"""
        response = "🤖 **Pyscription (Offline Mode)**\n\n"
        response += "I can help you with Python even without AI! Try asking about:\n\n"
        response += "• **Decorators** - 'How do decorators work?'\n"
        response += "• **Design Patterns** - 'Explain the singleton pattern'\n"
        response += "• **Exception Handling** - 'How to handle errors?'\n"
        response += "• **List Comprehensions** - 'What are comprehensions?'\n"
        response += "• **Classes & OOP** - 'How do Python classes work?'\n"
        response += "• **Code Analysis** - Paste Python code for analysis\n\n"
        
        if ml_context:
            if ml_context.get('patterns'):
                response += f"📊 I found {len(ml_context['patterns'])} patterns in your codebase.\n"
            if ml_context.get('available_docs'):
                response += "📚 I have access to Python documentation for better answers.\n"
        
        response += "\nFor full conversational AI, install Ollama:\n"
        response += "`curl -fsSL https://ollama.ai/install.sh | sh`"
        
        return response
# Contributing to Pyscription

Thank you for your interest in contributing to Pyscription! 🎉

We welcome contributions from everyone, whether you're fixing bugs, adding features, improving documentation, or suggesting enhancements.

## 🚀 Quick Start

### Development Setup

1. **Fork and Clone**
   ```bash
   git clone https://github.com/YOUR-USERNAME/pyscription.git
   cd pyscription
   ```

2. **Setup Development Environment**
   ```bash
   # Create virtual environment
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install development dependencies
   pip install -r requirements-dev.txt
   pip install -e .
   ```

3. **Install Pre-commit Hooks**
   ```bash
   pre-commit install
   ```

4. **Verify Setup**
   ```bash
   python3 -m pyscription --help
   pytest tests/
   ```

## 🎯 Ways to Contribute

### 🐛 Bug Reports
- Use the [issue template](https://github.com/your-username/pyscription/issues/new?template=bug_report.md)
- Include steps to reproduce
- Provide system information (OS, Python version)
- Include relevant code snippets or error messages

### ✨ Feature Requests
- Use the [feature request template](https://github.com/your-username/pyscription/issues/new?template=feature_request.md)
- Describe the problem you're trying to solve
- Explain your proposed solution
- Consider implementation complexity and maintenance

### 🔧 Code Contributions

#### High-Priority Areas
1. **Security Analysis Patterns** - Add new vulnerability detection rules
2. **Terminal UI Improvements** - Enhance styling and user experience
3. **AI Prompt Engineering** - Improve conversational responses
4. **Design Pattern Templates** - Add more code generation patterns
5. **Documentation Integration** - Better doc search and suggestions

#### Getting Started with Code
1. **Choose an Issue** - Look for issues labeled `good first issue`
2. **Discuss First** - Comment on the issue to discuss your approach
3. **Create Branch** - Use descriptive branch names like `feature/security-patterns`
4. **Write Tests** - All new features need comprehensive tests
5. **Update Docs** - Update relevant documentation

## 📝 Development Guidelines

### Code Style
- **Python Style**: Follow PEP 8, enforced by `black` and `flake8`
- **Type Hints**: Use type hints for all function signatures
- **Docstrings**: Use Google-style docstrings for all public functions
- **Modular Design**: Keep functions small and focused (< 50 lines)
- **No Large Files**: Split files > 500 lines into smaller modules

### Example Code Style
```python
def analyze_security_patterns(code: str, filename: str = "") -> List[SecurityIssue]:
    """Analyze code for security vulnerabilities.
    
    Args:
        code: Python source code to analyze
        filename: Optional filename for context
        
    Returns:
        List of detected security issues
        
    Raises:
        SecurityAnalysisError: If analysis fails
    """
    # Implementation here
    pass
```

### Testing
- **Coverage**: Maintain > 90% test coverage
- **Unit Tests**: Test individual functions in isolation
- **Integration Tests**: Test component interactions
- **Security Tests**: Test security analysis accuracy

```bash
# Run tests
pytest tests/

# Run with coverage
pytest tests/ --cov=pyscription --cov-report=html

# Run specific test
pytest tests/test_security_analyzer.py::test_detect_sql_injection
```

### Security Considerations
- **Input Validation**: Validate all user inputs
- **Code Execution**: Never execute arbitrary user code
- **File Access**: Validate file paths to prevent traversal attacks
- **Dependencies**: Keep dependencies minimal and well-maintained

## 🏗️ Architecture Guidelines

### Core Principles
1. **Modular Design** - Each module has a single responsibility
2. **Local Processing** - All computation happens locally
3. **Graceful Degradation** - System works without optional dependencies
4. **Beautiful UI** - Terminal interface should be professional and intuitive

### Adding New Modules
```python
# pyscription/core/new_analyzer.py
"""
New analyzer module for Pyscription
Follows the established patterns and interfaces
"""

from typing import Dict, List, Any
from .base_analyzer import BaseAnalyzer  # Use common base classes


class NewAnalyzer(BaseAnalyzer):
    """Analyzer for new functionality."""
    
    def analyze(self, code: str) -> Dict[str, Any]:
        """Analyze code and return structured results."""
        # Implementation here
        pass
```

### Terminal UI Guidelines
- Use the existing `Colors` class for consistent styling
- Follow the light blue theme established in `terminal_styling.py`
- Add progress indicators for long-running operations
- Provide clear user feedback for all actions

## 🧪 Testing Guidelines

### Test Structure
```
tests/
├── unit/                 # Unit tests for individual modules
│   ├── test_mentor.py
│   ├── test_security_analyzer.py
│   └── test_pattern_discovery.py
├── integration/          # Integration tests
│   ├── test_cli.py
│   └── test_end_to_end.py
├── fixtures/            # Test data and fixtures
│   ├── sample_code.py
│   └── vulnerable_code.py
└── conftest.py         # Pytest configuration
```

### Writing Tests
```python
import pytest
from pyscription.core.security_analyzer import SecurityPatternAnalyzer


def test_detects_hardcoded_credentials():
    """Test detection of hardcoded credentials."""
    code = '''
    password = "secret123"
    api_key = "sk-1234567890"
    '''
    
    analyzer = SecurityPatternAnalyzer()
    issues = analyzer.analyze_code_security(code)
    
    assert len(issues) >= 2
    assert any("hardcoded" in issue.description.lower() for issue in issues)
```

## 📚 Documentation

### Types of Documentation
1. **Code Comments** - Explain complex logic
2. **Docstrings** - Document all public APIs
3. **README** - Keep updated with new features
4. **Wiki** - Detailed guides and tutorials
5. **Examples** - Practical usage examples

### Documentation Standards
- Use clear, concise language
- Include code examples
- Keep documentation up-to-date with code changes
- Add screenshots for UI changes

## 🚀 Release Process

### Version Numbering
We follow [Semantic Versioning](https://semver.org/):
- **MAJOR**: Breaking changes
- **MINOR**: New features, backward compatible
- **PATCH**: Bug fixes, backward compatible

### Release Checklist
- [ ] All tests pass
- [ ] Documentation updated
- [ ] Version bumped in `setup.py`
- [ ] CHANGELOG.md updated
- [ ] Security review completed
- [ ] Performance regression testing

## 🤝 Community Guidelines

### Code of Conduct
- Be respectful and inclusive
- Focus on constructive feedback
- Help newcomers get started
- Celebrate contributions of all sizes

### Communication
- **GitHub Issues** - Bug reports and feature requests
- **GitHub Discussions** - General questions and ideas
- **Pull Request Reviews** - Code discussion and feedback

### Recognition
Contributors are recognized in:
- README.md contributors section
- Release notes
- GitHub contributor insights

## 🆘 Getting Help

### Common Issues
1. **Import Errors** - Check Python path and virtual environment
2. **Test Failures** - Ensure all dependencies installed
3. **Style Issues** - Run `black` and `flake8` before committing

### Where to Ask
- **Technical Questions** - GitHub Discussions
- **Bug Reports** - GitHub Issues
- **Feature Ideas** - GitHub Discussions or Issues

### Useful Commands
```bash
# Format code
black pyscription/

# Check style
flake8 pyscription/

# Type checking
mypy pyscription/

# Security check
bandit -r pyscription/

# Run all checks
pre-commit run --all-files
```

## 📋 Pull Request Process

1. **Fork** the repository
2. **Create** a feature branch from `main`
3. **Make** your changes with tests
4. **Run** the test suite and linting
5. **Write** a clear commit message
6. **Submit** a pull request with description
7. **Respond** to review feedback
8. **Celebrate** when merged! 🎉

### PR Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] Added tests for new functionality
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
```

---

Thank you for contributing to Pyscription! Your efforts help make Python development better for everyone. 🐍✨
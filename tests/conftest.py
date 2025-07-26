"""
Pytest configuration and fixtures for Pyscription tests
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from typing import Generator

from pyscription.core.doctor_interactive import MLEnhancedPyscription
from pyscription.core.security_analyzer import SecurityPatternAnalyzer


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for tests."""
    temp_path = Path(tempfile.mkdtemp())
    try:
        yield temp_path
    finally:
        shutil.rmtree(temp_path)


@pytest.fixture
def sample_python_code() -> str:
    """Sample Python code for testing."""
    return '''
def calculate_sum(a, b):
    """Calculate the sum of two numbers."""
    return a + b

class Calculator:
    """A simple calculator class."""
    
    def add(self, x, y):
        return x + y
    
    def multiply(self, x, y):
        return x * y

if __name__ == "__main__":
    calc = Calculator()
    result = calc.add(5, 3)
    print(f"Result: {result}")
'''


@pytest.fixture
def vulnerable_code() -> str:
    """Sample vulnerable code for security testing."""
    return '''
import os
import subprocess

# Hardcoded credentials
password = "super_secret_password"
api_key = "sk-1234567890abcdef"

def vulnerable_query(user_input):
    # SQL injection vulnerability
    query = "SELECT * FROM users WHERE name = '" + user_input + "'"
    return query

def command_injection(user_command):
    # Command injection vulnerability
    os.system("ls " + user_command)
    subprocess.call("grep " + user_command, shell=True)

def unsafe_eval(user_input):
    # Code injection vulnerability
    return eval(user_input)
'''


@pytest.fixture
def mentor_instance(temp_dir) -> MLEnhancedPyscription:
    """Create a Pyscription mentor instance for testing."""
    return MLEnhancedPyscription(data_dir=str(temp_dir))


@pytest.fixture
def security_analyzer() -> SecurityPatternAnalyzer:
    """Create a security analyzer instance for testing."""
    return SecurityPatternAnalyzer()


@pytest.fixture
def sample_files(temp_dir) -> dict:
    """Create sample Python files for testing."""
    files = {}
    
    # Simple Python file
    simple_file = temp_dir / "simple.py"
    simple_file.write_text('''
def hello_world():
    print("Hello, World!")

if __name__ == "__main__":
    hello_world()
''')
    files['simple'] = simple_file
    
    # Complex Python file
    complex_file = temp_dir / "complex.py"
    complex_file.write_text('''
class DataProcessor:
    def __init__(self, data):
        self.data = data
        self.results = []
    
    def process_complex_data(self, filters):
        # This is a complex method with high nesting
        for item in self.data:
            if item.get('active'):
                if item.get('priority') > 5:
                    for filter_type in filters:
                        if filter_type == 'important':
                            if item.get('category') in ['urgent', 'critical']:
                                if item.get('user_id') is not None:
                                    processed = self.transform_item(item)
                                    if processed:
                                        self.results.append(processed)
        return self.results
    
    def transform_item(self, item):
        # Long method that should be refactored
        result = {}
        result['id'] = item.get('id', 0)
        result['name'] = item.get('name', '').strip().title()
        result['status'] = 'processed'
        result['timestamp'] = item.get('created_at')
        result['priority'] = min(item.get('priority', 1), 10)
        result['category'] = item.get('category', 'general')
        result['user_id'] = item.get('user_id')
        result['metadata'] = item.get('metadata', {})
        return result
''')
    files['complex'] = complex_file
    
    # Vulnerable Python file
    vulnerable_file = temp_dir / "vulnerable.py"
    vulnerable_file.write_text('''
import os
import pickle

password = "hardcoded_secret"
api_token = "abc123xyz"

def sql_query(user_input):
    query = f"SELECT * FROM users WHERE id = {user_input}"
    return query

def execute_command(cmd):
    os.system("rm " + cmd)

def deserialize_data(data):
    return pickle.loads(data)
''')
    files['vulnerable'] = vulnerable_file
    
    return files
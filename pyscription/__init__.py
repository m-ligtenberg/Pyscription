"""
Pyscription CLI - ML-Enhanced Python Assistant
A modular, machine learning-enhanced Python development assistant.
"""

from .core.doctor_interactive import MLEnhancedPyscription
from .core.document_processor import DocumentProcessor  
from .core.pattern_discovery import PatternDiscovery
from .core.vectorizer import SimpleVectorizer
from .utils.documentation_downloader import DocumentationDownloader

__version__ = "1.0.0"
__author__ = "Pyscription Development Team"

__all__ = [
    'MLEnhancedPyscription',
    'DocumentProcessor', 
    'PatternDiscovery',
    'SimpleVectorizer',
    'DocumentationDownloader'
]
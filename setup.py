#!/usr/bin/env python3
"""
Setup script for Pyscription - ML-Enhanced Python Development Assistant
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read long description from README
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

# Read requirements
requirements = (this_directory / "requirements.txt").read_text().strip().split('\n')
requirements = [req.strip() for req in requirements if req.strip() and not req.startswith('#')]

setup(
    name="pyscription",
    version="1.0.0",
    author="Pyscription Team",
    author_email="hello@pyscription.dev",
    description="AI-Powered Python Development Assistant with Local ML and Security Analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/pyscription",
    project_urls={
        "Bug Tracker": "https://github.com/your-username/pyscription/issues",
        "Documentation": "https://github.com/your-username/pyscription/wiki",
        "Source Code": "https://github.com/your-username/pyscription",
        "Discussions": "https://github.com/your-username/pyscription/discussions",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Security",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Natural Language :: English",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "flake8>=5.0.0",
            "black>=22.0.0",
            "mypy>=1.0.0",
            "pre-commit>=2.20.0",
        ],
        "docs": [
            "sphinx>=5.0.0",
            "sphinx-rtd-theme>=1.0.0",
            "myst-parser>=0.18.0",
        ],
        "security": [
            "bandit>=1.7.0",
            "safety>=2.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "pyscription=pyscription.__main__:main",
        ],
    },
    include_package_data=True,
    package_data={
        "pyscription": [
            "data/*.json",
            "templates/*.py",
            "docs/*.md",
        ],
    },
    keywords=[
        "python", "ai", "ml", "development", "assistant", "security", 
        "code-analysis", "refactoring", "documentation", "patterns",
        "local-ai", "privacy", "terminal", "cli", "autonomous"
    ],
    zip_safe=False,
    platforms=["any"],
)
"""
Documentation downloader for Python documentation
Supports automatic download and extraction of official Python docs
"""

import os
import urllib.request
import tarfile
import tempfile
from pathlib import Path


class DocumentationDownloader:
    """Helper class to download Python documentation with local docs detection"""
    
    @staticmethod
    def find_local_docs() -> str:
        """Find local Python documentation in common locations"""
        possible_locations = [
            # Current project directory
            Path.cwd() / 'python_docs',
            Path.cwd().parent / 'python_docs',
            # Parent directories
            Path.cwd() / '..' / 'python_docs',
            Path.cwd() / '..' / '..' / 'python_docs',
            # Home directory
            Path.home() / 'python_docs',
            Path.home() / 'Documents' / 'python_docs',
            # Common development directories
            Path('/opt/python_docs'),
            Path('/usr/local/share/python_docs')
        ]
        
        for location in possible_locations:
            if location.exists() and location.is_dir():
                # Check if it contains documentation files
                txt_files = list(location.rglob('*.txt'))
                if len(txt_files) > 10:  # Reasonable threshold for Python docs
                    print(f"📚 Found local Python documentation at: {location}")
                    return str(location)
        
        return ""
    
    @staticmethod
    def download_python_docs(version: str = "3.11", target_dir: str = None) -> str:
        """Download Python documentation, checking for local docs first"""
        # First, check for local documentation
        local_docs = DocumentationDownloader.find_local_docs()
        if local_docs:
            print(f"✅ Using local Python documentation from: {local_docs}")
            return local_docs
        
        if target_dir is None:
            target_dir = Path.home() / '.pyscription' / 'python_docs'
        
        target_dir = Path(target_dir)
        target_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"📥 No local docs found, downloading Python {version} documentation...")
        print(f"Target directory: {target_dir}")
        
        # URLs for Python documentation
        doc_urls = {
            "3.11": "https://docs.python.org/3.11/archives/python-3.11.7-docs-text.tar.bz2",
            "3.10": "https://docs.python.org/3.10/archives/python-3.10.12-docs-text.tar.bz2",
            "3.9": "https://docs.python.org/3.9/archives/python-3.9.18-docs-text.tar.bz2"
        }
        
        if version not in doc_urls:
            print(f"❌ Version {version} not supported. Available: {list(doc_urls.keys())}")
            return ""
        
        try:
            url = doc_urls[version]
            
            # Download to temporary file
            with tempfile.NamedTemporaryFile(suffix='.tar.bz2', delete=False) as tmp_file:
                print("⬇️  Downloading...")
                urllib.request.urlretrieve(url, tmp_file.name)
                
                # Extract
                print("📦 Extracting...")
                with tarfile.open(tmp_file.name, 'r:bz2') as tar:
                    tar.extractall(target_dir)
                
                # Clean up
                os.unlink(tmp_file.name)
            
            print(f"✅ Python {version} documentation downloaded to {target_dir}")
            return str(target_dir)
            
        except Exception as e:
            print(f"❌ Error downloading documentation: {e}")
            print("💡 Try manually downloading from https://docs.python.org/")
            return ""
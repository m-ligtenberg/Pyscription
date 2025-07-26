"""
Documentation processor for ingesting and indexing Python documentation
Supports RST, Markdown, and plain text formats with semantic extraction
"""

import json
import os
import re
import math
import hashlib
import gzip
import pickle
from pathlib import Path
from typing import Dict, List, Any, Optional
from collections import Counter

from .vectorizer import SimpleVectorizer


class DocumentProcessor:
    """Processes Python documentation and creates searchable knowledge base"""
    
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self.docs_dir = data_dir / 'docs'
        self.docs_dir.mkdir(exist_ok=True)
        
        # ML components
        self.vectorizer = SimpleVectorizer()
        self.doc_embeddings = {}
        self.doc_index = {}
        
    def ingest_documentation(self, docs_path: str):
        """Ingest Python documentation from directory or files"""
        try:
            docs_path = Path(docs_path)
            
            if not docs_path.exists():
                print(f"❌ Documentation path {docs_path} not found")
                return 0
            
            print("📚 Ingesting Python documentation...")
            processed_docs = []
            
            # Check if we have read permissions
            if not os.access(docs_path, os.R_OK):
                print(f"❌ No read permissions for {docs_path}")
                return 0
            
            if docs_path.is_file():
                # Single file
                processed_docs = [self._process_doc_file(docs_path)]
            else:
                # Directory traversal
                for file_path in docs_path.rglob('*.rst'):
                    if file_path.is_file():
                        processed_docs.append(self._process_doc_file(file_path))
                
                for file_path in docs_path.rglob('*.md'):
                    if file_path.is_file():
                        processed_docs.append(self._process_doc_file(file_path))
                
                for file_path in docs_path.rglob('*.txt'):
                    if file_path.is_file():
                        processed_docs.append(self._process_doc_file(file_path))
        
            # Filter out None results
            processed_docs = [doc for doc in processed_docs if doc is not None]
            
            if not processed_docs:
                print("⚠️  No valid documentation files found")
                return 0
            
            print(f"✅ Processed {len(processed_docs)} documentation files")
            
            # Create embeddings and index
            self._create_doc_index(processed_docs)
            
            # Save processed documentation
            self._save_processed_docs(processed_docs)
            
            return len(processed_docs)
            
        except PermissionError as e:
            print(f"❌ Permission denied: {e}")
            return 0
        except Exception as e:
            print(f"❌ Error ingesting documentation: {e}")
            return 0
    
    def _process_doc_file(self, file_path: Path) -> Optional[Dict]:
        """Process a single documentation file"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Extract metadata
            doc = {
                'id': hashlib.md5(str(file_path).encode()).hexdigest()[:10],
                'path': str(file_path),
                'filename': file_path.name,
                'content': content,
                'sections': self._extract_sections(content),
                'functions': self._extract_functions_from_docs(content),
                'classes': self._extract_classes_from_docs(content),
                'examples': self._extract_code_examples(content),
                'keywords': self._extract_keywords(content)
            }
            
            return doc
            
        except Exception as e:
            print(f"⚠️  Error processing {file_path}: {e}")
            return None
    
    def _extract_sections(self, content: str) -> List[Dict]:
        """Extract sections from documentation"""
        sections = []
        
        # RST-style headers
        rst_patterns = [
            r'^(.+)\n=+\n',  # Title
            r'^(.+)\n-+\n',  # Section
            r'^(.+)\n\~+\n', # Subsection
        ]
        
        # Markdown headers
        md_patterns = [
            r'^#+\s+(.+)$',
        ]
        
        all_patterns = rst_patterns + md_patterns
        
        for i, pattern in enumerate(all_patterns):
            matches = re.finditer(pattern, content, re.MULTILINE)
            for match in matches:
                sections.append({
                    'title': match.group(1).strip(),
                    'level': i + 1,
                    'start_pos': match.start()
                })
        
        return sorted(sections, key=lambda x: x['start_pos'])
    
    def _extract_functions_from_docs(self, content: str) -> List[Dict]:
        """Extract function documentation"""
        functions = []
        
        # Pattern for function definitions in docs
        func_patterns = [
            r'^\.\.\s+function::\s+(\w+)\(([^)]*)\)',
            r'^\.\.\s+method::\s+(\w+)\(([^)]*)\)',
            r'^(\w+)\(([^)]*)\)\s*$',
            r'def\s+(\w+)\(([^)]*)\):',
        ]
        
        for pattern in func_patterns:
            matches = re.finditer(pattern, content, re.MULTILINE)
            for match in matches:
                functions.append({
                    'name': match.group(1),
                    'params': match.group(2),
                    'position': match.start()
                })
        
        return functions
    
    def _extract_classes_from_docs(self, content: str) -> List[Dict]:
        """Extract class documentation"""
        classes = []
        
        class_patterns = [
            r'^\.\.\s+class::\s+(\w+)',
            r'^class\s+(\w+)',
            r'^\s*class\s+(\w+)\(',
        ]
        
        for pattern in class_patterns:
            matches = re.finditer(pattern, content, re.MULTILINE)
            for match in matches:
                classes.append({
                    'name': match.group(1),
                    'position': match.start()
                })
        
        return classes
    
    def _extract_code_examples(self, content: str) -> List[Dict]:
        """Extract code examples from documentation"""
        examples = []
        
        # Code block patterns
        patterns = [
            r'```python\n(.*?)\n```',
            r'```\n(.*?)\n```',
            r'::\n\n((?:\s{4}.*\n)+)',
            r'>>> (.*?)(?=\n\S|\n\n|\Z)',
        ]
        
        for i, pattern in enumerate(patterns):
            matches = re.finditer(pattern, content, re.DOTALL | re.MULTILINE)
            for match in matches:
                code = match.group(1).strip()
                if len(code) > 10:  # Filter out very short snippets
                    examples.append({
                        'code': code,
                        'type': ['fenced', 'fenced', 'rst_literal', 'doctest'][i],
                        'position': match.start()
                    })
        
        return examples
    
    def _extract_keywords(self, content: str) -> List[str]:
        """Extract important keywords from documentation"""
        # Simple keyword extraction
        words = re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', content.lower())
        
        # Filter common words and keep Python-relevant terms
        python_keywords = {
            'def', 'class', 'import', 'from', 'return', 'if', 'else', 'elif',
            'for', 'while', 'try', 'except', 'finally', 'with', 'lambda',
            'yield', 'async', 'await', 'property', 'staticmethod', 'classmethod'
        }
        
        # Count word frequency
        word_counts = Counter(words)
        
        # Keep words that appear multiple times or are Python keywords
        keywords = []
        for word, count in word_counts.items():
            if count > 2 or word in python_keywords:
                if len(word) > 2:  # Skip very short words
                    keywords.append(word)
        
        return keywords[:50]  # Top 50 keywords
    
    def _create_doc_index(self, docs: List[Dict]):
        """Create searchable index of documentation"""
        print("🔍 Creating document index...")
        
        for doc in docs:
            doc_id = doc['id']
            
            # Combine all text content
            full_text = doc['content']
            section_texts = [s['title'] for s in doc['sections']]
            function_names = [f['name'] for f in doc['functions']]
            class_names = [c['name'] for c in doc['classes']]
            
            combined_text = ' '.join([full_text] + section_texts + function_names + class_names)
            
            # Create embedding
            embedding = self.vectorizer.vectorize(combined_text)
            self.doc_embeddings[doc_id] = embedding
            
            # Create keyword index
            self.doc_index[doc_id] = {
                'keywords': doc['keywords'],
                'functions': [f['name'] for f in doc['functions']],
                'classes': [c['name'] for c in doc['classes']],
                'filename': doc['filename']
            }
    
    def _save_processed_docs(self, docs: List[Dict]):
        """Save processed documentation to disk"""
        docs_file = self.docs_dir / 'processed_docs.json.gz'
        embeddings_file = self.docs_dir / 'embeddings.pkl.gz'
        index_file = self.docs_dir / 'index.json'
        
        # Save compressed docs
        with gzip.open(docs_file, 'wt') as f:
            json.dump(docs, f)
        
        # Save embeddings
        with gzip.open(embeddings_file, 'wb') as f:
            pickle.dump(self.doc_embeddings, f)
        
        # Save index
        with open(index_file, 'w') as f:
            json.dump(self.doc_index, f, indent=2)
        
        print(f"💾 Saved processed documentation to {self.docs_dir}")
    
    def load_processed_docs(self) -> bool:
        """Load previously processed documentation"""
        docs_file = self.docs_dir / 'processed_docs.json.gz'
        embeddings_file = self.docs_dir / 'embeddings.pkl.gz'
        index_file = self.docs_dir / 'index.json'
        
        if not all(f.exists() for f in [docs_file, embeddings_file, index_file]):
            return False
        
        try:
            # Load embeddings
            with gzip.open(embeddings_file, 'rb') as f:
                self.doc_embeddings = pickle.load(f)
            
            # Load index
            with open(index_file, 'r') as f:
                self.doc_index = json.load(f)
            
            print(f"✅ Loaded {len(self.doc_embeddings)} processed documents")
            return True
            
        except Exception as e:
            print(f"⚠️  Error loading processed docs: {e}")
            return False
    
    def semantic_search(self, query: str, top_k: int = 5) -> List[Dict]:
        """Perform semantic search on documentation"""
        if not self.doc_embeddings:
            return []
        
        query_embedding = self.vectorizer.vectorize(query)
        
        # Calculate similarities
        similarities = []
        for doc_id, doc_embedding in self.doc_embeddings.items():
            similarity = self._cosine_similarity(query_embedding, doc_embedding)
            similarities.append((doc_id, similarity))
        
        # Sort by similarity
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        # Return top results
        results = []
        for doc_id, similarity in similarities[:top_k]:
            if doc_id in self.doc_index:
                result = self.doc_index[doc_id].copy()
                result['doc_id'] = doc_id
                result['similarity'] = similarity
                results.append(result)
        
        return results
    
    def _cosine_similarity(self, vec1: Dict, vec2: Dict) -> float:
        """Calculate cosine similarity between two sparse vectors"""
        # Get intersection of keys
        common_keys = set(vec1.keys()) & set(vec2.keys())
        
        if not common_keys:
            return 0.0
        
        # Calculate dot product
        dot_product = sum(vec1[key] * vec2[key] for key in common_keys)
        
        # Calculate magnitudes
        mag1 = math.sqrt(sum(val ** 2 for val in vec1.values()))
        mag2 = math.sqrt(sum(val ** 2 for val in vec2.values()))
        
        if mag1 == 0 or mag2 == 0:
            return 0.0
        
        return dot_product / (mag1 * mag2)
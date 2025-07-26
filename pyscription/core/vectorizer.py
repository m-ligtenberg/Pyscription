"""
Simple TF-IDF vectorizer for text processing
Lightweight implementation optimized for documentation search
"""

import re
import math
from collections import defaultdict, Counter
from typing import Dict, List


class SimpleVectorizer:
    """Simple TF-IDF vectorizer for text"""
    
    def __init__(self):
        self.vocabulary = {}
        self.idf_scores = {}
        self.doc_count = 0
    
    def fit(self, documents: List[str]):
        """Fit the vectorizer on a collection of documents"""
        self.doc_count = len(documents)
        
        # Build vocabulary and document frequency
        doc_freq = defaultdict(int)
        
        for doc in documents:
            words = self._tokenize(doc)
            unique_words = set(words)
            
            for word in unique_words:
                doc_freq[word] += 1
                if word not in self.vocabulary:
                    self.vocabulary[word] = len(self.vocabulary)
        
        # Calculate IDF scores
        for word, freq in doc_freq.items():
            self.idf_scores[word] = math.log(self.doc_count / freq)
    
    def vectorize(self, document: str) -> Dict[str, float]:
        """Convert document to TF-IDF vector"""
        words = self._tokenize(document)
        word_counts = Counter(words)
        
        # Calculate TF-IDF
        vector = {}
        total_words = len(words)
        
        for word, count in word_counts.items():
            if word in self.vocabulary:
                tf = count / total_words
                idf = self.idf_scores.get(word, 0)
                vector[word] = tf * idf
        
        return vector
    
    def _tokenize(self, text: str) -> List[str]:
        """Simple tokenization"""
        # Convert to lowercase and extract words
        words = re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', text.lower())
        
        # Filter out very common words
        stop_words = {'the', 'is', 'at', 'which', 'on', 'and', 'or', 'but', 'in', 'with', 'a', 'an'}
        return [word for word in words if word not in stop_words and len(word) > 2]
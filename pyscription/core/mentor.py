"""
Main ML-Enhanced Pyscription with conversational AI
Integrates all components: documentation, patterns, ML analysis, and local AI
"""

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

from .document_processor import DocumentProcessor
from .pattern_discovery import PatternDiscovery
from .local_ai import LocalAIInterface


class MLEnhancedPyscription:
    """ML-enhanced Python assistant with conversational AI"""
    
    def __init__(self, data_dir: str = None):
        self.data_dir = Path(data_dir or Path.home() / '.pyscription')
        self.data_dir.mkdir(exist_ok=True)
        
        # Initialize core components
        self.doc_processor = DocumentProcessor(self.data_dir)
        self.pattern_discovery = PatternDiscovery(self.data_dir)
        self.ai_interface = LocalAIInterface()
        
        # Load existing data
        self.doc_processor.load_processed_docs()
        
        # Knowledge files
        self.interactions_file = self.data_dir / 'interactions.json'
        self.stats_file = self.data_dir / 'stats.json'
        
        self._init_files()
    
    def _init_files(self):
        """Initialize knowledge files"""
        if not self.interactions_file.exists():
            with open(self.interactions_file, 'w') as f:
                json.dump([], f)
        
        if not self.stats_file.exists():
            with open(self.stats_file, 'w') as f:
                json.dump({'queries': 0, 'successful_runs': 0}, f)
    
    def ingest_docs(self, docs_path: str) -> int:
        """Ingest Python documentation"""
        return self.doc_processor.ingest_documentation(docs_path)
    
    def smart_search(self, query: str) -> List[Dict]:
        """Intelligent search using ML"""
        # Semantic search in documentation
        doc_results = self.doc_processor.semantic_search(query, top_k=3)
        
        # Search in previous interactions
        interactions = self._load_interactions()
        interaction_results = self._search_interactions(query, interactions)
        
        # Combine results
        results = []
        
        for doc in doc_results:
            results.append({
                'type': 'documentation',
                'title': doc['filename'],
                'relevance': doc['similarity'],
                'content': f"Functions: {', '.join(doc['functions'][:5])}",
                'source': 'python_docs'
            })
        
        for interaction in interaction_results:
            results.append({
                'type': 'interaction',
                'title': interaction['query'][:50] + '...',
                'relevance': interaction['similarity'],
                'content': interaction['response'][:100] + '...',
                'source': 'previous_interaction'
            })
        
        return results
    
    def analyze_with_ml(self, code: str) -> Dict[str, Any]:
        """Analyze code using ML-discovered patterns"""
        # Basic analysis
        analysis = self._basic_code_analysis(code)
        
        # Pattern matching
        relevant_patterns = self.pattern_discovery.get_relevant_patterns(code)
        analysis['discovered_patterns'] = relevant_patterns
        
        # Documentation search for used functions
        doc_suggestions = self._get_doc_suggestions(code)
        analysis['doc_suggestions'] = doc_suggestions
        
        return analysis
    
    def chat_about_code(self, code: str = None, question: str = None) -> str:
        """Have a conversational chat about Python code"""
        if code:
            # Analyze code first to provide context
            ml_context = self.analyze_with_ml(code)
            
            if question:
                # Specific question about code
                response = self.ai_interface.analyze_and_chat(code, question)
            else:
                # General analysis
                response = self.ai_interface.analyze_and_chat(code)
            
            # Record interaction for learning
            self.add_interaction(
                f"Code analysis: {question or 'General analysis'}", 
                response
            )
            
            return response
        
        elif question:
            # General Python question without specific code
            # Build context from patterns and documentation
            ml_context = {
                'patterns': list(self.pattern_discovery.discovered_patterns.values())[:5],
                'available_docs': len(self.doc_processor.doc_embeddings) > 0
            }
            
            response = self.ai_interface.chat(question, ml_context)
            
            # Record interaction
            self.add_interaction(question, response)
            
            return response
        
        else:
            return "Please provide either code to analyze or a question to ask!"
    
    def generate_code_template(self, pattern_type: str, class_name: str = "GeneratedClass") -> str:
        """Generate code templates from patterns with AI enhancement"""
        # First, get the basic template
        template = self.pattern_discovery.generate_code_from_patterns(pattern_type, class_name)
        
        # Then ask AI to enhance it with explanations
        enhanced_question = f"""Here's a {pattern_type} pattern template I generated:

```python
{template}
```

Can you explain this pattern and suggest any improvements or variations that might be useful?"""
        
        ai_explanation = self.ai_interface.chat(enhanced_question)
        
        return f"{template}\n\n# AI Enhancement:\n# {ai_explanation}"
    
    def discover_patterns_from_history(self):
        """Discover patterns from interaction history"""
        interactions = self._load_interactions()
        code_samples = []
        
        for interaction in interactions:
            # Extract code from responses
            code_blocks = re.findall(r'```python\n(.*?)\n```', interaction.get('response', ''), re.DOTALL)
            code_samples.extend(code_blocks)
            
            # Also check if query contains code
            if 'def ' in interaction.get('query', '') or 'class ' in interaction.get('query', ''):
                code_samples.append(interaction['query'])
        
        if code_samples:
            self.pattern_discovery.discover_patterns(code_samples)
            return len(code_samples)
        
        return 0
    
    def get_ai_models(self) -> List[str]:
        """Get available AI models"""
        return self.ai_interface.get_available_models()
    
    def switch_ai_model(self, model_name: str) -> bool:
        """Switch AI model"""
        return self.ai_interface.switch_model(model_name)
    
    def clear_ai_history(self):
        """Clear AI conversation history"""
        self.ai_interface.clear_history()
    
    def _basic_code_analysis(self, code: str) -> Dict[str, Any]:
        """Basic code analysis"""
        import ast
        
        analysis = {
            'syntax_valid': True,
            'functions': [],
            'classes': [],
            'imports': [],
            'complexity': 1
        }
        
        try:
            tree = ast.parse(code)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    analysis['functions'].append(node.name)
                elif isinstance(node, ast.ClassDef):
                    analysis['classes'].append(node.name)
                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        analysis['imports'].append(alias.name)
                elif isinstance(node, (ast.If, ast.While, ast.For)):
                    analysis['complexity'] += 1
                    
        except SyntaxError as e:
            analysis['syntax_valid'] = False
            analysis['error'] = str(e)
        
        return analysis
    
    def _get_doc_suggestions(self, code: str) -> List[Dict]:
        """Get documentation suggestions for code"""
        import ast
        
        suggestions = []
        
        try:
            tree = ast.parse(code)
            
            # Extract function calls
            for node in ast.walk(tree):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                    func_name = node.func.id
                    # Search documentation for this function
                    search_results = self.doc_processor.semantic_search(func_name, top_k=2)
                    for result in search_results:
                        if result['similarity'] > 0.3:
                            suggestions.append({
                                'function': func_name,
                                'doc_file': result['filename'],
                                'relevance': result['similarity']
                            })
        
        except SyntaxError:
            pass
        
        return suggestions
    
    def _search_interactions(self, query: str, interactions: List[Dict]) -> List[Dict]:
        """Search previous interactions"""
        query_words = set(query.lower().split())
        results = []
        
        for interaction in interactions:
            interaction_words = set(interaction.get('query', '').lower().split())
            similarity = len(query_words & interaction_words) / len(query_words | interaction_words) if query_words | interaction_words else 0
            
            if similarity > 0.1:
                interaction['similarity'] = similarity
                results.append(interaction)
        
        return sorted(results, key=lambda x: x['similarity'], reverse=True)[:3]
    
    def _load_interactions(self) -> List[Dict]:
        """Load interaction history"""
        try:
            with open(self.interactions_file, 'r') as f:
                return json.load(f)
        except Exception:
            return []
    
    def add_interaction(self, query: str, response: str):
        """Add new interaction"""
        interactions = self._load_interactions()
        interactions.append({
            'query': query,
            'response': response,
            'timestamp': datetime.now().isoformat()
        })
        
        with open(self.interactions_file, 'w') as f:
            json.dump(interactions, f, indent=2)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get comprehensive system statistics"""
        return {
            'ml_stats': {
                'processed_documents': len(self.doc_processor.doc_embeddings),
                'discovered_patterns': len(self.pattern_discovery.discovered_patterns),
                'total_interactions': len(self._load_interactions()),
                'knowledge_base_size': sum(len(emb) for emb in self.doc_processor.doc_embeddings.values()) if self.doc_processor.doc_embeddings else 0
            },
            'ai_stats': {
                'available_models': self.get_ai_models(),
                'current_backend': type(self.ai_interface.backend).__name__,
                'conversation_length': len(self.ai_interface.conversation_history)
            }
        }
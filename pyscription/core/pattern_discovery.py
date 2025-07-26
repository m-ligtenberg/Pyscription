"""
Pattern discovery engine using ML and AST analysis
Detects design patterns, code smells, and naming conventions
"""

import ast
import json
import hashlib
from pathlib import Path
from typing import Dict, List, Tuple
from collections import defaultdict


class PatternDiscovery:
    """Machine learning-based pattern discovery in code"""
    
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self.patterns_file = data_dir / 'discovered_patterns.json'
        self.discovered_patterns = self._load_patterns()
    
    def discover_patterns(self, code_samples: List[str]) -> List[Dict]:
        """Discover common patterns in code samples"""
        if not code_samples:
            print("⚠️  No code samples provided for pattern discovery")
            return []
            
        print(f"🔍 Discovering code patterns from {len(code_samples)} samples...")
        
        patterns = []
        
        # AST-based pattern discovery
        ast_patterns = self._discover_ast_patterns(code_samples)
        patterns.extend(ast_patterns)
        
        # Text-based pattern discovery
        text_patterns = self._discover_text_patterns(code_samples)
        patterns.extend(text_patterns)
        
        # Import patterns
        import_patterns = self._discover_import_patterns(code_samples)
        patterns.extend(import_patterns)
        
        # Code smell detection
        code_smells = self._detect_code_smells(code_samples)
        patterns.extend(code_smells)
        
        # Design pattern detection
        design_patterns = self._detect_design_patterns(code_samples)
        patterns.extend(design_patterns)
        
        # Update discovered patterns
        for pattern in patterns:
            pattern_id = hashlib.md5(pattern['pattern'].encode()).hexdigest()[:10]
            self.discovered_patterns[pattern_id] = pattern
        
        try:
            self._save_patterns()
            print(f"✅ Discovered {len(patterns)} new patterns")
        except Exception as e:
            print(f"⚠️  Error saving patterns: {e}")
            
        return patterns
    
    def _detect_design_patterns(self, code_samples: List[str]) -> List[Dict]:
        """Detect common design patterns in code"""
        patterns = []
        
        for code in code_samples:
            try:
                tree = ast.parse(code)
                
                # Singleton pattern detection
                if self._is_singleton_pattern(tree):
                    patterns.append({
                        'type': 'design_pattern',
                        'pattern': 'Singleton',
                        'frequency': 1,
                        'description': 'Singleton design pattern detected'
                    })
                
                # Factory pattern detection
                if self._is_factory_pattern(tree):
                    patterns.append({
                        'type': 'design_pattern',
                        'pattern': 'Factory',
                        'frequency': 1,
                        'description': 'Factory design pattern detected'
                    })
                
                # Observer pattern detection
                if self._is_observer_pattern(tree):
                    patterns.append({
                        'type': 'design_pattern',
                        'pattern': 'Observer',
                        'frequency': 1,
                        'description': 'Observer design pattern detected'
                    })
                    
            except SyntaxError:
                continue
        
        return patterns
    
    def _is_singleton_pattern(self, tree) -> bool:
        """Detect Singleton pattern"""
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                # Look for __new__ method override
                for item in node.body:
                    if (isinstance(item, ast.FunctionDef) and 
                        item.name == '__new__' and
                        any(isinstance(stmt, ast.If) for stmt in item.body)):
                        return True
                        
                # Look for class variable _instance
                for item in node.body:
                    if (isinstance(item, ast.Assign) and
                        any(isinstance(target, ast.Name) and 
                            target.id.startswith('_instance') 
                            for target in item.targets)):
                        return True
        return False
    
    def _is_factory_pattern(self, tree) -> bool:
        """Detect Factory pattern"""
        factory_keywords = {'create', 'make', 'build', 'factory'}
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Method names suggesting factory
                if any(keyword in node.name.lower() for keyword in factory_keywords):
                    # Check if it returns different types based on conditions
                    has_conditional_return = False
                    for stmt in ast.walk(node):
                        if isinstance(stmt, ast.If) and any(isinstance(s, ast.Return) for s in ast.walk(stmt)):
                            has_conditional_return = True
                            break
                    if has_conditional_return:
                        return True
        return False
    
    def _is_observer_pattern(self, tree) -> bool:
        """Detect Observer pattern"""
        observer_methods = {'attach', 'detach', 'notify', 'subscribe', 'unsubscribe'}
        method_count = 0
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                for item in node.body:
                    if (isinstance(item, ast.FunctionDef) and
                        any(method in item.name.lower() for method in observer_methods)):
                        method_count += 1
                        
                # If class has multiple observer-like methods
                if method_count >= 2:
                    return True
        return False
    
    def _detect_code_smells(self, code_samples: List[str]) -> List[Dict]:
        """Detect code smells and anti-patterns"""
        smells = []
        
        for code in code_samples:
            try:
                tree = ast.parse(code)
                
                # Long method detection
                long_methods = self._detect_long_methods(tree)
                smells.extend(long_methods)
                
                # God class detection
                god_classes = self._detect_god_classes(tree)
                smells.extend(god_classes)
                
                # Deep nesting detection
                deep_nesting = self._detect_deep_nesting(tree)
                smells.extend(deep_nesting)
                
                # Too many parameters
                parameter_smells = self._detect_too_many_parameters(tree)
                smells.extend(parameter_smells)
                
            except SyntaxError:
                continue
        
        return smells
    
    def _detect_long_methods(self, tree) -> List[Dict]:
        """Detect methods that are too long"""
        smells = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Count lines of code (excluding comments and empty lines)
                loc = len([stmt for stmt in ast.walk(node) if isinstance(stmt, ast.stmt)])
                
                if loc > 20:  # Threshold for long method
                    smells.append({
                        'type': 'code_smell',
                        'pattern': f'long_method_{node.name}',
                        'frequency': 1,
                        'description': f'Long method "{node.name}" with {loc} statements (consider breaking down)'
                    })
        
        return smells
    
    def _detect_god_classes(self, tree) -> List[Dict]:
        """Detect classes with too many methods/responsibilities"""
        smells = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                method_count = sum(1 for item in node.body if isinstance(item, ast.FunctionDef))
                
                if method_count > 15:  # Threshold for god class
                    smells.append({
                        'type': 'code_smell',
                        'pattern': f'god_class_{node.name}',
                        'frequency': 1,
                        'description': f'God class "{node.name}" with {method_count} methods (consider splitting responsibilities)'
                    })
        
        return smells
    
    def _detect_deep_nesting(self, tree) -> List[Dict]:
        """Detect deeply nested code structures"""
        smells = []
        
        def get_nesting_depth(node, depth=0):
            max_depth = depth
            for child in ast.iter_child_nodes(node):
                if isinstance(child, (ast.If, ast.For, ast.While, ast.With, ast.Try)):
                    child_depth = get_nesting_depth(child, depth + 1)
                    max_depth = max(max_depth, child_depth)
                else:
                    child_depth = get_nesting_depth(child, depth)
                    max_depth = max(max_depth, child_depth)
            return max_depth
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                nesting_depth = get_nesting_depth(node)
                
                if nesting_depth > 4:  # Threshold for deep nesting
                    smells.append({
                        'type': 'code_smell',
                        'pattern': f'deep_nesting_{node.name}',
                        'frequency': 1,
                        'description': f'Deep nesting in "{node.name}" (depth: {nesting_depth}, consider extracting methods)'
                    })
        
        return smells
    
    def _detect_too_many_parameters(self, tree) -> List[Dict]:
        """Detect functions with too many parameters"""
        smells = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                param_count = len(node.args.args)
                
                if param_count > 6:  # Threshold for too many parameters
                    smells.append({
                        'type': 'code_smell',
                        'pattern': f'too_many_params_{node.name}',
                        'frequency': 1,
                        'description': f'Too many parameters in "{node.name}" ({param_count} params, consider parameter objects)'
                    })
        
        return smells
    
    def _discover_ast_patterns(self, code_samples: List[str]) -> List[Dict]:
        """Discover patterns using AST analysis"""
        patterns = []
        node_sequences = []
        
        for code in code_samples:
            try:
                tree = ast.parse(code)
                sequence = self._extract_node_sequence(tree)
                if len(sequence) > 2:
                    node_sequences.append(sequence)
            except SyntaxError:
                continue
        
        # Find common subsequences
        common_sequences = self._find_common_subsequences(node_sequences)
        
        for sequence, count in common_sequences.items():
            if count > 2:  # Appeared in at least 3 code samples
                patterns.append({
                    'type': 'ast_sequence',
                    'pattern': ' -> '.join(sequence),
                    'frequency': count,
                    'description': f'Common AST node sequence: {" -> ".join(sequence)}'
                })
        
        return patterns
    
    def _extract_node_sequence(self, tree) -> List[str]:
        """Extract sequence of AST node types"""
        sequence = []
        for node in ast.walk(tree):
            sequence.append(type(node).__name__)
        return sequence
    
    def _find_common_subsequences(self, sequences: List[List[str]], min_length: int = 3) -> Dict[Tuple, int]:
        """Find common subsequences in node sequences"""
        subsequence_counts = defaultdict(int)
        
        for sequence in sequences:
            # Generate all subsequences of minimum length
            for i in range(len(sequence) - min_length + 1):
                for j in range(i + min_length, len(sequence) + 1):
                    subseq = tuple(sequence[i:j])
                    if len(subseq) >= min_length:
                        subsequence_counts[subseq] += 1
        
        return dict(subsequence_counts)
    
    def _discover_text_patterns(self, code_samples: List[str]) -> List[Dict]:
        """Discover text-based patterns"""
        patterns = []
        
        # Function naming patterns
        function_names = []
        for code in code_samples:
            try:
                tree = ast.parse(code)
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        function_names.append(node.name)
            except SyntaxError:
                continue
        
        # Analyze naming conventions
        naming_patterns = self._analyze_naming_patterns(function_names)
        patterns.extend(naming_patterns)
        
        return patterns
    
    def _analyze_naming_patterns(self, names: List[str]) -> List[Dict]:
        """Analyze naming conventions in function names"""
        patterns = []
        
        if not names:
            return patterns
        
        # Check for common prefixes/suffixes
        prefixes = defaultdict(int)
        suffixes = defaultdict(int)
        
        for name in names:
            if '_' in name:
                parts = name.split('_')
                if len(parts) > 1:
                    prefixes[parts[0]] += 1
                    suffixes[parts[-1]] += 1
        
        # Report common prefixes
        for prefix, count in prefixes.items():
            if count > 2:
                patterns.append({
                    'type': 'naming_convention',
                    'pattern': f'function_prefix_{prefix}',
                    'frequency': count,
                    'description': f'Functions commonly start with "{prefix}_"'
                })
        
        return patterns
    
    def _discover_import_patterns(self, code_samples: List[str]) -> List[Dict]:
        """Discover common import patterns"""
        patterns = []
        import_combinations = defaultdict(int)
        
        for code in code_samples:
            try:
                tree = ast.parse(code)
                imports = []
                
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            imports.append(alias.name)
                    elif isinstance(node, ast.ImportFrom):
                        module = node.module or ''
                        for alias in node.names:
                            imports.append(f"{module}.{alias.name}")
                
                # Track combinations of imports
                if len(imports) > 1:
                    import_combo = tuple(sorted(imports))
                    import_combinations[import_combo] += 1
                    
            except SyntaxError:
                continue
        
        # Find commonly used together imports
        for combo, count in import_combinations.items():
            if count > 2 and len(combo) > 1:
                patterns.append({
                    'type': 'import_pattern',
                    'pattern': ', '.join(combo),
                    'frequency': count,
                    'description': f'Modules commonly imported together: {", ".join(combo)}'
                })
        
        return patterns
    
    def _load_patterns(self) -> Dict:
        """Load discovered patterns from disk"""
        if self.patterns_file.exists():
            try:
                with open(self.patterns_file, 'r') as f:
                    return json.load(f)
            except Exception:
                pass
        return {}
    
    def _save_patterns(self):
        """Save discovered patterns to disk"""
        with open(self.patterns_file, 'w') as f:
            json.dump(self.discovered_patterns, f, indent=2)
    
    def get_relevant_patterns(self, code: str) -> List[Dict]:
        """Get patterns relevant to the given code"""
        relevant = []
        
        try:
            tree = ast.parse(code)
            code_sequence = self._extract_node_sequence(tree)
            
            for pattern_id, pattern in self.discovered_patterns.items():
                if pattern['type'] == 'ast_sequence':
                    pattern_sequence = pattern['pattern'].split(' -> ')
                    if self._is_subsequence(pattern_sequence, code_sequence):
                        relevant.append(pattern)
                
        except SyntaxError:
            pass
        
        return relevant
    
    def _is_subsequence(self, pattern: List[str], sequence: List[str]) -> bool:
        """Check if pattern is a subsequence of sequence"""
        if len(pattern) > len(sequence):
            return False
        
        pattern_idx = 0
        for item in sequence:
            if pattern_idx < len(pattern) and item == pattern[pattern_idx]:
                pattern_idx += 1
        
        return pattern_idx == len(pattern)
    
    def generate_code_from_patterns(self, pattern_type: str, class_name: str = "GeneratedClass") -> str:
        """Generate code based on discovered patterns"""
        templates = {
            'singleton': self._generate_singleton_template,
            'factory': self._generate_factory_template,
            'observer': self._generate_observer_template
        }
        
        if pattern_type.lower() in templates:
            return templates[pattern_type.lower()](class_name)
        else:
            return f"# No template available for pattern type: {pattern_type}"
    
    def _generate_singleton_template(self, class_name: str) -> str:
        """Generate Singleton pattern template"""
        return f'''class {class_name}:
    """Singleton pattern implementation"""
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            # Initialize your singleton here
            self._data = {{}}
            self._initialized = True
    
    def get_instance(self):
        """Alternative way to get instance"""
        return self
    
    def reset(self):
        """Reset singleton state (useful for testing)"""
        self._data = {{}}
'''

    def _generate_factory_template(self, class_name: str) -> str:
        """Generate Factory pattern template"""
        return f'''class {class_name}Factory:
    """Factory pattern implementation"""
    
    @staticmethod
    def create_handler(handler_type: str):
        """Create handler based on type"""
        handlers = {{
            'json': JsonHandler,
            'xml': XmlHandler,
            'csv': CsvHandler,
        }}
        
        handler_class = handlers.get(handler_type.lower())
        if handler_class:
            return handler_class()
        else:
            raise ValueError(f"Unknown handler type: {{handler_type}}")
    
    @staticmethod
    def get_available_types():
        """Get list of available handler types"""
        return ['json', 'xml', 'csv']

class BaseHandler:
    """Base class for all handlers"""
    
    def handle(self, data):
        raise NotImplementedError("Subclasses must implement handle method")

class JsonHandler(BaseHandler):
    def handle(self, data):
        return f"Handling JSON data: {{data}}"

class XmlHandler(BaseHandler):
    def handle(self, data):
        return f"Handling XML data: {{data}}"

class CsvHandler(BaseHandler):
    def handle(self, data):
        return f"Handling CSV data: {{data}}"
'''

    def _generate_observer_template(self, class_name: str) -> str:
        """Generate Observer pattern template"""
        return f'''from abc import ABC, abstractmethod
from typing import List

class Observer(ABC):
    """Abstract observer interface"""
    
    @abstractmethod
    def update(self, subject: 'Subject') -> None:
        pass

class Subject:
    """Subject (observable) in observer pattern"""
    
    def __init__(self):
        self._observers: List[Observer] = []
        self._state = None
    
    def attach(self, observer: Observer) -> None:
        """Attach an observer"""
        if observer not in self._observers:
            self._observers.append(observer)
    
    def detach(self, observer: Observer) -> None:
        """Detach an observer"""
        if observer in self._observers:
            self._observers.remove(observer)
    
    def notify(self) -> None:
        """Notify all observers"""
        for observer in self._observers:
            observer.update(self)
    
    def set_state(self, state) -> None:
        """Change state and notify observers"""
        self._state = state
        self.notify()
    
    def get_state(self):
        """Get current state"""
        return self._state

class {class_name}(Subject):
    """Concrete subject implementation"""
    
    def __init__(self):
        super().__init__()
        self._data = {{}}
    
    def update_data(self, key, value):
        """Update data and notify observers"""
        self._data[key] = value
        self.set_state(self._data.copy())

class {class_name}Observer(Observer):
    """Concrete observer implementation"""
    
    def __init__(self, name: str):
        self._name = name
    
    def update(self, subject: Subject) -> None:
        """React to subject changes"""
        print(f"{{self._name}} received update: {{subject.get_state()}}")
'''
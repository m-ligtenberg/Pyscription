"""
Project-wide code analysis engine
Analyzes entire Python projects to understand architecture, patterns, and relationships
"""

import ast
import os
from pathlib import Path
from typing import Dict, List, Any, Set, Tuple
from collections import defaultdict, Counter
import json


class ProjectAnalyzer:
    """Analyzes entire Python projects for architecture patterns and relationships"""
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.analysis_cache = {}
        self.file_dependencies = defaultdict(set)
        self.class_hierarchy = defaultdict(list)
        self.function_calls = defaultdict(set)
        self.import_graph = defaultdict(set)
        
    def analyze_project(self) -> Dict[str, Any]:
        """Perform comprehensive project analysis"""
        print(f"🔍 Analyzing project: {self.project_path}")
        
        # Find all Python files
        python_files = self._find_python_files()
        print(f"📁 Found {len(python_files)} Python files")
        
        # Analyze each file
        file_analyses = {}
        for file_path in python_files:
            try:
                analysis = self._analyze_file(file_path)
                file_analyses[str(file_path.relative_to(self.project_path))] = analysis
            except Exception as e:
                print(f"⚠️  Error analyzing {file_path}: {e}")
        
        # Build project-wide insights
        project_analysis = {
            'files': file_analyses,
            'summary': self._build_project_summary(file_analyses),
            'architecture': self._analyze_architecture(file_analyses),
            'patterns': self._discover_project_patterns(file_analyses),
            'dependencies': self._analyze_dependencies(file_analyses),
            'recommendations': self._generate_recommendations(file_analyses)
        }
        
        return project_analysis
    
    def _find_python_files(self) -> List[Path]:
        """Find all Python files in the project"""
        python_files = []
        for file_path in self.project_path.rglob('*.py'):
            # Skip common directories
            if any(part.startswith('.') for part in file_path.parts):
                continue
            if any(part in ['__pycache__', 'venv', 'env', 'node_modules'] for part in file_path.parts):
                continue
            python_files.append(file_path)
        return python_files
    
    def _analyze_file(self, file_path: Path) -> Dict[str, Any]:
        """Analyze a single Python file"""
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        try:
            tree = ast.parse(content)
        except SyntaxError as e:
            return {'error': str(e), 'syntax_valid': False}
        
        analysis = {
            'syntax_valid': True,
            'lines_of_code': len([line for line in content.split('\n') if line.strip()]),
            'functions': self._extract_functions(tree),
            'classes': self._extract_classes(tree),
            'imports': self._extract_imports(tree),
            'complexity': self._calculate_complexity(tree),
            'docstrings': self._extract_docstrings(tree),
            'decorators': self._extract_decorators(tree),
            'async_usage': self._detect_async_usage(tree),
            'error_handling': self._analyze_error_handling(tree)
        }
        
        return analysis
    
    def _extract_functions(self, tree) -> List[Dict]:
        """Extract function information from AST"""
        functions = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions.append({
                    'name': node.name,
                    'args': len(node.args.args),
                    'is_async': isinstance(node, ast.AsyncFunctionDef),
                    'decorators': [self._get_decorator_name(d) for d in node.decorator_list],
                    'line_number': node.lineno,
                    'complexity': len([n for n in ast.walk(node) if isinstance(n, (ast.If, ast.For, ast.While))])
                })
        return functions
    
    def _extract_classes(self, tree) -> List[Dict]:
        """Extract class information from AST"""
        classes = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                methods = [n for n in node.body if isinstance(n, ast.FunctionDef)]
                classes.append({
                    'name': node.name,
                    'bases': [self._get_base_name(base) for base in node.bases],
                    'methods': len(methods),
                    'decorators': [self._get_decorator_name(d) for d in node.decorator_list],
                    'line_number': node.lineno,
                    'method_names': [m.name for m in methods]
                })
        return classes
    
    def _extract_imports(self, tree) -> List[Dict]:
        """Extract import information from AST"""
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append({
                        'type': 'import',
                        'module': alias.name,
                        'alias': alias.asname,
                        'line_number': node.lineno
                    })
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ''
                for alias in node.names:
                    imports.append({
                        'type': 'from_import',
                        'module': module,
                        'name': alias.name,
                        'alias': alias.asname,
                        'line_number': node.lineno
                    })
        return imports
    
    def _calculate_complexity(self, tree) -> int:
        """Calculate cyclomatic complexity"""
        complexity = 1  # Base complexity
        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.While, ast.For, ast.With, ast.Try)):
                complexity += 1
            elif isinstance(node, ast.BoolOp):
                complexity += len(node.values) - 1
        return complexity
    
    def _extract_docstrings(self, tree) -> Dict[str, int]:
        """Extract docstring information"""
        docstrings = {'module': 0, 'functions': 0, 'classes': 0}
        
        # Module docstring
        if (isinstance(tree.body[0], ast.Expr) and 
            isinstance(tree.body[0].value, ast.Constant) and 
            isinstance(tree.body[0].value.value, str)):
            docstrings['module'] = 1
        
        # Function and class docstrings
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if (node.body and isinstance(node.body[0], ast.Expr) and
                    isinstance(node.body[0].value, ast.Constant) and
                    isinstance(node.body[0].value.value, str)):
                    docstrings['functions'] += 1
            elif isinstance(node, ast.ClassDef):
                if (node.body and isinstance(node.body[0], ast.Expr) and
                    isinstance(node.body[0].value, ast.Constant) and
                    isinstance(node.body[0].value.value, str)):
                    docstrings['classes'] += 1
        
        return docstrings
    
    def _extract_decorators(self, tree) -> List[str]:
        """Extract decorator usage"""
        decorators = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                for decorator in node.decorator_list:
                    decorators.append(self._get_decorator_name(decorator))
        return decorators
    
    def _detect_async_usage(self, tree) -> Dict[str, int]:
        """Detect async/await usage"""
        async_usage = {'async_functions': 0, 'await_expressions': 0}
        for node in ast.walk(tree):
            if isinstance(node, ast.AsyncFunctionDef):
                async_usage['async_functions'] += 1
            elif isinstance(node, ast.Await):
                async_usage['await_expressions'] += 1
        return async_usage
    
    def _analyze_error_handling(self, tree) -> Dict[str, int]:
        """Analyze error handling patterns"""
        error_handling = {'try_blocks': 0, 'except_blocks': 0, 'finally_blocks': 0, 'raise_statements': 0}
        for node in ast.walk(tree):
            if isinstance(node, ast.Try):
                error_handling['try_blocks'] += 1
                error_handling['except_blocks'] += len(node.handlers)
                if node.finalbody:
                    error_handling['finally_blocks'] += 1
            elif isinstance(node, ast.Raise):
                error_handling['raise_statements'] += 1
        return error_handling
    
    def _get_decorator_name(self, decorator) -> str:
        """Get decorator name from AST node"""
        if isinstance(decorator, ast.Name):
            return decorator.id
        elif isinstance(decorator, ast.Attribute):
            return f"{decorator.value.id}.{decorator.attr}" if hasattr(decorator.value, 'id') else decorator.attr
        elif isinstance(decorator, ast.Call):
            return self._get_decorator_name(decorator.func)
        return str(decorator)
    
    def _get_base_name(self, base) -> str:
        """Get base class name from AST node"""
        if isinstance(base, ast.Name):
            return base.id
        elif isinstance(base, ast.Attribute):
            return f"{base.value.id}.{base.attr}" if hasattr(base.value, 'id') else base.attr
        return str(base)
    
    def _build_project_summary(self, file_analyses: Dict) -> Dict[str, Any]:
        """Build high-level project summary"""
        total_files = len(file_analyses)
        total_loc = sum(analysis.get('lines_of_code', 0) for analysis in file_analyses.values())
        total_functions = sum(len(analysis.get('functions', [])) for analysis in file_analyses.values())
        total_classes = sum(len(analysis.get('classes', [])) for analysis in file_analyses.values())
        
        # Average complexity
        complexities = [analysis.get('complexity', 1) for analysis in file_analyses.values()]
        avg_complexity = sum(complexities) / len(complexities) if complexities else 1
        
        return {
            'total_files': total_files,
            'total_lines_of_code': total_loc,
            'total_functions': total_functions,
            'total_classes': total_classes,
            'average_complexity': round(avg_complexity, 2),
            'files_with_errors': len([a for a in file_analyses.values() if not a.get('syntax_valid', True)])
        }
    
    def _analyze_architecture(self, file_analyses: Dict) -> Dict[str, Any]:
        """Analyze project architecture patterns"""
        # Identify common architectural patterns
        patterns = {
            'mvc_pattern': self._detect_mvc_pattern(file_analyses),
            'layered_architecture': self._detect_layered_architecture(file_analyses),
            'microservices_hints': self._detect_microservices_patterns(file_analyses),
            'design_patterns': self._detect_design_patterns(file_analyses)
        }
        
        return patterns
    
    def _discover_project_patterns(self, file_analyses: Dict) -> List[Dict]:
        """Discover common patterns across the project"""
        patterns = []
        
        # Naming conventions
        all_functions = []
        all_classes = []
        for analysis in file_analyses.values():
            all_functions.extend([f['name'] for f in analysis.get('functions', [])])
            all_classes.extend([c['name'] for c in analysis.get('classes', [])])
        
        # Function naming patterns
        if all_functions:
            naming_pattern = self._analyze_naming_convention(all_functions)
            if naming_pattern:
                patterns.append({
                    'type': 'naming_convention',
                    'category': 'functions',
                    'pattern': naming_pattern
                })
        
        # Class naming patterns
        if all_classes:
            naming_pattern = self._analyze_naming_convention(all_classes, is_class=True)
            if naming_pattern:
                patterns.append({
                    'type': 'naming_convention',
                    'category': 'classes',
                    'pattern': naming_pattern
                })
        
        # Import patterns
        import_patterns = self._analyze_import_patterns(file_analyses)
        patterns.extend(import_patterns)
        
        return patterns
    
    def _analyze_dependencies(self, file_analyses: Dict) -> Dict[str, Any]:
        """Analyze project dependencies"""
        external_imports = set()
        internal_imports = set()
        
        for analysis in file_analyses.values():
            for imp in analysis.get('imports', []):
                module = imp['module']
                if module.startswith('.') or any(file.startswith(module.replace('.', '/')) for file in file_analyses.keys()):
                    internal_imports.add(module)
                else:
                    external_imports.add(module)
        
        return {
            'external_dependencies': sorted(list(external_imports)),
            'internal_dependencies': sorted(list(internal_imports)),
            'dependency_count': len(external_imports),
            'coupling_score': len(internal_imports) / len(file_analyses) if file_analyses else 0
        }
    
    def _generate_recommendations(self, file_analyses: Dict) -> List[Dict]:
        """Generate improvement recommendations"""
        recommendations = []
        
        # Check for high complexity files
        high_complexity_files = [
            (filename, analysis) for filename, analysis in file_analyses.items()
            if analysis.get('complexity', 1) > 10
        ]
        
        if high_complexity_files:
            recommendations.append({
                'type': 'complexity',
                'priority': 'high',
                'title': 'High Complexity Files',
                'description': f"Found {len(high_complexity_files)} files with high complexity",
                'files': [filename for filename, _ in high_complexity_files[:5]],
                'suggestion': 'Consider breaking down complex functions and reducing nesting'
            })
        
        # Check for missing docstrings
        files_without_docs = [
            filename for filename, analysis in file_analyses.items()
            if sum(analysis.get('docstrings', {}).values()) == 0
        ]
        
        if len(files_without_docs) > len(file_analyses) * 0.5:
            recommendations.append({
                'type': 'documentation',
                'priority': 'medium',
                'title': 'Missing Documentation',
                'description': f"{len(files_without_docs)} files lack docstrings",
                'suggestion': 'Add docstrings to improve code maintainability'
            })
        
        # Check for error handling
        files_without_error_handling = [
            filename for filename, analysis in file_analyses.items()
            if analysis.get('error_handling', {}).get('try_blocks', 0) == 0 and
            len(analysis.get('functions', [])) > 3
        ]
        
        if files_without_error_handling:
            recommendations.append({
                'type': 'error_handling',
                'priority': 'medium',
                'title': 'Limited Error Handling',
                'description': f"{len(files_without_error_handling)} files lack error handling",
                'suggestion': 'Add try/except blocks for robust error handling'
            })
        
        return recommendations
    
    def _detect_mvc_pattern(self, file_analyses: Dict) -> bool:
        """Detect MVC architecture pattern"""
        mvc_indicators = ['model', 'view', 'controller', 'models', 'views', 'controllers']
        file_paths = list(file_analyses.keys())
        return any(indicator in path.lower() for path in file_paths for indicator in mvc_indicators)
    
    def _detect_layered_architecture(self, file_analyses: Dict) -> bool:
        """Detect layered architecture pattern"""
        layer_indicators = ['service', 'repository', 'dao', 'controller', 'handler', 'util']
        file_paths = list(file_analyses.keys())
        return any(indicator in path.lower() for path in file_paths for indicator in layer_indicators)
    
    def _detect_microservices_patterns(self, file_analyses: Dict) -> bool:
        """Detect microservices architecture hints"""
        microservice_indicators = ['api', 'service', 'handler', 'endpoint', 'router']
        file_paths = list(file_analyses.keys())
        return any(indicator in path.lower() for path in file_paths for indicator in microservice_indicators)
    
    def _detect_design_patterns(self, file_analyses: Dict) -> List[str]:
        """Detect design patterns in the codebase"""
        patterns = []
        
        for analysis in file_analyses.values():
            classes = analysis.get('classes', [])
            functions = analysis.get('functions', [])
            
            # Singleton pattern
            if any('__new__' in c.get('method_names', []) for c in classes):
                patterns.append('Singleton')
            
            # Factory pattern
            if any('factory' in f['name'].lower() or 'create' in f['name'].lower() for f in functions):
                patterns.append('Factory')
            
            # Observer pattern
            observer_methods = ['attach', 'detach', 'notify', 'subscribe', 'unsubscribe']
            if any(any(method in c.get('method_names', []) for method in observer_methods) for c in classes):
                patterns.append('Observer')
        
        return list(set(patterns))
    
    def _analyze_naming_convention(self, names: List[str], is_class: bool = False) -> str:
        """Analyze naming convention patterns"""
        if not names:
            return ""
        
        # Check for consistent patterns
        snake_case = sum(1 for name in names if '_' in name and name.islower())
        camel_case = sum(1 for name in names if name[0].islower() and any(c.isupper() for c in name[1:]))
        pascal_case = sum(1 for name in names if name[0].isupper() and any(c.isupper() for c in name[1:]))
        
        total = len(names)
        
        if snake_case / total > 0.7:
            return "snake_case (PEP 8 compliant)"
        elif camel_case / total > 0.7:
            return "camelCase (consider snake_case for Python)"
        elif pascal_case / total > 0.7:
            return "PascalCase" + (" (good for classes)" if is_class else " (consider snake_case for functions)")
        else:
            return "Mixed naming conventions (consider standardizing)"
    
    def _analyze_import_patterns(self, file_analyses: Dict) -> List[Dict]:
        """Analyze import patterns across the project"""
        patterns = []
        import_counter = Counter()
        
        for analysis in file_analyses.values():
            for imp in analysis.get('imports', []):
                import_counter[imp['module']] += 1
        
        # Find commonly used modules
        common_imports = [module for module, count in import_counter.most_common(10) if count > 1]
        
        if common_imports:
            patterns.append({
                'type': 'import_pattern',
                'category': 'common_dependencies',
                'pattern': f"Commonly used modules: {', '.join(common_imports[:5])}"
            })
        
        return patterns
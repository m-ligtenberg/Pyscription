"""
Advanced Security Vulnerability Pattern Recognition
Analyzes Python code for common security issues and vulnerabilities
"""

import ast
import re
import json
from typing import Dict, List, Any, Set, Tuple
from dataclasses import dataclass
from enum import Enum


class VulnerabilityLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class SecurityIssue:
    """Represents a security vulnerability or issue"""
    issue_type: str
    severity: VulnerabilityLevel
    description: str
    line_number: int
    code_snippet: str
    recommendation: str
    cwe_id: str = ""  # Common Weakness Enumeration ID
    owasp_category: str = ""


class SecurityPatternAnalyzer:
    """Analyzes Python code for security vulnerabilities"""
    
    def __init__(self):
        self.vulnerability_patterns = self._init_vulnerability_patterns()
        self.dangerous_imports = self._init_dangerous_imports()
        self.sql_injection_patterns = self._init_sql_patterns()
        self.command_injection_patterns = self._init_command_patterns()
        
    def analyze_code_security(self, code: str, filename: str = "") -> List[SecurityIssue]:
        """Analyze code for security vulnerabilities"""
        issues = []
        lines = code.split('\n')
        
        try:
            tree = ast.parse(code)
            
            # AST-based analysis
            issues.extend(self._analyze_dangerous_imports(tree, lines))
            issues.extend(self._analyze_hardcoded_secrets(tree, lines))
            issues.extend(self._analyze_sql_injection(tree, lines))
            issues.extend(self._analyze_command_injection(tree, lines))
            issues.extend(self._analyze_path_traversal(tree, lines))
            issues.extend(self._analyze_deserialization(tree, lines))
            issues.extend(self._analyze_random_usage(tree, lines))
            issues.extend(self._analyze_ssl_issues(tree, lines))
            
        except SyntaxError:
            pass  # Skip analysis for files with syntax errors
        
        # Regex-based analysis for patterns AST might miss
        issues.extend(self._analyze_regex_patterns(code, lines))
        
        return sorted(issues, key=lambda x: (x.severity.value, x.line_number))
    
    def _init_vulnerability_patterns(self) -> Dict[str, Dict]:
        """Initialize vulnerability detection patterns"""
        return {
            'hardcoded_password': {
                'patterns': [
                    r'password\s*=\s*["\'][^"\']+["\']',
                    r'pwd\s*=\s*["\'][^"\']+["\']',
                    r'secret\s*=\s*["\'][^"\']+["\']',
                    r'api_key\s*=\s*["\'][^"\']+["\']',
                    r'token\s*=\s*["\'][^"\']+["\']'
                ],
                'severity': VulnerabilityLevel.HIGH,
                'description': 'Hardcoded credentials detected',
                'recommendation': 'Use environment variables or secure credential management',
                'cwe_id': 'CWE-798',
                'owasp_category': 'A02:2021 – Cryptographic Failures'
            },
            'sql_injection': {
                'patterns': [
                    r'execute\(["\'].*%s.*["\']',
                    r'cursor\.execute\(["\'].*\+.*["\']',
                    r'query\s*=.*["\'].*%.*["\']',
                    r'SELECT.*\+.*FROM',
                    r'UPDATE.*\+.*SET',
                    r'DELETE.*\+.*FROM'
                ],
                'severity': VulnerabilityLevel.CRITICAL,
                'description': 'Potential SQL injection vulnerability',
                'recommendation': 'Use parameterized queries or ORM',
                'cwe_id': 'CWE-89',
                'owasp_category': 'A03:2021 – Injection'
            },
            'command_injection': {
                'patterns': [
                    r'os\.system\(["\'].*\+.*["\']',
                    r'subprocess\.call\(["\'].*\+.*["\']',
                    r'subprocess\.run\(["\'].*\+.*["\']',
                    r'os\.popen\(["\'].*\+.*["\']'
                ],
                'severity': VulnerabilityLevel.CRITICAL,
                'description': 'Potential command injection vulnerability',
                'recommendation': 'Sanitize input and use subprocess with list arguments',
                'cwe_id': 'CWE-78',
                'owasp_category': 'A03:2021 – Injection'
            }
        }
    
    def _init_dangerous_imports(self) -> Dict[str, Dict]:
        """Initialize dangerous import patterns"""
        return {
            'pickle': {
                'severity': VulnerabilityLevel.HIGH,
                'description': 'Pickle module can execute arbitrary code during deserialization',
                'recommendation': 'Use json or other safe serialization formats',
                'cwe_id': 'CWE-502'
            },
            'eval': {
                'severity': VulnerabilityLevel.CRITICAL,
                'description': 'eval() can execute arbitrary code',
                'recommendation': 'Avoid eval() or use ast.literal_eval() for safe evaluation',
                'cwe_id': 'CWE-95'
            },
            'exec': {
                'severity': VulnerabilityLevel.CRITICAL,
                'description': 'exec() can execute arbitrary code', 
                'recommendation': 'Avoid exec() or carefully validate input',
                'cwe_id': 'CWE-95'
            }
        }
    
    def _init_sql_patterns(self) -> List[str]:
        """Initialize SQL injection patterns"""
        return [
            r'SELECT\s+.*\s+FROM\s+.*\+',
            r'INSERT\s+INTO\s+.*\+',
            r'UPDATE\s+.*\s+SET\s+.*\+',
            r'DELETE\s+FROM\s+.*\+',
            r'cursor\.execute\s*\(\s*["\'].*%s',
            r'query\s*=\s*.*["\'].*%.*["\']'
        ]
    
    def _init_command_patterns(self) -> List[str]:
        """Initialize command injection patterns"""
        return [
            r'os\.system\s*\(\s*.*\+',
            r'subprocess\.(call|run|Popen)\s*\(\s*.*\+',
            r'os\.popen\s*\(\s*.*\+',
            r'commands\.(getoutput|getstatusoutput)\s*\(\s*.*\+'
        ]
    
    def _analyze_dangerous_imports(self, tree: ast.AST, lines: List[str]) -> List[SecurityIssue]:
        """Analyze for dangerous imports and function usage"""
        issues = []
        
        for node in ast.walk(tree):
            # Check for dangerous imports
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name in self.dangerous_imports:
                        danger_info = self.dangerous_imports[alias.name]
                        issues.append(SecurityIssue(
                            issue_type="dangerous_import",
                            severity=danger_info['severity'],
                            description=f"Dangerous import: {alias.name} - {danger_info['description']}",
                            line_number=node.lineno,
                            code_snippet=lines[node.lineno - 1] if node.lineno <= len(lines) else "",
                            recommendation=danger_info['recommendation'],
                            cwe_id=danger_info['cwe_id']
                        ))
            
            # Check for dangerous function calls
            elif isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    if node.func.id in ['eval', 'exec']:
                        danger_info = self.dangerous_imports[node.func.id]
                        issues.append(SecurityIssue(
                            issue_type="dangerous_function",
                            severity=danger_info['severity'],
                            description=f"Dangerous function: {node.func.id} - {danger_info['description']}",
                            line_number=node.lineno,
                            code_snippet=lines[node.lineno - 1] if node.lineno <= len(lines) else "",
                            recommendation=danger_info['recommendation'],
                            cwe_id=danger_info['cwe_id']
                        ))
        
        return issues
    
    def _analyze_hardcoded_secrets(self, tree: ast.AST, lines: List[str]) -> List[SecurityIssue]:
        """Analyze for hardcoded secrets and credentials"""
        issues = []
        secret_keywords = ['password', 'pwd', 'secret', 'api_key', 'token', 'key', 'auth']
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        var_name = target.id.lower()
                        if any(keyword in var_name for keyword in secret_keywords):
                            if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                                if len(node.value.value) > 3:  # Ignore very short strings
                                    issues.append(SecurityIssue(
                                        issue_type="hardcoded_secret",
                                        severity=VulnerabilityLevel.HIGH,
                                        description=f"Hardcoded credential in variable '{target.id}'",
                                        line_number=node.lineno,
                                        code_snippet=lines[node.lineno - 1] if node.lineno <= len(lines) else "",
                                        recommendation="Use environment variables or secure credential management",
                                        cwe_id="CWE-798",
                                        owasp_category="A02:2021 – Cryptographic Failures"
                                    ))
        
        return issues
    
    def _analyze_sql_injection(self, tree: ast.AST, lines: List[str]) -> List[SecurityIssue]:
        """Analyze for SQL injection vulnerabilities"""
        issues = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                # Check for cursor.execute with string formatting
                if (isinstance(node.func, ast.Attribute) and 
                    node.func.attr == 'execute'):
                    for arg in node.args:
                        if isinstance(arg, ast.BinOp) and isinstance(arg.op, ast.Mod):
                            issues.append(SecurityIssue(
                                issue_type="sql_injection",
                                severity=VulnerabilityLevel.CRITICAL,
                                description="SQL query using string formatting - potential injection vulnerability",
                                line_number=node.lineno,
                                code_snippet=lines[node.lineno - 1] if node.lineno <= len(lines) else "",
                                recommendation="Use parameterized queries with ? placeholders",
                                cwe_id="CWE-89",
                                owasp_category="A03:2021 – Injection"
                            ))
        
        return issues
    
    def _analyze_command_injection(self, tree: ast.AST, lines: List[str]) -> List[SecurityIssue]:
        """Analyze for command injection vulnerabilities"""
        issues = []
        dangerous_functions = ['system', 'popen', 'call', 'run', 'Popen']
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                func_name = None
                
                if isinstance(node.func, ast.Name):
                    func_name = node.func.id
                elif isinstance(node.func, ast.Attribute):
                    func_name = node.func.attr
                
                if func_name in dangerous_functions:
                    # Check if arguments use string concatenation
                    for arg in node.args:
                        if isinstance(arg, ast.BinOp) and isinstance(arg.op, ast.Add):
                            issues.append(SecurityIssue(
                                issue_type="command_injection",
                                severity=VulnerabilityLevel.CRITICAL,
                                description=f"Command execution with string concatenation in {func_name}()",
                                line_number=node.lineno,
                                code_snippet=lines[node.lineno - 1] if node.lineno <= len(lines) else "",
                                recommendation="Use subprocess with list arguments and validate input",
                                cwe_id="CWE-78",
                                owasp_category="A03:2021 – Injection"
                            ))
        
        return issues
    
    def _analyze_path_traversal(self, tree: ast.AST, lines: List[str]) -> List[SecurityIssue]:
        """Analyze for path traversal vulnerabilities"""
        issues = []
        file_functions = ['open', 'read', 'write', 'remove', 'unlink']
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name) and node.func.id in file_functions:
                    for arg in node.args:
                        if isinstance(arg, ast.BinOp):
                            issues.append(SecurityIssue(
                                issue_type="path_traversal",
                                severity=VulnerabilityLevel.MEDIUM,
                                description=f"File operation with dynamic path in {node.func.id}()",
                                line_number=node.lineno,
                                code_snippet=lines[node.lineno - 1] if node.lineno <= len(lines) else "",
                                recommendation="Validate and sanitize file paths, use os.path.basename()",
                                cwe_id="CWE-22",
                                owasp_category="A01:2021 – Broken Access Control"
                            ))
        
        return issues
    
    def _analyze_deserialization(self, tree: ast.AST, lines: List[str]) -> List[SecurityIssue]:
        """Analyze for unsafe deserialization"""
        issues = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if (isinstance(node.func, ast.Attribute) and 
                    node.func.attr in ['loads', 'load'] and
                    isinstance(node.func.value, ast.Name) and
                    node.func.value.id == 'pickle'):
                    issues.append(SecurityIssue(
                        issue_type="unsafe_deserialization",
                        severity=VulnerabilityLevel.CRITICAL,
                        description="Unsafe pickle deserialization - can execute arbitrary code",
                        line_number=node.lineno,
                        code_snippet=lines[node.lineno - 1] if node.lineno <= len(lines) else "",
                        recommendation="Use json or other safe serialization formats",
                        cwe_id="CWE-502",
                        owasp_category="A08:2021 – Software and Data Integrity Failures"
                    ))
        
        return issues
    
    def _analyze_random_usage(self, tree: ast.AST, lines: List[str]) -> List[SecurityIssue]:
        """Analyze for weak random number generation"""
        issues = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if (isinstance(node.func, ast.Attribute) and 
                    isinstance(node.func.value, ast.Name) and
                    node.func.value.id == 'random'):
                    issues.append(SecurityIssue(
                        issue_type="weak_random",
                        severity=VulnerabilityLevel.MEDIUM,
                        description="Using random module for potentially security-sensitive operations",
                        line_number=node.lineno,
                        code_snippet=lines[node.lineno - 1] if node.lineno <= len(lines) else "",
                        recommendation="Use secrets module for cryptographically secure random numbers",
                        cwe_id="CWE-338",
                        owasp_category="A02:2021 – Cryptographic Failures"
                    ))
        
        return issues
    
    def _analyze_ssl_issues(self, tree: ast.AST, lines: List[str]) -> List[SecurityIssue]:
        """Analyze for SSL/TLS security issues"""
        issues = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                # Check for SSL context with verification disabled
                if (isinstance(node.func, ast.Attribute) and 
                    node.func.attr in ['create_default_context', 'create_unverified_context']):
                    if node.func.attr == 'create_unverified_context':
                        issues.append(SecurityIssue(
                            issue_type="ssl_verification_disabled",
                            severity=VulnerabilityLevel.HIGH,
                            description="SSL certificate verification disabled",
                            line_number=node.lineno,
                            code_snippet=lines[node.lineno - 1] if node.lineno <= len(lines) else "",
                            recommendation="Use create_default_context() and enable certificate verification",
                            cwe_id="CWE-295",
                            owasp_category="A02:2021 – Cryptographic Failures"
                        ))
        
        return issues
    
    def _analyze_regex_patterns(self, code: str, lines: List[str]) -> List[SecurityIssue]:
        """Analyze code using regex patterns for issues AST can't catch"""
        issues = []
        
        for pattern_name, pattern_info in self.vulnerability_patterns.items():
            for pattern in pattern_info['patterns']:
                for i, line in enumerate(lines, 1):
                    if re.search(pattern, line, re.IGNORECASE):
                        issues.append(SecurityIssue(
                            issue_type=pattern_name,
                            severity=pattern_info['severity'],
                            description=pattern_info['description'],
                            line_number=i,
                            code_snippet=line.strip(),
                            recommendation=pattern_info['recommendation'],
                            cwe_id=pattern_info.get('cwe_id', ''),
                            owasp_category=pattern_info.get('owasp_category', '')
                        ))
        
        return issues
    
    def generate_security_report(self, issues: List[SecurityIssue], filename: str = "") -> Dict[str, Any]:
        """Generate a comprehensive security report"""
        if not issues:
            return {
                'filename': filename,
                'total_issues': 0,
                'risk_score': 0,
                'summary': 'No security issues detected',
                'issues_by_severity': {},
                'recommendations': []
            }
        
        # Count issues by severity
        severity_counts = {}
        for issue in issues:
            severity = issue.severity.value
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
        
        # Calculate risk score (weighted by severity)
        risk_weights = {'low': 1, 'medium': 3, 'high': 7, 'critical': 15}
        risk_score = sum(severity_counts.get(sev, 0) * weight for sev, weight in risk_weights.items())
        
        # Group issues by type
        issues_by_type = {}
        for issue in issues:
            issue_type = issue.issue_type
            if issue_type not in issues_by_type:
                issues_by_type[issue_type] = []
            issues_by_type[issue_type].append({
                'line': issue.line_number,
                'description': issue.description,
                'severity': issue.severity.value,
                'code_snippet': issue.code_snippet,
                'recommendation': issue.recommendation,
                'cwe_id': issue.cwe_id,
                'owasp_category': issue.owasp_category
            })
        
        # Generate top recommendations
        recommendations = list(set(issue.recommendation for issue in issues))[:5]
        
        return {
            'filename': filename,
            'total_issues': len(issues),
            'risk_score': risk_score,
            'severity_counts': severity_counts,
            'issues_by_type': issues_by_type,
            'recommendations': recommendations,
            'summary': f"Found {len(issues)} security issues with risk score {risk_score}"
        }


# Integration with the main Pyscription system
def integrate_security_analysis(mentor_instance):
    """Integrate security analysis into the main Pyscription system"""
    security_analyzer = SecurityPatternAnalyzer()
    
    def analyze_code_security(code: str, filename: str = "") -> Dict[str, Any]:
        """Add security analysis capability to mentor"""
        issues = security_analyzer.analyze_code_security(code, filename)
        return security_analyzer.generate_security_report(issues, filename)
    
    # Add as method to mentor instance
    mentor_instance.analyze_code_security = analyze_code_security
    return mentor_instance
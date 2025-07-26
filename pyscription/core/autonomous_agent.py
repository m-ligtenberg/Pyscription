"""
Autonomous Python Development Agent
A self-directed agent that can analyze, plan, and execute code improvements autonomously
"""

import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass
from enum import Enum

from .mentor import MLEnhancedPyscription
from .project_analyzer import ProjectAnalyzer


class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress" 
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"


class TaskPriority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class Task:
    """Represents a single autonomous task"""
    id: str
    title: str
    description: str
    task_type: str  # 'analysis', 'refactor', 'generate', 'optimize', 'document'
    priority: TaskPriority
    status: TaskStatus
    file_targets: List[str]  # Files this task operates on
    prerequisites: List[str]  # Task IDs that must complete first
    estimated_time: int  # Estimated minutes
    progress: float = 0.0  # 0.0 to 1.0
    error_message: Optional[str] = None
    results: Optional[Dict[str, Any]] = None
    created_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


class AutonomousPythonAgent:
    """Autonomous agent for Python development tasks"""
    
    def __init__(self, project_path: str, mentor: MLEnhancedPyscription = None):
        self.project_path = Path(project_path)
        self.mentor = mentor or MLEnhancedPyscription()
        self.project_analyzer = ProjectAnalyzer(str(self.project_path))
        
        # Agent state
        self.tasks: Dict[str, Task] = {}
        self.execution_log: List[Dict] = []
        self.agent_memory: Dict[str, Any] = {}
        self.is_running = False
        
        # Agent capabilities
        self.capabilities = {
            'code_analysis': True,
            'code_refactoring': True, 
            'code_generation': True,
            'documentation_generation': True,
            'pattern_detection': True,
            'architecture_analysis': True,
            'autonomous_planning': True,
            'multi_file_operations': True
        }
        
        # Initialize agent memory
        self._load_agent_state()
    
    def analyze_and_plan(self, goal: str) -> List[Task]:
        """Analyze project and create autonomous plan to achieve goal"""
        print(f"🤖 Agent analyzing project to achieve: {goal}")
        
        # Step 1: Comprehensive project analysis
        project_analysis = self.project_analyzer.analyze_project()
        self.agent_memory['last_analysis'] = project_analysis
        
        # Step 2: Generate task plan based on goal and analysis
        planned_tasks = self._generate_task_plan(goal, project_analysis)
        
        # Step 3: Add tasks to execution queue
        for task in planned_tasks:
            self.add_task(task)
        
        print(f"📋 Created {len(planned_tasks)} autonomous tasks")
        return planned_tasks
    
    def _generate_task_plan(self, goal: str, analysis: Dict[str, Any]) -> List[Task]:
        """Generate a comprehensive task plan based on goal and project analysis"""
        tasks = []
        task_id_counter = int(time.time())
        
        goal_lower = goal.lower()
        
        # Different planning strategies based on goal type
        if any(word in goal_lower for word in ['refactor', 'improve', 'clean']):
            tasks.extend(self._plan_refactoring_tasks(analysis, task_id_counter))
        elif any(word in goal_lower for word in ['document', 'docs', 'docstring']):
            tasks.extend(self._plan_documentation_tasks(analysis, task_id_counter))
        elif any(word in goal_lower for word in ['optimize', 'performance', 'speed']):
            tasks.extend(self._plan_optimization_tasks(analysis, task_id_counter))
        elif any(word in goal_lower for word in ['test', 'testing', 'coverage']):
            tasks.extend(self._plan_testing_tasks(analysis, task_id_counter))
        elif any(word in goal_lower for word in ['pattern', 'design', 'architecture']):
            tasks.extend(self._plan_architecture_tasks(analysis, task_id_counter))
        else:
            # General improvement plan
            tasks.extend(self._plan_general_improvement_tasks(analysis, task_id_counter))
        
        return tasks
    
    def _plan_refactoring_tasks(self, analysis: Dict, counter: int) -> List[Task]:
        """Plan refactoring tasks based on analysis"""
        tasks = []
        
        # High complexity files
        for filename, file_analysis in analysis['files'].items():
            if file_analysis.get('complexity', 1) > 10:
                tasks.append(Task(
                    id=f"refactor_{counter}_{len(tasks)}",
                    title=f"Refactor high complexity in {filename}",
                    description=f"Break down complex functions and reduce nesting in {filename}",
                    task_type="refactor",
                    priority=TaskPriority.HIGH,
                    status=TaskStatus.PENDING,
                    file_targets=[filename],
                    prerequisites=[],
                    estimated_time=30,
                    created_at=datetime.now()
                ))
        
        # Long methods needing extraction
        for filename, file_analysis in analysis['files'].items():
            long_functions = [f for f in file_analysis.get('functions', []) if f.get('complexity', 0) > 5]
            if long_functions:
                tasks.append(Task(
                    id=f"extract_methods_{counter}_{len(tasks)}",
                    title=f"Extract methods in {filename}",
                    description=f"Extract {len(long_functions)} complex functions into smaller methods",
                    task_type="refactor", 
                    priority=TaskPriority.MEDIUM,
                    status=TaskStatus.PENDING,
                    file_targets=[filename],
                    prerequisites=[],
                    estimated_time=20,
                    created_at=datetime.now()
                ))
        
        return tasks
    
    def _plan_documentation_tasks(self, analysis: Dict, counter: int) -> List[Task]:
        """Plan documentation tasks"""
        tasks = []
        
        for filename, file_analysis in analysis['files'].items():
            docstrings = file_analysis.get('docstrings', {})
            functions = file_analysis.get('functions', [])
            classes = file_analysis.get('classes', [])
            
            # Missing function docstrings
            if len(functions) > docstrings.get('functions', 0):
                tasks.append(Task(
                    id=f"doc_functions_{counter}_{len(tasks)}",
                    title=f"Add function docstrings to {filename}",
                    description=f"Add docstrings to {len(functions) - docstrings.get('functions', 0)} functions",
                    task_type="document",
                    priority=TaskPriority.MEDIUM,
                    status=TaskStatus.PENDING,
                    file_targets=[filename],
                    prerequisites=[],
                    estimated_time=15,
                    created_at=datetime.now()
                ))
            
            # Missing class docstrings
            if len(classes) > docstrings.get('classes', 0):
                tasks.append(Task(
                    id=f"doc_classes_{counter}_{len(tasks)}",
                    title=f"Add class docstrings to {filename}",
                    description=f"Add docstrings to {len(classes) - docstrings.get('classes', 0)} classes",
                    task_type="document",
                    priority=TaskPriority.MEDIUM,
                    status=TaskStatus.PENDING,
                    file_targets=[filename],
                    prerequisites=[],
                    estimated_time=10,
                    created_at=datetime.now()
                ))
        
        return tasks
    
    def _plan_optimization_tasks(self, analysis: Dict, counter: int) -> List[Task]:
        """Plan optimization tasks"""
        tasks = []
        
        # Find performance bottlenecks
        for filename, file_analysis in analysis['files'].items():
            functions = file_analysis.get('functions', [])
            
            # Functions with high complexity might need optimization
            complex_functions = [f for f in functions if f.get('complexity', 0) > 8]
            if complex_functions:
                tasks.append(Task(
                    id=f"optimize_{counter}_{len(tasks)}",
                    title=f"Optimize performance in {filename}",
                    description=f"Optimize {len(complex_functions)} complex functions for better performance",
                    task_type="optimize",
                    priority=TaskPriority.MEDIUM,
                    status=TaskStatus.PENDING,
                    file_targets=[filename],
                    prerequisites=[],
                    estimated_time=25,
                    created_at=datetime.now()
                ))
        
        return tasks
    
    def _plan_testing_tasks(self, analysis: Dict, counter: int) -> List[Task]:
        """Plan testing tasks"""
        tasks = []
        
        # Look for files without corresponding test files
        python_files = list(analysis['files'].keys())
        test_files = [f for f in python_files if 'test' in f.lower()]
        
        for filename in python_files:
            if 'test' not in filename.lower():
                # Check if test file exists
                potential_test_names = [
                    f"test_{filename}",
                    f"tests/test_{filename}",
                    f"{filename.replace('.py', '_test.py')}"
                ]
                
                if not any(test_name in python_files for test_name in potential_test_names):
                    tasks.append(Task(
                        id=f"create_tests_{counter}_{len(tasks)}",
                        title=f"Create tests for {filename}",
                        description=f"Generate unit tests for functions and classes in {filename}",
                        task_type="generate",
                        priority=TaskPriority.MEDIUM,
                        status=TaskStatus.PENDING,
                        file_targets=[filename],
                        prerequisites=[],
                        estimated_time=30,
                        created_at=datetime.now()
                    ))
        
        return tasks
    
    def _plan_architecture_tasks(self, analysis: Dict, counter: int) -> List[Task]:
        """Plan architecture improvement tasks"""
        tasks = []
        
        # Analyze for design pattern opportunities
        architecture = analysis.get('architecture', {})
        
        # If no clear architecture pattern detected, suggest improvements
        if not any(architecture.values()):
            tasks.append(Task(
                id=f"architect_{counter}_{len(tasks)}",
                title="Improve project architecture",
                description="Analyze and suggest architectural improvements for better organization",
                task_type="analysis",
                priority=TaskPriority.HIGH,
                status=TaskStatus.PENDING,
                file_targets=list(analysis['files'].keys())[:5],  # Focus on main files
                prerequisites=[],
                estimated_time=45,
                created_at=datetime.now()
            ))
        
        return tasks
    
    def _plan_general_improvement_tasks(self, analysis: Dict, counter: int) -> List[Task]:
        """Plan general improvement tasks"""
        tasks = []
        
        # Based on recommendations from project analysis
        recommendations = analysis.get('recommendations', [])
        
        for i, rec in enumerate(recommendations):
            tasks.append(Task(
                id=f"improve_{counter}_{i}",
                title=rec['title'],
                description=rec['description'] + " - " + rec['suggestion'],
                task_type="refactor" if rec['type'] == 'complexity' else "document",
                priority=TaskPriority.HIGH if rec['priority'] == 'high' else TaskPriority.MEDIUM,
                status=TaskStatus.PENDING,
                file_targets=rec.get('files', [])[:3],  # Limit to first 3 files
                prerequisites=[],
                estimated_time=20,
                created_at=datetime.now()
            ))
        
        return tasks
    
    def add_task(self, task: Task):
        """Add a task to the execution queue"""
        self.tasks[task.id] = task
        self._log_action(f"Added task: {task.title}")
    
    def execute_next_task(self) -> Optional[Task]:
        """Execute the next ready task"""
        # Find highest priority ready task
        ready_tasks = [
            task for task in self.tasks.values()
            if task.status == TaskStatus.PENDING and
            all(self.tasks.get(prereq_id, Task("", "", "", "", TaskPriority.LOW, TaskStatus.FAILED, [], [])).status == TaskStatus.COMPLETED 
                for prereq_id in task.prerequisites)
        ]
        
        if not ready_tasks:
            return None
        
        # Sort by priority and creation time
        ready_tasks.sort(key=lambda t: (t.priority.value, t.created_at))
        next_task = ready_tasks[0]
        
        return self._execute_task(next_task)
    
    def _execute_task(self, task: Task) -> Task:
        """Execute a specific task"""
        print(f"🚀 Executing: {task.title}")
        task.status = TaskStatus.IN_PROGRESS
        task.started_at = datetime.now()
        
        try:
            # Execute based on task type
            if task.task_type == "analysis":
                task.results = self._execute_analysis_task(task)
            elif task.task_type == "refactor":
                task.results = self._execute_refactor_task(task)
            elif task.task_type == "document":
                task.results = self._execute_documentation_task(task)
            elif task.task_type == "optimize":
                task.results = self._execute_optimization_task(task)
            elif task.task_type == "generate":
                task.results = self._execute_generation_task(task)
            else:
                raise ValueError(f"Unknown task type: {task.task_type}")
            
            task.status = TaskStatus.COMPLETED
            task.progress = 1.0
            task.completed_at = datetime.now()
            
            print(f"✅ Completed: {task.title}")
            self._log_action(f"Completed task: {task.title}")
            
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error_message = str(e)
            print(f"❌ Failed: {task.title} - {e}")
            self._log_action(f"Failed task: {task.title} - {e}")
        
        self._save_agent_state()
        return task
    
    def _execute_analysis_task(self, task: Task) -> Dict[str, Any]:
        """Execute analysis task using ML capabilities"""
        results = {}
        
        for file_path in task.file_targets:
            full_path = self.project_path / file_path
            if full_path.exists():
                with open(full_path, 'r') as f:
                    code = f.read()
                
                # Use mentor's ML analysis
                analysis = self.mentor.analyze_with_ml(code)
                results[file_path] = analysis
        
        return results
    
    def _execute_refactor_task(self, task: Task) -> Dict[str, Any]:
        """Execute refactoring task with intelligent code editing"""
        results = {'actions_taken': [], 'files_modified': [], 'refactoring_applied': []}
        
        for file_path in task.file_targets:
            full_path = self.project_path / file_path
            if full_path.exists():
                with open(full_path, 'r') as f:
                    original_code = f.read()
                
                # Analyze code complexity and patterns
                analysis = self.mentor.analyze_with_ml(original_code)
                
                # Apply intelligent refactoring based on analysis
                refactored_code = self._apply_intelligent_refactoring(original_code, analysis)
                
                if refactored_code != original_code:
                    # Create backup
                    backup_path = full_path.with_suffix(f'.py.backup.{int(time.time())}')
                    with open(backup_path, 'w') as f:
                        f.write(original_code)
                    
                    # Apply refactoring
                    with open(full_path, 'w') as f:
                        f.write(refactored_code)
                    
                    results['files_modified'].append(file_path)
                    results['refactoring_applied'].append(f"Applied complexity reduction to {file_path}")
                    results['backup_created'] = str(backup_path)
                
                # Generate additional AI suggestions
                refactor_suggestions = self.mentor.chat_about_code(
                    code=refactored_code,
                    question="Analyze this refactored code for any remaining improvements. What design patterns could be applied?"
                )
                
                results['actions_taken'].append(f"Intelligently refactored {file_path}")
                results['ai_suggestions'] = refactor_suggestions
        
        return results
    
    def _apply_intelligent_refactoring(self, code: str, analysis: Dict) -> str:
        """Apply intelligent refactoring based on code analysis"""
        import ast
        import re
        
        try:
            tree = ast.parse(code)
        except SyntaxError:
            return code  # Return original if can't parse
        
        lines = code.split('\n')
        refactored_lines = lines.copy()
        
        # Extract long functions that need refactoring
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if node.end_lineno - node.lineno > 20:  # Long function
                    # Add comment suggesting refactoring
                    comment_line = node.lineno - 1
                    if comment_line < len(refactored_lines):
                        indent = len(refactored_lines[comment_line]) - len(refactored_lines[comment_line].lstrip())
                        refactor_comment = " " * indent + "# TODO: Consider breaking this function into smaller methods"
                        if "# TODO:" not in refactored_lines[comment_line]:
                            refactored_lines.insert(comment_line, refactor_comment)
                
                # Add missing docstrings
                if not ast.get_docstring(node):
                    func_line = node.lineno
                    if func_line < len(refactored_lines):
                        indent = len(refactored_lines[func_line]) - len(refactored_lines[func_line].lstrip())
                        docstring = " " * (indent + 4) + f'"""TODO: Add docstring for {node.name}"""'
                        refactored_lines.insert(func_line, docstring)
        
        # Add missing docstrings to classes
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                if not ast.get_docstring(node):
                    class_line = node.lineno
                    if class_line < len(refactored_lines):
                        indent = len(refactored_lines[class_line]) - len(refactored_lines[class_line].lstrip())
                        docstring = " " * (indent + 4) + f'"""TODO: Add docstring for {node.name} class"""'
                        refactored_lines.insert(class_line, docstring)
        
        # Improve variable names if they're too short
        refactored_code = '\n'.join(refactored_lines)
        
        # Replace common poor variable names
        poor_names = {
            r'\bx\b(?![a-zA-Z])': 'value',
            r'\bdata\b(?![a-zA-Z])': 'items', 
            r'\btemp\b(?![a-zA-Z])': 'result',
            r'\bi\b(?![a-zA-Z])': 'index',
            r'\bj\b(?![a-zA-Z])': 'inner_index'
        }
        
        for pattern, replacement in poor_names.items():
            # Only replace in variable contexts, not in strings
            refactored_code = re.sub(pattern, replacement, refactored_code)
        
        return refactored_code
    
    def _execute_documentation_task(self, task: Task) -> Dict[str, Any]:
        """Execute documentation task"""
        results = {'docstrings_added': 0, 'files_modified': []}
        
        for file_path in task.file_targets:
            full_path = self.project_path / file_path
            if full_path.exists():
                with open(full_path, 'r') as f:
                    code = f.read()
                
                # Use AI to generate documentation
                doc_suggestions = self.mentor.chat_about_code(
                    code=code,
                    question="Generate proper docstrings for all functions and classes in this code. Follow Google or NumPy docstring conventions."
                )
                
                results['files_modified'].append(file_path)
                results['documentation_suggestions'] = doc_suggestions
        
        return results
    
    def _execute_optimization_task(self, task: Task) -> Dict[str, Any]:
        """Execute optimization task"""
        results = {'optimizations_identified': [], 'estimated_improvement': ''}
        
        for file_path in task.file_targets:
            full_path = self.project_path / file_path
            if full_path.exists():
                with open(full_path, 'r') as f:
                    code = f.read()
                
                # AI-powered optimization suggestions
                optimization_suggestions = self.mentor.chat_about_code(
                    code=code,
                    question="Analyze this code for performance bottlenecks and suggest specific optimizations. Focus on algorithmic improvements, data structure choices, and Python-specific optimizations."
                )
                
                results['optimizations_identified'].append(file_path)
                results['suggestions'] = optimization_suggestions
        
        return results
    
    def _execute_generation_task(self, task: Task) -> Dict[str, Any]:
        """Execute code generation task"""
        results = {'generated_files': [], 'code_generated': ''}
        
        if 'test' in task.title.lower():
            # Generate test files
            for file_path in task.file_targets:
                full_path = self.project_path / file_path
                if full_path.exists():
                    with open(full_path, 'r') as f:
                        code = f.read()
                    
                    # AI-generated tests
                    test_code = self.mentor.chat_about_code(
                        code=code,
                        question="Generate comprehensive unit tests for this code using pytest. Include edge cases, error conditions, and proper mocking where necessary."
                    )
                    
                    results['code_generated'] = test_code
                    results['target_file'] = f"test_{file_path}"
        
        return results
    
    def run_autonomous_session(self, max_tasks: int = 10, time_limit_minutes: int = 60) -> Dict[str, Any]:
        """Run autonomous execution session"""
        print(f"🤖 Starting autonomous session (max {max_tasks} tasks, {time_limit_minutes} min limit)")
        
        self.is_running = True
        start_time = datetime.now()
        tasks_completed = 0
        
        session_results = {
            'tasks_completed': 0,
            'tasks_failed': 0,
            'total_time': 0,
            'completed_tasks': [],
            'failed_tasks': []
        }
        
        while (self.is_running and 
               tasks_completed < max_tasks and 
               (datetime.now() - start_time).total_seconds() < time_limit_minutes * 60):
            
            task = self.execute_next_task()
            
            if task is None:
                print("🎯 No more ready tasks to execute")
                break
            
            if task.status == TaskStatus.COMPLETED:
                tasks_completed += 1
                session_results['tasks_completed'] += 1
                session_results['completed_tasks'].append(task.title)
            elif task.status == TaskStatus.FAILED:
                session_results['tasks_failed'] += 1
                session_results['failed_tasks'].append(task.title)
        
        end_time = datetime.now()
        session_results['total_time'] = (end_time - start_time).total_seconds() / 60  # minutes
        
        print(f"🏁 Session complete: {session_results['tasks_completed']} completed, {session_results['tasks_failed']} failed")
        return session_results
    
    def get_status_report(self) -> Dict[str, Any]:
        """Get comprehensive status report"""
        pending_tasks = [t for t in self.tasks.values() if t.status == TaskStatus.PENDING]
        in_progress_tasks = [t for t in self.tasks.values() if t.status == TaskStatus.IN_PROGRESS]
        completed_tasks = [t for t in self.tasks.values() if t.status == TaskStatus.COMPLETED]
        failed_tasks = [t for t in self.tasks.values() if t.status == TaskStatus.FAILED]
        
        return {
            'total_tasks': len(self.tasks),
            'pending': len(pending_tasks),
            'in_progress': len(in_progress_tasks),
            'completed': len(completed_tasks),
            'failed': len(failed_tasks),
            'next_task': pending_tasks[0].title if pending_tasks else "None",
            'completion_rate': len(completed_tasks) / len(self.tasks) if self.tasks else 0,
            'capabilities': self.capabilities,
            'agent_memory_size': len(self.agent_memory)
        }
    
    def _log_action(self, action: str):
        """Log agent actions"""
        self.execution_log.append({
            'timestamp': datetime.now().isoformat(),
            'action': action
        })
    
    def _save_agent_state(self):
        """Save agent state to disk"""
        state_file = self.project_path / '.pyscription_agent_state.json'
        
        state = {
            'tasks': {tid: {
                'id': t.id, 'title': t.title, 'description': t.description,
                'task_type': t.task_type, 'priority': t.priority.value,
                'status': t.status.value, 'file_targets': t.file_targets,
                'prerequisites': t.prerequisites, 'estimated_time': t.estimated_time,
                'progress': t.progress, 'error_message': t.error_message,
                'results': t.results, 'created_at': t.created_at.isoformat() if t.created_at else None,
                'started_at': t.started_at.isoformat() if t.started_at else None,
                'completed_at': t.completed_at.isoformat() if t.completed_at else None
            } for tid, t in self.tasks.items()},
            'execution_log': self.execution_log[-100:],  # Keep last 100 entries
            'agent_memory': self.agent_memory
        }
        
        with open(state_file, 'w') as f:
            json.dump(state, f, indent=2)
    
    def _load_agent_state(self):
        """Load agent state from disk"""
        state_file = self.project_path / '.pyscription_agent_state.json'
        
        if state_file.exists():
            try:
                with open(state_file, 'r') as f:
                    state = json.load(f)
                
                # Restore tasks
                for tid, task_data in state.get('tasks', {}).items():
                    task = Task(
                        id=task_data['id'],
                        title=task_data['title'],
                        description=task_data['description'],
                        task_type=task_data['task_type'],
                        priority=TaskPriority(task_data['priority']),
                        status=TaskStatus(task_data['status']),
                        file_targets=task_data['file_targets'],
                        prerequisites=task_data['prerequisites'],
                        estimated_time=task_data['estimated_time'],
                        progress=task_data['progress'],
                        error_message=task_data['error_message'],
                        results=task_data['results'],
                        created_at=datetime.fromisoformat(task_data['created_at']) if task_data['created_at'] else None,
                        started_at=datetime.fromisoformat(task_data['started_at']) if task_data['started_at'] else None,
                        completed_at=datetime.fromisoformat(task_data['completed_at']) if task_data['completed_at'] else None
                    )
                    self.tasks[tid] = task
                
                self.execution_log = state.get('execution_log', [])
                self.agent_memory = state.get('agent_memory', {})
                
            except Exception as e:
                print(f"⚠️  Could not load agent state: {e}")
    
    def stop(self):
        """Stop the autonomous agent"""
        self.is_running = False
        print("🛑 Agent stopped")
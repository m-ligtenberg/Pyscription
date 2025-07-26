"""
Autonomous Agent CLI Mode
Allows Pyscription to work autonomously like an AI agent
Beautiful terminal UI with modern styling and progress visualization
"""

import argparse
import time
from pathlib import Path
import sys
from datetime import datetime

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

from pyscription.core.autonomous_agent import AutonomousPythonAgent, TaskStatus, TaskPriority
from pyscription.core.mentor import MLEnhancedPyscription
from pyscription.utils.terminal_styling import ui, Colors


class AgentCLI:
    """Command-line interface for autonomous agent mode"""
    
    def __init__(self, project_path: str = "."):
        self.project_path = Path(project_path).resolve()
        self.mentor = MLEnhancedPyscription()
        self.agent = AutonomousPythonAgent(str(self.project_path), self.mentor)
        
    def run_interactive_agent(self):
        """Run interactive agent mode"""
        # Beautiful header
        ui.print_header("Pyscription - Autonomous Agent Mode", 
                       "Self-Directed Python Development AI")
        
        # Project info
        ui.print_section("Project Information", "📁")
        print(f"{Colors.BG_LIGHT_BLUE}{Colors.DARK_BLUE}  📂 Working Directory: {Colors.BOLD}{self.project_path}{Colors.RESET}")
        print()
        
        # Capabilities section
        ui.print_section("Agent Capabilities", "🚀")
        capabilities = [
            "🔍 Analyze your entire codebase autonomously",
            "📋 Plan multi-step improvement tasks", 
            "🛠️  Execute refactoring and optimizations",
            "📝 Generate documentation and tests",
            "🧠 Learn from your coding patterns",
            "⚡ Work independently with progress tracking"
        ]
        for capability in capabilities:
            print(f"{Colors.BG_LIGHT_BLUE}{Colors.DARK_BLUE}  {capability}{Colors.RESET}")
        print()
        
        # Commands section
        commands = [
            ("plan <goal>", "Analyze and create autonomous execution plan"),
            ("execute [N]", "Execute next N tasks (default: 1)"),
            ("auto [N] [time]", "Run autonomously for N tasks or time minutes"),
            ("status", "Show current tasks and progress dashboard"),
            ("tasks", "List all tasks with beautiful formatting"),
            ("results <task_id>", "Show detailed results of completed task"),
            ("stop", "Stop any running autonomous session"),
            ("clear", "Clear all tasks"),
            ("help", "Show this help"),
            ("quit", "Exit agent mode")
        ]
        ui.print_command_help(commands)
        
        while True:
            try:
                user_input = ui.input_prompt("Agent>", "agent").strip()
                
                if not user_input:
                    continue
                    
                if user_input.lower() in ['quit', 'exit', 'q']:
                    ui.print_success("🤖 Agent shutting down. State saved automatically.")
                    break
                
                self._handle_agent_command(user_input)
                    
            except KeyboardInterrupt:
                ui.print_warning("🤖 Agent interrupted. Stopping gracefully...")
                self.agent.stop()
                break
            except EOFError:
                ui.print_info("🤖 Agent shutting down.")
                break
            except Exception as e:
                ui.print_error(f"Error: {e}")
    
    def _handle_agent_command(self, command: str):
        """Handle agent commands"""
        parts = command.split()
        cmd = parts[0].lower()
        args = parts[1:] if len(parts) > 1 else []
        
        if cmd == 'plan':
            if not args:
                print("Usage: plan <goal>")
                print("Examples:")
                print("  plan refactor the codebase for better maintainability")
                print("  plan add comprehensive documentation")
                print("  plan optimize for performance")
                print("  plan create unit tests for all modules")
                return
            
            goal = ' '.join(args)
            print(f"\n🎯 Planning to achieve: {goal}")
            
            try:
                tasks = self.agent.analyze_and_plan(goal)
                print(f"\n📋 Created execution plan with {len(tasks)} tasks:")
                for i, task in enumerate(tasks[:5], 1):  # Show first 5
                    priority_emoji = "🔥" if task.priority == TaskPriority.HIGH else "⚡" if task.priority == TaskPriority.MEDIUM else "📌"
                    print(f"  {i}. {priority_emoji} {task.title}")
                    print(f"     └─ {task.description}")
                
                if len(tasks) > 5:
                    print(f"     ... and {len(tasks) - 5} more tasks")
                
                print(f"\n💡 Use 'execute' to start, or 'auto' for autonomous execution")
                
            except Exception as e:
                print(f"❌ Planning failed: {e}")
        
        elif cmd == 'execute':
            count = int(args[0]) if args and args[0].isdigit() else 1
            
            print(f"\n🚀 Executing next {count} task{'s' if count > 1 else ''}...")
            
            executed = 0
            for _ in range(count):
                task = self.agent.execute_next_task()
                if task is None:
                    print("✅ No more tasks ready for execution")
                    break
                executed += 1
                
                if task.status == TaskStatus.COMPLETED:
                    print(f"  ✅ {task.title}")
                else:
                    print(f"  ❌ {task.title} - {task.error_message}")
            
            if executed > 0:
                print(f"\n📊 Executed {executed} task{'s' if executed > 1 else ''}")
        
        elif cmd == 'auto':
            max_tasks = int(args[0]) if args and args[0].isdigit() else 10
            time_limit = int(args[1]) if len(args) > 1 and args[1].isdigit() else 30
            
            print(f"\n🤖 Starting autonomous session:")
            print(f"   • Max tasks: {max_tasks}")
            print(f"   • Time limit: {time_limit} minutes")
            print(f"   • Press Ctrl+C to stop")
            print()
            
            try:
                results = self.agent.run_autonomous_session(max_tasks, time_limit)
                
                print(f"\n🏁 Autonomous session completed:")
                print(f"   ✅ Tasks completed: {results['tasks_completed']}")
                print(f"   ❌ Tasks failed: {results['tasks_failed']}")
                print(f"   ⏱️  Total time: {results['total_time']:.1f} minutes")
                
                if results['completed_tasks']:
                    print(f"\n✅ Completed tasks:")
                    for task_title in results['completed_tasks']:
                        print(f"   • {task_title}")
                
                if results['failed_tasks']:
                    print(f"\n❌ Failed tasks:")
                    for task_title in results['failed_tasks']:
                        print(f"   • {task_title}")
                        
            except KeyboardInterrupt:
                print(f"\n🛑 Autonomous session stopped by user")
                self.agent.stop()
        
        elif cmd == 'status':
            status = self.agent.get_status_report()
            ui.print_agent_status(status)
        
        elif cmd == 'tasks':
            if not self.agent.tasks:
                print("📋 No tasks in queue. Use 'plan <goal>' to create tasks.")
                return
            
            print(f"\n📋 All Tasks ({len(self.agent.tasks)} total):")
            
            # Group by status
            for status in [TaskStatus.IN_PROGRESS, TaskStatus.PENDING, TaskStatus.COMPLETED, TaskStatus.FAILED]:
                tasks_in_status = [t for t in self.agent.tasks.values() if t.status == status]
                if not tasks_in_status:
                    continue
                
                status_emoji = {"in_progress": "🚀", "pending": "⏳", "completed": "✅", "failed": "❌"}
                print(f"\n{status_emoji[status.value]} {status.value.title()} ({len(tasks_in_status)}):")
                
                for task in sorted(tasks_in_status, key=lambda t: t.created_at or datetime.min):
                    priority_emoji = "🔥" if task.priority == TaskPriority.HIGH else "⚡" if task.priority == TaskPriority.MEDIUM else "📌"
                    progress_bar = f"({task.progress:.0%})" if task.progress > 0 else ""
                    print(f"  {priority_emoji} {task.id[:8]}... {task.title} {progress_bar}")
                    if task.error_message:
                        print(f"     └─ Error: {task.error_message}")
        
        elif cmd == 'results':
            if not args:
                print("Usage: results <task_id>")
                print("Use 'tasks' to see available task IDs")
                return
            
            task_id_prefix = args[0]
            matching_tasks = [t for t in self.agent.tasks.values() if t.id.startswith(task_id_prefix)]
            
            if not matching_tasks:
                print(f"❌ No task found with ID starting with '{task_id_prefix}'")
                return
            
            task = matching_tasks[0]
            print(f"\n📊 Task Results: {task.title}")
            print(f"   Status: {task.status.value}")
            print(f"   Priority: {task.priority.value}")
            print(f"   Progress: {task.progress:.0%}")
            
            if task.estimated_time:
                print(f"   Estimated time: {task.estimated_time} minutes")
            
            if task.started_at and task.completed_at:
                actual_time = (task.completed_at - task.started_at).total_seconds() / 60
                print(f"   Actual time: {actual_time:.1f} minutes")
            
            if task.file_targets:
                print(f"   Target files: {', '.join(task.file_targets)}")
            
            if task.results:
                print(f"\n📝 Results:")
                for key, value in task.results.items():
                    if isinstance(value, str) and len(value) > 200:
                        print(f"   {key}: {value[:200]}...")
                    else:
                        print(f"   {key}: {value}")
            
            if task.error_message:
                print(f"\n❌ Error: {task.error_message}")
        
        elif cmd == 'stop':
            self.agent.stop()
            print("🛑 Stopped autonomous execution")
        
        elif cmd == 'clear':
            confirm = input("⚠️  Clear all tasks? This cannot be undone. (y/N): ")
            if confirm.lower() == 'y':
                self.agent.tasks.clear()
                print("🧹 All tasks cleared")
            else:
                print("❌ Cancelled")
        
        elif cmd == 'help':
            print("\n🤖 Pyscription Agent Commands:")
            print("   plan <goal>         - Create autonomous execution plan")
            print("   execute [N]         - Execute next N tasks")
            print("   auto [N] [time]     - Run autonomously")
            print("   status              - Show agent status")
            print("   tasks               - List all tasks")
            print("   results <task_id>   - Show task results")
            print("   stop                - Stop autonomous execution")
            print("   clear               - Clear all tasks")
            print("\n💡 Example workflow:")
            print("   1. plan refactor codebase for better maintainability")
            print("   2. auto 5 30    (run 5 tasks or 30 minutes)")
            print("   3. status       (check progress)")
        
        else:
            print(f"❌ Unknown command: {cmd}")
            print("Type 'help' for available commands")


def main():
    """Main entry point for agent mode"""
    parser = argparse.ArgumentParser(description='Pyscription - Autonomous Agent Mode')
    parser.add_argument('--project', '-p', default='.', help='Project directory to analyze')
    parser.add_argument('--goal', '-g', help='Autonomous goal to achieve')
    parser.add_argument('--auto', '-a', action='store_true', help='Start autonomous execution immediately')
    parser.add_argument('--max-tasks', type=int, default=10, help='Maximum tasks for autonomous mode')
    parser.add_argument('--time-limit', type=int, default=30, help='Time limit in minutes for autonomous mode')
    
    args = parser.parse_args()
    
    # Initialize agent
    cli = AgentCLI(args.project)
    
    # Handle direct goal execution
    if args.goal:
        print(f"🎯 Autonomous goal: {args.goal}")
        tasks = cli.agent.analyze_and_plan(args.goal)
        print(f"📋 Created {len(tasks)} tasks")
        
        if args.auto:
            print(f"🤖 Starting autonomous execution...")
            results = cli.agent.run_autonomous_session(args.max_tasks, args.time_limit)
            print(f"✅ Completed {results['tasks_completed']} tasks in {results['total_time']:.1f} minutes")
        else:
            print("💡 Use --auto flag to start autonomous execution")
        return
    
    # Interactive mode
    cli.run_interactive_agent()


if __name__ == "__main__":
    main()
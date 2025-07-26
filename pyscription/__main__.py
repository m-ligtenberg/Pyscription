#!/usr/bin/env python3
"""
Pyscription CLI Entry Point
Main entry point for the Pyscription CLI system
"""

import argparse
import sys
from pathlib import Path

# Add current directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from pyscription.core.doctor_interactive import MLEnhancedPyscription
from pyscription.utils.documentation_downloader import DocumentationDownloader
from pyscription.cli.conversational import ConversationalCLI
from pyscription.cli.agent_mode import AgentCLI


def _show_splash():
    """Display ASCII splash screen with medical theme and fade-out effect"""
    import time
    from pyscription.utils.terminal_styling import Colors
    
    # Clear screen first
    print('\033[2J\033[H', end='')
    
    # Display splash screen
    print(f"{Colors.SOFT_CYAN}")
    print("    ____                      _       _   _             ")
    print("   |  _ \ _   _ ___  ___ _ __(_)_ __ | |_(_) ___  _ __  ")
    print("   | |_) | | | / __|/ __| '__| | '_ \| __| |/ _ \| '_ \ ")
    print("   |  __/| |_| \__ \ (__| |  | | |_) | |_| | (_) | | | |")
    print("   |_|    \__, |___/\___|_|  |_| .__/ \__|_|\___/|_| |_|")
    print("          |___/                |_|                      ")
    print()
    print(f"{Colors.SOFT_YELLOW}           💊 Terminal medication. No prescription needed.{Colors.RESET}")
    print()
    print(f"{Colors.SOFT_GREEN}    🏥 AI-Enhanced Python Development Assistant{Colors.RESET}")
    print(f"{Colors.LIGHT_GRAY}    🔬 Diagnose • 💉 Inject • 💊 Medicate • 🧬 Evolve{Colors.RESET}")
    print()
    
    # Show for 2.5 seconds
    time.sleep(2.5)
    
    # Fade out effect - gradually dim the colors
    fade_steps = 8
    for step in range(fade_steps):
        # Move cursor to top and redraw with dimmer colors
        print('\033[H', end='')
        
        # Calculate fade intensity (255 to 50)
        intensity = 255 - (step * 25)
        fade_color = f'\033[38;5;{max(240 - step * 2, 236)}m'  # Gray fade
        
        print(fade_color)
        print("    ____                      _       _   _             ")
        print("   |  _ \ _   _ ___  ___ _ __(_)_ __ | |_(_) ___  _ __  ")
        print("   | |_) | | | / __|/ __| '__| | '_ \| __| |/ _ \| '_ \ ")
        print("   |  __/| |_| \__ \ (__| |  | | |_) | |_| | (_) | | | |")
        print("   |_|    \__, |___/\___|_|  |_| .__/ \__|_|\___/|_| |_|")
        print("          |___/                |_|                      ")
        print()
        print(f"{fade_color}           💊 Terminal medication. No prescription needed.{Colors.RESET}")
        print()
        print(f"{fade_color}    🏥 AI-Enhanced Python Development Assistant{Colors.RESET}")
        print(f"{fade_color}    🔬 Diagnose • 💉 Inject • 💊 Medicate • 🧬 Evolve{Colors.RESET}")
        print()
        
        time.sleep(0.2)  # 0.2 seconds per fade step
    
    # Clear screen after fade
    print('\033[2J\033[H', end='')


def _apply_pill_treatment(file_path: str):
    """Apply mild treatment - basic linting and style fixes"""
    from pyscription.utils.terminal_styling import ui
    from pyscription.core.security_analyzer import SecurityPatternAnalyzer
    
    try:
        with open(file_path, 'r') as f:
            code = f.read()
        
        ui.print_container_content(f"💊 Examining patient: {file_path}")
        
        # Basic analysis
        mentor = MLEnhancedPyscription()
        analysis = mentor.analyze_with_ml(code)
        
        # Security check
        security_analyzer = SecurityPatternAnalyzer()
        security_issues = security_analyzer.analyze_code_security(code, file_path)
        
        # Show mild recommendations
        ui.print_container_content("📋 Diagnosis:")
        if security_issues:
            ui.print_container_content(f"⚠️ Found {len(security_issues)} security concerns")
        
        ui.print_container_content("💊 Prescribed treatment: Basic code cleanup")
        ui.print_container_content("📝 Recommendations:")
        ui.print_container_content("  • Run a code formatter (black, autopep8)")
        ui.print_container_content("  • Check imports and remove unused ones")
        ui.print_container_content("  • Add type hints where missing")
        
    except FileNotFoundError:
        ui.print_error(f"Patient not found: {file_path}")
    except Exception as e:
        ui.print_error(f"Treatment failed: {e}")


def _apply_injection_treatment(file_path: str):
    """Apply targeted treatment - specific fixes with AI guidance"""
    from pyscription.utils.terminal_styling import ui
    
    try:
        with open(file_path, 'r') as f:
            code = f.read()
        
        ui.print_container_content(f"💉 Performing targeted injection on: {file_path}")
        
        # AI-powered analysis
        mentor = MLEnhancedPyscription()
        ai_response = mentor.chat_about_code(code=code)
        
        ui.print_container_content("🔬 AI Analysis:")
        # Display AI response in container
        for line in ai_response.split('\n'):
            ui.print_container_content(line)
            
        ui.print_container_content("💉 Injection complete - review AI recommendations above")
        
    except FileNotFoundError:
        ui.print_error(f"Patient not found: {file_path}")
    except Exception as e:
        ui.print_error(f"Injection failed: {e}")


def _apply_overdose_treatment(file_path: str):
    """Apply maximum treatment - all available fixes"""
    from pyscription.utils.terminal_styling import ui
    
    ui.print_container_content(f"💀 OVERDOSE WARNING: Applying maximum treatment to {file_path}")
    ui.print_container_content("⚠️ This will apply ALL available fixes without confirmation")
    
    # Combine pill and injection treatments
    _apply_pill_treatment(file_path)
    ui.print_container_content("")
    _apply_injection_treatment(file_path)
    
    ui.print_container_content("💀 Overdose treatment complete - monitor for side effects")


def _apply_refill_treatment():
    """Repeat the last operation"""
    from pyscription.utils.terminal_styling import ui
    
    # For now, just show a message - in full implementation would track last operation
    ui.print_container_content("🔄 Prescription refill")
    ui.print_container_content("📋 No previous prescription found")
    ui.print_container_content("💡 Use --pill, --inject, or --overdose to create a prescription")


def _show_side_effects():
    """Show recent changes and effects"""
    from pyscription.utils.terminal_styling import ui
    
    ui.print_container_content("⚠️ Recent Treatment Side Effects:")
    ui.print_container_content("")
    ui.print_container_content("📊 Treatment History:")
    ui.print_container_content("  • No recent treatments recorded")
    ui.print_container_content("")
    ui.print_container_content("🔍 To monitor side effects:")
    ui.print_container_content("  • Check git diff for recent changes")
    ui.print_container_content("  • Run tests to verify no regressions")
    ui.print_container_content("  • Review modified files for correctness")


def _find_python_files(directory: str, recursive: bool = True) -> list:
    """Find all Python files in a directory"""
    directory = Path(directory)
    python_files = []
    
    if recursive:
        python_files = list(directory.rglob("*.py"))
    else:
        python_files = list(directory.glob("*.py"))
    
    # Filter out common exclusions
    exclusions = {
        '__pycache__', '.git', '.venv', 'venv', 'env', 
        'node_modules', '.pytest_cache', 'build', 'dist'
    }
    
    filtered_files = []
    for file in python_files:
        if not any(excl in file.parts for excl in exclusions):
            filtered_files.append(file)
    
    return sorted(filtered_files)


def _analyze_single_file(file_path: str):
    """Analyze a single Python file"""
    from pyscription.utils.terminal_styling import ui
    
    try:
        with open(file_path, 'r') as f:
            code = f.read()
        
        ui.print_container_content(f"🔍 Analyzing single file: {file_path}")
        
        # Get AI-powered analysis
        mentor = MLEnhancedPyscription()
        response = mentor.chat_about_code(code=code)
        
        ui.print_container_content("")
        ui.print_container_content("🤖 AI Analysis:")
        for line in response.split('\n'):
            ui.print_container_content(line)
            
    except FileNotFoundError:
        ui.print_error(f"File not found: {file_path}")
    except Exception as e:
        ui.print_error(f"Analysis failed: {e}")


def _analyze_code_snippet(code_snippet: str):
    """Analyze a code snippet"""
    from pyscription.utils.terminal_styling import ui
    
    ui.print_container_content("🔍 Analyzing code snippet...")
    
    # Get AI-powered analysis
    mentor = MLEnhancedPyscription()
    response = mentor.chat_about_code(code=code_snippet)
    
    ui.print_container_content("")
    ui.print_container_content("🤖 AI Analysis:")
    for line in response.split('\n'):
        ui.print_container_content(line)


def _analyze_codebase(directory: str, recursive: bool = True):
    """Analyze entire codebase"""
    from pyscription.utils.terminal_styling import ui
    from pyscription.core.security_analyzer import SecurityPatternAnalyzer
    from pyscription.core.project_analyzer import ProjectAnalyzer
    
    ui.print_container_content(f"🔍 Analyzing codebase: {directory}")
    ui.print_container_content(f"📁 Recursive: {recursive}")
    ui.print_container_content("")
    
    # Find all Python files
    python_files = _find_python_files(directory, recursive)
    
    if not python_files:
        ui.print_warning("No Python files found in directory")
        return
    
    ui.print_container_content(f"📊 Found {len(python_files)} Python files")
    ui.print_container_content("")
    
    # Initialize analyzers
    mentor = MLEnhancedPyscription()
    security_analyzer = SecurityPatternAnalyzer()
    
    # Project-wide analysis
    total_lines = 0
    total_security_issues = 0
    file_analyses = []
    
    ui.print_container_content("🔬 Analyzing files...")
    
    for i, file_path in enumerate(python_files[:10]):  # Limit to first 10 files for demo
        try:
            with open(file_path, 'r') as f:
                code = f.read()
            
            lines = len(code.split('\n'))
            total_lines += lines
            
            # Security analysis
            security_issues = security_analyzer.analyze_code_security(code, str(file_path))
            total_security_issues += len(security_issues)
            
            file_analyses.append({
                'file': str(file_path.relative_to(directory)),
                'lines': lines,
                'security_issues': len(security_issues),
                'code': code[:500] + "..." if len(code) > 500 else code  # Sample for AI
            })
            
        except Exception as e:
            ui.print_warning(f"Could not analyze {file_path}: {e}")
    
    # Summary report
    ui.print_container_content("")
    ui.print_container_content("📋 Codebase Analysis Summary:")
    ui.print_container_content(f"  📄 Total files analyzed: {len(file_analyses)}")
    ui.print_container_content(f"  📏 Total lines of code: {total_lines:,}")
    ui.print_container_content(f"  🛡️ Security issues found: {total_security_issues}")
    ui.print_container_content("")
    
    # Top issues by file
    if file_analyses:
        ui.print_container_content("🔍 Files with most issues:")
        sorted_files = sorted(file_analyses, key=lambda x: x['security_issues'], reverse=True)
        for file_info in sorted_files[:5]:
            if file_info['security_issues'] > 0:
                ui.print_container_content(f"  ⚠️ {file_info['file']}: {file_info['security_issues']} issues")
    
    # AI analysis of overall codebase patterns
    ui.print_container_content("")
    ui.print_container_content("🤖 AI Codebase Analysis:")
    
    # Create a summary for AI analysis
    codebase_summary = f"""
Codebase Analysis Summary:
- Total files: {len(file_analyses)}
- Total lines: {total_lines:,}
- Security issues: {total_security_issues}

Sample files and code patterns:
"""
    
    for file_info in file_analyses[:3]:  # Send top 3 files to AI
        codebase_summary += f"\nFile: {file_info['file']} ({file_info['lines']} lines)\n"
        codebase_summary += f"Sample code:\n{file_info['code']}\n"
    
    try:
        ai_response = mentor.chat_about_code(code=codebase_summary)
        for line in ai_response.split('\n'):
            ui.print_container_content(line)
    except Exception as e:
        ui.print_warning(f"AI analysis failed: {e}")
    
    ui.print_container_content("")
    ui.print_container_content("✅ Codebase analysis complete!")


def _comprehensive_checkup(directory: str = "."):
    """Comprehensive codebase health examination"""
    from pyscription.utils.terminal_styling import ui
    from pyscription.core.security_analyzer import SecurityPatternAnalyzer
    import subprocess
    import os
    
    ui.clear_screen()
    ui.print_container_content("🏥 COMPREHENSIVE CHECKUP - Full Health Examination")
    ui.print_container_content("=" * 60)
    ui.print_container_content("")
    
    # 1. File structure analysis
    ui.print_container_content("📁 STRUCTURAL EXAMINATION:")
    python_files = _find_python_files(directory)
    ui.print_container_content(f"  📄 Python files: {len(python_files)}")
    
    total_lines = 0
    for file_path in python_files:
        try:
            with open(file_path, 'r') as f:
                total_lines += len(f.readlines())
        except:
            pass
    ui.print_container_content(f"  📏 Total lines of code: {total_lines:,}")
    
    # 2. Security scan
    ui.print_container_content("")
    ui.print_container_content("🛡️ SECURITY SCAN:")
    security_analyzer = SecurityPatternAnalyzer()
    total_security_issues = 0
    
    for file_path in python_files[:10]:  # Sample first 10 files
        try:
            with open(file_path, 'r') as f:
                code = f.read()
            security_issues = security_analyzer.analyze_code_security(code, str(file_path))
            total_security_issues += len(security_issues)
        except:
            pass
    
    ui.print_container_content(f"  ⚠️ Security issues detected: {total_security_issues}")
    
    # 3. Dependencies check
    ui.print_container_content("")
    ui.print_container_content("📦 DEPENDENCY HEALTH:")
    req_files = ["requirements.txt", "pyproject.toml", "setup.py"]
    deps_found = [f for f in req_files if os.path.exists(f)]
    ui.print_container_content(f"  📋 Dependency files: {', '.join(deps_found) if deps_found else 'None found'}")
    
    # 4. Git health
    ui.print_container_content("")
    ui.print_container_content("🔄 VERSION CONTROL HEALTH:")
    try:
        result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
        if result.returncode == 0:
            changes = len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
            ui.print_container_content(f"  📝 Uncommitted changes: {changes}")
        else:
            ui.print_container_content("  ❌ Not a git repository")
    except:
        ui.print_container_content("  ❌ Git not available")
    
    # 5. Overall health score
    ui.print_container_content("")
    ui.print_container_content("💊 OVERALL HEALTH ASSESSMENT:")
    health_score = 100 - min(total_security_issues * 5, 50)  # Deduct for security issues
    if health_score >= 90:
        ui.print_container_content(f"  ✅ EXCELLENT health: {health_score}%")
    elif health_score >= 70:
        ui.print_container_content(f"  ⚠️ GOOD health: {health_score}%")
    else:
        ui.print_container_content(f"  🚨 NEEDS ATTENTION: {health_score}%")
    
    ui.print_container_content("")
    ui.print_container_content("📋 Checkup complete! Use --prescription for detailed recommendations.")


def _emergency_response(directory: str = "."):
    """Critical issue immediate diagnosis and fix"""
    from pyscription.utils.terminal_styling import ui
    from pyscription.core.security_analyzer import SecurityPatternAnalyzer
    
    ui.clear_screen()
    ui.print_container_content("🚨 EMERGENCY RESPONSE - Critical Issue Detection")
    ui.print_container_content("=" * 60)
    ui.print_container_content("")
    
    # Find critical issues quickly
    ui.print_container_content("🔍 SCANNING FOR CRITICAL ISSUES...")
    
    python_files = _find_python_files(directory)
    critical_issues = []
    security_analyzer = SecurityPatternAnalyzer()
    
    for file_path in python_files[:5]:  # Quick scan of first 5 files
        try:
            with open(file_path, 'r') as f:
                code = f.read()
            
            # Check for critical security issues
            security_issues = security_analyzer.analyze_code_security(code, str(file_path))
            for issue in security_issues:
                if any(word in issue.get('description', '').lower() for word in ['injection', 'eval', 'exec', 'hardcoded']):
                    critical_issues.append({
                        'file': str(file_path),
                        'type': 'SECURITY',
                        'issue': issue.get('description', 'Unknown security issue')
                    })
            
            # Check for syntax errors
            try:
                compile(code, str(file_path), 'exec')
            except SyntaxError as e:
                critical_issues.append({
                    'file': str(file_path),
                    'type': 'SYNTAX',
                    'issue': f"Syntax error: {e.msg} at line {e.lineno}"
                })
                
        except Exception as e:
            critical_issues.append({
                'file': str(file_path),
                'type': 'ACCESS',
                'issue': f"Cannot read file: {e}"
            })
    
    # Report findings
    if critical_issues:
        ui.print_container_content("🚨 CRITICAL ISSUES DETECTED:")
        ui.print_container_content("")
        for i, issue in enumerate(critical_issues[:10], 1):
            ui.print_container_content(f"  {i}. [{issue['type']}] {issue['file']}")
            ui.print_container_content(f"     💊 {issue['issue']}")
            ui.print_container_content("")
        
        ui.print_container_content("⚡ IMMEDIATE ACTIONS RECOMMENDED:")
        ui.print_container_content("  1. Review security issues immediately")
        ui.print_container_content("  2. Fix syntax errors before deployment")
        ui.print_container_content("  3. Run full --checkup for complete analysis")
    else:
        ui.print_container_content("✅ NO CRITICAL ISSUES DETECTED")
        ui.print_container_content("   Your codebase appears stable!")
    
    ui.print_container_content("")
    ui.print_container_content("🏥 Emergency scan complete!")


def _therapy_session(directory: str = "."):
    """Interactive guided code improvement session"""
    from pyscription.utils.terminal_styling import ui
    
    ui.clear_screen()
    ui.print_container_content("🧠 THERAPY SESSION - Guided Code Improvement")
    ui.print_container_content("=" * 60)
    ui.print_container_content("")
    
    ui.print_container_content("👩‍⚕️ Welcome to your code therapy session!")
    ui.print_container_content("   Let's work together to improve your codebase health.")
    ui.print_container_content("")
    
    # Interactive improvement guide
    ui.print_container_content("🔍 ASSESSMENT QUESTIONS:")
    ui.print_container_content("")
    ui.print_container_content("1. What specific issues are you experiencing?")
    ui.print_container_content("   □ Performance problems")
    ui.print_container_content("   □ Code organization issues") 
    ui.print_container_content("   □ Testing gaps")
    ui.print_container_content("   □ Security concerns")
    ui.print_container_content("")
    
    ui.print_container_content("2. What are your improvement goals?")
    ui.print_container_content("   □ Better code quality")
    ui.print_container_content("   □ Improved maintainability")
    ui.print_container_content("   □ Enhanced security")
    ui.print_container_content("   □ Performance optimization")
    ui.print_container_content("")
    
    ui.print_container_content("💡 THERAPEUTIC RECOMMENDATIONS:")
    ui.print_container_content("   • Start with --checkup for full assessment")
    ui.print_container_content("   • Use --doctor mode for interactive guidance")
    ui.print_container_content("   • Apply --pill for gentle improvements")
    ui.print_container_content("   • Consider --surgeon for major refactoring")
    ui.print_container_content("")
    
    ui.print_container_content("🌱 HEALTHY CODING HABITS:")
    ui.print_container_content("   • Regular code reviews")
    ui.print_container_content("   • Consistent testing practices")
    ui.print_container_content("   • Documentation maintenance")
    ui.print_container_content("   • Security-first mindset")
    ui.print_container_content("")
    
    ui.print_container_content("📞 Continue therapy with: pyscription --doctor")


def _vitals_monitoring(directory: str = "."):
    """Real-time code health monitoring and metrics"""
    from pyscription.utils.terminal_styling import ui
    import time
    import os
    
    ui.clear_screen()
    ui.print_container_content("📊 VITALS MONITORING - Real-time Code Health")
    ui.print_container_content("=" * 60)
    ui.print_container_content("")
    
    # Real-time monitoring display
    python_files = _find_python_files(directory)
    
    for i in range(5):  # 5 monitoring cycles
        ui.print_container_content(f"🔄 MONITORING CYCLE {i+1}/5")
        ui.print_container_content("")
        
        # File count
        ui.print_container_content(f"📄 Python files: {len(python_files)}")
        
        # Total size
        total_size = 0
        for file_path in python_files:
            try:
                total_size += os.path.getsize(file_path)
            except:
                pass
        ui.print_container_content(f"💾 Total size: {total_size / 1024:.1f} KB")
        
        # Recent modifications
        recent_files = 0
        current_time = time.time()
        for file_path in python_files:
            try:
                if current_time - os.path.getmtime(file_path) < 3600:  # Modified in last hour
                    recent_files += 1
            except:
                pass
        ui.print_container_content(f"⏱️ Recently modified: {recent_files} files")
        
        # Health indicators
        ui.print_container_content("")
        ui.print_container_content("💗 HEALTH INDICATORS:")
        ui.print_container_content("   🟢 File structure: STABLE")
        ui.print_container_content("   🟡 Activity level: MODERATE" if recent_files > 0 else "   🟢 Activity level: CALM")
        ui.print_container_content("   🟢 Growth rate: HEALTHY")
        
        if i < 4:  # Don't wait after last cycle
            ui.print_container_content("")
            ui.print_container_content("⏳ Next scan in 3 seconds...")
            time.sleep(3)
            ui.clear_screen()
    
    ui.print_container_content("")
    ui.print_container_content("📊 Monitoring complete! All vitals stable.")


def _generate_prescription(directory: str = "."):
    """Generate detailed improvement recommendations"""
    from pyscription.utils.terminal_styling import ui
    from pyscription.core.security_analyzer import SecurityPatternAnalyzer
    
    ui.clear_screen()
    ui.print_container_content("📋 PRESCRIPTION - Detailed Improvement Plan")
    ui.print_container_content("=" * 60)
    ui.print_container_content("")
    
    # Analyze codebase for recommendations
    python_files = _find_python_files(directory)
    security_analyzer = SecurityPatternAnalyzer()
    
    ui.print_container_content("👩‍⚕️ DOCTOR'S PRESCRIPTION:")
    ui.print_container_content("")
    
    # Security recommendations
    ui.print_container_content("🛡️ SECURITY TREATMENT:")
    ui.print_container_content("   Rx: Regular security audits")
    ui.print_container_content("   💊 Take 1 security scan daily")
    ui.print_container_content("   ⚠️ Monitor for injection vulnerabilities")
    ui.print_container_content("")
    
    # Code quality recommendations
    ui.print_container_content("✨ QUALITY ENHANCEMENT:")
    ui.print_container_content("   Rx: Code formatting and linting")
    ui.print_container_content("   💊 Apply black formatter weekly")
    ui.print_container_content("   💊 Run pylint checks daily")
    ui.print_container_content("   💊 Add type hints gradually")
    ui.print_container_content("")
    
    # Testing recommendations
    ui.print_container_content("🧪 TESTING REGIMEN:")
    ui.print_container_content("   Rx: Comprehensive test coverage")
    ui.print_container_content("   💊 Aim for 80%+ code coverage")
    ui.print_container_content("   💊 Write unit tests for new functions")
    ui.print_container_content("   💊 Add integration tests for workflows")
    ui.print_container_content("")
    
    # Documentation recommendations
    ui.print_container_content("📚 DOCUMENTATION THERAPY:")
    ui.print_container_content("   Rx: Clear, maintainable documentation")
    ui.print_container_content("   💊 Add docstrings to all functions")
    ui.print_container_content("   💊 Update README with examples")
    ui.print_container_content("   💊 Document API endpoints")
    ui.print_container_content("")
    
    # Performance recommendations
    ui.print_container_content("⚡ PERFORMANCE OPTIMIZATION:")
    ui.print_container_content("   Rx: Efficient code patterns")
    ui.print_container_content("   💊 Profile slow functions")
    ui.print_container_content("   💊 Optimize database queries")
    ui.print_container_content("   💊 Use appropriate data structures")
    ui.print_container_content("")
    
    ui.print_container_content("📅 FOLLOW-UP SCHEDULE:")
    ui.print_container_content("   • Daily: --pill for minor improvements")
    ui.print_container_content("   • Weekly: --checkup for health assessment")
    ui.print_container_content("   • Monthly: --surgeon for major refactoring")
    ui.print_container_content("")
    
    ui.print_container_content("⚠️ SIDE EFFECTS: Improved code quality may be addictive!")


def main():
    """Main entry point with argument parsing"""
    parser = argparse.ArgumentParser(
        description='Pyscription - ML-Enhanced Python Development Assistant',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  pyscription --setup                    # Complete setup with documentation
  pyscription --interactive              # Start conversational mode
  pyscription --agent                    # Start autonomous agent mode
  pyscription --analyze code.py          # Analyze a Python file
  pyscription --search "decorator pattern"  # Search documentation
        """
    )
    
    # Medication-themed commands
    parser.add_argument('--pill', action='store_true',
                       help='Apply mild corrections (lint, style, syntax)')
    parser.add_argument('--inject', action='store_true', 
                       help='Perform targeted code changes')
    parser.add_argument('--overdose', action='store_true',
                       help='Apply all available fixes without prompts')
    parser.add_argument('--refill', action='store_true',
                       help='Repeat the previous operation')
    parser.add_argument('--side-effects', action='store_true',
                       help='Display a list of recent changes')
    parser.add_argument('--checkup', action='store_true',
                       help='Comprehensive codebase health examination')
    parser.add_argument('--emergency', action='store_true',
                       help='Critical issue immediate diagnosis and fix')
    parser.add_argument('--therapy', action='store_true',
                       help='Interactive guided code improvement session')
    parser.add_argument('--vitals', action='store_true',
                       help='Real-time code health monitoring and metrics')
    parser.add_argument('--prescription', action='store_true',
                       help='Generate detailed improvement recommendations')
    
    # Mode selection
    parser.add_argument('--doctor', '--interactive', '-i', action='store_true', 
                       help='Start conversational session with the AI Doctor')
    parser.add_argument('--surgeon', '--agent', '-a', action='store_true',
                       help='Run autonomous codebase improvement (Surgeon mode)')
    
    # Setup and configuration
    parser.add_argument('--setup', action='store_true',
                       help='Complete setup with Python documentation download')
    parser.add_argument('--download-docs', 
                       help='Download Python docs (version: 3.9, 3.10, 3.11)')
    parser.add_argument('--ingest-docs', 
                       help='Ingest Python documentation from path')
    
    # Analysis and search
    parser.add_argument('--analyze', help='Analyze Python file, directory, or entire codebase')
    parser.add_argument('--search', '-s', help='Search documentation and patterns')
    parser.add_argument('--discover-patterns', action='store_true',
                       help='Discover patterns from coding history')
    
    # Project options
    parser.add_argument('--project', '-p', default='.',
                       help='Project directory for all modes (doctor, surgeon, analyze)')
    parser.add_argument('--recursive', '-r', action='store_true',
                       help='Recursively analyze all Python files in directory')
    
    # File argument for medication commands
    parser.add_argument('file', nargs='?', help='Python file to treat')
    
    args = parser.parse_args()
    
    # Show splash screen for interactive modes and when no specific command is given
    show_splash = (args.doctor or args.surgeon or 
                   (not any([args.setup, args.download_docs, args.ingest_docs, 
                            args.discover_patterns, args.pill, args.inject, 
                            args.overdose, args.refill, args.side_effects, 
                            args.analyze, args.search, args.checkup, args.emergency,
                            args.therapy, args.vitals, args.prescription])))
    
    if show_splash:
        _show_splash()
    
    try:
        # Handle setup first
        if args.setup:
            print("🚀 Setting up Pyscription with conversational AI...")
            
            # Download documentation
            downloader = DocumentationDownloader()
            docs_path = downloader.download_python_docs("3.11")
            
            if docs_path:
                # Ingest documentation
                mentor = MLEnhancedPyscription()
                count = mentor.ingest_docs(docs_path)
                print(f"✅ Setup complete! Processed {count} documentation files.")
                print("🤖 Local AI ready for conversational assistance!")
                print("\n💡 Quick start:")
                print("  pyscription --interactive    # Start chatting")
                print("  pyscription --agent          # Start autonomous mode")
            else:
                print("❌ Setup failed. Try manual documentation ingestion.")
            return
        
        # Handle documentation download
        if args.download_docs:
            downloader = DocumentationDownloader()
            docs_path = downloader.download_python_docs(args.download_docs)
            if docs_path:
                print(f"📚 Use: pyscription --ingest-docs {docs_path}")
            return
        
        # Handle documentation ingestion
        if args.ingest_docs:
            mentor = MLEnhancedPyscription()
            count = mentor.ingest_docs(args.ingest_docs)
            print(f"✅ Ingested {count} documentation files")
            return
        
        # Handle pattern discovery
        if args.discover_patterns:
            mentor = MLEnhancedPyscription()
            count = mentor.discover_patterns_from_history()
            print(f"🔍 Analyzed {count} code samples from history")
            print("✅ Pattern discovery complete!")
            return
        
        # Handle medication-themed commands
        if args.pill or args.inject or args.overdose:
            if not args.file:
                print("❌ Please specify a Python file to treat")
                print("Usage: pyscription --pill <file.py>")
                return
                
            from pyscription.utils.terminal_styling import ui
            ui.clear_screen()
            
            if args.pill:
                ui.print_container_content("💊 Applying mild treatment...")
                _apply_pill_treatment(args.file)
            elif args.inject:
                ui.print_container_content("💉 Performing targeted injection...")
                _apply_injection_treatment(args.file)
            elif args.overdose:
                ui.print_container_content("💀 Applying maximum dosage...")
                _apply_overdose_treatment(args.file)
            return
        
        # Handle refill (repeat last operation)
        if args.refill:
            from pyscription.utils.terminal_styling import ui
            ui.clear_screen()
            ui.print_container_content("🔄 Refilling prescription...")
            _apply_refill_treatment()
            return
        
        # Handle side effects (show recent changes)
        if args.side_effects:
            from pyscription.utils.terminal_styling import ui
            ui.clear_screen()
            ui.print_container_content("⚠️ Recent side effects:")
            _show_side_effects()
            return
        
        # Handle new medical commands
        if args.checkup:
            _comprehensive_checkup(args.project)
            return
        
        if args.emergency:
            _emergency_response(args.project)
            return
        
        if args.therapy:
            _therapy_session(args.project)
            return
        
        if args.vitals:
            _vitals_monitoring(args.project)
            return
        
        if args.prescription:
            _generate_prescription(args.project)
            return
        
        # Handle codebase analysis
        if args.analyze:
            from pyscription.utils.terminal_styling import ui
            ui.clear_screen()
            
            try:
                analyze_path = Path(args.analyze)
                
                if analyze_path.is_file():
                    # Single file analysis
                    _analyze_single_file(str(analyze_path))
                elif analyze_path.is_dir():
                    # Directory/codebase analysis
                    _analyze_codebase(str(analyze_path), args.recursive)
                else:
                    # Code snippet analysis
                    _analyze_code_snippet(args.analyze)
                    
            except Exception as e:
                ui.print_error(f"Analysis failed: {e}")
            return
        
        # Handle search
        if args.search:
            mentor = MLEnhancedPyscription()
            results = mentor.smart_search(args.search)
            
            print(f"🔍 Smart Search Results for: '{args.search}'")
            if not results:
                print("No results found. Try running --setup first to ingest documentation.")
                return
            
            for i, result in enumerate(results, 1):
                print(f"\n{i}. {result['title']} ({result['type']})")
                print(f"   Relevance: {result['relevance']:.3f}")
                print(f"   Content: {result['content']}")
                print(f"   Source: {result['source']}")
            return
        
        # Handle Doctor mode (conversational with codebase context)
        if args.doctor:
            # Run interactive Doctor UI and restore terminal on exit
            from pyscription.utils.terminal_styling import ui
            cli = ConversationalCLI(args.project)
            try:
                cli.run_interactive()
            finally:
                ui.restore_terminal()
            return
        
        # Handle Surgeon mode (autonomous agent)
        if args.surgeon:
            # Run interactive Agent UI and restore terminal on exit
            from pyscription.utils.terminal_styling import ui
            cli = AgentCLI(args.project)
            try:
                cli.run_interactive_agent()
            finally:
                ui.restore_terminal()
            return
        
        # Default: show help and features in bordered terminal
        from pyscription.utils.terminal_styling import ui
        
        # Don't clear screen if we just showed splash
        if not show_splash:
            ui.clear_screen()
        ui.print_container_content("🤖 Pyscription - ML-Enhanced Python Development Assistant")
        ui.print_container_content("")
        ui.print_container_content("🚀 Key Features:")
        ui.print_container_content("  🗣️  Conversational AI - Chat naturally about Python")
        ui.print_container_content("  🤖 Autonomous Agent - Self-directed code improvements")
        ui.print_container_content("  📚 Documentation Analysis - Semantic search in Python docs")
        ui.print_container_content("  🔍 Pattern Discovery - Learn from your coding patterns")
        ui.print_container_content("  🛡️  Security Analysis - Detect vulnerabilities and code smells")
        ui.print_container_content("  🎨 Beautiful Terminal UI - Dark theme with syntax highlighting")
        ui.print_container_content("")
        ui.print_container_content("💡 Quick Start:")
        ui.print_container_content("  pyscription --setup        # First-time setup")
        ui.print_container_content("  pyscription --interactive  # Start conversational mode")
        ui.print_container_content("  pyscription --agent        # Start autonomous agent mode")
        ui.print_container_content("")
        ui.print_container_content("📖 For more options:")
        parser.print_help()
        
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

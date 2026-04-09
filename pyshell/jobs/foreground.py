"""Foreground job execution - Windows compatible"""

import subprocess
import sys
from colors import Colors


def run_foreground(parts, job_table, terminal):
    """Run command in foreground using subprocess (Windows compatible)"""
    if not parts:
        return True
    
    try:
        # Run and wait for completion
        result = subprocess.run(parts)
        
        # Update exit code
        if hasattr(result, 'returncode'):
            terminal.last_exit_code = result.returncode
        
        return result.returncode == 0
        
    except FileNotFoundError:
        print(f"{Colors.RED}Command not found: {parts[0]}{Colors.RESET}")
        return False
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.RESET}")
        return False
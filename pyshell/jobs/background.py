"""Background job execution - Windows compatible"""

import subprocess
import os
from colors import Colors


def run_background(parts, job_table, terminal):
    """Run command in background using subprocess.Popen"""
    if not parts:
        return True
    
    # Remove the '&' if present
    if parts and parts[-1] == '&':
        parts = parts[:-1]
    
    if not parts:
        print(f"{Colors.RED}Error: no command after &{Colors.RESET}")
        return False
    
    # Join command for shell=True (better compatibility on Windows)
    cmd_str = ' '.join(parts)
    
    # Handle null redirection properly for Windows vs Unix
    null_device = 'NUL' if os.name == 'nt' else '/dev/null'
    
    try:
        # Start process without waiting
        process = subprocess.Popen(
            cmd_str,
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0
        )
        
        # Get next job ID
        job_id = job_table.next_id
        
        # Add to job table
        job = job_table.add(process.pid, cmd_str)
        job.add_process(process.pid, parts[0])
        job.process_obj = process  # Store the Popen object for later control
        
        # Print job info like bash does
        print(f"[{job_id}] {process.pid}")
        
        return True
        
    except FileNotFoundError:
        print(f"{Colors.RED}Command not found: {parts[0]}{Colors.RESET}")
        return False
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.RESET}")
        return False
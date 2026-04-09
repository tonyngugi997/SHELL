"""Background job execution - Windows compatible"""

import subprocess
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
    
    # Join command for shell=True on Windows (better compatibility)
    cmd_str = ' '.join(parts)
    
    try:
        # Start process without waiting
        process = subprocess.Popen(
            cmd_str,
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL
        )
        
        # Get next job ID
        job_id = job_table.next_id
        
        # Add to job table
        job = job_table.add(process.pid, cmd_str)
        job.add_process(process.pid, parts[0])
        
        # Print job info
        print(f"[{job_id}] {process.pid}")
        
        return True
        
    except FileNotFoundError:
        print(f"{Colors.RED}Command not found: {parts[0]}{Colors.RESET}")
        return False
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.RESET}")
        return False
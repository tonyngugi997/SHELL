"""Background job execution — shell continues, terminal detached"""

import os
import sys
import signal


def run_background(parts, job_table, terminal):
    """
    Run a command in the background.
    Shell returns immediately. Job can't read from terminal.
    """
    if not parts:
        return True
    
    # Remove the '&' from arguments if present
    if parts and parts[-1] == '&':
        parts = parts[:-1]
    
    if not parts:
        return True
    
    # Fork a child process
    pid = os.fork()
    
    if pid == 0:
        # ----- CHILD PROCESS -----
        # Create new process group
        os.setpgid(0, 0)
        
        # Redirect stdin to /dev/null (so background job can't read keyboard)
        devnull = open(os.devnull, 'r')
        os.dup2(devnull.fileno(), 0)
        devnull.close()
        
        # Reset signal handlers
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        signal.signal(signal.SIGTSTP, signal.SIG_DFL)
        signal.signal(signal.SIGCONT, signal.SIG_DFL)
        
        # Execute the command
        try:
            os.execvp(parts[0], parts)
        except FileNotFoundError:
            sys.exit(127)
        except Exception:
            sys.exit(1)
    
    else:
        # ----- PARENT PROCESS (SHELL) -----
        # Put child in its own process group
        os.setpgid(pid, pid)
        
        # Add to job table
        job = job_table.add(pid, ' '.join(parts))
        job.add_process(pid, parts[0])
        
        # Print job info (like bash does)
        print(f"[{job.job_id}] {pid}")
        
        # Don't wait — shell returns immediately
        return True
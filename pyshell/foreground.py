"""Foreground job execution — shell waits, terminal attached"""

import os
import sys
import signal


def run_foreground(parts, job_table, terminal):
    """
    Run a command in the foreground.
    Shell waits for completion. Terminal signals go to the job.
    """
    if not parts:
        return True
    
    # Fork a child process
    pid = os.fork()
    
    if pid == 0:
        # ----- CHILD PROCESS -----
        # Create new process group (child becomes group leader)
        os.setpgid(0, 0)
        
        # Reset signal handlers to default (shell's handlers don't apply)
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
        
        # Wait for child (simple wait for now, will add signal handling later)
        try:
            wpid, status = os.waitpid(pid, 0)
        except ChildProcessError:
            pass
        
        return True
"""SignalHandler - handles SIGCHLD to track child processes"""

import os
import signal


class SignalHandler:
    """Manages SIGCHLD signal to track when child processes change state"""
    
    def __init__(self, job_table):
        self.job_table = job_table
        self.old_handler = None
        self.is_windows = os.name == 'nt'
    
    def setup(self):
        """Install the SIGCHLD handler (Unix only)"""
        if self.is_windows:
            return  # No SIGCHLD on Windows
        self.old_handler = signal.signal(signal.SIGCHLD, self._handler)
    
    def restore(self):
        """Restore the original signal handler"""
        if self.is_windows:
            return
        if self.old_handler:
            signal.signal(signal.SIGCHLD, self.old_handler)
    
    def _handler(self, sig, frame):
        """Called when any child process changes state"""
        if self.is_windows:
            return
        
        while True:
            try:
                pid, status = os.waitpid(-1, os.WNOHANG | os.WUNTRACED)
                
                if pid == 0:
                    break
                
                if os.WIFSTOPPED(status):
                    self.job_table.update_state(pid, stopped=True)
                elif os.WIFEXITED(status) or os.WIFSIGNALED(status):
                    exit_code = 0
                    if os.WIFEXITED(status):
                        exit_code = os.WEXITSTATUS(status)
                    elif os.WIFSIGNALED(status):
                        exit_code = 128 + os.WTERMSIG(status)
                    self.job_table.update_state(pid, stopped=False, exit_code=exit_code)
                    
            except ChildProcessError:
                break
            except Exception:
                break
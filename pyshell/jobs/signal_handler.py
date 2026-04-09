"""SignalHandler - tracks child processes (Windows compatible)"""

import os
import threading
import time
from colors import Colors


class SignalHandler:
    """Manages child process tracking (uses polling on Windows)"""
    
    def __init__(self, job_table):
        self.job_table = job_table
        self.is_windows = os.name == 'nt'
        self.running = True
        self._poll_thread = None
    
    def setup(self):
        """Start tracking child processes"""
        if self.is_windows:
            # Windows: start polling thread
            self.running = True
            self._poll_thread = threading.Thread(target=self._poll_processes, daemon=True)
            self._poll_thread.start()
        else:
            # Unix: use SIGCHLD handler
            import signal
            signal.signal(signal.SIGCHLD, self._handler)
    
    def restore(self):
        """Stop tracking"""
        self.running = False
    
    def _poll_processes(self):
        """Poll for finished processes (Windows)"""
        while self.running:
            try:
                import subprocess
                # Check all jobs
                for job in list(self.job_table.jobs.values()):
                    for pid, _ in job.processes:
                        # Check if process still running
                        try:
                            import ctypes
                            kernel32 = ctypes.windll.kernel32
                            handle = kernel32.OpenProcess(0x1000, False, pid)
                            if handle:
                                exit_code = ctypes.c_ulong()
                                kernel32.GetExitCodeProcess(handle, ctypes.byref(exit_code))
                                kernel32.CloseHandle(handle)
                                if exit_code.value != 259:  # STILL_ACTIVE
                                    # Process finished
                                    self.job_table.update_state(pid, stopped=False, exit_code=exit_code.value)
                        except:
                            # Process doesn't exist
                            self.job_table.update_state(pid, stopped=False, exit_code=0)
            except:
                pass
            time.sleep(0.5)  # Check every 500ms
    
    def _handler(self, sig, frame):
        """Unix SIGCHLD handler"""
        while True:
            try:
                pid, status = os.waitpid(-1, os.WNOHANG | os.WUNTRACED)
                if pid == 0:
                    break
                if os.WIFEXITED(status) or os.WIFSIGNALED(status):
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
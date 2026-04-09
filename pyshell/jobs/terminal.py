"""TerminalController - low-level terminal control for job management"""

import os
import sys
import signal


class TerminalController:
    """Controls terminal foreground/background and signal sending"""
    
    def __init__(self):
        # Save shell's process group (works on Unix, safe fallback on Windows)
        try:
            self.shell_pgid = os.getpgrp()
        except AttributeError:
            # Windows doesn't have process groups
            self.shell_pgid = os.getpid()
        
        self.stdin_fd = sys.stdin.fileno()
        self.is_windows = os.name == 'nt'
    
    def set_foreground(self, pgid: int):
        """Move a process group to the foreground (Unix only)"""
        if self.is_windows:
            return  # Not supported on Windows
        try:
            os.tcsetpgrp(self.stdin_fd, pgid)
        except OSError:
            pass
    
    def set_shell_foreground(self):
        """Move shell back to foreground (Unix only)"""
        if self.is_windows:
            return
        try:
            os.tcsetpgrp(self.stdin_fd, self.shell_pgid)
        except OSError:
            pass
    
    def create_process_group(self, pid: int):
        """Put a process in its own process group (Unix only)"""
        if self.is_windows:
            return
        try:
            os.setpgid(pid, pid)
        except OSError:
            pass
    
    def join_process_group(self, pid: int, pgid: int):
        """Make a process join an existing process group (Unix only)"""
        if self.is_windows:
            return
        try:
            os.setpgid(pid, pgid)
        except OSError:
            pass
    
    def send_signal_to_group(self, pgid: int, sig: int):
        """Send a signal to an entire process group (Unix only)"""
        if self.is_windows:
            # On Windows, send to individual process
            try:
                os.kill(pgid, sig)
            except OSError:
                pass
            return
        try:
            os.kill(-pgid, sig)  # Negative PID = process group
        except OSError:
            pass
    
    def send_signal_to_pid(self, pid: int, sig: int):
        """Send a signal to a single process"""
        try:
            os.kill(pid, sig)
        except OSError:
            pass
    
    def is_foreground(self, pgid: int) -> bool:
        """Check if a process group is in foreground (Unix only)"""
        if self.is_windows:
            return True  # On Windows, assume foreground
        try:
            fg = os.tcgetpgrp(self.stdin_fd)
            return fg == pgid
        except OSError:
            return False
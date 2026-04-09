"""TerminalController - low-level terminal control for job management"""

import os
import sys
import signal


class TerminalController:
    """Controls terminal foreground/background and signal sending"""
    
    def __init__(self):
        self.shell_pgid = os.getpgrp()  # Save shell's process group
        self.stdin_fd = sys.stdin.fileno()
    
    def set_foreground(self, pgid: int):
        """Move a process group to the foreground"""
        try:
            os.tcsetpgrp(self.stdin_fd, pgid)
        except OSError:
            # Not a terminal or already in foreground
            pass
    
    def set_shell_foreground(self):
        """Move shell back to foreground"""
        try:
            os.tcsetpgrp(self.stdin_fd, self.shell_pgid)
        except OSError:
            pass
    
    def create_process_group(self, pid: int):
        """Put a process in its own process group"""
        try:
            os.setpgid(pid, pid)
        except OSError:
            pass
    
    def join_process_group(self, pid: int, pgid: int):
        """Make a process join an existing process group (for pipelines)"""
        try:
            os.setpgid(pid, pgid)
        except OSError:
            pass
    
    def send_signal_to_group(self, pgid: int, sig: int):
        """Send a signal to an entire process group"""
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
        """Check if a process group is in foreground"""
        try:
            fg = os.tcgetpgrp(self.stdin_fd)
            return fg == pgid
        except OSError:
            return False
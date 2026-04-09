"""SignalHandler - handles SIGCHLD to track child processes"""

import os
import signal


class SignalHandler:
    """Manages SIGCHLD signal to track when child processes change state"""
    
    def __init__(self, job_table):
        self.job_table = job_table
        self.old_handler = None
    
    def setup(self):
        """Install the SIGCHLD handler"""
        self.old_handler = signal.signal(signal.SIGCHLD, self._handler)
    
    def restore(self):
        """Restore the original signal handler"""
        if self.old_handler:
            signal.signal(signal.SIGCHLD, self.old_handler)
    
    def _handler(self, sig, frame):
        """Called when any child process changes state (exits, stops, continues)"""
        # We'll fill this in later
        pass
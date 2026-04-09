"""SignalHandler - manages job status and cleanup"""

import threading
import time
import signal
import sys
from colors import Colors


class SignalHandler:
    def __init__(self, job_table):
        self.job_table = job_table
        self.is_windows = os.name == 'nt'
        self.running = True
        self._poll_thread = None
        self._original_sigint = None
        self._original_sigtstp = None
    
    def setup(self):
        """Setup signal handlers (Unix) or polling thread (Windows)"""
        if self.is_windows:
            # Windows: use polling thread
            self.running = True
            self._poll_thread = threading.Thread(target=self._poll_processes, daemon=True)
            self._poll_thread.start()
        else:
            # Unix: setup real signal handlers
            self._original_sigint = signal.signal(signal.SIGINT, self._handle_sigint)
            self._original_sigtstp = signal.signal(signal.SIGTSTP, self._handle_sigtstp)
    
    def restore(self):
        """Restore original signal handlers"""
        if not self.is_windows:
            if self._original_sigint:
                signal.signal(signal.SIGINT, self._original_sigint)
            if self._original_sigtstp:
                signal.signal(signal.SIGTSTP, self._original_sigtstp)
        else:
            self.running = False
            if self._poll_thread:
                self._poll_thread.join(timeout=1.0)
    
    def _handle_sigint(self, signum, frame):
        """Handle Ctrl+C - send to foreground process group"""
        print(f"\n{Colors.RESET}", end='')
        # In a real shell, we'd forward SIGINT to the foreground job
        # For now, just show a new prompt
        sys.stdout.write(f"\n{Colors.RED}^C{Colors.RESET}\n")
        # Don't exit the shell itself
    
    def _handle_sigtstp(self, signum, frame):
        """Handle Ctrl+Z - stop foreground job"""
        print(f"\n{Colors.RESET}", end='')
        sys.stdout.write(f"\n{Colors.YELLOW}^Z{Colors.RESET}\n")
        # In a real shell, we'd stop the foreground job
        # For now, just show a new prompt
    
    def _poll_processes(self):
        """Poll for finished processes (Windows only)"""
        while self.running:
            try:
                for job_id, job in list(self.job_table.jobs.items()):
                    if hasattr(job, 'process_obj') and job.process_obj:
                        # Check if process has finished
                        poll = job.process_obj.poll()
                        if poll is not None and job.state != "terminated":
                            # Process finished - update its state
                            job.terminate(poll)
                            # Don't remove immediately - let jobs command show it first
                            
                            # Print notification like bash does
                            if job.state == "terminated":
                                if poll == 0:
                                    status = "Done"
                                else:
                                    status = f"Done({poll})"
                                # Only print if shell is at prompt (simplified)
                                print(f"\n{Colors.DIM}[{job.job_id}]  {status}  {job.command}{Colors.RESET}")
                                # Print new prompt marker
                                print(f"{Colors.GREEN}┌─{Colors.CYAN}[...]{Colors.GREEN}─┘{Colors.RESET}")
            except Exception as e:
                # Silently ignore errors during polling
                pass
            time.sleep(0.5)  # Poll every 500ms
    
    def check_finished_jobs(self):
        """Check for finished jobs and update their status"""
        for job_id, job in list(self.job_table.jobs.items()):
            if hasattr(job, 'process_obj') and job.process_obj:
                poll = job.process_obj.poll()
                if poll is not None and job.state != "terminated":
                    job.terminate(poll)
    
    def wait_for_job(self, job):
        """Wait for a specific job to complete"""
        if hasattr(job, 'process_obj') and job.process_obj:
            try:
                returncode = job.process_obj.wait()
                job.terminate(returncode)
                return returncode
            except Exception:
                return -1
        return None
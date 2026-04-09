"""Job class - represents one command or pipeline"""

class Job:
    """Represents a job (one command or pipeline with optional &)"""
    
    def __init__(self, job_id: int, pgid: int, command: str):
        self.job_id = job_id          # 1, 2, 3...
        self.pgid = pgid              # Process group ID (same for all processes in pipeline)
        self.command = command        # Original command string
        self.processes = []           # List of (pid, cmd_part)
        self.state = "running"        # running, stopped, terminated
        self.exit_code = None         # Exit code when finished
    
    def add_process(self, pid: int, cmd_part: str):
        """Add a process to this job (for pipelines)"""
        self.processes.append((pid, cmd_part))
    
    def stop(self):
        """Mark job as stopped (Ctrl+Z)"""
        self.state = "stopped"
    
    def resume(self):
        """Mark job as running again (fg/bg)"""
        self.state = "running"
    
    def terminate(self, exit_code: int = 0):
        """Mark job as terminated"""
        self.state = "terminated"
        self.exit_code = exit_code
    
    def is_complete(self) -> bool:
        """Check if all processes in job have finished"""
        # This will be filled in later when we track process status
        return self.state == "terminated"
    
    def __repr__(self) -> str:
        return f"Job({self.job_id}, pgid={self.pgid}, state={self.state}, cmd={self.command[:50]})"
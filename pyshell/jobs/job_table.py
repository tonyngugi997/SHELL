"""JobTable - manages all active jobs"""

from .job import Job


class JobTable:
    """Manages all jobs created by the shell"""
    
    def __init__(self):
        self.jobs = {}          # job_id -> Job
        self.next_id = 1
        self.current_job = None   # Last job stopped or backgrounded (%+ or %%)
        self.previous_job = None  # Second last job (%-)
    
    def add(self, pgid: int, command: str) -> Job:
        """Add a new job to the table"""
        job = Job(self.next_id, pgid, command)
        self.jobs[self.next_id] = job
        
        # Update current/previous tracking
        self.previous_job = self.current_job
        self.current_job = job
        
        self.next_id += 1
        return job
    
    def remove(self, job_id: int):
        """Remove a job from the table (job finished)"""
        if job_id in self.jobs:
            del self.jobs[job_id]
            # Update current/previous if needed
            if self.current_job and self.current_job.job_id == job_id:
                self.current_job = None
            # Don't reset next_id — it only increases
    
    def get(self, job_id: int) -> Job | None:
        """Get job by ID"""
        return self.jobs.get(job_id)
    
    def get_by_pgid(self, pgid: int) -> Job | None:
        """Find job by process group ID"""
        for job in self.jobs.values():
            if job.pgid == pgid:
                return job
        return None
    
    def get_by_pid(self, pid: int) -> Job | None:
        """Find job containing a specific PID"""
        for job in self.jobs.values():
            for p, _ in job.processes:
                if p == pid:
                    return job
        return None
    
    def update_state(self, pid: int, stopped: bool = False, exit_code: int = 0):
        """Update job state based on child process status"""
        job = self.get_by_pid(pid)
        if job:
            if stopped:
                job.stop()
            else:
                # Check if all processes in job are done
                # For now, assume single-process jobs
                job.terminate(exit_code)
                self.remove(job.job_id)
    
    def get_job_from_ref(self, ref: str) -> Job | None:
        """Parse %1, %+, %%, %- references"""
        if not ref.startswith('%'):
            return None
        
        if ref in ('%+', '%%'):
            return self.current_job
        if ref == '%-':
            return self.previous_job
        
        # %1, %2, etc.
        try:
            job_id = int(ref[1:])
            return self.get(job_id)
        except ValueError:
            return None
    
    def list_all(self) -> list:
        """Return all jobs"""
        return list(self.jobs.values())
    
    def __len__(self) -> int:
        return len(self.jobs)
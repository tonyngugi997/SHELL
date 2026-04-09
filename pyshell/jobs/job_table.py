"""JobTable - manages all jobs"""

from .jobs import Job


class JobTable:
    def __init__(self):
        self.jobs = {}
        self.next_id = 1
        self.current_job = None
        self.previous_job = None
    
    def add(self, pgid, command):
        job = Job(self.next_id, pgid, command)
        self.jobs[self.next_id] = job
        self._update_job_references(job)
        self.next_id += 1
        return job
    
    def _update_job_references(self, job):
        """Update current and previous job references"""
        # Shift current to previous, set new current
        if self.current_job and self.current_job.job_id != job.job_id:
            self.previous_job = self.current_job
        self.current_job = job
    
    def remove(self, job_id):
        """Remove a job from the table"""
        if job_id in self.jobs:
            job_to_remove = self.jobs[job_id]
            
            # Update current/previous references
            if self.current_job and self.current_job.job_id == job_id:
                # Find the next most recent job as current
                remaining_jobs = [j for jid, j in self.jobs.items() if jid != job_id]
                if remaining_jobs:
                    # Get the job with highest ID (most recent)
                    self.current_job = max(remaining_jobs, key=lambda j: j.job_id)
                    # Update previous to the second most recent
                    remaining_except_current = [j for j in remaining_jobs if j.job_id != self.current_job.job_id]
                    if remaining_except_current:
                        self.previous_job = max(remaining_except_current, key=lambda j: j.job_id)
                    else:
                        self.previous_job = None
                else:
                    self.current_job = None
                    self.previous_job = None
            elif self.previous_job and self.previous_job.job_id == job_id:
                self.previous_job = None
            
            del self.jobs[job_id]
    
    def get(self, job_id):
        return self.jobs.get(job_id)
    
    def get_by_pid(self, pid):
        for job in self.jobs.values():
            for p, _ in job.processes:
                if p == pid:
                    return job
        return None
    
    def get_job_from_ref(self, ref):
        """Parse job reference like %, %1, %+, %-, %%"""
        if not ref:
            return self.current_job
        
        if ref in ('%+', '%%', '%'):
            return self.current_job
        if ref == '%-':
            return self.previous_job
        if ref.startswith('%'):
            try:
                job_id = int(ref[1:])
                return self.get(job_id)
            except ValueError:
                return None
        return None
    
    def list_all(self):
        """Return all jobs sorted by job_id (oldest first)"""
        return sorted(self.jobs.values(), key=lambda j: j.job_id)
    
    def cleanup_finished_jobs(self):
        """Remove jobs that have been marked for cleanup"""
        to_remove = []
        for job_id, job in self.jobs.items():
            if hasattr(job, '_cleanup_ready') and job._cleanup_ready:
                to_remove.append(job_id)
        
        for job_id in to_remove:
            self.remove(job_id)
    
    def __len__(self):
        return len(self.jobs)
    
    def __str__(self):
        return f"JobTable({len(self.jobs)} jobs, current={self.current_job.job_id if self.current_job else None})"
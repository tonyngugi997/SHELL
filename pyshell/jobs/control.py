"""Job control commands: fg, bg, jobs, kill"""

import os
import signal
import subprocess
from colors import Colors


def jobs_cmd(args, utils, job_table):
    """List all jobs (like bash's jobs command)"""
    # First, update status of all jobs
    for job_id, job in job_table.jobs.items():
        if hasattr(job, 'process_obj') and job.process_obj:
            poll = job.process_obj.poll()
            if poll is not None and job.state != "terminated":
                # Job has finished
                job.terminate(poll)
    
    jobs = job_table.list_all()
    
    if not jobs:
        # No jobs - no output (bash doesn't print anything)
        return True
    
    for job in jobs:
        # Determine status and formatting like bash
        if job.state == "terminated":
            if job.exit_code == 0:
                status = "Done"
            else:
                status = f"Done({job.exit_code})"
            color = Colors.DIM
        elif job.state == "stopped":
            status = "Stopped"
            color = Colors.YELLOW
        else:  # running
            status = "Running"
            color = Colors.GREEN
        
        # Marker for current/previous job (like bash: + and -)
        marker = ""
        if job_table.current_job and job_table.current_job.job_id == job.job_id:
            marker = "+"
        elif job_table.previous_job and job_table.previous_job.job_id == job.job_id:
            marker = "-"
        
        # Format like bash: [1]+  Running  ping 127.0.0.1 &
        print(f"[{job.job_id}]{marker}  {color}{status}{Colors.RESET}  {job.command}")
    
    # Mark finished jobs for cleanup (but don't remove yet)
    for job_id, job in job_table.jobs.items():
        if job.state == "terminated" and not hasattr(job, '_cleanup_ready'):
            # First time showing this finished job
            job._cleanup_ready = True
    
    return True


def fg(args, utils, job_table, terminal):
    """Bring a job to the foreground"""
    # Parse job specification
    if not args:
        job = job_table.current_job
    else:
        job = job_table.get_job_from_ref(args[0])
    
    if not job:
        print(f"{Colors.RED}fg: job not found{Colors.RESET}")
        return False
    
    # Check if job is still running
    if hasattr(job, 'process_obj') and job.process_obj:
        poll = job.process_obj.poll()
        if poll is not None:
            print(f"{Colors.RED}fg: job has already finished{Colors.RESET}")
            job_table.remove(job.job_id)
            return False
    
    print(f"{Colors.YELLOW}fg: {job.command}{Colors.RESET}")
    
    # On Unix-like systems, we would bring to foreground
    # On Windows, we just wait for it
    if hasattr(job, 'process_obj') and job.process_obj:
        try:
            # Wait for the process to complete
            job.process_obj.wait()
            job.terminate(job.process_obj.returncode)
            print(f"{Colors.DIM}[{job.job_id}]  Done  {job.command}{Colors.RESET}")
            job_table.remove(job.job_id)
        except Exception as e:
            print(f"{Colors.RED}Error: {e}{Colors.RESET}")
            return False
    
    return True


def bg(args, utils, job_table, terminal):
    """Resume a stopped job in the background"""
    if not args:
        job = job_table.current_job
    else:
        job = job_table.get_job_from_ref(args[0])
    
    if not job:
        print(f"{Colors.RED}bg: job not found{Colors.RESET}")
        return False
    
    if job.state != "stopped":
        print(f"{Colors.YELLOW}bg: job {job.job_id} is already running{Colors.RESET}")
        return True
    
    print(f"{Colors.YELLOW}bg: {job.command}{Colors.RESET}")
    
    # On Windows, we can't easily resume stopped processes
    # Mark as running and continue
    job.resume()
    return True


def kill_cmd(args, utils, job_table, terminal):
    """Terminate a job or process (like kill %1)"""
    if not args:
        print(f"{Colors.RED}kill: usage: kill <job_id>{Colors.RESET}")
        return False
    
    target = args[0]
    
    # Parse job reference
    if target.startswith('%'):
        job = job_table.get_job_from_ref(target)
        if not job:
            print(f"{Colors.RED}kill: job {target} not found{Colors.RESET}")
            return False
        
        # Terminate the job's process
        if hasattr(job, 'process_obj') and job.process_obj:
            try:
                job.process_obj.terminate()
                print(f"[{job.job_id}]  Terminated  {job.command}")
                job.terminate(-1)  # Mark as terminated with signal
                job_table.remove(job.job_id)
                return True
            except Exception as e:
                print(f"{Colors.RED}kill: error: {e}{Colors.RESET}")
                return False
        else:
            print(f"{Colors.RED}kill: cannot terminate job {job.job_id}{Colors.RESET}")
            return False
    else:
        # Try to kill by PID
        try:
            pid = int(target)
            if os.name == 'nt':  # Windows
                subprocess.run(f'taskkill /PID {pid} /F', shell=True, capture_output=True)
            else:  # Unix
                os.kill(pid, signal.SIGTERM)
            print(f"Terminated process {pid}")
            return True
        except ValueError:
            print(f"{Colors.RED}kill: invalid argument: {target}{Colors.RESET}")
            return False
        except Exception as e:
            print(f"{Colors.RED}kill: error: {e}{Colors.RESET}")
            return False
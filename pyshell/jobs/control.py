"""Job control commands: fg, bg, jobs, kill"""

import os
import signal
from colors import Colors


def jobs_cmd(args, utils, job_table):
    """List all active jobs"""
    jobs = job_table.list_all()
    
    if not jobs:
        print(f"{Colors.DIM}No active jobs{Colors.RESET}")
        return True
    
    for job in jobs:
        # Determine color based on state
        if job.state == "running":
            state_color = Colors.GREEN
        elif job.state == "stopped":
            state_color = Colors.YELLOW
        else:
            state_color = Colors.RED
        
        # Marker for current/previous job
        marker = ""
        if job_table.current_job and job_table.current_job.job_id == job.job_id:
            marker = "+"
        elif job_table.previous_job and job_table.previous_job.job_id == job.job_id:
            marker = "-"
        
        print(f"[{job.job_id}]{marker}  {state_color}{job.state}{Colors.RESET}  {job.command}")
    
    return True


def fg(args, utils, job_table, terminal):
    """Bring a job to the foreground"""
    if not args:
        job = job_table.current_job
    else:
        job = job_table.get_job_from_ref(args[0])
    
    if not job:
        print(f"{Colors.RED}fg: job not found{Colors.RESET}")
        return False
    
    print(f"{job.command}")
    
    if terminal.is_windows:
        print(f"{Colors.YELLOW}fg: limited support on Windows (use kill to terminate){Colors.RESET}")
        return True
    
    # Unix: move to foreground
    terminal.set_foreground(job.pgid)
    
    if job.state == "stopped":
        terminal.send_signal_to_group(job.pgid, signal.SIGCONT)
        job.resume()
    
    # Wait for job to finish or stop
    exit_code = 0
    while True:
        try:
            pid, status = os.waitpid(-job.pgid, 0)
            if os.WIFEXITED(status):
                exit_code = os.WEXITSTATUS(status)
                job_table.remove(job.job_id)
                break
            elif os.WIFSIGNALED(status):
                exit_code = 128 + os.WTERMSIG(status)
                job_table.remove(job.job_id)
                break
            elif os.WIFSTOPPED(status):
                job.stop()
                break
        except ChildProcessError:
            break
    
    terminal.set_shell_foreground()
    utils.last_exit_code = exit_code
    return exit_code == 0


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
    
    if terminal.is_windows:
        print(f"{Colors.YELLOW}bg: not supported on Windows (processes run independently){Colors.RESET}")
        return True
    
    terminal.send_signal_to_group(job.pgid, signal.SIGCONT)
    job.resume()
    print(f"[{job.job_id}] {job.command}")
    return True


def kill_cmd(args, utils, job_table, terminal):
    """Terminate a job or process"""
    if not args:
        print(f"{Colors.RED}kill: usage: kill <job_id> or <PID>{Colors.RESET}")
        return False
    
    target = args[0]
    
    # Job reference: %1, %+, %%, %-
    if target.startswith('%'):
        job = job_table.get_job_from_ref(target)
        if not job:
            print(f"{Colors.RED}kill: job not found: {target}{Colors.RESET}")
            return False
        
        # Kill all processes in the job
        for pid, _ in job.processes:
            terminal.send_signal_to_pid(pid, signal.SIGTERM)
        
        # Remove from job table
        job_table.remove(job.job_id)
        print(f"Terminated job {job.job_id}")
        return True
    
    # PID
    try:
        pid = int(target)
        terminal.send_signal_to_pid(pid, signal.SIGTERM)
        job_table.update_state(pid, stopped=False, exit_code=143)
        print(f"Terminated process {pid}")
        return True
    except ValueError:
        print(f"{Colors.RED}kill: invalid argument: {target}{Colors.RESET}")
        return False
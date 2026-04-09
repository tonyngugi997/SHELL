"""Professional job display – ASCII-safe, works on any terminal"""

import os
import time
import signal
import psutil
from datetime import datetime
from rich.live import Live
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.console import Console
from rich.align import Align
from rich import box

console = Console(force_terminal=True)  # Force terminal mode even on Windows
import colorama
colorama.init()

class JobDisplay:
    """Robust job dashboard with ASCII borders and no icons"""

    def __init__(self, job_table):
        self.job_table = job_table
        self.console = Console()
        self.watch_mode_active = False



    def _get_brand_header(self):
        """Generate an advanced brand header (ASCII art + metadata)"""
        from datetime import datetime
        from colors import Colors

        header_lines = [
            "",
            f"{Colors.CYAN}╔══════════════════════════════════════════════════════════════════════════╗{Colors.RESET}",
            f"{Colors.CYAN}║{Colors.RESET}  {Colors.BOLD}{Colors.BRIGHT_WHITE}██████╗ ██╗   ██╗███████╗██╗  ██╗███████╗██╗     ██╗{Colors.RESET}      {Colors.CYAN}║{Colors.RESET}",
            f"{Colors.CYAN}║{Colors.RESET}  {Colors.BOLD}{Colors.BRIGHT_WHITE}██╔══██╗╚██╗ ██╔╝██╔════╝██║  ██║██╔════╝██║     ██║{Colors.RESET}      {Colors.CYAN}║{Colors.RESET}",
            f"{Colors.CYAN}║{Colors.RESET}  {Colors.BOLD}{Colors.BRIGHT_WHITE}██████╔╝ ╚████╔╝ ███████╗███████║█████╗  ██║     ██║{Colors.RESET}      {Colors.CYAN}║{Colors.RESET}",
            f"{Colors.CYAN}║{Colors.RESET}  {Colors.BOLD}{Colors.BRIGHT_WHITE}██╔═══╝   ╚██╔╝  ╚════██║██╔══██║██╔══╝  ██║     ██║{Colors.RESET}      {Colors.CYAN}║{Colors.RESET}",
            f"{Colors.CYAN}║{Colors.RESET}  {Colors.BOLD}{Colors.BRIGHT_WHITE}██║        ██║   ███████║██║  ██║███████╗███████╗███████╗{Colors.RESET}{Colors.CYAN}║{Colors.RESET}",
            f"{Colors.CYAN}║{Colors.RESET}  {Colors.BOLD}{Colors.BRIGHT_WHITE}╚═╝        ╚═╝   ╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝{Colors.RESET}{Colors.CYAN}║{Colors.RESET}",
            f"{Colors.CYAN}╠══════════════════════════════════════════════════════════════════════════╣{Colors.RESET}",
            f"{Colors.CYAN}║{Colors.RESET}  {Colors.BRIGHT_YELLOW}Advanced Job Control{Colors.RESET}              {Colors.DIM}v2.0 | {datetime.now().strftime('%Y-%m-%d')}{Colors.RESET}  {Colors.CYAN}║{Colors.RESET}",
            f"{Colors.CYAN}╚══════════════════════════════════════════════════════════════════════════╝{Colors.RESET}",
            ""
        ]
        return "\n".join(header_lines)




    def _get_process_info(self, pid):
        try:
            import psutil
            proc = psutil.Process(pid)
            cpu = proc.cpu_percent(interval=0.1)
            mem = proc.memory_info().rss / (1024 * 1024)
            create_time = proc.create_time()
            runtime = time.time() - create_time
            return {'cpu': cpu, 'mem': mem, 'runtime': runtime, 'exists': True}
        except:
            return {'exists': False}

    def _format_runtime(self, seconds):
        if seconds < 60:
            return f"{seconds:.1f}s"
        elif seconds < 3600:
            mins = int(seconds // 60)
            secs = int(seconds % 60)
            return f"{mins}m {secs}s"
        else:
            hours = int(seconds // 3600)
            mins = int((seconds % 3600) // 60)
            return f"{hours}h {mins}m"

    def _get_status_ascii(self, job):
        """ASCII-only status markers"""
        if job.state == "terminated":
            if job.exit_code == 0:
                return "[OK] Done", "green"
            else:
                return f"[!!] Failed({job.exit_code})", "red"
        elif job.state == "stopped":
            return "[||] Stopped", "yellow"
        elif job.state == "running":
            return "[>] Running", "green"
        else:
            return "[?] Unknown", "magenta"

    def generate_table(self):
        # Update job states
        for job in self.job_table.list_all():
            if hasattr(job, 'process_obj') and job.process_obj:
                poll = job.process_obj.poll()
                if poll is not None and job.state != "terminated":
                    job.terminate(poll)

        jobs = self.job_table.list_all()
        if not jobs:
            return Panel("[dim]No active jobs[/]", title=" Jobs Dashboard ", border_style="blue", box=box.ASCII2)

        table = Table(
            title=" Jobs Dashboard ",
            box=box.ASCII2,        
            border_style="cyan",
            header_style="bold cyan",
            show_lines=True,         
            show_edge=True,           
            safe_box=True,            
            expand=False,             
            width=min(120, console.size.width)  
        )

        table.add_column("JOB", justify="right", style="dim", width=6, no_wrap=True)
        table.add_column("STATUS", justify="left", width=12, no_wrap=True)
        table.add_column("PID", justify="right", width=8, no_wrap=True)
        table.add_column("EXIT", justify="center", width=6, no_wrap=True)
        table.add_column("RUNTIME", justify="right", width=10, no_wrap=True)
        table.add_column("CPU%", justify="right", width=8, no_wrap=True)
        table.add_column("MEM", justify="right", width=10, no_wrap=True)
        table.add_column("COMMAND", no_wrap=False, max_width=50)

        for job in jobs:
            marker = ""
            if self.job_table.current_job and self.job_table.current_job.job_id == job.job_id:
                marker = "+ "
            elif self.job_table.previous_job and self.job_table.previous_job.job_id == job.job_id:
                marker = "- "
            job_id_str = f"{marker}{job.job_id}"

            status_text, status_color = self._get_status_ascii(job)
            status = f"[{status_color}]{status_text}[/]"

            pid_val = job.process_obj.pid if hasattr(job, 'process_obj') and job.process_obj else job.pgid
            pid_str = str(pid_val) if pid_val else "-"

            if job.state == "terminated":
                exit_str = f"[green]{job.exit_code}[/]" if job.exit_code == 0 else f"[red]{job.exit_code}[/]"
            else:
                exit_str = "[dim]-[/]"

            if job.state == "running" and hasattr(job, 'process_obj') and job.process_obj:
                info = self._get_process_info(job.process_obj.pid)
                if info['exists']:
                    runtime_str = self._format_runtime(info['runtime'])
                    cpu_val = info['cpu']
                    mem_val = info['mem']
                    if cpu_val < 1:
                        cpu_str = f"[green]{cpu_val:.1f}[/]"
                    elif cpu_val < 10:
                        cpu_str = f"[yellow]{cpu_val:.1f}[/]"
                    else:
                        cpu_str = f"[red]{cpu_val:.1f}[/]"
                    mem_str = f"{mem_val:.1f} MB"
                else:
                    runtime_str = "-"
                    cpu_str = "-"
                    mem_str = "-"
            else:
                runtime_str = "-"
                cpu_str = "-"
                mem_str = "-"

            cmd = job.command
            if len(cmd) > 50:
                cmd = cmd[:47] + "..."

            table.add_row(job_id_str, status, pid_str, exit_str, runtime_str, cpu_str, mem_str, cmd)

        return table


    def display_jobs(self):
        """Single shot display with brand header"""
        console.print(self._get_brand_header())
        table = self.generate_table()
        console.print(table)
        jobs = self.job_table.list_all()
        total = len(jobs)
        running = sum(1 for j in jobs if j.state == "running")
        done = sum(1 for j in jobs if j.state == "terminated")
        stopped = sum(1 for j in jobs if j.state == "stopped")
        footer = f"Total: {total}  ▶ {running} running  ✓ {done} done  ⏸ {stopped} stopped"
        console.print(Align.center(f"[dim]{footer}[/]"))



    def watch_jobs(self):
        self.watch_mode_active = True

        def signal_handler(signum, frame):
            self.watch_mode_active = False
            raise KeyboardInterrupt()

        signal.signal(signal.SIGINT, signal_handler)

        try:
            with Live(console=self.console, screen=True, auto_refresh=False, transient=False) as live:
                while self.watch_mode_active:
                    layout = Layout()
                    layout.split(
                        Layout(name="header", size=12),   # enough for brand header
                        Layout(name="body"),
                        Layout(name="footer", size=3)
                    )
                    # Brand header as a Panel
                    header_content = self._get_brand_header()
                    header = Panel(
                        header_content,
                        border_style="blue",
                        box=box.ASCII2,
                        padding=(0, 1)
                    )
                    body = self.generate_table()
                    footer = Panel(
                        Align.center("[bold yellow]Ctrl+C[/] to exit watch mode", vertical="middle"),
                        border_style="dim",
                        box=box.ASCII2
                    )
                    layout["header"].update(header)
                    layout["body"].update(body)
                    layout["footer"].update(footer)

                    live.update(layout, refresh=True)
                    time.sleep(1.5)
        except KeyboardInterrupt:
            console.print("\n[yellow]Exiting watch mode...[/]")
        finally:
            self.watch_mode_active = False
            signal.signal(signal.SIGINT, signal.SIG_DFL)
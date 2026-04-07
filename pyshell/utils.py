# utils.py
import os
import sys
import subprocess
import re
from datetime import datetime
from colors import Colors

try:
    import readline
    READLINE_AVAILABLE = True
except ImportError:
    READLINE_AVAILABLE = False

HISTORY_FILE = os.path.expanduser("~/.pyshell_history")
MAX_HISTORY = 1000


class ShellUtils:
    def __init__(self):
        self.command_history = []
        self.last_exit_code = 0
        self._load_history()

    def _load_history(self):
        if not READLINE_AVAILABLE:
            return
        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, 'r') as f:
                    for line in f:
                        cmd = line.strip()
                        if cmd:
                            self.command_history.append(cmd)
                            readline.add_history(cmd)
            except (IOError, OSError):
                pass

    def _save_history(self):
        if not READLINE_AVAILABLE:
            return
        try:
            with open(HISTORY_FILE, 'w') as f:
                for cmd in self.command_history[-MAX_HISTORY:]:
                    f.write(cmd + '\n')
        except (IOError, OSError):
            pass

    def add_command(self, command):
        if not command or command.isspace():
            return
        self.command_history.append(command)
        if READLINE_AVAILABLE:
            readline.add_history(command)
        self._save_history()

    def get_history(self, limit=None):
        if limit:
            return self.command_history[-limit:]
        return self.command_history

    def expand_vars(self, cmd):
        def replace_var(match):
            var_name = match.group(1) or match.group(2)
            return os.environ.get(var_name, '')
        pattern = r'\$([A-Za-z_][A-Za-z0-9_]*|\{([A-Za-z_][A-Za-z0-9_]*)\})'
        return re.sub(pattern, replace_var, cmd)

    def fetch_prompt(self):
        user = os.environ.get('USER', os.environ.get('USERNAME', 'user'))
        host = os.environ.get('HOSTNAME', 'localhost')
        cwd = os.getcwd()
        home = os.path.expanduser("~")
        if cwd.startswith(home):
            cwd = "~" + cwd[len(home):]
        timestamp = datetime.now().strftime("%H:%M:%S")

        prompt = f"{Colors.DIM}┌─{Colors.RESET}"
        prompt += f"{Colors.CYAN}[{timestamp}]{Colors.RESET}"
        prompt += f"{Colors.DIM}─{Colors.RESET}"
        prompt += f"{Colors.GREEN}[{user}@{host}]{Colors.RESET}"
        prompt += f"{Colors.DIM}─{Colors.RESET}"
        prompt += f"{Colors.YELLOW}[{cwd}]{Colors.RESET}"

        if self.last_exit_code != 0:
            prompt += f" {Colors.RED}[{self.last_exit_code}]{Colors.RESET}"

        prompt += f"\n{Colors.DIM}└─{Colors.RESET}{Colors.MAGENTA}➤{Colors.RESET} $ "
        return prompt

    def execute_external(self, args):
        try:
            result = subprocess.run(
                args,
                stdin=sys.stdin,
                stdout=sys.stdout,
                stderr=sys.stderr,
                text=True,
                shell=False
            )
            self.last_exit_code = result.returncode
            return result.returncode == 0
        except FileNotFoundError:
            if os.name == 'nt':
                try:
                    result = subprocess.run(
                        ' '.join(args),
                        stdin=sys.stdin,
                        stdout=sys.stdout,
                        stderr=sys.stderr,
                        text=True,
                        shell=True
                    )
                    self.last_exit_code = result.returncode
                    return result.returncode == 0
                except Exception:
                    pass
            print(f"{Colors.RED}Command not found: {args[0]}{Colors.RESET}")
            self.last_exit_code = 127
            return False
        except PermissionError:
            print(f"{Colors.RED}Permission denied: {args[0]}{Colors.RESET}")
            self.last_exit_code = 126
            return False
        except Exception as e:
            print(f"{Colors.RED}Error: {e}{Colors.RESET}")
            self.last_exit_code = 1
            return False
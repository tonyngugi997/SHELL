# utils.py
import os
import sys
import subprocess
import re
from datetime import datetime
from colors import Colors
from redirection import *

HISTORY_FILE = os.path.expanduser("~/.pyshell_history")
MAX_HISTORY = 1000


class ShellUtils:
    def __init__(self):
        self.command_history = []
        self.last_exit_code = 0
        self._load_history()
        self.aliases = {}
        self._load_history()
        self._load_aliases()

    ALIASES_FILE = os.path.expanduser("~/.pyshell_aliases")

    def _load_aliases(self):
        """Load aliases from file"""
        if not os.path.exists(self.ALIASES_FILE):
            return
        try:
            with open(self.ALIASES_FILE, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and '=' in line:
                        name, value = line.split('=', 1)
                        self.aliases[name] = value
        except (IOError, OSError):
            pass

    def _save_aliases(self):
        """Save aliases to file"""
        try:
            with open(self.ALIASES_FILE, 'w') as f:
                for name, value in self.aliases.items():
                    f.write(f"{name}={value}\n")
        except (IOError, OSError):
            pass

    def expand_alias(self, cmd):
        """Expand alias if command matches"""
        parts = cmd.split()
        if not parts:
            return cmd
        first = parts[0]
        if first in self.aliases:
            alias_cmd = self.aliases[first]
            rest = ' '.join(parts[1:]) if len(parts) > 1 else ''
            if rest:
                return f"{alias_cmd} {rest}"
            return alias_cmd
        return cmd


    def _load_history(self):
        if not os.path.exists(HISTORY_FILE):
            return
        try:
            with open(HISTORY_FILE, 'r') as f:
                for line in f:
                    cmd = line.strip()
                    if cmd:
                        self.command_history.append(cmd)
        except (IOError, OSError):
            pass

    def _save_history(self):
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
        """Execute external command with stdin redirection"""
        new_args, stdin_file, stdout_file, stderr_file, append_stdout, append_stderr = RedirectionParser.parse(args)
        
        if new_args is None:
            return False
        
        if not new_args:
            print(f"{Colors.RED}Error: no command specified{Colors.RESET}")
            return False
        
        # Open stdin file if specified
        stdin_handle = None
        if stdin_file:
            stdin_handle = RedirectionParser.open_redirection(stdin_file, is_input=True)
            if stdin_handle is None:
                return False
        
        try:
            result = subprocess.run(
                new_args,
                stdin=stdin_handle or None,
                text=True,
                capture_output=True
            )
            
            # Print output (no file redirection yet)
            if result.stdout:
                print(result.stdout, end='')
            if result.stderr:
                print(f"{Colors.RED}{result.stderr}{Colors.RESET}", end='')
            
            self.last_exit_code = result.returncode
            return result.returncode == 0
            
        except FileNotFoundError:
            print(f"{Colors.RED}Command not found: {new_args[0]}{Colors.RESET}")
            self.last_exit_code = 127
            return False
        except Exception as e:
            print(f"{Colors.RED}Error: {e}{Colors.RESET}")
            self.last_exit_code = 1
            return False
        finally:
            if stdin_handle:
                stdin_handle.close()

    def is_unclosed_quote(self, text):
        """Check if text has unclosed quotes"""
        in_single = False
        in_double = False
        i = 0
        while i < len(text):
            ch = text[i]
            if ch == '\\' and i + 1 < len(text):
                # Skip escaped characters
                i += 2
                continue
            elif ch == "'" and not in_double:
                in_single = not in_single
            elif ch == '"' and not in_single:
                in_double = not in_double
            i += 1
        return in_single or in_double
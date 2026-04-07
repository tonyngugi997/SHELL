#!/usr/bin/env python3
import os
import sys
import shlex
import signal
import subprocess
from datetime import datetime
from pathlib import Path
from tkinter import EXCEPTION

try:
    import readline
    READLINE_AVAILABLE = True
except ImportError:
    READLINE_AVAILABLE = False

# CONFIGURATION

HISTORY_FILE = os.path.expanduser("~/.pyshell_history")
MAX_HISTORY = 1000

# ANSI Colors
class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'

# UTILITIES

class ShellUtils:
    """Utility functions for the shell"""
    
    def __init__(self):
        self.command_history = []
        self.last_exit_code = 0
        self._load_history()
    
    def _load_history(self):
        """Load command history from file"""
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
        """Save command history to file"""
        if not READLINE_AVAILABLE:
            return
        try:
            with open(HISTORY_FILE, 'w') as f:
                for cmd in self.command_history[-MAX_HISTORY:]:
                    f.write(cmd + '\n')
        except (IOError, OSError):
            pass
    
    def add_command(self, command):
        """Add command to history"""
        if not command or command.isspace():
            return
        self.command_history.append(command)
        if READLINE_AVAILABLE:
            readline.add_history(command)
        self._save_history()
    
    def get_history(self, limit=None):
        """Return command history as list"""
        if limit:
            return self.command_history[-limit:]
        return self.command_history
    
    def expand_vars(self, cmd):
        """Expand environment variables in command"""
        import re
        
        def replace_var(match):
            var_name = match.group(1) or match.group(2)
            return os.environ.get(var_name, '')
        
        pattern = r'\$([A-Za-z_][A-Za-z0-9_]*|\{([A-Za-z_][A-Za-z0-9_]*)\})'
        return re.sub(pattern, replace_var, cmd)
    
    def fetch_prompt(self):
        """Generate the shell prompt"""
        user = os.environ.get('USER', os.environ.get('USERNAME', 'user'))
        host = os.environ.get('HOSTNAME', 'localhost')
        cwd = os.getcwd()
        home = os.path.expanduser("~")
        
        if cwd.startswith(home):
            cwd = "~" + cwd[len(home):]
        
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Build prompt
        prompt = f"{Colors.DIM}┌─{Colors.RESET}"
        prompt += f"{Colors.CYAN}[{timestamp}]{Colors.RESET}"
        prompt += f"{Colors.DIM}─{Colors.RESET}"
        prompt += f"{Colors.GREEN}[{user}@{host}]{Colors.RESET}"
        prompt += f"{Colors.DIM}─{Colors.RESET}"
        prompt += f"{Colors.YELLOW}[{cwd}]{Colors.RESET}"
        
        # Show exit code if non-zero
        if self.last_exit_code != 0:
            prompt += f" {Colors.RED}[{self.last_exit_code}]{Colors.RESET}"
        
        prompt += f"\n{Colors.DIM}└─{Colors.RESET}{Colors.MAGENTA}➤{Colors.RESET} $ "
        
        return prompt
    
    def execute_external(self, args):
        """Execute an external command"""
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

# ============================================================================
# BUILTIN COMMANDS
# ============================================================================

class Builtins:
    """Built-in shell commands"""
    
    @staticmethod
    def cmd_exit(args, utils):
        """Exit the shell"""
        print("Goodbye!")
        sys.exit(0)
    
    @staticmethod
    def cmd_echo(args, utils):
        """Print arguments to stdout"""
        print(" ".join(args))
        utils.last_exit_code = 0
        return True
    @staticmethod
    def cmd_ls(args, urils):
        "ls command"
        try:
            if os.name == 'nt':
                subprocess.run("dir", shell=True)       
            else:
                subprocess.run("ls")
        except Exception as e:
            return
        
    
    @staticmethod
    def cmd_cd(args, utils):
        """Change directory"""
        if not args:
            target = os.path.expanduser("~")
        else:
            target = args[0]
            if target == "~":
                target = os.path.expanduser("~")
            elif target == "-":
                target = os.environ.get('OLDPWD', '.')
        
        try:
            old = os.getcwd()
            os.chdir(target)
            os.environ['OLDPWD'] = old
            utils.last_exit_code = 0
            return True
        except FileNotFoundError:
            print(f"{Colors.RED}cd: {target}: No such directory{Colors.RESET}")
            utils.last_exit_code = 1
            return False
        except NotADirectoryError:
            print(f"{Colors.RED}cd: {target}: Not a directory{Colors.RESET}")
            utils.last_exit_code = 1
            return False
        except PermissionError:
            print(f"{Colors.RED}cd: {target}: Permission denied{Colors.RESET}")
            utils.last_exit_code = 1
            return False
    
    @staticmethod
    def cmd_pwd(args, utils):
        """Print working directory"""
        print(os.getcwd())
        utils.last_exit_code = 0
        return True
    
    @staticmethod
    def cmd_history(args, utils):
        """Show command history"""
        limit = None
        if args and args[0].isdigit():
            limit = int(args[0])
        
        history = utils.get_history(limit)
        for i, cmd in enumerate(history, 1):
            print(f"{i:4d}  {cmd}")
        
        utils.last_exit_code = 0
        return True
    
    @staticmethod
    def cmd_clear(args, utils):
        """Clear the screen"""
        os.system('clear' if os.name != 'nt' else 'cls')
        utils.last_exit_code = 0
        return True
    
    @staticmethod
    def cmd_help(args, utils):
        """Show help information"""
        commands = {
            'exit': 'Exit the shell',
            'echo': 'Print text to console',
            'cd': 'Change directory',
            'pwd': 'Print working directory',
            'history': 'Show command history',
            'clear': 'Clear the screen',
            'help': 'Show this help message',
            'ls': 'List contents of a directory'
        }
        
        print(f"\n{Colors.BOLD}Available Commands:{Colors.RESET}\n")
        for cmd, desc in commands.items():
            print(f"  {Colors.GREEN}{cmd:<10}{Colors.RESET} {desc}")
        print(f"\n{Colors.DIM}External commands are also available (ls, cat, grep, etc.){Colors.RESET}\n")
        utils.last_exit_code = 0
        return True
 

# ============================================================================
# MAIN SHELL
# ============================================================================

class ProfessionalShell:
    """Main shell class"""
    
    def __init__(self):
        self.utils = ShellUtils()
        self.builtins = Builtins()
        self.running = True
        
        # Built-in command mapping
        self.builtin_commands = {
            'exit': self.builtins.cmd_exit,
            'quit': self.builtins.cmd_exit,
            'echo': self.builtins.cmd_echo,
            'cd': self.builtins.cmd_cd,
            'pwd': self.builtins.cmd_pwd,
            'history': self.builtins.cmd_history,
            'clear': self.builtins.cmd_clear,
            'cls': self.builtins.cmd_clear,
            'help': self.builtins.cmd_help,
            '?': self.builtins.cmd_help,
            'ls': self.builtins.cmd_ls,

        }
        
        # Setup signal handlers
        signal.signal(signal.SIGINT, self._handle_sigint)
    
    def _handle_sigint(self, sig, frame):
        """Handle Ctrl+C gracefully"""
        print()  # New line
        sys.stdout.write(self.utils.fetch_prompt())
        sys.stdout.flush()
        self.utils.last_exit_code = 130
    
    def _print_banner(self):
        """Display startup banner"""
        os.system('clear' if os.name != 'nt' else 'cls')
        
        width = 60
        border = "═" * (width - 2)
        
        print(f"╔{border}╗")
        print(f"║{'Professional Python Shell v2.0':^{width-2}}║")
        print(f"║{'─' * (width-2):^{width-2}}║")
        print(f"║{'Type \"help\" for commands':^{width-2}}║")
        print(f"║{'Type \"exit\" to quit':^{width-2}}║")
        print(f"╚{border}╝")
        print()
    
    def _parse_pipeline(self, cmd_string):
        """Parse and execute a pipeline (cmd1 | cmd2 | cmd3)"""
        commands = [c.strip() for c in cmd_string.split('|')]
        
        processes = []
        prev_stdout = None
        
        for i, cmd in enumerate(commands):
            try:
                parts = shlex.split(cmd)
            except ValueError as e:
                print(f"{Colors.RED}Error: {e}{Colors.RESET}")
                return False
            
            if not parts:
                continue
            
            # Determine stdin and stdout
            stdin = prev_stdout if prev_stdout else None
            stdout = subprocess.PIPE if i < len(commands) - 1 else None
            
            try:
                proc = subprocess.Popen(
                    parts,
                    stdin=stdin,
                    stdout=stdout,
                    stderr=subprocess.PIPE,
                    text=True,
                    shell=False
                )
                processes.append(proc)
                
                if stdout == subprocess.PIPE:
                    prev_stdout = proc.stdout
                else:
                    prev_stdout = None
                    
            except FileNotFoundError:
                print(f"{Colors.RED}Command not found: {parts[0]}{Colors.RESET}")
                return False
        
        # Get output from last command
        if processes and processes[-1].stdout:
            output, _ = processes[-1].communicate()
            if output:
                print(output, end='')
        
        # Wait for all processes and check exit codes
        success = True
        for proc in processes:
            proc.wait()
            if proc.returncode != 0:
                success = False
        
        self.utils.last_exit_code = 0 if success else 1
        return success
    
    def _execute_pipeline(self, cmd_string):
        """Execute a command that may contain pipes"""
        return self._parse_pipeline(cmd_string)
    
    def _execute_command(self, cmd):
        """Execute a single command (no pipes)"""
        if not cmd or cmd.isspace():
            return True
        
        # Expand environment variables
        cmd = self.utils.expand_vars(cmd)
        
        try:
            parts = shlex.split(cmd)
        except ValueError as e:
            print(f"{Colors.RED}Error: {e}{Colors.RESET}")
            self.utils.last_exit_code = 1
            return False
        
        if not parts:
            return True
        
        command = parts[0].lower()
        args = parts[1:]
        
        # Check if it's a builtin command
        if command in self.builtin_commands:
            return self.builtin_commands[command](args, self.utils)
        
        # Otherwise, execute external command
        return self.utils.execute_external(parts)
    
    def run(self):
        """Main shell loop"""
        self._print_banner()
        
        while self.running:
            try:
                # Get prompt and input
                sys.stdout.write(self.utils.fetch_prompt())
                sys.stdout.flush()
                
                try:
                    cmd = input().strip()
                except EOFError:
                    print("\nGoodbye!")
                    break
                
                # Add to history
                if cmd and not cmd.isspace():
                    self.utils.add_command(cmd)
                
                # Check for pipes
                if '|' in cmd and not (cmd.startswith('"') and '"' in cmd[1:]):
                    self._execute_pipeline(cmd)
                else:
                    self._execute_command(cmd)
                    
            except KeyboardInterrupt:
                # Already handled by signal handler
                continue
            except Exception as e:
                print(f"{Colors.RED}Unexpected error: {e}{Colors.RESET}")
                self.utils.last_exit_code = 1


# ENTRY POINT

def main():
    """Main entry point"""
    try:
        shell = ProfessionalShell()
        shell.run()
    except KeyboardInterrupt:
        print("\nGoodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"{Colors.RED}Fatal error: {e}{Colors.RESET}")
        sys.exit(1)

if __name__ == "__main__":
    main()
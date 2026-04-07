# shell.py
import os
import sys
import shlex
import signal
import subprocess
from colors import Colors
from utils import ShellUtils
from commands import Builtins

# Handle readline for different platforms
READLINE_AVAILABLE = False
try:
    import pyreadline as readline
    READLINE_AVAILABLE = True
except ImportError:
    try:
        import readline
        READLINE_AVAILABLE = True
    except ImportError:
        pass


class ProfessionalShell:
    def __init__(self):
        self.utils = ShellUtils()
        self.builtins = Builtins()
        self.running = True
        self._executor = self._get_executor()

        self.builtin_commands = {
            'exit': self.builtins.cmd_exit,
            'quit': self.builtins.cmd_exit,
            'echo': self.builtins.cmd_echo,
            'ls': self.builtins.cmd_ls,
            'cd': self.builtins.cmd_cd,
            'pwd': self.builtins.cmd_pwd,
            'history': self.builtins.cmd_history,
            'clear': self.builtins.cmd_clear,
            'cls': self.builtins.cmd_clear,
            'help': self.builtins.cmd_help,
            '?': self.builtins.cmd_help,
            'repeat': self.builtins.cmd_repeat,
            'alias': self.builtins.cmd_alias,
            'unalias': self.builtins.cmd_unalias,
        }

        signal.signal(signal.SIGINT, self._handle_sigint)
        
        # Tab completion - only works on Linux/Mac with GNU readline
        if READLINE_AVAILABLE and os.name != 'nt':
            try:
                import rlcompleter
                readline.parse_and_bind("tab: complete")
                print("Tab completion enabled")
            except:
                pass

    def _get_executor(self):
        def executor(cmd_str):
            return self._execute_command(cmd_str)
        return executor

    def _handle_sigint(self, sig, frame):
        print()
        sys.stdout.write(self.utils.fetch_prompt())
        sys.stdout.flush()
        self.utils.last_exit_code = 130

    def _print_banner(self):
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

    def _has_pipe_outside_quotes(self, cmd):
        in_single = False
        in_double = False
        i = 0
        while i < len(cmd):
            ch = cmd[i]
            if ch == "'" and not in_double:
                in_single = not in_single
            elif ch == '"' and not in_single:
                in_double = not in_double
            elif ch == '|' and not (in_single or in_double):
                return True
            i += 1
        return False

    def _parse_pipeline(self, cmd_string):
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

        if processes and processes[-1].stdout:
            output, _ = processes[-1].communicate()
            if output:
                print(output, end='')

        success = True
        for proc in processes:
            proc.wait()
            if proc.returncode != 0:
                success = False

        self.utils.last_exit_code = 0 if success else 1
        return success

    def _execute_pipeline(self, cmd_string):
        return self._parse_pipeline(cmd_string)

    def _execute_command(self, cmd):
        if not cmd or cmd.isspace():
            return True

        # Expand aliases FIRST
        cmd = self.utils.expand_alias(cmd)
        
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

        if command in self.builtin_commands:
            return self.builtin_commands[command](args, self.utils, self._executor)

        return self.utils.execute_external(parts)

    def run(self):
        self._print_banner()

        while self.running:
            try:
                sys.stdout.write(self.utils.fetch_prompt())
                sys.stdout.flush()

                try:
                    cmd = input().strip()
                except EOFError:
                    print("\nGoodbye!")
                    break

                if cmd and not cmd.isspace():
                    self.utils.add_command(cmd)

                if self._has_pipe_outside_quotes(cmd):
                    self._execute_pipeline(cmd)
                else:
                    self._execute_command(cmd)

            except KeyboardInterrupt:
                continue
            except Exception as e:
                print(f"{Colors.RED}Unexpected error: {e}{Colors.RESET}")
                self.utils.last_exit_code = 1

        return self.utils.last_exit_code


if __name__ == "__main__":
    shell = ProfessionalShell()
    sys.exit(shell.run())
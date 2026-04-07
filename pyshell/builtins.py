# pyshell/builtins.py
import os
import sys
import subprocess
from .colors import Colors


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
    def cmd_ls(args, utils):
        """List directory contents (built-in version)"""
        # Build command: 'ls' on Unix, 'dir' on Windows
        if os.name == 'nt':
            cmd = ['cmd', '/c', 'dir']
            # On Windows, we pass args as-is (e.g., /w, /b)
            cmd.extend(args)
        else:
            cmd = ['ls']
            cmd.extend(args)
        try:
            subprocess.run(cmd)
            utils.last_exit_code = 0
        except FileNotFoundError:
            print(f"{Colors.RED}Command not found: {cmd[0]}{Colors.RESET}")
            utils.last_exit_code = 127
        except Exception as e:
            print(f"{Colors.RED}Error: {e}{Colors.RESET}")
            utils.last_exit_code = 1
        return utils.last_exit_code == 0

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
            'ls': 'List directory contents'
        }
        print(f"\n{Colors.BOLD}Available Commands:{Colors.RESET}\n")
        for cmd, desc in commands.items():
            print(f"  {Colors.GREEN}{cmd:<10}{Colors.RESET} {desc}")
        print(f"\n{Colors.DIM}External commands are also available (cat, grep, etc.){Colors.RESET}\n")
        utils.last_exit_code = 0
        return True
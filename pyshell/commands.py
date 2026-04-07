# commands.py
import os
import sys
import subprocess
from colors import Colors


class Builtins:
    @staticmethod
    def cmd_exit(args, utils, executor=None):
        print("Goodbye!")
        sys.exit(0)

    @staticmethod
    def cmd_echo(args, utils, executor=None):
        print(" ".join(args))
        utils.last_exit_code = 0
        return True

    @staticmethod
    def cmd_ls(args, utils, executor=None):
        try:
            if os.name == 'nt':
                cmd = ['cmd', '/c', 'dir']
                cmd.extend(args)
                result = subprocess.run(cmd, shell=False)
            else:
                cmd = ['ls']
                cmd.extend(args)
                result = subprocess.run(cmd)
            utils.last_exit_code = result.returncode
            return utils.last_exit_code == 0
        except FileNotFoundError:
            print(f"{Colors.RED}Command not found{Colors.RESET}")
            utils.last_exit_code = 127
            return False
        except Exception as e:
            print(f"{Colors.RED}Error: {e}{Colors.RESET}")
            utils.last_exit_code = 1
            return False

    @staticmethod
    def cmd_cd(args, utils, executor=None):
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
    def cmd_pwd(args, utils, executor=None):
        print(os.getcwd())
        utils.last_exit_code = 0
        return True

    @staticmethod
    def cmd_history(args, utils, executor=None):
        limit = None
        if args and args[0].isdigit():
            limit = int(args[0])
        history = utils.get_history(limit)
        for i, cmd in enumerate(history, 1):
            print(f"{i:4d}  {cmd}")
        utils.last_exit_code = 0
        return True

    @staticmethod
    def cmd_clear(args, utils, executor=None):
        os.system('clear' if os.name != 'nt' else 'cls')
        utils.last_exit_code = 0
        return True

    @staticmethod
    def cmd_help(args, utils, executor=None):
        commands = {
            'exit': 'Exit the shell',
            'echo': 'Print text to console',
            'cd': 'Change directory',
            'pwd': 'Print working directory',
            'history': 'Show command history',
            'clear': 'Clear the screen',
            'help': 'Show this help message',
            'ls': 'List directory contents',
            'repeat': 'Repeat a command multiple times',
        }
        print(f"\n{Colors.BOLD}Available Commands:{Colors.RESET}\n")
        for cmd, desc in commands.items():
            print(f"  {Colors.GREEN}{cmd:<10}{Colors.RESET} {desc}")
        print(f"\n{Colors.DIM}External commands are also available{Colors.RESET}\n")
        utils.last_exit_code = 0
        return True

    @staticmethod
    def cmd_repeat(args, utils, executor=None):
        if len(args) < 2:
            print(f"{Colors.RED}Usage: repeat <count> <command>{Colors.RESET}")
            utils.last_exit_code = 1
            return False

        try:
            count = int(args[0])
        except ValueError:
            print(f"{Colors.RED}Error: count must be a number, got '{args[0]}'{Colors.RESET}")
            utils.last_exit_code = 1
            return False

        if count <= 0:
            print(f"{Colors.RED}Error: count must be positive, got {count}{Colors.RESET}")
            utils.last_exit_code = 1
            return False

        command_parts = args[1:]
        cmd_str = ' '.join(command_parts)
        success = True

        for i in range(count):
            if count > 1:
                print(f"{Colors.DIM}[{i+1}/{count}]{Colors.RESET}", end=" ")

            if executor:
                try:
                    result = executor(cmd_str)
                    if not result:
                        success = False
                        print(f"{Colors.RED}Command failed at iteration {i+1}{Colors.RESET}")
                        break
                except Exception as e:
                    print(f"{Colors.RED}Error: {e}{Colors.RESET}")
                    success = False
                    break
            else:
                try:
                    result = subprocess.run(command_parts, capture_output=False, text=True)
                    if result.returncode != 0:
                        success = False
                        print(f"{Colors.RED}Command failed at iteration {i+1}{Colors.RESET}")
                        break
                except FileNotFoundError:
                    print(f"{Colors.RED}Command not found: {command_parts[0]}{Colors.RESET}")
                    success = False
                    break
                except Exception as e:
                    print(f"{Colors.RED}Error: {e}{Colors.RESET}")
                    success = False
                    break

        utils.last_exit_code = 0 if success else 1
        return success
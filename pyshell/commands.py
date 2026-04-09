# commands.py
import os
import sys
import subprocess
from colors import Colors


class Builtins:
    @staticmethod
    def cmd_sleep(args, utils, executor=None):
        """Sleep for N seconds (built-in, works on all platforms)"""
        if not args:
            print(f"{Colors.RED}Usage: sleep <seconds>{Colors.RESET}")
            utils.last_exit_code = 1
            return False
        
        try:
            seconds = float(args[0])
            if seconds <= 0:
                print(f"{Colors.YELLOW}Sleep: ignoring non-positive value{Colors.RESET}")
                return True
            
            import time
            time.sleep(seconds)
            utils.last_exit_code = 0
            return True
        except ValueError:
            print(f"{Colors.RED}Error: invalid number: {args[0]}{Colors.RESET}")
            utils.last_exit_code = 1
            return False
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
    
    @staticmethod
    def cmd_alias(args, utils, executor=None):
        """Create or show aliases"""
        if not args:
            # Show all aliases
            if not utils.aliases:
                print(f"{Colors.DIM}No aliases defined{Colors.RESET}")
            else:
                print(f"{Colors.BOLD}Aliases:{Colors.RESET}")
                for name, cmd in utils.aliases.items():
                    print(f"  {Colors.GREEN}{name}{Colors.RESET} = '{cmd}'")
            utils.last_exit_code = 0
            return True
        
        # Parse alias name=value
        alias_str = ' '.join(args)
        if '=' not in alias_str:
            print(f"{Colors.RED}Usage: alias name='command'{Colors.RESET}")
            utils.last_exit_code = 1
            return False
        
        name, value = alias_str.split('=', 1)
        name = name.strip()
        value = value.strip().strip("'\"")
        
        if not name:
            print(f"{Colors.RED}Error: alias name cannot be empty{Colors.RESET}")
            utils.last_exit_code = 1
            return False
        
        utils.aliases[name] = value
        utils._save_aliases()
        print(f"{Colors.GREEN}Alias created: {name} -> '{value}'{Colors.RESET}")
        utils.last_exit_code = 0
        return True
    
    @staticmethod
    def cmd_unalias(args, utils, executor=None):
        """Remove an alias"""
        if not args:
            print(f"{Colors.RED}Usage: unalias <name>{Colors.RESET}")
            utils.last_exit_code = 1
            return False
        
        name = args[0]
        if name in utils.aliases:
            del utils.aliases[name]
            utils._save_aliases()
            print(f"{Colors.GREEN}Removed alias: {name}{Colors.RESET}")
        else:
            print(f"{Colors.RED}Alias not found: {name}{Colors.RESET}")
            utils.last_exit_code = 1
            return False
        
        utils.last_exit_code = 0
        return True
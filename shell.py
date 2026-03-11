import sys
import time
import os
from datetime import datetime
import subprocess

from reference import ShellUI
from utility_tools import Utils


if os.name == "nt":

    os.system("")

previous_directory = None

global command_history
command_history = []

def fetch_prompt():
 
    RESET = "\033[0m"
    GREEN = "\033[92m"
    CYAN = "\033[96m"
    YELLOW = "\033[93m"
    MAGENTA = "\033[95m"
    DIM = "\033[2m"

    user = "user"
    host = "localhost"

    current_dir = os.getcwd()

    # Replace home directory with "~"
    home = os.path.expanduser("~")
    if current_dir.startswith(home):
        current_dir = "~" + current_dir[len(home):]

    timestamp = datetime.now().strftime("%H:%M:%S")

    top = (
        f"{DIM}╭─{RESET}"
        f"{CYAN}[{timestamp}]{RESET}"
        f"{DIM}─{RESET}"
        f"{GREEN}[{user}@{host}]{RESET}"
        f"{DIM}─{RESET}"
        f"{YELLOW}[{current_dir}]{RESET}"
    )

    bottom = f"{DIM}╰─{RESET}{MAGENTA}➤{RESET} $ "

    return f"{top}\n{bottom}"

# Cd logic
def handle_cd(parts):
    global previous_directory

    if len(parts) == 1:
        target = os.path.expanduser("~")
    else:
        target = parts[1]
        if target == "~":
            target = os.path.expanduser("~")
        elif target == "-":
            if previous_directory:
                target = previous_directory
            else:
                print("No previous directory")
                return
    try:
        current = os.getcwd()
        os.chdir(target)
        previous_directory = current

    except FileNotFoundError:
        print(f"{target}: directory not found")
    except NotADirectoryError:
        print(f"{target}: not a directory")
    except PermissionError:
        print(f"permission denied: {target}")



def shell():
    ui = ShellUI()
    ui.banner()
    utils = Utils(command_history)
    while True:

        sys.stdout.write(fetch_prompt())
        sys.stdout.flush()

        cmd = input().strip()
        utils.add_command(cmd)

        if not cmd:
            print("invalid argument")
            continue

        parts = cmd.split()
        command = parts[0].lower()

        
        if command == "exit":
            print("Exiting shell...")
            time.sleep(2)
            print("bye!")
            sys.exit()

        elif command == "echo":
            if len(parts) > 1:
                print(" ".join(parts[1:]))
            else:
                print()

        
        elif command == "help":

            help_menu = {
                "exit": "Exit the shell",
                "echo": "Print text to the console",
                "help": "Show this help message",
                "clear": "Clear the screen",
                "date": "Show current date and time",
                "sleep": "Pause execution for N seconds",
                "dir": "List directory contents",
                "cd": "Change directory"
            }

            print("\nAvailable commands:\n")

            for cmd_name, description in help_menu.items():
                print(f"{cmd_name:<10} - {description}")

            print()

        elif command == "clear":
            subprocess.run("cls" if os.name == "nt" else "clear", shell=True)

        elif command == "date":
            now = datetime.now()
            print(now.strftime("%Y-%m-%d %H:%M:%S"))

        elif command == "sleep":

            if len(parts) > 1:
                try:
                    seconds = float(parts[1])
                    print(f"Sleeping for {seconds} seconds...")
                    time.sleep(seconds)
                    print("Done!")

                except ValueError:
                    print(f"Error: Invalid number of seconds: {parts[1]}")
            else:
                print("Error: sleep requires a number of seconds")
        elif command == "dir":
            subprocess.run("dir" if os.name == "nt" else "ls", shell=True)
        elif command == "cd":
            handle_cd(parts)

        elif command == "history":
            utils =  Utils(command_history)
            print("command History:")
            print(utils.history())

        else:
            print(f"invalid command: {cmd}")


if __name__ == "__main__":

    try:
        shell()

    except KeyboardInterrupt:
        print("\nExiting shell...")
        time.sleep(2)
        sys.exit()
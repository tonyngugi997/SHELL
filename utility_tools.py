import os
from datetime import datetime
import time
import threading
import keyboard


class Utils:
    def __init__(self, history_list):
        self.command_history = history_list
        self.current_input = ""

    def add_command(self, command):
        self.command_history.append(command)

    def history(self):
        if not self.command_history:
            return "No commands in history."

        output = []

        for index, command in enumerate(self.command_history, start=1):
            output.append(f"{index}: {command}")

        return "\n".join(output)
    def grep(self,text, pattern):

        result = []
        lines  = text.split('\n')

        for line in lines:
            if pattern.lower() in line.lower():
                result.append(line)
        return "\n".join(result) if result else "No matches found."
    
    
    def fetch_prompt(self):
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
    def key_listener(self):
        " listens for arrow up and down key presses to navigate command history "
        while True:
            def on_key_event(event):
                if event.event_type == keyboard.KEY_DOWN:
                    if event.name == 'up':
                        print('up arrow pressed')
                    elif event.name == 'down':
                        print('down arrow pressed')
            keyboard.hook(on_key_event)
    threading.Event().wait(1)
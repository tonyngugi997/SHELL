import os
from datetime import datetime
import time
import threading
import keyboard


class Utils:
    def __init__(self, history_list):
        self.command_history = history_list
        self.current_input = ""
        self.pending_input = ""

    def get_pending_command(self):
        """Get any command waiting from keyboard thread"""
        cmd = self.pending_command
        self.pending_command = None  # Clear it after reading
        return cm

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
    
    class Utils:
        def __init__(self, history_list):
            self.command_history = history_list
            self.listening = True
            self.current_input = ""  # This will store what user is typing
            self.pending_command = None  # This will store history commands to show
        
    # ADD THIS NEW METHOD
    def get_pending_command(self):
        """Get any command waiting from keyboard thread"""
        cmd = self.pending_command
        self.pending_command = None  # Clear it after reading
        return cmd

    def key_listener(self):
        """Watch for arrow keys in the background"""
        import threading
        
        def on_key_event(event):
            if event.event_type == keyboard.KEY_DOWN:       
                if event.name == 'up':
                    # For now, just set a test message
                    self.pending_command = "TEST FROM UP ARROW"
                    print("\n[DEBUG] Up arrow detected!")  # This will show in terminal
                elif event.name == 'down':
                    self.pending_command = "TEST FROM DOWN ARROW"
                    print("\n[DEBUG] Down arrow detected!")
        
        keyboard.hook(on_key_event)
        print("Keyboard listener started")
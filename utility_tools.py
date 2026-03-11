class Utils:
    def __init__(self, history_list):
        self.command_history = history_list


    def add_command(self, command):
        self.command_history.append(command)

    def history(self):
        if not self.command_history:
            return "No commands in history."

        output = []

        for index, command in enumerate(self.command_history, start=1):
            output.append(f"{index}: {command}")

        return "\n".join(output)
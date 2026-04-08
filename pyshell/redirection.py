# redirection.py
"""Handle shell redirections: > , >> , < , 2> , &>"""


class RedirectionParser:
    @staticmethod
    def open_redirection(filepath, append=False, is_input=False):
        """Open file for redirection with proper error handling"""
        if is_input:
            try:
                return open(filepath, 'r')
            except FileNotFoundError:
                print(f"Error: file not found: {filepath}")
                return None
            except PermissionError:
                print(f"Error: permission denied: {filepath}")
                return None
        else:
            mode = 'a' if append else 'w'
            try:
                return open(filepath, mode)
            except PermissionError:
                print(f"Error: permission denied: {filepath}")
                return None
            except IsADirectoryError:
                print(f"Error: is a directory: {filepath}")
                return None
            
    """Parse and handle shell redirections"""
    @staticmethod
    def parse(args):
        stdin_file = None
        stdout_file = None
        stderr_file = None
        append_stdout = False
        append_stderr = False
        
        new_args = []
        i = 0
        while i < len(args):
            arg = args[i]
            
            # Output redirection (overwrite): > filename
            if arg == '>':
                if i + 1 >= len(args):
                    print("Error: missing filename for >")
                    return None, None, None, None, False, False
                stdout_file = args[i + 1]
                append_stdout = False
                i += 2
                continue

            # Append redirection: >> filename
            elif arg == '>>':
                if i + 1 >= len(args):
                    print("Error: missing filename for >>")
                    return None, None, None, None, False, False
                stdout_file = args[i + 1]
                append_stdout = True
                i += 2
                continue
            
            # Input redirection: < filename
            elif arg == '<':
                if i + 1 >= len(args):
                    print("Error: missing filename for <")
                    return None, None, None, None, False, False
                stdin_file = args[i + 1]
                i += 2
                continue
            
            # Stderr redirection: 2> filename
            elif arg == '2>':
                if i + 1 >= len(args):
                    print("Error: missing filename for 2>")
                    return None, None, None, None, False, False
                stderr_file = args[i + 1]
                append_stderr = False
                i += 2
                continue

                        # Stderr append: 2>> filename
            elif arg == '2>>':
                if i + 1 >= len(args):
                    print("Error: missing filename for 2>>")
                    return None, None, None, None, False, False
                stderr_file = args[i + 1]
                append_stderr = True
                i += 2
                continue


                        # Combined stdout+stderr: &> filename
            elif arg == '&>':
                if i + 1 >= len(args):
                    print("Error: missing filename for &>")
                    return None, None, None, None, False, False
                stdout_file = args[i + 1]
                stderr_file = args[i + 1]
                append_stdout = False
                append_stderr = False
                i += 2
                continue

                        # Combined append: &>> filename
            elif arg == '&>>':
                if i + 1 >= len(args):
                    print("Error: missing filename for &>>")
                    return None, None, None, None, False, False
                stdout_file = args[i + 1]
                stderr_file = args[i + 1]
                append_stdout = True
                append_stderr = True
                i += 2
                continue
            
            else:
                new_args.append(arg)
                i += 1
        
        return new_args, stdin_file, stdout_file, stderr_file, append_stdout, append_stderr
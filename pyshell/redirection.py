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
        
        else:
            new_args.append(arg)
            i += 1
    
    return new_args, stdin_file, stdout_file, stderr_file, append_stdout, append_stderr
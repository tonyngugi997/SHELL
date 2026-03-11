import sys
import time
import os
from datetime import datetime

if os.name == 'nt':
    os.system('')

def grab_banner():
    banner =  """
        |_____________________________________________|
        |pwoer lies in the sh3!!-- Tony Ngugi         |
        |_____________________________________________|
                |-------------------------------|                  
                |author Tony Ngugi | localhost  |
                |-------------------------------| 
                |email: tonyngugi997@gmail.com  |
                |-------------------------------|                                       
                |github:Tonyngugi997            |
                |-------------------------------|
                
                            

"""

    return banner
print(grab_banner())

def shell():
    def fetch_prompt():
        current_dir = os.getcwd()
        #home = os.path.expanduser("~")

       # if current_dir.startswith(home):
            #current_dir = "~" + current_dir[len(home)]
        GREEN = '\033[92m'
        DARK_GREEN = '\033[2;32m'
        BRIGHT_GREEN = '\033[1;92m'
        RESET = '\033[0m'

        timestamp = datetime.now().strftime('%H:%M:%S')
        return f"{DARK_GREEN}[{timestamp}]{RESET}{GREEN}-- [{BRIGHT_GREEN}user{GREEN}@{BRIGHT_GREEN}unknown{GREEN}-- [{BRIGHT_GREEN}{current_dir}{GREEN}]\n{GREEN}>> {RESET} $ "

    while True:
        #os.system('cls' if os.name == 'nt' else 'clear')
        sys.stdout.write(fetch_prompt())
        sys.stdout.flush()     

        cmd = input()
        if not cmd:
            print('invalid argument')
            continue
        
        parts = cmd.split()
        command = parts[0].lower()
        
        if command == 'exit':
            print('Exiting shell...')
            time.sleep(3)
            print('bye!')
            sys.exit()
            
        elif command == 'echo':
            if len(parts) > 1:
                print(' '.join(parts[1:]))
            else:
                print() 
                
        elif command == 'help':
             def get_help():
                help_ = {
                    'exit': 'Exit the shell',
                    'echo': 'Print text to the console',
                    'help': 'Show this help message',
                    'clear': 'Clear the screen',
                    'date': 'Show current date and time',
                    'sleep': 'Pause execution for N seconds'
                }
                return help
             print(help)
        
            
        elif command == 'clear':
            os.system('cls' if os.name == 'nt' else 'clear')
            
        elif command == 'date':
            now = datetime.now()
            print(now.strftime('%Y-%m-%d %H:%M:%S'))
            
        elif command == 'sleep':
            if len(parts) > 1:
                try:
                    seconds = float(parts[1])
                    print(f'Sleeping for {seconds} seconds...')
                    time.sleep(seconds)
                    print('Done!')
                except ValueError:
                    print(f'Error: Invalid number of seconds: {parts[1]}')
            else:
                print('Error: sleep requires a number of seconds')

        elif command == 'dir':
            os.system('dir' if os.name == 'nt' else 'ls')
        elif command == 'cd':
           
           if len(parts) > 1:
            try:  
                dir_path = parts[1:]
                os.chdir(str(dir_path))
            except NotADirectoryError:
                print(f"{dir_path}: is not a directory.")
            except PermissionError:
                print(f'permision denied for {dir_path}')
           else:
               print(f"{dir_path}: does not exist")
        else:
            print(f'invalid command: {cmd}')

if __name__ == '__main__':
    try:
        shell()
    except KeyboardInterrupt:
        print('\nExiting shell...')
        time.sleep(2)
        sys.exit()
# completer.py
import os

try:
    import pyreadline as readline
except ImportError:
    try:
        import readline
    except ImportError:
        readline = None


class Completer:
    def __init__(self):
        self.matches = []
    
    def complete(self, text, state):
        if readline is None:
            return None
            
        if state == 0:
            line = readline.get_line_buffer()
            start = readline.get_begidx()
            end = readline.get_endidx()
            
            if ' ' in line[:start]:
                word = line.split()[-1] if line.split() else ''
            else:
                word = text
            
            path = os.path.expanduser(word)
            dirname = os.path.dirname(path) if os.path.dirname(path) else '.'
            basename = os.path.basename(path)
            
            try:
                files = os.listdir(dirname)
                self.matches = []
                for f in files:
                    if f.startswith(basename):
                        full = os.path.join(dirname, f)
                        if os.path.isdir(full):
                            f += '/'
                        self.matches.append(f)
                self.matches.sort()
            except Exception:
                self.matches = []
        
        return self.matches[state] if state < len(self.matches) else None
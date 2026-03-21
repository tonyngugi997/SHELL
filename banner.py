import os
import shutil

class ShellUI:
    """
    Handles shell UI components with advanced cyberpunk-themed banner
    """
    
    def _get_terminal_width(self):
        """Get terminal width for responsive design"""
        try:
            return shutil.get_terminal_size().columns
        except:
            return 80
    
    def banner(self):
        """Display an epic, hyper-stylized banner with fierce Python"""
        
        # Clear screen
        os.system("cls" if os.name == "nt" else "clear")
        
        # Terminal width check
        term_width = self._get_terminal_width()
        
        # Advanced color palette
        RESET = "\033[0m"
        BOLD = "\033[1m"
        DIM = "\033[2m"
        ITALIC = "\033[3m"
        UNDERLINE = "\033[4m"
        BLINK = "\033[5m"
        REVERSE = "\033[7m"
        
        # True 24-bit RGB colors
        SCALE_GREEN1 = "\033[38;2;80;200;80m"    # Bright green
        SCALE_GREEN2 = "\033[38;2;40;160;40m"    # Forest green
        SCALE_GREEN3 = "\033[38;2;20;120;20m"    # Dark green
        SCALE_GREEN4 = "\033[38;2;10;80;10m"     # Very dark green
        SCALE_HIGHLIGHT = "\033[38;2;180;255;180m" # Highlight
        SCALE_BROWN = "\033[38;2;139;69;19m"      # Brown for patterns
        
        # Eye colors
        EYE_RED = "\033[38;2;255;0;0m"            # Pure red
        EYE_GLOW = "\033[38;2;255;100;100m"       # Red glow
        EYE_PUPIL = "\033[38;2;0;0;0m"             # Black
        EYE_HIGHLIGHT = "\033[38;2;255;255;255m"   # White
        
        # Fang colors
        FANG_WHITE = "\033[38;2;255;255;255m"
        TONGUE_RED = "\033[38;2;255;50;50m"
        
        # Accent colors
        GOLD = "\033[38;2;255;215;0m"
        CYBER_BLUE = "\033[38;2;0;255;255m"
        NEON_PURPLE = "\033[38;2;200;0;255m"
        DARK_PURPLE = "\033[38;2;100;0;150m"
        SILVER = "\033[38;2;192;192;192m"
        
        # Border characters
        BORDER_V = "║"
        BORDER_H = "═"
        
        # snake head
        fierce_cobra = f"""
{SCALE_GREEN2}                                  ╔════╗
{SCALE_GREEN1}                              ╔══╝    ╚══╗
{SCALE_GREEN3}                            ╔╝            ╚╗
{SCALE_GREEN2}                           ╔               ╗
{SCALE_GREEN1}                          ╔    {EYE_RED}◉{SCALE_GREEN1}      {EYE_RED}◉{SCALE_GREEN1}    ╗
{SCALE_GREEN3}                          ║     {EYE_GLOW}══{SCALE_GREEN3}    {EYE_GLOW}══{SCALE_GREEN3}     ║
{SCALE_GREEN2}                          ║         {FANG_WHITE}▼▼{SCALE_GREEN2}         ║
{SCALE_GREEN1}                          ║   {SCALE_BROWN}╔════╗{SCALE_GREEN1}   {FANG_WHITE}/  \\{SCALE_GREEN1}   {SCALE_BROWN}╔════╗{SCALE_GREEN1}   ║
{SCALE_GREEN3}                           ║  {SCALE_BROWN}║    ║{SCALE_GREEN3}   {TONGUE_RED}/    \\{SCALE_GREEN3}   {SCALE_BROWN}║    ║{SCALE_GREEN3}  ║
{SCALE_GREEN2}                            ║ {SCALE_BROWN}╚════╝{SCALE_GREEN2}   {TONGUE_RED}\\____/{SCALE_GREEN2}   {SCALE_BROWN}╚════╝{SCALE_GREEN2} ║
{SCALE_GREEN1}                             ║    {SCALE_GREEN3}╔{SCALE_GREEN1}    ║    {SCALE_GREEN3}╔{SCALE_GREEN1}    ║
{SCALE_GREEN3}                              ║  {SCALE_GREEN1}╔{SCALE_GREEN3} ═╝  ╚═ {SCALE_GREEN1}╔{SCALE_GREEN3}  ║
{SCALE_GREEN2}                               ║{SCALE_GREEN1}╔{SCALE_GREEN2}        {SCALE_GREEN1}╔{SCALE_GREEN2}║
{SCALE_GREEN1}                                ║{SCALE_GREEN3}╚══════{SCALE_GREEN1}╝
{SCALE_GREEN3}                                 ║{SCALE_GREEN2}██████{SCALE_GREEN3}║
{SCALE_GREEN2}                                 ║{SCALE_GREEN1}██{TONGUE_RED}██{EYE_RED}██{SCALE_GREEN1}║
{SCALE_GREEN1}                                 ╚══════╝"""

        #  for smaller terminals
        clear_snake = f"""
{SCALE_GREEN2}                        .--=+* cobra *+=--.
{SCALE_GREEN3}                     .+{SCALE_GREEN1}              {SCALE_GREEN3}+.
{SCALE_GREEN1}                  .+{SCALE_GREEN2}    {EYE_RED}⊙{SCALE_GREEN2}      {EYE_RED}⊙{SCALE_GREEN2}    {SCALE_GREEN1}+.
{SCALE_GREEN2}                 +{SCALE_GREEN3}       {EYE_GLOW}══{SCALE_GREEN2}   {EYE_GLOW}══{SCALE_GREEN3}       {SCALE_GREEN2}+
{SCALE_GREEN1}                +           {FANG_WHITE}▼▼{SCALE_GREEN1}           +
{SCALE_GREEN3}               +        {SCALE_BROWN}╔════╗{SCALE_GREEN3}        +
{SCALE_GREEN2}              +        {SCALE_BROWN}║    ║{SCALE_GREEN2}        +
{SCALE_GREEN1}             +         {SCALE_BROWN}╚════╝{SCALE_GREEN1}         +
{SCALE_GREEN3}            +      {TONGUE_RED}/   ||   \\{SCALE_GREEN3}      +
{SCALE_GREEN2}           +       {TONGUE_RED}/    ||    \\{SCALE_GREEN2}       +
{SCALE_GREEN1}          +             {FANG_WHITE}||||{SCALE_GREEN1}             +
{SCALE_GREEN3}         +              {FANG_WHITE}||||{SCALE_GREEN3}              +
{SCALE_GREEN2}        +               {FANG_WHITE}||||{SCALE_GREEN2}               +
{SCALE_GREEN1}       +                 {FANG_WHITE}||||{SCALE_GREEN1}                 +
{SCALE_GREEN3}      +          {TONGUE_RED}🔥 COBRA STRIKE 🔥{SCALE_GREEN3}          +
{SCALE_GREEN2}     +{SCALE_GREEN1}═══════════════════════════════════{SCALE_GREEN2}+"""

        # Choose the best snake for terminal size
        if term_width < 100:
            snake_art = clear_snake
        else:
            snake_art = fierce_cobra
        
        
        print(f"\n{NEON_PURPLE}{BOLD}╔══════════════════════════════════════════════════════════════════════════════╗{RESET}")
        print(f"{NEON_PURPLE}║{RESET}{CYBER_BLUE}{BOLD}     ████████╗ ██████╗ ███╗   ██╗██╗   ██╗    {GOLD}███████╗██╗  ██╗███████╗██╗     ██╗     {RESET}{NEON_PURPLE}║")
        print(f"{NEON_PURPLE}║{RESET}{CYBER_BLUE}{BOLD}     ╚══██╔══╝██╔═══██╗████╗  ██║╚██╗ ██╔╝    {GOLD}██╔════╝██║  ██║██╔════╝██║     ██║     {RESET}{NEON_PURPLE}║")
        print(f"{NEON_PURPLE}║{RESET}{CYBER_BLUE}{BOLD}        ██║   ██║   ██║██╔██╗ ██║ ╚████╔╝     {GOLD}███████╗███████║█████╗  ██║     ██║     {RESET}{NEON_PURPLE}║")
        print(f"{NEON_PURPLE}║{RESET}{CYBER_BLUE}{BOLD}        ██║   ██║   ██║██║╚██╗██║  ╚██╔╝      {GOLD}╚════██║██╔══██║██╔══╝  ██║     ██║     {RESET}{NEON_PURPLE}║")
        print(f"{NEON_PURPLE}║{RESET}{CYBER_BLUE}{BOLD}        ██║   ╚██████╔╝██║ ╚████║   ██║       {GOLD}███████║██║  ██║███████╗███████╗███████╗{RESET}{NEON_PURPLE}║")
        print(f"{NEON_PURPLE}║{RESET}{CYBER_BLUE}{BOLD}        ╚═╝    ╚═════╝ ╚═╝  ╚═══╝   ╚═╝       {GOLD}╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝{RESET}{NEON_PURPLE}║")
        print(f"{NEON_PURPLE}╠══════════════════════════════════════════════════════════════════════════════╣{RESET}")
        
        
        print(f"{NEON_PURPLE}║{RESET}  {BLINK}{EYE_RED}{BOLD}⚠⚠⚠  VENOMOUS CODE - HANDLE WITH EXTREME CARE  ⚠⚠⚠{RESET}                  {NEON_PURPLE}║")
        print(f"{NEON_PURPLE}╠══════════════════════════════════════════════════════════════════════════════╣{RESET}")
        
        
        print(f"{NEON_PURPLE}║{RESET}{BOLD}{CYBER_BLUE}                   🐍 TERMINAL COBRA v1.1 🐍{RESET}                      {NEON_PURPLE}║")
        print(f"{NEON_PURPLE}║{RESET}                                                                        {NEON_PURPLE}║")
        
        # Print the snake
        for line in snake_art.split('\n'):
            print(f"{NEON_PURPLE}║{RESET}  {line:<70} {NEON_PURPLE}║")
        
        
        print(f"{NEON_PURPLE}║{RESET}                                                                        {NEON_PURPLE}║")
        print(f"{NEON_PURPLE}╠══════════════════════════════════════════════════════════════════════════════╣{RESET}")
        
        
        print(f"{NEON_PURPLE}║{RESET}{GOLD}{BOLD}   ╔════════════════════════════════════════════════════════════════╗{RESET}      {NEON_PURPLE}║")
        print(f"{NEON_PURPLE}║{RESET}{GOLD}{BOLD}   ║{RESET}                  {CYBER_BLUE}{BOLD}{UNDERLINE}AUTHOR INFORMATION{UNDERLINE}{RESET}                   {GOLD}{BOLD}║{RESET}      {NEON_PURPLE}║")
        print(f"{NEON_PURPLE}║{RESET}{GOLD}{BOLD}   ╠════════════════════════════════════════════════════════════════╣{RESET}      {NEON_PURPLE}║")
        
    
        print(f"{NEON_PURPLE}║{RESET}{GOLD}{BOLD}   ║{RESET}  {EYE_RED}{BOLD}██▀███   ▄▄▄        ██████  ██▓ ███▄    █ {RESET}                              {GOLD}{BOLD}║{RESET}      {NEON_PURPLE}║")
        print(f"{NEON_PURPLE}║{RESET}{GOLD}{BOLD}   ║{RESET}  {EYE_RED}{BOLD}▓██ ▒ ██▒▒████▄    ▒██    ▒ ▓██▒ ██ ▀█   █ {RESET}                              {GOLD}{BOLD}║{RESET}      {NEON_PURPLE}║")
        print(f"{NEON_PURPLE}║{RESET}{GOLD}{BOLD}   ║{RESET}  {EYE_RED}{BOLD}▓██ ░▄█ ▒▒██  ▀█▄  ░ ▓██▄   ▒██▒▓██  ▀█ ██▒{RESET}                              {GOLD}{BOLD}║{RESET}      {NEON_PURPLE}║")
        print(f"{NEON_PURPLE}║{RESET}{GOLD}{BOLD}   ║{RESET}  {EYE_RED}{BOLD}▒██▀▀█▄  ░██▄▄▄▄██   ▒   ██▒░██░▓██▒  ▐▌██▒{RESET}                              {GOLD}{BOLD}║{RESET}      {NEON_PURPLE}║")
        print(f"{NEON_PURPLE}║{RESET}{GOLD}{BOLD}   ║{RESET}  {EYE_RED}{BOLD}░██▓ ▒██▒ ▓█   ▓██▒▒██████▒▒░██░▒██░   ▓██░{RESET}                              {GOLD}{BOLD}║{RESET}      {NEON_PURPLE}║")
        print(f"{NEON_PURPLE}║{RESET}{GOLD}{BOLD}   ║{RESET}  {EYE_RED}{BOLD}░ ▒▓ ░▒▓░ ▒▒   ▓▒█░▒ ▒▓▒ ▒ ░░▓  ░ ▒░   ▒ ▒ {RESET}                              {GOLD}{BOLD}║{RESET}      {NEON_PURPLE}║")
        print(f"{NEON_PURPLE}║{RESET}{GOLD}{BOLD}   ║{RESET}  {EYE_RED}{BOLD}  ░▒ ░ ▒░  ▒   ▒▒ ░░ ░▒  ░ ░ ▒ ░░ ░░   ░ ▒░{RESET}                              {GOLD}{BOLD}║{RESET}      {NEON_PURPLE}║")
        print(f"{NEON_PURPLE}║{RESET}{GOLD}{BOLD}   ║{RESET}  {EYE_RED}{BOLD}  ░░   ░   ░   ▒   ░  ░  ░   ▒ ░   ░   ░ ░ {RESET}                              {GOLD}{BOLD}║{RESET}      {NEON_PURPLE}║")
        print(f"{NEON_PURPLE}║{RESET}{GOLD}{BOLD}   ║{RESET}  {EYE_RED}{BOLD}   ░           ░  ░      ░   ░           ░ {RESET}                              {GOLD}{BOLD}║{RESET}      {NEON_PURPLE}║")
        print(f"{NEON_PURPLE}║{RESET}{GOLD}{BOLD}   ╠════════════════════════════════════════════════════════════════╣{RESET}      {NEON_PURPLE}║")
        
        # Contact information
        print(f"{NEON_PURPLE}║{RESET}{GOLD}{BOLD}   ║{RESET}  {SILVER}┌─{CYBER_BLUE} AUTHOR  {SILVER}─────────────────────────────────┐{RESET}                {GOLD}{BOLD}║{RESET}      {NEON_PURPLE}║")
        print(f"{NEON_PURPLE}║{RESET}{GOLD}{BOLD}   ║{RESET}  {SILVER}│{RESET}  {GOLD}●{RESET} {BOLD}{CYBER_BLUE}Tony Ngugi{ITALIC} - P0w3r l!es in the Sh3ll{RESET}                {SILVER}│{RESET}    {GOLD}{BOLD}║{RESET}      {NEON_PURPLE}║")
        print(f"{NEON_PURPLE}║{RESET}{GOLD}{BOLD}   ║{RESET}  {SILVER}├─────────────────────────────────────────────────┤{RESET}    {GOLD}{BOLD}║{RESET}      {NEON_PURPLE}║")
        print(f"{NEON_PURPLE}║{RESET}{GOLD}{BOLD}   ║{RESET}  {SILVER}│{RESET}  {EYE_GLOW}◉{RESET} {UNDERLINE}GITHUB{UNDERLINE} : {CYBER_BLUE}tonyngugi997{RESET}                             {SILVER}│{RESET}    {GOLD}{BOLD}║{RESET}      {NEON_PURPLE}║")
        print(f"{NEON_PURPLE}║{RESET}{GOLD}{BOLD}   ║{RESET}  {SILVER}│{RESET}  {EYE_GLOW}◉{RESET} {UNDERLINE}EMAIL{UNDERLINE}  : {CYBER_BLUE}tonyngugi997@gmail.com{RESET}                  {SILVER}│{RESET}    {GOLD}{BOLD}║{RESET}      {NEON_PURPLE}║")
        print(f"{NEON_PURPLE}║{RESET}{GOLD}{BOLD}   ║{RESET}  {SILVER}│{RESET}  {EYE_GLOW}◉{RESET} {UNDERLINE}VERSION{UNDERLINE} : {GOLD}v1.1{RESET} (Cobra Strike Edition)               {SILVER}│{RESET}    {GOLD}{BOLD}║{RESET}      {NEON_PURPLE}║")
        print(f"{NEON_PURPLE}║{RESET}{GOLD}{BOLD}   ║{RESET}  {SILVER}│{RESET}  {EYE_GLOW}◉{RESET} {UNDERLINE}STATUS{UNDERLINE}  : {SCALE_GREEN2}●{RESET} ACTIVE  {EYE_RED}●{RESET} VENOMOUS  {GOLD}⚡{RESET} READY TO STRIKE   {SILVER}│{RESET}    {GOLD}{BOLD}║{RESET}      {NEON_PURPLE}║")
        print(f"{NEON_PURPLE}║{RESET}{GOLD}{BOLD}   ║{RESET}  {SILVER}└─────────────────────────────────────────────────┘{RESET}                {GOLD}{BOLD}║{RESET}      {NEON_PURPLE}║")
        

        print(f"{NEON_PURPLE}║{RESET}{GOLD}{BOLD}   ║{RESET}  {EYE_RED}{BOLD}⚠⚠⚠  VENOMOUS CODE - HANDLE WITH EXTREME CARE  ⚠⚠⚠{RESET}                 {GOLD}{BOLD}║{RESET}      {NEON_PURPLE}║")
        print(f"{NEON_PURPLE}║{RESET}{GOLD}{BOLD}   ╚════════════════════════════════════════════════════════════════╝{RESET}      {NEON_PURPLE}║")
        
        # Stats line
        print(f"{NEON_PURPLE}║{RESET}                                                                        {NEON_PURPLE}║")
        print(f"{NEON_PURPLE}║{RESET}  {DIM}┌─────────────────────────────────────────────────────────────────────┐{RESET}   {NEON_PURPLE}║")
    
        print(f"{NEON_PURPLE}║{RESET}  {DIM}└─────────────────────────────────────────────────────────────────────┘{RESET}   {NEON_PURPLE}║")
        
        # Final border
        print(f"{NEON_PURPLE}╚══════════════════════════════════════════════════════════════════════════════╝{RESET}")
        
        # Snake scale footer with author credit
        print(f"\n{SCALE_GREEN2}      ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄")
        print(f"{SCALE_GREEN1}      █{EYE_RED} ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄ {EYE_RED}█")
        print(f"{SCALE_GREEN3}      ██ {GOLD}🔥 CRAFTED BY TONY NGUGI 🔥{SCALE_GREEN3} ██")
        print(f"{SCALE_GREEN2}      █{EYE_GLOW} ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀ {EYE_GLOW}█")
        print(f"{SCALE_GREEN1}      ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀")
        
        
        print(f"\n{EYE_RED}{BOLD}{BLINK}⚠⚠⚠  VENOMOUS CODE - HANDLE WITH EXTREME CARE  ⚠⚠⚠{RESET}")
        
        
        print(f"\n{SCALE_GREEN3}{ITALIC}                           🐍 \"Coding with venom, striking with precision\" - Tony Ngugi 🐍{RESET}")
        print()  # Final newline
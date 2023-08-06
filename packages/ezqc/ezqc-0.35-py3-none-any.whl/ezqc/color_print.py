# Color escape sequences
RESET = "\033[0m"
BOLD = "\033[1m"
UNDERLINE = "\033[4m"
# Text color escape sequences
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
PURPLE = "\033[35m"
CYAN = "\033[36m"

def print_color(text, color):
    if (color == "yellow" or color == "YELLOW"):
        print(YELLOW + text + RESET)
    if (color == "green" or color == "GREEN"):
        print(GREEN + text + RESET)
    if (color == "RED" or color == "red"):
        print(RED + text + RESET)
    

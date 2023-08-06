"""A implementation of colored text."""
import os
BLACK = "\u001b[30m"
GREY = "\u001b[30m"
GRAY = "\u001b[30m"
RED = "\u001b[31m"
GREEN = "\u001b[32m"
YELLOW = "\u001b[33m"
BLUE = "\u001b[34m"
MAGENTA = "\u001b[35m"
CYAN = "\u001b[36m"
WHITE = "\u001b[37m"
RESET = "\033[0m"

def rgb(red, green, blue):
    """RGB colored start part without reset character"""
    return f"\u001b[38;2;{red};{green};{blue}m"


def colored(text, color):
    """Colored text"""
    if color.startswith('\u001b'):
        return color + text + RESET
    return globals()[color.upper()] + text + RESET

def background_color(color):
    """Set the background color. Only accepts colors in the form 'red' or 'green', not txtadv.color.RED or \u001b[36m"""
    os.system('setterm -term linux -back '+color)
    
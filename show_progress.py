import curses

def wrapper(func):
    curses.wrapper(func)
    

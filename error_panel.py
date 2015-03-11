import curses
class ErrorPanel(object):
    Y_POS = 15
    
    def __init__(self, screen):
        self.screen = screen

    def print_error(self, msg):
        self.screen.addstr(ErrorPanel.Y_POS, 0, msg, curses.A_BOLD)

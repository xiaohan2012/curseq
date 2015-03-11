from mode import (Mode, SelectionMode)
from errors import InvalidModeError

class Controller(object):
    MODE_ORDINARY = 0
    MODE_SELECTION = 1
    
    def __init__(self, screen):
        self.screen = screen
        self.modes = {
            Controller.MODE_ORDINARY: Mode(self.screen),
            Controller.MODE_SELECTION: SelectionMode(self.screen)
        }
        self.mode = None
        self.enter_mode(Controller.MODE_ORDINARY)
        
    def enter_mode(self, name):
        if name in self.modes:
            if self.mode: # we have some mode before
                old_mode = self.mode
                self.mode = self.modes[name]
                self.mode_name = name
                self.mode.copy_context_from(old_mode)
            else: # a brand new mode
                self.mode = self.modes[name]
                self.mode_name = name
            
        else:
            raise InvalidModeError("Available modes are %r" %(self.modes.keys()))
    
    def set_sentence(self, sent):
        for mode in self.modes.values():
            mode.set_sentence(sent)

    @property
    def sent(self):
        for mode in self.modes.values():
            if mode.sent is not None:
                return mode.sent

        return None

    def display_sentence(self):
        self.mode.display_sentence()
        
    def in_mode(self, name):
        return self.mode_name == name

    # interaction stuff
    def left_arrow_pressed(self):
        self.mode.left_arrow_pressed()

    def right_arrow_pressed(self):
        self.mode.right_arrow_pressed()

            
    def key_pressed(self, keyboard_code):
        self.mode.key_pressed(keyboard_code)

    

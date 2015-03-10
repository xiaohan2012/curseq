from state import (State, AnnotatingState)
from errors import InvalidControllerStateError

class Controller(object):
    STATE_ORDINARY = 0
    STATE_ANNOTATING = 1
    
    def __init__(self, screen):
        self.screen = screen
        self.states = {
            Controller.STATE_ORDINARY: State(self.screen),
            Controller.STATE_ANNOTATING: AnnotatingState(self.screen)
        }
        self.state = None
        self.enter_state(Controller.STATE_ORDINARY)
        
    def enter_state(self, name):
        if name in self.states:
            if self.state: # we have some state before
                old_state = self.state
                self.state = self.states[name]
                self.state_name = name
                self.state.copy_context_from(old_state)
            else: # a brand new state
                self.state = self.states[name]
                self.state_name = name
            
        else:
            raise InvalidControllerStateError("Available states are %r" %(self.states.keys()))
    
    def set_sentence(self, sent):
        for state in self.states.values():
            state.set_sentence(sent)

    def display_sentence(self):
        self.state.display_sentence()

        
    def in_state(self, name):
        return self.state_name == name


    # interaction stuff
    def left_arrow_pressed(self):
        self.state.left_arrow_pressed()

    def right_arrow_pressed(self):
        self.state.right_arrow_pressed()

            
    def key_pressed(self, keyboard_code):
        self.state.key_pressed(keyboard_code)

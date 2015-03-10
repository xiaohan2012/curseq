import curses
from word import Word
from errors import CursorMoveError

ENCODING = "utf8" 
CURRENT_WORD_STYLE_ID = 10
SELECTED_WORD_STYLE_ID = 11

DEFAULT_STATE2COLOR_MAPPING = {
    Word.STATE_SUBJECT: (curses.COLOR_RED, 0),
    Word.STATE_PREDICATE: (curses.COLOR_GREEN, 0),
    Word.STATE_OJBECT: (curses.COLOR_BLUE, 0),
    CURRENT_WORD_STYLE_ID: (0, curses.COLOR_WHITE),
    SELECTED_WORD_STYLE_ID: (0, curses.COLOR_YELLOW)
}

class State(object):
    def __init__(self, screen, 
                 state2color = DEFAULT_STATE2COLOR_MAPPING):
        self.SCREEN = screen
        
        self.SENT_PLACEMENT_YX = (0, 0)
        
        # init colors
        for state, (fg, bg) in state2color.items():
            curses.init_pair(state, fg, bg)

    def copy_context_from(self, state):
        assert isinstance(state, State)
        self.sent = state.sent
        self.current_word_index = state.current_word_index
        self.word_count = len(self.sent.words)
        
    def set_sentence(self, sent):
        self.SCREEN.clear()
        self.sent = sent
        self.current_word_index = 0
        self.current_cursor_y, self.current_cursor_x = \
                                                       self.SENT_PLACEMENT_YX
        
        self.word_count = len(self.sent.words)
        
        # init cursor
        curses.setsyx(*self.SENT_PLACEMENT_YX)
            
    def sentence_display_data(self):
        """
        If you want to modify how the sentence is displayed, modify this function
        """
        data = []
        cur_y, cur_x = self.SENT_PLACEMENT_YX
        for i, word in enumerate(self.sent):
            if self.current_word_index == i: # if current word, display the the `current` style
                color_pair = curses.color_pair(CURRENT_WORD_STYLE_ID)
            else:
                color_pair = curses.color_pair(word.state)
            
            data.append((cur_y, cur_x+1, word.encode(ENCODING), color_pair))

            cur_x += (len(word)+1)
        return data

    def display_sentence(self):
        for piece in self.sentence_display_data():
            self.SCREEN.addstr(*piece)

    def move_prev_word(self):
        self.current_word_index -= 1
        cur_word = self.sent[self.current_word_index]
        self.current_cursor_x -= len(cur_word)
        # curses.setsyx(self.current_cursor_y, self.current_cursor_x)
        
    def move_next_word(self):
        self.current_word_index += 1
        cur_word = self.sent[self.current_word_index]
        self.current_cursor_x += len(cur_word)
        
    def left_arrow_pressed(self):
        if self.current_word_index == 0:
            raise CursorMoveError("Reached the left boundary of sentence")
        else:
            self.move_prev_word()
            self.display_sentence()
            
    def right_arrow_pressed(self):
        if self.current_word_index == self.word_count - 1:
            raise CursorMoveError("Reached the right boundary of sentence")
        else:
            self.move_next_word()
            self.display_sentence()
            
class AnnotatingState(State):
    def __init__(self, *args, **kwargs):
        self.key2state = {
            ord('s'): Word.STATE_SUBJECT,
            ord('p'): Word.STATE_PREDICATE,
            ord('o'): Word.STATE_OJBECT
        }

        # selected range info
        self.selected_anchor_index = None
        self.selected_drift_index = None

        super(AnnotatingState, self).__init__(*args, **kwargs)

    def set_sentence(self, sent):
        """
        WARN: Invalid to set a sentence when in annotating mode?
        """
        super(AnnotatingState, self).set_sentence(sent)
        # self.selected_range_start = self.current_word_index
        # self.selected_range_end = self.current_word_index
        
    def copy_context_from(self, state):
        super(AnnotatingState, self).copy_context_from(state)
        
        self.selected_anchor_index = state.current_word_index
        self.selected_drift_index = state.current_word_index
        
    def get_selection_range(self):
        if self.selected_anchor_index <= self.selected_drift_index: # anchor ... drift
            return (self.selected_anchor_index, self.selected_drift_index)
        else: # drift .... anchor
            return (self.selected_drift_index, self.selected_anchor_index)

    def sentence_display_data(self):
        """
        If you want to modify how the sentence is displayed, modify this function
        """
        start_index, end_index = self.get_selection_range()
        data = []
        cur_y, cur_x = self.SENT_PLACEMENT_YX
        for i, word in enumerate(self.sent):
            if (i >= start_index and i <= end_index):
                #within range
                color_pair = curses.color_pair(SELECTED_WORD_STYLE_ID)
            else:
                color_pair = curses.color_pair(word.state)
            
            data.append((cur_y, cur_x+1, word.encode(ENCODING), color_pair))

            cur_x += (len(word)+1)
        return data
        
    def key_pressed(self, keyboard_code):
        start,end = self.get_selection_range()
        if keyboard_code in self.key2state:
            for w in self.sent.words[start:end+1]:
                w.set_state(self.key2state[keyboard_code])
        else:
            raise ValueError("Invalid key %r pressed. Limited to %r" %(keyboard_code, 
                                                                       self.key2state.keys()))

    def display_debug_info(self):
        self.SCREEN.addstr(5, 0, "anchor: " + str(self.selected_anchor_index))
        self.SCREEN.addstr(6, 0, "drift: " + str(self.selected_drift_index))
        self.SCREEN.addstr(7, 0, "index: " + str(self.current_word_index))
        
    def move_prev_word(self):
        super(AnnotatingState, self).move_prev_word()
        self.selected_drift_index -= 1
            
        self.display_debug_info()
        
    def move_next_word(self):
        super(AnnotatingState, self).move_next_word()
        self.selected_drift_index += 1
        
        self.display_debug_info()

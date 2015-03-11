import curses
from word import Word
from errors import CursorMoveError

ENCODING = "utf8" 
CURRENT_WORD_STYLE_ID = 10
SELECTED_WORD_STYLE_ID = 11
DEFAULT_WORD_STYLE_ID = 12

DEFAULT_LABEL2COLOR_MAPPING = {
    Word.LABEL_SUBJECT: (curses.COLOR_RED, 0),
    Word.LABEL_PREDICATE: (curses.COLOR_GREEN, 0),
    Word.LABEL_OJBECT: (curses.COLOR_BLUE, 0),
    DEFAULT_WORD_STYLE_ID: (curses.COLOR_WHITE, 0),
    CURRENT_WORD_STYLE_ID: (0, curses.COLOR_WHITE),
    SELECTED_WORD_STYLE_ID: (0, curses.COLOR_YELLOW)
}

KEY_TO_LABEL_MAPPING = {
    ord('a'): Word.LABEL_SUBJECT,
    ord('s'): Word.LABEL_PREDICATE,
    ord('d'): Word.LABEL_OJBECT
}

class Mode(object):
    def __init__(self, screen, 
                 label2color = DEFAULT_LABEL2COLOR_MAPPING, 
                 key2label = KEY_TO_LABEL_MAPPING):
        self.SCREEN = screen
        
        self.SENT_PLACEMENT_YX = (0, 0)
        
        # init colors
        for label, (fg, bg) in label2color.items():
            curses.init_pair(label, fg, bg)

        self.key2label = KEY_TO_LABEL_MAPPING
        self.valid_annotation_chars = [chr(c) for c in self.key2label]
        
    def copy_context_from(self, mode):
        assert isinstance(mode, Mode)
        self.sent = mode.sent
        self.current_word_index = mode.current_word_index
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
            
    def display_sentence(self):
        for piece in self.sentence_display_data():
            self.SCREEN.addstr(*piece)
        
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

    def key_pressed(self, keyboard_code):
        start,end = self.get_selection_range()
        if keyboard_code in self.key2label:
            for w in self.sent.words[start:end+1]:
                w.set_label(self.key2label[keyboard_code])
        else:
            raise ValueError("Invalid key %r pressed. Limited to %r" %(keyboard_code, 
                                                                       self.valid_annotation_chars))
    #######
    # The following changes
    #######
    def move_prev_word(self):
        self.current_word_index -= 1
        cur_word = self.sent[self.current_word_index]
        self.current_cursor_x -= len(cur_word)
        # curses.setsyx(self.current_cursor_y, self.current_cursor_x)
        
    def move_next_word(self):
        self.current_word_index += 1
        cur_word = self.sent[self.current_word_index]
        self.current_cursor_x += len(cur_word)

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
                if word.label is not None:
                    color_pair = curses.color_pair(word.label)
                else:
                    color_pair = curses.color_pair(DEFAULT_WORD_STYLE_ID)
            
            data.append((cur_y, cur_x+1, word.encode(ENCODING), color_pair))

            cur_x += (len(word)+1)
        return data

    def get_selection_range(self):
        return (self.current_word_index, self.current_word_index)
            
class SelectionMode(Mode):
    def __init__(self, *args, **kwargs):        
        # selected range info
        self.selected_anchor_index = None
        self.selected_drift_index = None

        super(SelectionMode, self).__init__(*args, **kwargs)

    def copy_context_from(self, mode):
        super(SelectionMode, self).copy_context_from(mode)
        
        self.selected_anchor_index = mode.current_word_index
        self.selected_drift_index = mode.current_word_index
        
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
                if word.label is not None:
                    color_pair = curses.color_pair(word.label)
                else:
                    color_pair = curses.color_pair(DEFAULT_WORD_STYLE_ID)
            data.append((cur_y, cur_x+1, word.encode(ENCODING), color_pair))

            cur_x += (len(word)+1)
        return data
                
    def move_prev_word(self):
        super(SelectionMode, self).move_prev_word()
        self.selected_drift_index -= 1
            
        # self.display_debug_info()
        
    def move_next_word(self):
        super(SelectionMode, self).move_next_word()
        self.selected_drift_index += 1
        
        # self.display_debug_info()

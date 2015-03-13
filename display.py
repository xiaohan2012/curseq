import curses

class DisplayData(object):
    def __init__(self, start_index, end_index, words):
        self.start_index = start_index
        self.end_index = end_index
        self.words = words
        
    def __repr__(self):
        return "DisplayData(start=%d, end=%d, data=%r)" %(self.start_index, self.end_index, self.words)

DEFAULT_WORD_STYLE_ID = 0
CURRENT_WORD_STYLE_ID = 1
HIGHLIGHT_WORD_STYLE_ID = 2

class Display(object):
    """Display that prints stuff on screen"""
    def __init__(self, screen, config):
        curses.init_pair(CURRENT_WORD_STYLE_ID, 0, curses.COLOR_WHITE)
        curses.init_pair(HIGHLIGHT_WORD_STYLE_ID, 0, curses.COLOR_GREEN)

        self.config = config
        self.screen = screen
        self.max_row, self.max_col = screen.getmaxyx()        
        
        self.sent_y = 17
        
        self.instruction_y = 0
        
        self.debug_info_y = 20
        self.error_info_y = 22
        
        self.word_spacing = 2
        self.line_space = 1        
        
        
    def display_sentence(self, data):        
        self.screen.clear()
        self.display_config()

        y = self.sent_y
        x = 0
        
        label_number = len(data.words[0]) - 1
        for i, word in enumerate(data.words):
            
            max_length = max([len(w) for w in  word])
            if x + max_length + self.word_spacing > self.max_col:
                y += (label_number + self.line_space + 1)
                x = 0
            
            for y_offset, stuff in enumerate(word):
                if y_offset == 0 and i >= data.start_index and i<= data.end_index:
                    style_id = CURRENT_WORD_STYLE_ID
                else:
                    style_id = DEFAULT_WORD_STYLE_ID

                self.screen.addstr(y+y_offset, x, stuff.encode("utf8"), curses.color_pair(style_id))
                    
            x += (max_length + self.word_spacing)
            
    def display_error(self, data):
        self.screen.addstr(self.error_info_y, 0, data)

    def display_pressed_key(self, c):
        self.screen.addch(self.debug_info_y, 0, c)

    def display_config(self):

        
        y = self.instruction_y
        self.screen.addstr(y, 0, "Labels:")
        
        y+=1; self.screen.addstr(y, 0, "-"*10)
        for group_name, labels in self.config["labels"].items():
            y+=1; self.screen.addstr(y, 0, "%s: %s" %(group_name, ' | '.join(labels)))
        
        y+=2; self.screen.addstr(y,0,"Control Keys:")
        y+=1; self.screen.addstr(y, 0, "-"*10)
        for key, value in self.config.items():
            if key != "labels":
                y+=1; self.screen.addstr(y, 0, "%s: %r" %(key, value))

        y+=2; self.screen.addstr(y,0,"Work Space:")
        y+=1; self.screen.addstr(y,0,"#"*20)

        if self.sent_y <= y: # adjust work space y 
            self.sent_y = y+1
            

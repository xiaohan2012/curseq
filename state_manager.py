from op import (Op, Label, CancelLabel, 
                CursorMoveOp, CursorLeft, CursorRight, CursorUp, CursorDown, 
                ConfirmSentence, SetMark)
from sent import Sentence
from display import DisplayData

class StateManager(object):
    """
    Internal state manager of the app

    >>> from session import AnnotationSession
    >>> session = AnnotationSession("data/test_data/session.pkl", "data/test_data/sents.txt", "data/test_data/output")
    >>> sm = StateManager(session, label_groups = ["label_set1"])
    >>> sm.current_index
    0
    >>> sm.receive(CursorLeft()); sm.receive(CursorLeft())
    >>> sm.current_index
    1
    >>> sm.receive(CursorRight())
    >>> sm.current_index
    2
    >>> sm.receive(CursorRight()); sm.receive(CursorRight()); sm.receive(CursorRight())
    >>> sm.current_index
    2
    >>> sm.receive(Label("label_set1", "some_label"))
    >>> sm.get_display_data()
    DisplayData(start=2, end=2, data=[('a', '-'), ('b', '-'), ('c', 'some_label')])
    >>> sm.cancel_label()
    >>> sm.get_display_data()
    DisplayData(start=2, end=2, data=[('a', '-'), ('b', '-'), ('c', '-')])
    >>> sm.cancel_label() # no effect
    >>> sm.get_display_data()
    DisplayData(start=2, end=2, data=[('a', '-'), ('b', '-'), ('c', '-')])
    >>> sm.set_mark() # mark on 
    >>> sm.select_on
    True
    >>> sm.receive(CursorLeft())
    >>> sm.get_selection_range()
    (1, 2)
    >>> sm.receive(Label("label_set1", "some_label"))
    >>> sm.get_display_data()
    DisplayData(start=2, end=2, data=[('a', '-'), ('b', 'some_label'), ('c', 'some_label')])
    >>> sm.select_on
    False
    >>> sm.cancel_label()
    >>> sm.receive(Label("label_set1", "some_label"))
    >>> sm.receive(ConfirmSentence())
    >>> print open("data/test_data/output/0.txt").read()
    a  -
    b  -
    c  some_label
    >>> sm.get_display_data()
    DisplayData(start=0, end=0, data=[('d', '-'), ('e', '-'), ('f', '-')])
    >>> sm.receive(ConfirmSentence())
    >>> print open("data/test_data/output/1.txt").read()
    d  -
    e  -
    f  -
    >>> import os
    >>> os.remove("data/test_data/session.pkl")
    >>> os.remove("data/test_data/output/0.txt")
    >>> os.remove("data/test_data/output/1.txt")
    """
    def __init__(self, session, label_groups):
        self.session = session
        
        self.set_sentence(session.next_sentence())

        self.label_groups = label_groups
        
        self.reset()
        
    def reset(self):
        self.selection_anchor = None
        self.selection_offset = None

        self.current_index = 0

        self.select_on = False

        self.labeled_ranges = []
        
    def set_sentence(self, sent):
        """ sent is unicode string"""
        self.sent = Sentence.from_unicode(sent)
        self.index_max = len(self.sent) - 1

    def receive(self, op):
        assert isinstance(op, Op)
        if isinstance(op, CursorMoveOp):
            if isinstance(op, CursorLeft):
                self.cursor_left()
            elif isinstance(op, CursorRight):
                self.cursor_right()
            elif isinstance(op, CursorUp):
                self.cursor_up()
            elif isinstance(op, CursorDown):
                self.cursor_down()

        elif isinstance(op, Label):
            self.label(op)
        elif isinstance(op, CancelLabel):
            self.cancel_label()
        elif isinstance(op, ConfirmSentence):
            self.confirm_sentence()
        elif isinstance(op, SetMark):
            self.set_mark()

    def get_selection_range(self):
        if self.select_on:
            start_index, end_index = self.selection_anchor, self.selection_anchor + self.selection_offset
            if self.selection_offset < 0:
                start_index, end_index = end_index, start_index
        else:
            start_index, end_index = self.current_index, self.current_index
            
        return start_index, end_index

    def label(self, label):
        start_index, end_index = self.get_selection_range()
        self.labeled_ranges.append((start_index, end_index))

        for word in self.sent[start_index : end_index+1]:
            word.set_label(label.group, label.name)
            
        # quit selection mode
        self.select_on = False

    def cancel_label(self):
        for i, (start, end) in enumerate(self.labeled_ranges):
            if self.current_index >= start and self.current_index <= end:
                for word in self.sent[start: end+1]:
                    word.reset_label()

                self.labeled_ranges.remove(self.labeled_ranges[i])
                break

    def confirm_sentence(self):
        # save
        self.session.save_annotation(self.get_annotation_data())

        # move on
        try:
            self.set_sentence(self.session.next_sentence())            
        except IOError:
            self.set_sentence("Sentence exhausts")
            self.session.close()
        self.reset()
    def set_mark(self):
        if self.select_on:
            self.select_on = False
        else:
            self.select_on = True

        if self.select_on:
            self.selection_anchor = self.current_index
            self.selection_offset = 0
        else:
            self.selection_anchor = None
            self.selection_offset = None

    def cursor_left(self):
        if self.select_on:
            if self.selection_anchor + self.selection_offset > 0:
                self.selection_offset -= 1
        else:
            if self.current_index > 0:
                self.current_index -= 1
            else:
                self.current_index = self.index_max
                
    def cursor_right(self):
        if self.select_on:
            if self.selection_anchor + self.selection_offset < self.index_max:
                self.selection_offset += 1
        else:
            if self.current_index < self.index_max:
                self.current_index += 1
            else:
                self.current_index = 0

    def cursor_up(self):
        raise NotImplementedError

    def cursor_down(self):
        raise NotImplementedError

    def get_annotation_data(self):
        data = []
        for w in self.sent:
            item = [unicode(w).encode('utf8')] 
            item += [w.labels.get(key, "-") for key in self.label_groups]
            data.append(tuple(item))
        return data
        
    def get_display_data(self):
        data = self.get_annotation_data()
            
        start, end = self.get_selection_range()
        
        return DisplayData(start, end, data)

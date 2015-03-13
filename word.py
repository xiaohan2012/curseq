#!/usr/bin/python
# coding=UTF-8
from errors import InvalidWordLabelError

class Word(unicode):
    u"""
    >>> w = Word(u"You")
    >>> w.set_label("role", "product")
    >>> w.labels
    {'role': 'product'}
    >>> w.reset_label()
    >>> w.labels
    {}
    """
    
    
    def __init__(self, s):
        self.labels = {}
        super(Word, self).__init__(s)
    
    def set_label(self, labelset_name, label):
        self.labels[labelset_name] = label

    def reset_label(self):
        self.labels = {}

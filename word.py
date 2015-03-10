#!/usr/bin/python
# coding=UTF-8
from errors import InvalidWordStateError

class Word(unicode):
    u"""
    >>> w = Word(u"€")
    >>> w
    W(`€`)
    >>> w.state 
    0
    >>> w.set_state(2)
    >>> w.state
    2
    >>> w.set_state(-1) # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    InvalidWordStateError...
    """
    
    STATE_DEFAULT = 0
    STATE_SELECTED = 1
    STATE_SUBJECT = 2
    STATE_PREDICATE = 3
    STATE_OJBECT = 4

    VALID_STATES = (STATE_DEFAULT, STATE_SUBJECT, STATE_SELECTED, 
                  STATE_PREDICATE, STATE_OJBECT)
    def __init__(self, s, state = STATE_DEFAULT):
        self.state = state
        super(Word, self).__init__(s)
    
    def set_state(self, state):
        if state not in Word.VALID_STATES:
            raise InvalidWordStateError("Valid states are %r" %(Word.VALID_STATES,))
        else:
            self.state = state

    def __repr__(self):
        return "W(`%s`)" %(unicode(self).encode("utf8"))

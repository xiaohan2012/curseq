#!/usr/bin/python
# coding=UTF-8
from errors import InvalidWordLabelError

class Word(unicode):
    u"""
    >>> w = Word(u"You")
    >>> w
    You
    >>> w.label 
    >>> w.set_label(Word.LABEL_SUBJECT)
    >>> w.label
    2
    >>> w.set_label(-1) # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    InvalidWordLabelError...
    >>> w
    <subject>You</subject>
    """
    
    
    LABEL_SUBJECT = 2
    LABEL_PREDICATE = 3
    LABEL_OJBECT = 4        
    
    VALID_LABELS = (LABEL_SUBJECT, LABEL_PREDICATE, LABEL_OJBECT)

    LABEL2TAG = {
        LABEL_SUBJECT: "subject",
        LABEL_PREDICATE: "predicate",
        LABEL_OJBECT: "object",
    }
    
    def __init__(self, s):
        self.label = None
        super(Word, self).__init__(s)
    
    def set_label(self, label):
        if label not in Word.VALID_LABELS:
            raise InvalidWordLabelError("Valid labels are %r" %(Word.VALID_LABELS,))
        else:
            self.label = label

    def __repr__(self):
        if self.label:
            tag = Word.LABEL2TAG[self.label]
            return "<%s>%s</%s>" %(tag, unicode(self).encode("utf8"), tag)
        else:
            return unicode(self).encode("utf8")

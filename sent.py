#!/usr/bin/python
# coding=UTF-8

import nltk
from word import Word

class Sentence(list):
    u"""
    
    >>> s = Sentence.from_unicode(u"I love €.")
    >>> s
    [u'I', u'love', u'\\u20ac', u'.']
    """

    def __init__(self, words, **kwargs):
        self.words = words
        super(Sentence, self).__init__(words, **kwargs)

    @classmethod
    def from_unicode(cls, s):
        words = [Word(w) 
                 for w in nltk.word_tokenize(s)]

        return Sentence(words)    

    def __getitem__(self, index):
        return self.words[index]

    def __repr__(self):
        return repr(self.words)

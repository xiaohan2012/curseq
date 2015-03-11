#!/usr/bin/python
# coding=UTF-8

import nltk
from word import Word

class Sentence(list):
    u"""
    
    >>> s = Sentence.from_unicode(u"I love €.")
    >>> s.words
    [W(`I`), W(`love`), W(`€`), W(`.`)]
    """

    def __init__(self, words, **kwargs):
        self.words = words
        super(Sentence, self).__init__(words, **kwargs)

    @classmethod
    def from_unicode(cls, s):
        words = [Word(w) 
                 for w in nltk.word_tokenize(s)]

        return Sentence(words)    

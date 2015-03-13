#!/usr/bin/python
# coding=UTF-8
"""
Handling the task continuation/break etc.
"""
import os
try:
    from cPickle import (load, dump)
except ImportError:
    from pickle import (load, dump)

import codecs
import tabulate

class SessionError(Exception):
    pass

class AnnotationSession(object):
    u"""
    >>> s = AnnotationSession("data/test_data/session.pkl", "data/test_data/sents.txt", "data/test_data/output")
    >>> s.current_sent_id
    -1
    >>> s.next_sentence()
    u'a b c'
    >>> s.current_sent_id
    0
    >>> s.close()
    >>> s.next_sentence()# doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    SessionError...
    >>> new_session = AnnotationSession("data/test_data/session.pkl")
    >>> new_session.next_sentence(); 
    u'a b c'
    >>> new_session.current_sent_id
    0
    >>> new_session.save_annotation([('a', '-', 'VB'), ('b', 'PROD', '-'), ('c', 'PER', '-')])
    >>> print open("data/test_data/output/0.txt").read()
    a  -     VB
    b  PROD  -
    c  PER   -
    >>> new_session.next_sentence(); 
    u'd e f'
    >>> new_session.close() # session canceled halfway
    
    >>> new_session = AnnotationSession("data/test_data/session.pkl")
    >>> new_session.next_sentence(); 
    u'd e f'
    >>> new_session.current_sent_id
    1
    >>> new_session.save_annotation([('d', '-', 'VB'), ('e', 'PROD', '-'), ('f', 'PER', '-')])
    >>> print open("data/test_data/output/1.txt").read()
    d  -     VB
    e  PROD  -
    f  PER   -
    >>> new_session.next_sentence(); s.next_sentence()# doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    IOError...
    >>> os.remove("data/test_data/session.pkl")
    >>> os.remove("data/test_data/output/0.txt")
    >>> os.remove("data/test_data/output/1.txt")

    >>> s = AnnotationSession("data/test_data/session.pkl", "data/test_data/unicode_test_sents.txt", "data/test_data/output")
    >>> sent = s.next_sentence()
    >>> s.save_annotation([(u"€400", u'-'), (u"£302m", u"-")])
    >>> os.remove("data/test_data/session.pkl")
    """
    def __init__(self, session_path, sentence_path = None, output_dir = None):
        self.active = True
        
        if os.path.exists(session_path):
            session_data = load(open(session_path))
            self.current_sent_id = session_data["current_sent_id"]            
            self.output_dir = session_data["output_dir"]
            self.sentence_path = session_data["sentence_path"]
            
            self.sent_file = codecs.open(self.sentence_path, "r", "utf8")
            
            for i in xrange(self.current_sent_id):
                self.sent_file.readline()

            if self.current_sent_id >= 0:
                self.current_sent_id -= 1 # to resume the process
        else:
            assert sentence_path is not None
            assert output_dir is not None
            
            self.output_dir = output_dir
            self.sentence_path = sentence_path
            self.current_sent_id = -1

            self.sent_file = codecs.open(self.sentence_path, "r", "utf8")

        self.session_path = session_path

    def get_session_data(self, ):
        return {"current_sent_id": self.current_sent_id, 
                "sentence_path": self.sentence_path, 
                "output_dir": self.output_dir} 
            
    def next_sentence(self):
        if self.active:
            line = self.sent_file.readline().strip()
            if len(line) == 0:
                raise IOError("No more to read from '%s'" %(self.sentence_path))
            # save the state automatically
            self.current_sent_id += 1
            self._save_session()
            
            return line
        else:
            raise SessionError("Session is not active")

    def _save_session(self):
        dump(self.get_session_data(), open(self.session_path, "w"))
        
    def save_annotation(self, annotation):
        if self.active:
            output_path = os.path.join(self.output_dir, "%d.txt" %(self.current_sent_id))
            with codecs.open(output_path, "w", "utf8") as f:
                f.write(tabulate.tabulate(annotation, tablefmt="plain"))

            self.annotated = True
        else:
            raise SessionError("Session is not active")
            
    def close(self):
        self.active = False

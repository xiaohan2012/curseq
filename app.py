#!/usr/bin/python
# coding=UTF-8

import curses
from curses import wrapper

import locale
locale.setlocale(locale.LC_ALL,"")

from session import AnnotationSession
from state_manager import StateManager
from trie_fsa import InvalidTransition
from app_fsa import AppFSA
from display import Display

from config import config

def main(stdscr):
    curses.start_color()
    curses.curs_set(0)

    fsa = AppFSA.from_config(config)
    
    session = AnnotationSession(".session/test", "data/20150213/sents.txt", "data/20150213/output")
    label_groups = config["labels"].keys()
    sm = StateManager(session, label_groups)
    
    display = Display(stdscr, config)
    display.display_sentence(sm.get_display_data())
    while True:        
        c = stdscr.getch()        
        try:
            c = chr(c)
        except ValueError:
            pass
        try:
            fsa.take(c)
        except InvalidTransition, e:
            display.display_error(str(e))
            continue
            
        if fsa.can_terminate:
            operation = fsa.ops[0]            
            sm.receive(operation)            
            display.display_sentence(sm.get_display_data())
            fsa.reset()
        else:
            continue
        
wrapper(main)

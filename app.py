#!/usr/bin/python
# coding=UTF-8

import curses
from curses import wrapper

import locale
locale.setlocale(locale.LC_ALL,"")

from sent import Sentence
from controller import Controller
from errors import CursorMoveError

from error_panel import ErrorPanel

KEY_RIGHT = ord("l")
KEY_LEFT = ord("j")

sentences = [u"AgustaWestland Introduces New Customer Service Plans For Its Commercial HelicoptersI", 
             u"The DSE is working to launch another subsidiary company for providing IT related services following the practice of other renowned stock exchanges across the world.", 
             u"With Songo Songo production declining below infrastructure capacity and markets continuing to expand, the company has been developing plans to embark upon a first phase of Songo Songo development,\" Orca said in its release."]

sentences = iter(sentences)

def main(stdscr):
    curses.start_color()
    curses.curs_set(0)

    ctrl = Controller(stdscr)
    
    err_panel = ErrorPanel(stdscr)
    
    while 1:
        c = stdscr.getch()

        if c == curses.KEY_ENTER or c == ord('\n'):
            sent = sentences.next()
            ctrl.set_sentence(Sentence.from_unicode(sent))
            ctrl.display_sentence()
                
        elif c == ord(' '):
            if ctrl.in_mode(Controller.MODE_SELECTION):
                ctrl.enter_mode(Controller.MODE_ORDINARY)
            else:
                ctrl.enter_mode(Controller.MODE_SELECTION)
            ctrl.display_sentence()
        elif c == KEY_RIGHT:
            try:
                ctrl.right_arrow_pressed()
            except CursorMoveError:
                pass
        elif c == KEY_LEFT:
            try:
                ctrl.left_arrow_pressed()
            except CursorMoveError:
                pass
        else:
            stdscr.addstr(8,0,"%c pressed" %chr(c))
            try:
                ctrl.key_pressed(c)
                #back to ordinary
                ctrl.enter_mode(Controller.MODE_ORDINARY)
                ctrl.display_sentence()
            except ValueError,  e:
                err_panel.print_error(str(e))

wrapper(main)

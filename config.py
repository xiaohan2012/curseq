import curses
config = {
    "labels": {
        "role": [{"name": "subject", "key": "a"}, 
                 {"name": "predicate", "key": "s"}, 
                 {"name": "object", "key": "d"}],
        "is_product": [{"name": "is_product", "key": "f"}],
    }, 
    "CancelLabel": curses.KEY_BACKSPACE,

    "CursorUp": "i",
    "CursorDown": "k",
    "CursorLeft": "j",
    "CursorRight": "l",

    "SetMark": " ",
    "ConfirmSentence": "\n",
}

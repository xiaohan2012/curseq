import curses
config = {
    "labels": {
        "role": ["subject", "predicate", "object"],
        "is_product": ["is_product"],
    }, 
    "CancelLabel": curses.KEY_BACKSPACE,

    "CursorUp": "i",
    "CursorDown": "k",
    "CursorLeft": "j",
    "CursorRight": "l",

    "SetMark": " ",
    "ConfirmSentence": "\n",
}

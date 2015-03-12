import curses
config = {
    "labels": {
        "role": ["subject", "predicate", "problem"],
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

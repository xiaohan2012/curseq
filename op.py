class Op(object):
    pass

####################
## Label operation
####################
class Label(Op):
    def __init__(self, group, name):
        self.group = group
        self.name = name

    def __str__(self):
        return "Label(%s, %s)" %(self.group, self.name)

    def __repr__(self):
        return str(self)

class CancelLabel(Op):
    pass

#####################
## Cursor movement 
#####################

class CursorMoveOp(Op):
    pass

class CursorLeft(CursorMoveOp):
    pass

class CursorRight(CursorMoveOp):
    pass

class CursorUp(CursorMoveOp):
    pass

class CursorDown(CursorMoveOp):
    pass

####################
## Other operations
####################
class ConfirmSentence(Op):
    pass

class SetMark(Op):
    pass

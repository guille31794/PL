# ==============================================================================
#  MY GRAMMAR FOR A BOOLEAN CALCULATOR
# (ASCENDING IMPLEMENTATION USING SLY WITH AST DECORATION):
# ==============================================================================
# entry   -> entry instruc ';'  instruc.s.action()
#         -> ε
#
# instruc -> type_ opor         instruc.s = new nodeInstruc(type_.s, opor.s)
#
# type_   -> ID EQ              type_.s   = new nodeAssign(ID.lexval)
#         -> PRINT              type_.s   = new nodePrint()
#
# opor    -> opor1 OR opand     opor.s    = new nodeOr(opor1.s, opand.s)
#         -> opand              opor.s    = opand.s
#
# opand   -> opand1 AND opnot   opand.s   = new nodeAnd(opand1.s, opnot.s)
#         -> opnot              opand.s   = opnot.s
#
# opnot   -> NOT brace          opnot.s   = new nodeNot(brace.s)
#         -> brace              opnot.s   = brace.s
#
# brace   -> '(' opor ')'       brace.s   = opor.s
#         -> ID                 brace.s   = new nodeID(ID.lexval)
#         -> TRUE               brace.s   = new nodeTrue()
#         -> FALSE              brace.s   = new nodeFalse()
# ==============================================================================
from sly import Lexer, Parser


class eLexer(Lexer):
    tokens = {ID, EQ, PRINT, OR, AND, NOT, TRUE, FALSE}
    ignore = " \t"
    literals = {"(", ")", ";"}

    EQ = r":="
    ID = r"[a-zA-Z_][a-zA-Z0-9_]*"

    ID["true"] = TRUE
    ID["false"] = FALSE
    ID["not"] = NOT
    ID["and"] = AND
    ID["or"] = OR
    ID["print"] = PRINT


# End Lexer


table = {}


class node:
    def action(self):
        pass


class nodeInstruc(node):
    def __init__(self, n1, n2):
        self.n1 = n1
        self.n2 = n2

    def action(self):
        return self.n1.action(self.n2.action())


class nodeAssign(node):
    def __init__(self, id_):
        self.id_ = id_

    def action(self, val):
        table[self.id_] = val


class nodePrint(node):
    def action(self, val):
        print("El resultado es " + str(int(val)))


class nodeOr(node):
    def __init__(self, n1, n2):
        self.n1 = n1
        self.n2 = n2

    def action(self):
        return self.n1.action() or self.n2.action()


class nodeAnd(node):
    def __init__(self, n1, n2):
        self.n1 = n1
        self.n2 = n2

    def action(self):
        return self.n1.action() and self.n2.action()


class nodeNot(node):
    def __init__(self, n):
        self.n = n

    def action(self):
        return not self.n.action()


class nodeID(node):
    def __init__(self, id_):
        self.id_ = id_

    def action(self):
        return table[self.id_]


class nodeTrue(node):
    def action(self):
        return True


class nodeFalse(node):
    def action(self):
        return False


class eParser(Parser):
    tokens = eLexer.tokens

    def __init__(self):
        self.names = {}

    @_('entry instruc ";"')
    def entry(self, p):
        p.instruc.action()

    @_("")
    def entry(self, p):
        pass

    @_("type_ opor")
    def instruc(self, p):
        return nodeInstruc(n1=p.type_, n2=p.opor)

    @_("ID EQ")
    def type_(self, p):
        return nodeAssign(id_=p.ID)

    @_("PRINT")
    def type_(self, p):
        return nodePrint()

    @_("opor OR opand")
    def opor(self, p):
        return nodeOr(n1=p.opand, n2=p.opnot)

    @_("opand")
    def opor(self, p):
        return p.opand

    @_("opand AND opnot")
    def opand(self, p):
        return nodeAnd(n1=p.opand, n2=p.opnot)

    @_("opnot")
    def opand(self, p):
        return p.opnot

    @_("NOT brace")
    def opnot(self, p):
        return nodeNot(n=p.brace)

    @_("brace")
    def opnot(self, p):
        return p.brace

    @_('"(" opor ")"')
    def brace(self, p):
        return p.opor

    @_("ID")
    def brace(self, p):
        return nodeID(id_=p.ID)

    @_("TRUE")
    def brace(self, p):
        return nodeTrue()

    @_("FALSE")
    def brace(self, p):
        return nodeFalse()


# End Parser

if __name__ == "__main__":
    lexer = eLexer()
    parser = eParser()

    while True:
        try:
            data = input("> ")
        except EOFError:
            break
        if data:
            parser.parse(lexer.tokenize(data))

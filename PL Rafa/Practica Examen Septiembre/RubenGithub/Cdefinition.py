# ==============================================================================
#  MY GRAMMAR FOR C DEFINITION WITH POINTERS
# (ASCENDING IMPLEMENTATION USING SLY):
# ==============================================================================
# defi  -> type {list_.h = type.s} list_ ';' defi
#       -> ε
#
# type_ -> INT              type_.s = NodoInt()
#       -> CHAR             type_.s = NodoChar()
#       -> FLOAT            type_.s = NodoFloat()
#
# list_ -> {elemt.h = list_.h} elemt {rest.h = list_.h} rest
#
# rest  -> ',' {elemt.h = rest.h} elemt {rest1.h = rest.h} rest1
#       -> ε
#
# elemt -> '*' {elemt1.h = NodePointer(elemt.h)} elemt1
#       -> ID  table[ID.lexval] = elemt.h
# ==============================================================================
from sly import Lexer, Parser


class defLexer(Lexer):
    tokens = {INT, FLOAT, CHAR, ID}
    ignore = " \t"
    literals = {";", ",", "*"}

    ID = r"[a-zA-Z_][0-9a-zA-Z_]*"
    ID["char"] = CHAR
    ID["int"] = INT
    ID["float"] = FLOAT


table = {}


class Node:
    def print_(self):
        pass


class NodePointer(Node):
    def __init__(self, n):
        self.n = n

    def print_(self):
        return "pointer to " + self.n.print_()


class NodeInt(Node):
    def print_(self):
        return "int"


class NodeFloat(Node):
    def print_(self):
        return "float"


class NodeChar(Node):
    def print_(self):
        return "char"


class defParser(Parser):
    tokens = defLexer.tokens

    def __init__(self):
        self.names = {}

    @_('type_ list_ ";" defi')
    def defi(self, t):
        return t.type_

    @_("")
    def defi(self, t):
        pass

    @_("INT")
    def type_(self, t):
        return NodeInt()

    @_("CHAR")
    def type_(self, t):
        return NodeChar()

    @_("FLOAT")
    def type_(self, t):
        return NodeFloat()

    @_("empty5 elemt empty4 rest")
    def list_(self, t):
        return t[-2]

    @_("")
    def empty4(self, t):
        return t[-3]

    @_("")
    def empty5(self, t):
        return t[-1]

    @_('"," empty3 elemt empty2 rest')
    def rest(self, t):
        return t[-4]

    @_("")
    def empty2(self, t):
        return t[-4]

    @_("")
    def empty3(self, t):
        return t[-2]

    @_("")
    def rest(self, t):
        return t[-1]

    @_('"*" empty1 elemt')
    def elemt(self, t):
        return t.empty1

    @_("")
    def empty1(self, t):
        return NodePointer(t[-2])

    @_("ID")
    def elemt(self, t):
        table[t.ID] = t[-2].print_()


if __name__ == "__main__":

    lexer = defLexer()
    parser = defParser()

    while True:
        try:
            data = input("\n --> ")
        except EOFError:
            break
        if data:
            parser.parse(lexer.tokenize(data))
        print(table)

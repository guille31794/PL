# ==============================================================================
#  MY GRAMMAR FOR C DEFINITION WITH POINTERS
# (ASCENDING IMPLEMENTATION USING SLY):
# ==============================================================================
# entry -> entry defi ';'
#       -> ε
#
# defi  -> type_ elem rest
#
# type_ -> INT                  
#       -> CHAR             
#       -> FLOAT            
#
# elem  -> '*' elem
#       -> ID
#
# rest  -> ',' elem rest
#       -> ε
# ==============================================================================
from sly import Lexer, Parser


class c_defLexer(Lexer):
    tokens = {INT, CHAR, FLOAT, ID}
    ignore = " \t"
    literals = {"*", ",", ";"}

    ID = r"[a-zA-z_][a-zA-z0-9_]*"
    ID["int"] = INT
    ID["char"] = CHAR
    ID["float"] = FLOAT


# End Lexer

table = {}


class Node:
    def print_(self):
        pass


class NodeInt(Node):
    def print_(self):
        return "int"


class NodeChar(Node):
    def print_(self):
        return "char"


class NodeFloat(Node):
    def print_(self):
        return "float"


class NodePointer(Node):
    def __init__(self, n):
        self.n = n

    def print_(self):
        return "pointer to " + self.n.print_()


class c_defParser(Parser):
    tokens = c_defLexer.tokens

    def __init__(self):
        self.names = {}

    @_('entry defi ";"')
    def entry(self, p):
        pass

    @_("")
    def entry(self, p):
        pass

    @_("type_ empty1 elem empty2 rest")
    def defi(self, p):
        pass

    @_("")
    def empty1(self, p):
        return p[-1]  # return the value of type to elem

    @_("")
    def empty2(self, p):
        return p[-3]

    @_("INT")
    def type_(self, p):
        return NodeInt()

    @_("CHAR")
    def type_(self, p):
        return NodeChar()

    @_("FLOAT")
    def type_(self, p):
        return NodeFloat()

    @_('"*" empty5 elem')
    def elem(self, p):
        pass

    @_("")
    def empty5(self, p):
        return NodePointer(n=p[-2])

    @_("ID")
    def elem(self, p):
        table[p.ID] = p[-2].print_()

    @_('"," empty3 elem empty4 rest')
    def rest(self, p):
        pass

    @_("")
    def empty3(self, p):
        return p[-2]

    @_("")
    def empty4(self, p):
        return p[-4]

    @_("")
    def rest(self, p):
        pass


# End Parser

if __name__ == "__main__":

    lexer = c_defLexer()
    parser = c_defParser()

    while True:
        try:
            text = input("> ")
        except EOFError:
            break
        if text:
            parser.parse(lexer.tokenize(text))
        print(table)

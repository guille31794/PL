# ==============================================================================
# My translation scheme for offset parameters Pascal style.
# That is, the parameters are put on the stack from left to right.
# ==============================================================================
# entry -> ID '(' type_ ID rest ')'     print("Offset de" +p.ID1+ '=' +p.rest)
#
# rest  -> ',' type_ ID rest            print("Offset de" +p.ID1+ '=' +p.rest)
#                                       rest.s  = p.rest '+' p.type_
#       -> ε                            rest.s  = 4
#
# type_ -> INT                          type_.s = sizeof(int)
#       -> CHAR                         type_.s = sizeof(char)
#       -> FLOAT                        type_.s = sizeof(float)
# ==============================================================================
from sly import Lexer, Parser


class offsetLexer(Lexer):
    tokens = {ID, INT, CHAR, FLOAT}
    ignore = " \t"
    literals = {"(", ")", ","}

    ID = r"[a-zA-Z_][a-zA-Z_]*"
    ID["int"] = INT
    ID["char"] = CHAR
    ID["float"] = FLOAT


# End Lexer


class offsetParser(Parser):
    tokens = offsetLexer.tokens

    def __init__(self):
        self.names = {}

    @_('ID "(" type_ ID rest ")"')
    def entry(self, p):
        print("Offset de " + p.ID1 + " = " + p.rest)

    @_('"," type_ ID rest')
    def rest(self, p):
        print("Offset de " + p.ID + " = " + p.rest)
        return p.rest + " +" + p.type_

    @_("")
    def rest(self, p):
        return "4"

    @_("INT")
    def type_(self, p):
        return " sizeof(int)"

    @_("CHAR")
    def type_(self, p):
        return " sizeof(char)"

    @_("FLOAT")
    def type_(self, p):
        return " sizeof(float)"


# End Parser


if __name__ == "__main__":
    lexer = offsetLexer()
    parser = offsetParser()

    while True:
        try:
            data = input("> ")
        except EOFError:
            break
        if data:
            parser.parse(lexer.tokenize(data))

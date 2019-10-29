# ==============================================================================
#  MY GRAMMAR FOR PASS A BINARY NUMBER TO DECIMAL NUMBER.
# This definition supports binary floating point numbers and calculates its
# value. Example: 10011.101 => 19.625;
#  (ASCENDING IMPLEMENTATION USING SLY):
# ==============================================================================
# entry  -> entry binNum ';'
#        -> ε
#
# binNum -> sec comma
#
# comma  -> '.' sec
#        -> ε
#
# sec    -> sec dig
#        -> dig
#
# dig    -> DIGIT
# ==============================================================================
from sly import Lexer, Parser


class Bin2DecLexer(Lexer):
    tokens = {DIGIT}
    ignore = " \t"
    literals = {".", ";"}

    DIGIT = r"[0-1]+"


class Bin2DecParser(Parser):
    tokens = Bin2DecLexer.tokens

    def __init__(self):
        self.names = {}

    @_('entry binNum ";"')
    def entry(self, t):
        print(" 10 base number --> " + str(t.binNum))

    @_("")
    def entry(self, t):
        pass

    @_("sec comma")
    def binNum(self, t):
        number = 0.0
        longIzq = len(t.sec)
        cont = longIzq - 1
        for i in range(0, longIzq):
            number += float(t.sec[cont]) * pow(2, i)
            cont -= 1
        if t.comma != "empty":
            longDrch = len(t.comma)
            for i in range(0, longDrch):
                number += float(t.comma[i]) * pow(2, -(i + 1))
        return number

    @_('"." sec')
    def comma(self, t):
        return t.sec

    @_("")
    def comma(self, t):
        return "empty"

    @_("sec dig")
    def sec(self, t):
        return t.sec + t.dig

    @_("dig")
    def sec(self, t):
        return t.dig

    @_("DIGIT")
    def dig(self, t):
        return t.DIGIT


if __name__ == "__main__":

    lexer = Bin2DecLexer()
    parser = Bin2DecParser()

    while True:
        try:
            data = input("\n Binary number  --> ")
        except EOFError:
            break
        if data:
            parser.parse(lexer.tokenize(data))

# ==============================================================================
#  MY GRAMMAR FOR A BASIC CALCULATOR (ASCENDING IMPLEMENTATION USING SLY):
# ==============================================================================
# entry -> entry expr ';'   print(expr.s)
#       -> ε
#
# expr  -> expr '+' add     expr.s  = expr1.s + add.s
#       -> add              expr.s  = add.s
#
# add   -> add '-' sub      add.s   = add1.s - sub.s
#       -> sub              add.s   = sub.s
#
# sub   -> sub '*' fact     sub.s   = sub1.s * fact.s
#       -> fact             sub.s   = fact.s
#
# fact  -> fact '/' final   fact.s  = fact1.s / final.s
#       -> '-' final        fact.s  = - final.s
#       -> final            fact.s  = final.s
#
# final -> '(' expr ')'     final.s = expr.s
#       -> NUM              final.s = NUM.lexval
# ==============================================================================
from sly import Lexer, Parser


class CalcLexer(Lexer):
    tokens = {NUM}
    ignore = " \t"
    literals = {"+", "-", "*", "/", "(", ")", ";"}

    NUM = r"[0-9]+"

    @_(r"[0-9]+")
    def NUM(self, t):
        t.value = int(t.value)
        return t


class CalcParser(Parser):
    tokens = CalcLexer.tokens

    def __init__(self):
        self.names = {}

    @_('entry expr ";"')
    def entry(self, t):
        print(t.expr)

    @_("")
    def entry(self, t):
        print(" ")

    @_('expr "+" add')
    def expr(self, t):
        return t.expr + t.add

    @_("add")
    def expr(self, t):
        return t.add

    @_('add "-" sub')
    def add(self, t):
        return t.add - t.sub

    @_("sub")
    def add(self, t):
        return t.sub

    @_('sub "*" fact')
    def sub(self, t):
        return t.sub * t.fact

    @_("fact")
    def sub(self, t):
        return t.fact

    @_('fact "/" final')
    def fact(self, t):
        return t.fact / t.final

    @_('"-" final')
    def fact(self, t):
        return -t.final

    @_("final")
    def fact(self, t):
        return t.final

    @_('"(" expr ")"')
    def final(self, t):
        return t.expr

    @_("NUM")
    def final(self, t):
        return t.NUM


if __name__ == "__main__":

    lexer = CalcLexer()
    parser = CalcParser()

    while True:
        try:
            data = input("---> ")
        except EOFError:
            break
        if data:
            parser.parse(lexer.tokenize(data))

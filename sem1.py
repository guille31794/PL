from sly import Lexer, Parser

class CalcLexer(Lexer):
    tokens = {DIGIT}

    ignore = ' \t'
    literals = {'.'}

    @_(r'[0-1]')
    def DIGIT(self, p):
        p.value = int(p.value)
        return p


class CalcParser(Parser):
    tokens = CalcLexer.tokens

    @_('num')
    def entrada(self, p):
        print(" Decimal value is: ", p.num)

    @_('sec "." sec')
    def num(self, p):
        return p.sec0[0] + p.sec1[0] / pow(2, p.sec1[1])
    
    @_('sec dig')
    def sec(self, p):
        return [p.sec[0] * 2 + p.dig, p.sec[1] + 1]

    @_('dig')
    def sec(self, p):
        return [p.dig, 1]

    @_('DIGIT')
    def dig(self, p):
        return p.DIGIT

if __name__ == "__main__":
    lexer = CalcLexer()
    parser = CalcParser()
    while True:
        try:
            text = input('Insert Binary Number > ')
        except EOFError:
            break
        if text:
            parser.parse(lexer.tokenize(text))
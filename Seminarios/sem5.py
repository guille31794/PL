from sly import Lexer, Parser

ta = None
ind = 0
tokens = None
tokenlist = None

class CalcLexer(Lexer):
    tokens = {ID, CHAR, INT, FLOAT}
    ignore = ' \t'
    literals = {',', '(', ')'}

    # Regular expression rules for tokens
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    ID['char'] = CHAR
    ID['int'] = INT
    ID['float'] = FLOAT

    @_(r'\n+')
    def newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1

from sly import Lexer,Parser

Tabla = {}

class CalcLexer(Lexer):
    # Set of tokens
    tokens = { NUMBER, ID, PLUS, MINUS,
    TIMES, DIVIDE, ASSIGN, EQ, AND, OR, NOT,
    LT, GT, LE, GE}

    literals = { '(', ')', '{', '}', ';'}

    ignore = ' \t'
    #ignore_comment = r''
    #ignore_comment_line = r'//'

    # RegEx for tokens
    PLUS = r'\+'
    MINUS = r'-'
    TIMES = r'\*'
    DIVIDE = r'/'
    EQ = r'=='
    ASSIGN = r'='
    AND = r'&&'
    OR = r'\|\|' 
    NOT = r'!'
    LT = r'<'
    GT = r'>'
    LE = r'<='
    GE = r'>='

    @_(r'\d+')
    def NUMBER(self, t):
        t.value = int(t.value)
        return t

    # Identifiers and keywords
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    
class CalcParser(Parser):
    # Get the token list from the lexer
    tokens = CalcLexer.tokens

    # Grammar rules and actions
    @_('ID ASSIGN expr ";"')
    def assign(self, p):
        Tabla[p.ID] = p.expr
        return Tabla[p.ID]

    @_('expr')
    def assign(self, p):
        return p.expr

    @_('expr AND term')
    def expr(self, p):
        return p.expr and p.term

    @_('expr OR term')
    def expr(self, p):
        return p.expr or p.term
    
    @_('term')
    def expr(self, p):
        return p.term

    @_('term EQ logic')
    def term(self,p):
        return p.term == p.logic

    @_('logic')
    def term(self, p):
        return p.logic

    @_('logic PLUS factor')
    def logic(self, p):
        return p.logic + p.factor

    @_('logic MINUS factor')
    def logic(self, p):
        return p.logic - p.factor

    @_('factor')
    def logic(self, p):
        return p.factor

    @_('factor TIMES cipher')
    def factor(self, p):
        return p.factor * p.cipher

    @_('factor DIVIDE cipher')
    def factor(self, p):
        return p.factor / p.cipher 

    @_('cipher')
    def factor(self, p):
        return p.cipher

    @_('MINUS cipher')
    def cipher(self, p):
        return - p.cipher

    @_('NOT cipher')
    def cipher(self, p):
        return ~p.cipher

    @_('ID')
    def cipher(self, p):
        if p.ID not in Tabla:
            Tabla[p.ID] = 0

        return Tabla[p.ID]
    
    @_('NUMBER')
    def cipher(self, p):
        return p.NUMBER

if __name__ == "__main__":
    lexer = CalcLexer()
    parser = CalcParser()

    while True:
        try:
            text = input('calc > ')
            result = parser.parse(lexer.tokenize(text))
            print(result)
            print(Tabla)
        except EOFError:
            break 
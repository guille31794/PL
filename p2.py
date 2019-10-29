from sly import Lexer,Parser

Tabla = {}

class CalcLexer(Lexer):
    # Set of tokens
    tokens = { NUMBER, ID, PLUS, MINUS,
    TIMES, DIVIDE, ASSIGN, EQ, AND, OR, NOT,
    LT, GT, LE, GE, NE, PR, WORD, STR}

    literals = { '(', ')', '{', '}', ';', '"', '%' ','}

    ignore = ' \t'

    # RegEx for tokens
    PLUS = r'\+'
    MINUS = r'-'
    TIMES = r'\*'
    DIVIDE = r'/'
    EQ = r'=='
    ASSIGN = r'='
    AND = r'&&'
    OR = r'\|\|'
    NE = r'!=' 
    NOT = r'!'
    LT = r'<'
    GT = r'>'
    LE = r'<='
    GE = r'>='
    PR = r'printf'

    @_(r'\d+')
    def NUMBER(self, t):
        t.value = int(t.value)
        return t

    # Identifiers and keywords
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'

    #STR = r'[a-zA-Z!¿?]'
    
class CalcParser(Parser):
    # Get the token list from the lexer
    tokens = CalcLexer.tokens

    # Grammar rules and actions
    '''
    @_('PR "(" \" expr \" ")", ')
    @_('PR "(" string vars")" ";"')
    def print(self, p):
        print(p.str)

    @_('str word')
    def string(self, p):
    '''

    @_('ID ASSIGN expr ";"')
    def assign(self, p):
        Tabla[p.ID] = p.expr
        return Tabla[p.ID]

    @_('expr ";"')
    def assign(self, p):
        return p.expr

    @_('expr AND term')
    def expr(self, p):
        return p.expr and p.term

    @_('expr OR term')
    def expr(self, p):
        if(p.expr or p.term):
            return 1
        else:
            return 0
        
    @_('term')
    def expr(self, p):
        return p.term

    @_('term EQ logic')
    def term(self,p):
        return int(p.term == p.logic)

    @_('logic')
    def term(self, p):
        return p.logic

    @_('logic NE neqExpr')
    def logic(self, p):
        return int(p.logic != p.neqExpr)

    @_('neqExpr')
    def logic(self, p):
        return p.neqExpr

    @_('neqExpr LT operator')
    def neqExpr(self, p):
        return int(p.neqExpr < p.operator)

    @_('neqExpr GT operator')
    def neqExpr(self, p):
        return int(p.neqExpr > p.operator)

    @_('operator')
    def neqExpr(self, p):
        return p.operator

    @_('operator LE operatorEQ')
    def operator(self, p):
        return int(p.operator <= p.operatorEQ)

    @_('operator GE operatorEQ')
    def operator(self, p):
        return int(p.operator >= p.operatorEQ)

    @_('operatorEQ')
    def operator(self, p):
        return p.operatorEQ

    @_('operatorEQ MINUS factor')
    def operatorEQ(self, p):
        return p.operatorEQ - p.factor

    @_('operatorEQ PLUS factor')
    def operatorEQ(self, p):
        return p.operatorEQ + p.factor

    @_('factor')
    def operatorEQ(self, p):
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
        return int(not p.cipher)

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
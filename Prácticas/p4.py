from sly import Lexer, Parser

Tabla = {}
printf = []

class CalcLexer(Lexer):
    # Set of tokens
    tokens = {NUMBER, ID, PLUS, MINUS,
              TIMES, DIVIDE, ASSIGN, EQ, AND, OR, NOT,
              LT, GT, LE, GE, NE, PR, CAD, INT}

    literals = {'(', ')', '{', '}', ';', '"', '%', ','}

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
    INT = r'int'

    @_(r'\d+')
    def NUMBER(self, t):
        t.value = int(t.value)
        return t

    # Identifiers and keywords
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'

    @_(r'\"[\w\s\%,]*\"')
    def CAD(self, t):
        t.value = str(t.value)
        return t

class CalcParser(Parser):
    # Get the token list from the lexer
    tokens = CalcLexer.tokens

    # Grammar rules and actions
    @_('PR "(" CAD param ";"')
    def entrada(self, p):
        if p.CAD.find("%d%") > -1:
            cad = p.CAD.replace("%d", str(printf.pop()), 1)
            while cad.find("%d") > -1:
                cad = cad.replace("%d", str(printf.pop()), 1)
            print(cad[1:len(cad)-1])
        elif p.CAD.find("%d ") > -1:
            cad = p.CAD.replace("%d", str(printf.pop()), 1)
            while cad.find("%d") > -1:
                cad = cad.replace("%d", str(printf.pop()), 1)
            print(cad[1:len(cad)-1])
        elif p.CAD.find("%d\"") > -1:
            cad = p.CAD.replace("%d", str(printf.pop()), 1)
            while cad.find("%d") > -1:
                cad = cad.replace("%d", str(printf.pop()), 1)
            print(cad[1:len(cad)-1])
        else:
            print(p.CAD[1:len(p.CAD)-1])

    @_('"," ID param')
    def param(self, p):
        printf.append(Tabla[p.ID])

    @_('")"')
    def param(self, p):
        pass      

    @_('declare ";"')
    def entrada(self, p):
        return p.declare

    @_('assign ";"')
    def entrada(self, p):
        return p.assign

    @_('INT vars')
    def declare(self, p):
        pass
        
    @_('INT assign')
    def declare(self, p):
        return p.assign
        
    @_('ID')
    def vars(self,p):
        if p.ID not in Tabla:
            Tabla[p.ID] = 0
        else:
            print("Error,", p.ID, "re-declared.")
    
    @_('ID "," vars')
    def vars(self, p):
        if p.ID not in Tabla:
            Tabla[p.ID] = 0
        else:
            print("Error,", p.ID, "re-declared.")

    @_('ID ASSIGN assign')
    def assign(self, p):
        Tabla[p.ID] = p.assign
        return Tabla[p.ID]

    @_('expr')
    def assign(self, p):
        return p.expr

    @_('expr AND term')
    def expr(self, p):
        if(p.expr and p.term):
            return 1
        else:
            return 0

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
    def term(self, p):
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

    @_('"(" assign ")"')
    def cipher(self, p):
        return p.assign


if __name__ == "__main__":
    lexer = CalcLexer()
    parser = CalcParser()

    while True:
        try:
            text = input('calc > ')
            result = parser.parse(lexer.tokenize(text))
        except EOFError:
            break

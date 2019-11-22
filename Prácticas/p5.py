from sly import Lexer, Parser

Variables = {}
Pointer = {}
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
    @_('whatever ";" sentence')
    def sentence(self, p):
        pass
    
    @_('')
    def sentence(self, p):
        pass
    
    @_('printf')
    def whatever(self, p):
        pass

    @_('declaration')
    def whatever(self, p):
        pass

    @_('assign')
    def whatever(self, p):
        pass

    @_('PR "(" CAD param')
    def printf(self, p):
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
        printf.append(Variables[p.ID])

    @_('")"')
    def param(self, p):
        pass      
    
    @_('INT types')
    def declaration(self, p):
        pass

    @_('variable')
    def types(self, p):
        pass

    '''@_('pointer')
    def types(self, p):
        pass'''

    @_('ID empty1 empty4 variableSeparator')
    def variable(self, p):
        if p.empty1:
            if p.empty4:
                Variables[p.ID] = 0
                return Variables[p.ID]
            else:
                print("error: conflicting types for", p.ID)
        else:
            print("Error.", p.ID, "redeclared.")
    
    @_('ID ASSIGN empty2 empty5 cipher variableSeparator')
    def variable(self, p):
        if p.empty2:
            if p.empty5:
                Variables[p.ID] = p.cipher
                return Variables[p.ID]
            else:
                print("error: conflicting types for", p.ID)
        else:
            print("Error.", p.ID, "redeclared")

    @_('"," variable')
    def variableSeparator(self, p):
        pass
    
    @_('')
    def variableSeparator(self,p):
        pass

    @_('ID ASSIGN empty3 assign')
    def assign(self, p):
        if p.empty3:
            Variables[p.ID] = p.assign
            return Variables[p.ID]
        else:
            print("Error.", p.ID, "not declared")

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
        if p.ID not in Variables:
            Variables[p.ID] = 0

        return Variables[p.ID]

    @_('NUMBER')
    def cipher(self, p):
        return p.NUMBER

    @_('"(" assign ")"')
    def cipher(self, p):
        return p.assign

    # Controls wether or not variable is declared
    # previously to declaration
    @_('')
    def empty1(self, p):
        if p[-1] in Variables:
            return False
        else:
            return True

    # Controls wether or not variable is declared
    # previously to initialization
    @_('')
    def empty2(self, p):
        if p[-2] in Variables:
            return False
        else:
            return True

    # Controls wether or not variable is declared
    # previously to assignation
    @_('')
    def empty3(self, p):
        if p[-2] in Variables:
            return True
        else:
            return False

    # Controls wether or not a variable name it's
    # a declared pointer
    @_('')
    def empty4(self, p):
        if p[-2] in Pointer:
            return False
        else:
            return True

    @_('')
    def empty5(self, p):
        if p[-3] in Pointer:
            return False
        else:
            return True

if __name__ == "__main__":
    lexer = CalcLexer()
    parser = CalcParser()

    while True:
        try:
            text = input('calc > ')
            result = parser.parse(lexer.tokenize(text))
            print(Variables)
        except EOFError:
            break

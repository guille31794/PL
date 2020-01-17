from sly import Lexer

class CalcLexer(Lexer):
    # Set of tokens
    tokens = {NUMBER, ID, PLUS, MINUS,
              TIMES, DIVIDE, ASSIGN, EQ, AND, OR, NOT,
              LT, GT, LE, GE, NE, PR, CAD, INT, AMPERSAND, SC}

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
    AMPERSAND = r'&'
    SC = r'scanf'

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
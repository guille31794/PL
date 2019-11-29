from sly import Lexer, Parser
import sys

Variables = {}
Pointer = {}
printf = []
scanf = []

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

class Node():
    def write():
        pass

class IntNode():
    def write(self, p):
        return (int)p

class SumNode():
    def write(s1, s2):
        return s1 + s2

class SubNode():
    def write(s1, s2):
        return s1 - s2

class ProdNode():
    def write(s1, s2):
        return s1 * s2

class DivNode():
    def write(s1, s2):
        return s1 / s2

class UnaryNode():
    def write(s):
        return -s

class AndNode():
    def write(s1, s2):
        if s1 and s2:
            return 1
        else:
            return 0

class OrNode():
    def write(s1, s2):
        if s1 or s2:
            return 1
        else: 
            return 0

class NotNode():
    def write(s1):
        return int(not s1)

class GrNode():
    def write(s1, s2):
        return int(s1 > s2)

class LsNode():
    def write(s1, s2):
        return int(s1 < s2)

class GrEqNode():
    def write(s1, s2):
        return int(s1 >= s2)

class LsEqNode():
    def write(s1, s2):
        return int(s1 <= s2)

class DistincNode():
    def write(s1, s2):
        return int(s1 != s2)



if __name__ == "__main__":
    lexer = CalcLexer()

    while True:
        try:
            text = input('calc > ')
            result = parser.parse(lexer.tokenize(text))
            print(Variables)
            print(Pointer)
        except EOFError:
            break

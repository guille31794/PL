'''
Exercise 1

1) Tree in the picture

2)  
    S.s
    A.s
    ID.s
    X.lexval
    Y.lexval
    Z.lexval
    K.lexval
    
3)
    S.s := A.s
    A.s := A1.s*10 + ID.lexval
    ID.s := X.lexval
    ID.s := Y.lexval
    ID.s := Z.lexval
    ID.s := K.lexval
    X.lexval := 1
    Y.lexval := 2
    Z.lexval := 3
    K.lexval := 4

Exercise 2

1) Tree in the picture

2)
    S.s
    A.s
    ID.s
    X.lexval
    Y.lexval
    Z.lexval
    K.lexval

3)
    S -> {A1.h := A2.s;}A 
    A -> {ID.h = A1.h*10}ID + {A2.h = ID.s}A
    ID -> {}X
        | Y
        | Z
        | K
    X.lexval -> 1
    Y.lexval -> 2
    Z.lexval -> 3
    K.lexval -> 4
'''

from sly import Lexer, Parser
tabla = {}

class CalcLexer(Lexer):
    tokens = {ID}
    ignore = ' \t'

    # Regular expression rules for tokens
    ID = r'[A-Z]'
    
    @_(r'\n+')
    def newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1

class CalcParser(Parser):
    tokens = CalcLexer.tokens

    def __init__(self):
        self.names = { }

    @_('empty1 A')
    def S(self, p):
        pass
    
    @_(' ')
    def empty1(self, p):
        return 0
    
    @_('ID empty2 A')
    def A(self, p):
        tabla[p.ID] = p[-2]
    
    @_(' ')
    def empty2(self, p):
        return p[-2] + 1
      
    @_('ID')
    def A(self, p):
        tabla[p.ID] = p[-2] + 1
    
if __name__ == '__main__':
    lexer = CalcLexer()
    parser = CalcParser()
    while True:
        try:
            text = input('data type list > ')
        except EOFError:
            break
        if text:
            parser.parse(lexer.tokenize(text))
        print(tabla)
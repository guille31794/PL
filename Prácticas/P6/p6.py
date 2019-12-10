from parser import *

if __name__ == "__main__":
    lex = CalcLexer()
    par = CalcParser()

    while True:
        try:
            text = input('calc > ')
            result = par.parse(lex.tokenize(text))
            print(Variables)
            print(Pointer)
        except EOFError:
            break

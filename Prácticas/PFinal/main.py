from parser import *

if __name__ == "__main__":
    lex = CalcLexer()
    par = CalcParser()

    # Restart file
    f = open("asembler.asm", "w")
    # Write prologue
    s = ".text\nglobl main\n.type main, @function\nmain:\n\n"
    s = s + "pushl %ebp\nmovl %esp, %ebp\n"
    f.write(s)
    f.close()

    while True:
        try:
            text = input('calc > ')
            result = par.parse(lex.tokenize(text))
            print(Variables)
            print(Pointer)
        except EOFError:
            break
        finally:
            # Write epilogue
            f = open("asembler.asm", "a")
            s = "\nmovl %ebp, %esp\npopl %ebp\nret"
            f.close()

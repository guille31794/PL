# ==============================================================================
# *** MY GRAMMAR ***
# ==============================================================================
# entry     -> linea ";" entry
#           -> ε
#
# linea     -> decl
#           -> asig
#           -> result
#
# ------------------------------------------------------------------------------
# Declaraciones de int, char, float, punteros y arrays
#
# decl      -> type_ (1)rest        {(1)rest.h = type_.s}
#
# type_     -> INTEGER              {type_.s = new TipoInteger()}
#           -> FLOAT                {type_.s = new TipoFloat()}
#           -> CHAR                 {type_.s = new TipoChar()}
#
# rest      -> (5)pointer (2)comma  {(5)pointer.h = rest.h}
#                                   {(2)comma.h   = rest.h}
#                                   {rest.s       = tabla[pointer.s]}
#           -> ID dim comma
#
# comma     -> "," (3)rest          {(3)rest.h = comma.h}
#           -> ε
#
# pointer   -> "*" (4)p_ ID         {pointer.s = new TipoPuntero(p_.s)}
#                                   {(4)p_.h   = pointer.h}
#                                   {print(ID.lexval+ "=>" +pointer.s.print_())}
#
# p_        -> "*" p_               {p_.s = new TipoPuntero(p_1.s)}
#           -> ε                    {p_.s = new TipoPuntero(p_1.h)}
#
# dim       -> "[" val "]" dim
#           -> ε
#
# val       -> NUM
#           -> pointer
#
# ------------------------------------------------------------------------------
# Asignaciones de ID y punteros, operaciones o asignación directamente
#
# asig      -> ID       "=" sum
#           -> pointer  "=" sum
#
# sum       -> fact "+" sum
#           -> fact
#
# fact      -> val "*" fact
#           -> val
#
# ------------------------------------------------------------------------------
# Ver valor de variables, punteros o arrays
#
# result    -> ID dim
#           -> pointer
#           -> "&" ID
#
# ==============================================================================

from sly import Lexer, Parser

pcont = 1
tabla = {}


class Tipo():
    def print_(self):
        pass


class TipoEntero(Tipo):
    def print_(self):
        return "Entero"


class TipoFloat(Tipo):
    def print_(self):
        return "Flotante"


class TipoCharacter(Tipo):
    def print_(self):
        return "Character"


class TipoPuntero(Tipo):
    def __init__(self, e):
        self.e = e

    def print_(self):
        if type(self.e) == str:
            return "Puntero a(" + self.e + ")"
        else:
            return "Puntero a(" + self.e.print_() + ")"


class Nodo():
    def tag_(self):
        pass


class MyLexer(Lexer):
    tokens = {ID, INTEGER, CHAR, FLOAT, NUM}
    ignore = r' \t'
    ignore_comments = r'\/\/.*'
    literals = {"*", ",", ";", "&", "+", "=", "[", "]"}

    # expresiones regulares para los tokens
    ID = r'[a-zA-Z_][a-zA-Z_0-9]*'
    ID['int'] = INTEGER
    ID['char'] = CHAR
    ID['float'] = FLOAT
    NUM = r'[0-9][0-9]*'


class MyParser(Parser):
    tokens = MyLexer.tokens

    def __init__(self):
        self.names = {}

    @_('linea ";" entry')
    def entry(self, p):
        pass

    @_('')
    def entry(self, p):
        pass

    @_('decl')
    def linea(self, p):
        print("Entra decl")
        pass

    @_('asig')
    def linea(self, p):
        pass

    @_('result')
    def linea(self, p):
        pass

    @_('type_ empty1 rest')
    def decl(self, p):
        pass

    @_('')
    def empty1(self, p):
        return p[-1]

    @_('INTEGER')
    def type_(self, p):
        print("Entra INTEGER")
        return TipoEntero()

    @_('FLOAT')
    def type_(self, p):
        return TipoFloat()

    @_('CHAR')
    def type_(self, p):
        return TipoCharacter()

    @_('empty5 pointer empty2 comma')
    def rest(self, p):
        print("Entra rest")
        return p[-2]

    @_('')
    def empty5(self, p):
        return p[-1]

    @_('')
    def empty2(self, p):
        return p[-3]

    @_('ID dim comma')
    def rest(self, p):
        pass

# comma     -> "," (3)rest          {(3)rest.h = comma.h}
    @_('"," empty3 rest')
    def comma(self, p):
        print(p[-2].print_())
        return p[-2]

    @_('')
    def empty3(self, p):
        return p[-2]

    @_('')
    def comma(self, p):
        pass

    @_('"*" empty4 p_ ID')
    def pointer(self, p):
        # puntero = TipoPuntero(p.p_)
        print(p.ID + " => " + p.p_.print_())
        return TipoPuntero(p.p_)

    @_('')
    def empty4(self, p):
        return p[-2]

    @_('"*" p_')
    def p_(self, p):
        return TipoPuntero(e=p.p_)

    @_('')
    def p_(self, p):
        return TipoPuntero(e=p[-2])

    @_('"[" val "]" dim')
    def dim(self, p):
        pass

    @_('')
    def dim(self, p):
        pass

    @_('NUM')
    def val(self, p):
        pass

    @_('pointer')
    def val(self, p):
        pass

    @_('ID "=" sum')
    def asig(self, p):
        pass

    @_('pointer "=" sum')
    def asig(self, p):
        pass

    @_('fact "+" sum')
    def sum(self, p):
        pass

    @_('fact')
    def sum(self, p):
        pass

    @_('val "*" fact')
    def fact(self, p):
        pass

    @_('val')
    def fact(self, p):
        pass

    @_('ID dim')
    def result(self, p):
        pass

    @_('pointer')
    def result(self, p):
        pass

    @_('"&" ID')
    def result(self, p):
        pass


if __name__ == "__main__":
    lexer = MyLexer()
    parser = MyParser()

    while True:
        try:
            data = input(" > ")
        except EOFError:
            break
        if data:
            parser.parse(lexer.tokenize(data))

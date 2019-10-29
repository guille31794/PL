# ==============================================================================
#  MY GRAMMAR FOR C DEFINITION WITH POINTERS
# (DOWN RECURSIVE IMPLEMENTATION USING SLY):
# ==============================================================================
# First and follow set calculation:
# - FIRST:
#       First(entry) = {INT, CHAR, FLOAT, ε}
#       First(defi)  = {INT, CHAR, FLOAT}
#       First(type_) = {INT, CHAR, FLOAT}
#       First(list_) = {'*', ID}
#       First(elemt) = {'*', ID}
#       First(rest)  = {',', ε}
#
# - FOLLOW:
#       Follow(entry)                                = {$}
#       Follow(defi)  = First(entry) U Follow(entry) = {INT, CHAR, FLOAT, $}
#       Follow(type_) = First(list_)                 = {'*', ID}
#       Follow(list_)                                = {';'}
#       Follow(rest)  = Follow(list_)                = {';'}
#       Follow(elemt) = First(rest) U Follow(list_)  = {',', ;}
# ==============================================================================
# entry -> defi entry
#       -> ε
#
# defi  -> type_ {list_.h = type.s} list_ ';'
#
# type_ -> INT              type_.s = NodoInt()
#       -> CHAR             type_.s = NodoChar()
#       -> FLOAT            type_.s = NodoFloat()
#
# list_ -> {elemt.h = list_.h} elemt {rest.h = list_.h} rest
#
# rest  -> ',' {elemt.h = rest.h} elemt {rest1.h = rest.h} rest1
#       -> ε
#
# elemt -> '*' {elemt1.h = NodePointer(elemt.h)} elemt1
#       -> ID  table[ID.lexval] = elemt.h
# ==============================================================================
from sly import Lexer
from Cdefinition import defLexer

# Globals variables
table = {}
ta = None
ind = 0
tokens = None
tokenlist = None


class Node:
    def print_():
        pass


class NodeInt(Node):
    def print_():
        return "int"


class NodeFloat(Node):
    def print_():
        return "float"


class NodeChar(Node):
    def print_():
        return "char"


class NodePointer(Node):
    def __init__(self, n):
        self.n = n

    def print_(self):
        return "pointer to " + self.n.print_()


def defi():
    global ta, tokens
    if ta.type == tokens[0] or ta.type == tokens[1] or ta.type == tokens[3]:
        type_s = type_()
        list_h = type_s
        list_(list_h)  # ???
        block(";")
    else:
        yyerror("in definition")


# end of defi rule


def entry():
    global ta, ind, tokens
    if ta.type == tokens[0] or ta.type == tokens[1] or ta.type == tokens[3]:
        defi()
        entry()
    else:
        if ind < len(tokenlist):  # end of the entry
            yyerror("in entry")


# end of entry rule


def type_():
    global ta, tokens
    if ta.type == tokens[3]:
        block("INT")
        return NodeInt
    else:
        if ta.type == tokens[1]:
            block("FLOAT")
            return NodeFloat
        else:
            if ta.type == tokens[0]:
                block("CHAR")
                return NodeChar
            else:
                yyerror("in type")


# end of type_ rule


def list_(list_h):
    global ta, tokens
    if ta.type == tokens[2] or ta.value == "*":  # look at 1st sets 4 conds?
        elemt(list_h)  # ???
        rest(list_h)
    else:
        yyerror("in list")


# end of list_ rule


def elemt(elemt_h):
    global ta, tokens
    if ta.value == "*":
        block("*")
        elemt1_h = NodePointer(elemt_h)
        elemt(elemt1_h)
    else:
        if ta.type == tokens[2]:
            IDlexval = ta.value
            block("ID")
            table[IDlexval] = elemt_h.print_()
        else:
            yyerror("in element")


# end of elemt rule


def rest(rest_h):
    global ta
    if ta.value == ",":
        block(",")
        elemt(rest_h)
        rest(rest_h)
    else:
        if ta.value != ";":
            yyerror("in rest")


# end of rest rule


def yyerror(msj):
    print("syntax error " + msj)


# end of yyerror function


def block(obj):
    global ta, ind, tokenlist
    if ta.type == obj:
        ind += 1
        if ind < len(tokenlist):
            ta = tokenlist[ind]
    else:
        yyerror("in block")


# end of block function

# ==============================================================================
# Main
# ==============================================================================
if __name__ == "__main__":

    lexer = defLexer()
    tokens = sorted(defLexer.tokens)  # alphabethical order

    while True:
        try:
            data = input("\n --> ")
        except EOFError:
            break
        if data:
            tokenlist = list(lexer.tokenize(data))
            ta = tokenlist[ind]
            entry()
        ind = 0
        print("\nList of variables:")
        print("=======================================\n")
        print(table)

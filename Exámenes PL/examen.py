from sly import Lexer
from nodo import *

ta = None
ind = 0
tokens = None
tokenlist = None

class CalcLexer(Lexer):
    tokens = {ID, NUMBER, ASSIGN, EQ, PRINT, AND, OR, NOT }
    ignore = ' \t'
    literals = { ';', '<', '>', '(', ')'}

    # Regular expression rules for tokens
    ID            = r'[a-zA-Z_][a-zA-Z0-9_]*'
    NUMBER		  = r'\d+'
    ASSIGN		  = r':='
    EQ			  = r'=='
    ID['print']   = PRINT
    ID['and']     = AND
    ID['or']      = OR
    ID['not']     = NOT

    # Convierte los string numéricos a int
    @_(r'\d+')
    def NUMBER(self, t):
        t.value = int(t.value)
        return t
    
    @_(r'\n+')
    def newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print("Caracter ilegal '%s'" % t.value[0])
        self.index += 1

# Función de entrada
def entrada():
    global ta, ind, tokens, tokenlist
    if ta.type == tokens[3] || ta.type == tokens[7]
    	expr_s = expr()
    	expr_s.evalua()
        entrada()
    else:
        if ind < len(tokenlist):
            print("error en entrada")
# Fin de entrada()

# Función expr
def expr():
	global ta, tokens
	if ta.type == tokens[3]:
		IDlexval = ta.value
		cuadra('ID')
		linea_s = nodoAsig(IDlexval, linea())
		cuadra(';')
		return linea_s
	else
		if ta.type == tokens[7]:
			cuadra('PRINT')
			linea_s = nodoPrint(linea())
			cuadra(';')
			return linea_s
		else:
			print("error en expr")
# Fin de expr()

# Función linea
def linea():
	global ta, tokens
	if ta.type == tokens[4]:
		cuadra('NOT')
		linea_s = operOR()
		return linea_s
	else:
		if ta.type == tokens[3]:
			IDlexval = ta.value
			cuadra('ID')
			linea2_h = NodoId(IDlexval)
			linea2_s = linea2(linea2_h)
			return linea2_s
		else:
			if ta.type == tokens[5]:
				NUMlexval = ta.value
				cuadra('NUMBER')
				linea2_h = NodoNum(NUMlexval)
				linea2_s = linea2(linea2_h)
				return linea2_s
			else:
				if ta.type == '(':
					cuadra('(')
					linea2_h = linea()
					linea2_s = linea2(linea2_h)
					return linea2_s
				else:
					print("error en linea.")

def operOR():
	global ta, tokens
	if ta.type == tokens[4]:
		cuadra('NOT')
		linea2_s = operAND()
		return linea2_s
	else:
		if ta.type == tokens[3]:
			IDlexval = ta.value
			cuadra('ID')
			linea2_h = NodoId(IDlexval)
			linea2_s = linea2(linea2_h)
			return linea2_s
		else:
			if ta.type == tokens[5]:
				NUMlexval = ta.value
				cuadra('NUMBER')
				linea2_h = NodoNum(NUMlexval)
				linea2_s = linea2(linea2_h)
				return linea2_s
			else:
				if ta.type == '(':
					cuadra('(')
					linea2_h = linea()
					linea2_s = linea2(linea2_h)
					return linea2_s
				else:
					print("error en operOR.")

def operAND():
	global ta, tokens
	if ta.type == tokens[4]:
		cuadra('NOT')
		linea2_s = operNOT()
		return linea2_s
	else:
		if ta.type == tokens[3]:
			IDlexval = ta.value
			cuadra('ID')
			linea2_h = NodoId(IDlexval)
			linea2_s = linea2(linea2_h)
			return linea2_s
		else:
			if ta.type == tokens[5]:
				NUMlexval = ta.value
				cuadra('NUMBER')
				linea2_h = NodoNum(NUMlexval)
				linea2_s = linea2(linea2_h)
				return linea2_s
			else:
				if ta.type == '(':
					cuadra('(')
					linea2_h = linea()
					linea2_s = linea2(linea2_h)
					return linea2_s
				else:
					print("error en operAND.")

def operNOT():
	global ta, tokens
	if ta.type == tokens[4]:
		cuadra('NOT')
		linea2_s = hoja()
		return linea2_s
	else:
		if ta.type == tokens[3]:
			IDlexval = ta.value
			cuadra('ID')
			linea2_h = NodoId(IDlexval)
			linea2_s = linea2(linea2_h)
			return linea2_s
		else:
			if ta.type == tokens[5]:
				NUMlexval = ta.value
				cuadra('NUMBER')
				linea2_h = NodoNum(NUMlexval)
				linea2_s = linea2(linea2_h)
				return linea2_s
			else:
				if ta.type == '(':
					cuadra('(')
					linea2_h = linea()
					linea2_s = linea2(linea2_h)
					return linea2_s
				else:
					print("error en operNOT.")

def linea2():

def hoja():

def R():

def T():

# Función para verificar el token actual
def cuadra(obj):
    global ta, ind, tokenlist
    if ta.type == obj:
        ind += 1
        if ind < len(tokenlist): # Guarda en ta el nuevo token si aún quedan
            ta = tokenlist[ind]
    else:
        print("Error en cuadra.")
# Fin de cuadra()

if __name__ == '__main__':
    lexer = CalcLexer()
    tokens = CalcLexer.tokens
    tokens = sorted(tokens) # orden: and, assign, eq, id, not, number, or, print

    while True:
        try:
            datos = input('Entrada > ')
        except EOFError:
            break

        if datos:
            # print(tokens) # Muestra la lista de tokens
            tokenlist = list(lexer.tokenize(datos))
            ta = tokenlist[ind]
            entrada()

        ind = 0
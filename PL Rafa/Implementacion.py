# ==============================================================================
# MyGrammar
# ==============================================================================
# entrada -> linea ";" entrada
#		  -> ε
#
# linea   -> decl 
#		  -> instruc
#
# decl 	  -> tipo resto
#
# tipo 	  -> INTEGER
#		  -> CHAR
#		  -> FLOAT
# 
# resto   -> resto "," dec
#		  -> dec
#
# dec 	  -> ID
#  		  -> puntero ID
#		  -> ID dim
#
# puntero -> "*" puntero
#		  -> "*"
#
# dim	  -> "[" NUMI "]" dim
#  		  -> "[" NUMI "]"
#
# instruc -> asig
#		  -> var
#		  -> "&" ID
#
# vect 	  -> "[" valor "]" vect
#  		  -> "[" valor "]"
# 
# valor   -> ID
#   	  -> puntero ID
#  		  -> num
#
# num 	  -> NUMI
#		  -> NUMF
#
# asig 	  -> var "=" expr
#
# var 	  -> ID
#		  -> puntero ID
#  		  -> ID vect
#
# expr 	  -> sum "+" expr
#		  -> sum
#
# sum     -> fact "*" sum
#		  -> fact
#
# fact 	  -> var
#		  -> num
#		  -> "(" expr ")"
#
# ==============================================================================

from sly import Lexer, Parser
#------VARIABLES GLOBALES-------------------------------------------------------

tablatipo = {}
VarAux = None

#-----LEXER---------------------------------------------------------------------

class ExamLexer(Lexer):
    	
	tokens = {INT, CHAR, FLOAT, ID, NUMI, NUMF}
	literals = {'*', ',', ';', '[', ']', '&', '=', '+'}
	ignore = ' \t'
	ignore_comm = r'\/\/.*'

	ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
	ID['int'] = INT
	ID['char'] = CHAR
	ID['float'] = FLOAT

	@_(r'\d+')
	def NUMI(self, t):
		t.value = int(t.value)
		return t

	@_(r'\d+.\d+')
	def NUMF(self, t):
		t.value = float(t.value)
		return t

	@_('\n+')
	def newline(self, t):
		self.lineno += t.value.count('\n')


#----CLASES TIPO----------------------------------------

class Tipo():
	def escribe(self):
		pass

class TInt(Tipo):
	def escribe(self):
		tipo = "Entero"
		return tipo

class TChar(Tipo):
	def escribe(self):
		tipo = "Caracter"
		return tipo

class TFloat(Tipo):
	def escribe(self):
		tipo = "Flotante"
		return tipo

class Tpuntero(Tipo):
	def __init__(self, elm):
		self.elm = elm

	def escribe(self):
		tipo = "Puntero_a("+self.elm.escribe()+")"
		return tipo

class Tarray(Tipo):
	def __init__(self, dim, elm):
		self.dim = dim
		self.elm = elm
	def escribe(self):
		tipo = "array("+str(self.dim)+","+self.elm.escribe()+")"	
		return tipo

#-----CLASES NODO-----------------------------------

class Nodo():
	def etiqueta(self):
		pass

class NodoID(Nodo):
	def __init__(self, nom):
		self.nom = nom
	def etiqueta(self):
		tipo = "ID("+self.nom+")"
		return tipo

class NodoPuntero(Nodo):
	def __init__(self, ref):
		self.ref = ref
	def etiqueta(self):
		tipo = "puntero a "+self.ref.etiqueta()
		return tipo

class NodoAmp(Nodo):
	def __init__(self, ref):
		self.ref = ref
	def etiqueta(self):
		tipo = "ampersand a "+self.ref.etiqueta()
		return tipo

class NodoAsig(Nodo):
	def __init__(self, x, y):
		self.x = x
		self.y = y
	def etiqueta(self):
		tipo = "asignacion("+self.x.etiqueta()+" = "+self.y.etiqueta()+")"
		return tipo

class NodoSuma(Nodo):
	def __init__(self, sum1, sum2):
		self.sum1 = sum1
		self.sum2 = sum2
	def etiqueta(self):
		tipo = "suma("+self.sum1.etiqueta()+" + "+self.sum2.etiqueta()+")"
		return tipo

class NodoProd(Nodo):
	def __init__(self, prod1, prod2):
		self.prod1 = prod1
		self.prod2 = prod2
	def etiqueta(self):
		tipo = "producto("+self.prod1.etiqueta()+" * "+self.prod2.etiqueta()+")"
		return tipo

class NodoCteI(Nodo):
	def __init__(self, val):
		self.val = val
	def etiqueta(self):
		tipo = "CteEnt("+str(self.val)+")"
		return tipo

class NodoCteF(Nodo):
	def __init__(self, val):
		self.val = val
	def etiqueta(self):
		tipo = "CteFl("+str(self.val)+")"
		return tipo

class NodoArray(Nodo):
	def __init__(self, base, dim, ind):
		self.base = base
		self.dim = dim
		self.ind = ind
	def etiqueta(self):
		cont = ""
		nodo = self.base
		self.ind.reverse()
		for i in range(self.dim):
			nodo = NodoArrayAux(nodo)
			cont += " e indice("+self.ind[i].etiqueta()+")"
		tipo = nodo.etiqueta()+cont
		return tipo			

class NodoArrayAux(Nodo):
	def __init__(self, base):
		self.base = base
	def etiqueta(self):
		tipo = "array base("+self.base.etiqueta()+")"
		return tipo

class NodoIndice(Nodo):
	def __init__(self, ind):
		self.ind = ind
	def etiqueta(self):
		tipo = "e indice("+self.ind.etiqueta()+")"
		return tipo

class Nodoftoi(Nodo):
	def __init__(self, var):
		self.var = var
	def etiqueta(self):
		tipo = "funcion : ftoi("+self.var.etiqueta()+")"
		return tipo

class Nodoitof(Nodo):
	def __init__(self, var):
		self.var = var
	def etiqueta(self):
		tipo = "funcion : itof("+self.var.etiqueta()+")"
		return tipo

class Nodoctoi(Nodo):
	def __init__(self, var):
		self.var = var
	def etiqueta(self):
		tipo = "funcion : ctoi("+self.var.etiqueta()+")"
		return tipo

class Nodoitoc(Nodo):
	def __init__(self, var):
		self.var = var
	def etiqueta(self):
		tipo = "funcion : itoc("+self.var.etiqueta()+")"
		return tipo

#------FUNCIONES AUXILIARES--------------------------

def unifica(t1, t2):
	return t1.escribe() == t2.escribe()	

def escribir(t,n):
	print("El Tipo resultante de la expresión es: ",t.escribe())
	print("Y el árbol de nodos para la expresión es: ",n.etiqueta())

#------PARSER------------------------------------------

class ExamParser(Parser):
	tokens = ExamLexer.tokens

	@_('linea ";" entrada')
	def entrada(self, p):
		pass

	@_(' ')
	def entrada(self, p):
		pass

	@_('declaracion')
	def linea(self, p):
		pass

	@_('instruccion')
	def linea(self, p):
		pass

	@_('tipo empty0 resto')
	def declaracion(self, p):
		pass

	@_('resto "," dec')
	def resto(self, p):
		pass

	@_('dec')
	def resto(self, p):
		pass

	@_('ID')
	def dec(self, p):
		print(p.ID,"=>",VarAux.escribe())
		tablatipo[p.ID] = VarAux

	@_('puntero ID')
	def dec(self, p):
		nodo = VarAux
		for i in range(p.puntero):
			nodo = Tpuntero(nodo)
		print(p.ID,"=>",nodo.escribe())
		tablatipo[p.ID] = nodo

	@_('ID dim')
	def dec(self, p):
		nodo = VarAux
		(vec, Dcont) = p.dim
		for i in range(Dcont):
			nodo = Tarray(vec[i], nodo)
		print(p.ID, "=>", nodo.escribe())
		tablatipo[p.ID] = nodo

	@_(' ')
	def empty0(self, p):
		global VarAux
		VarAux = p[-1]

	@_('INT')
	def tipo(self, p):
		nodo = TInt()
		return nodo

	@_('CHAR')
	def tipo(self, p):
		nodo = TChar()
		return nodo

	@_('FLOAT')
	def tipo(self, p):
		nodo = TFloat()
		return nodo

	@_('"*" puntero')
	def puntero(self, p):
		return p.puntero+1

	@_('"*"')
	def puntero(self, p):
		Pcont = 1
		return Pcont

	@_('"[" NUMI "]" dim')
	def dim(self, p):
		vec, Dcont = p.dim
		vec.append(p.NUMI)
		Dcont += 1
		return (vec, Dcont)

	@_('"[" NUMI "]"')
	def dim(self, p):
		vec = [p.NUMI]
		Dcont = 1
		return (vec, Dcont)

	@_('asignacion')
	def instruccion(self, p):
		tipo, nodo = p.asignacion
		escribir(tipo, nodo)	

	@_('var')
	def instruccion(self, p):
		tipo, nodo = p.var
		escribir(tipo, nodo)

	@_('"&" ID')
	def instruccion(self, p):
		tipo = tablatipo[p.ID]
		tipo = Tpuntero(tipo)
		nodo = NodoID(p.ID)
		nodo = NodoAmp(nodo)
		escribir(tipo, nodo)	

	@_('"[" valor "]" vect')
	def vect(self, p):
		vec, Vcont = p.vect
		tipo, nodo = p.valor
		vec.append(nodo)
		Vcont +=1
		return (vec, Vcont)

	@_('"[" valor "]"')
	def vect(self, p):
		tipo, nodo = p.valor
		vec = [nodo]
		Vcont = 1
		return (vec, Vcont)

	@_('ID')
	def valor(self, p):
		tipo = tablatipo[p.ID]
		nodo = NodoID(p.ID)
		return (tipo, nodo)
	
	@_('puntero ID')
	def valor(self, p):
		tipo = tablatipo[p.ID]
		for i in range(p.puntero):
			tipo = tipo.elm
		nodo = NodoID(p.ID)
		for i in range(p.puntero):
			nodo = NodoPuntero(nodo)
		return (tipo, nodo)

	@_('num')
	def valor(self, p):
		return p.num	

	@_('NUMI')
	def num(self, p):
		tipo = TInt()
		nodo = NodoCteI(p.NUMI)
		return (tipo, nodo)	

	@_('NUMF')
	def num(self, p):
		tipo = TFloat()
		nodo = NodoCteF(p.NUMF)
		return (tipo, nodo)

	@_('var "=" expr')
	def asignacion(self, p):
		tv, nv = p.var
		te, ne = p.expr
		if(not unifica(tv, te)):
			if(tv.escribe() == "Entero" and te.escribe() == "Flotante"):
				tipo = TInt()
				ne = Nodoftoi(ne)
			else:
				if(tv.escribe() == "Flotante" and te.escribe() == "Entero"):
					tipo = TFloat()
					ne = Nodoitof(ne)
				else:
					if(tv.escribe() == "Entero" and te.escribe() == "Caracter"):
						tipo = TInt()
						ne = Nodoctoi(ne)
					else:
						if(tv.escribe() == "Caracter" and te.escribe() == "Entero"):
							tipo = TChar()
							ne = Nodoitoc(ne)
						else:
							print("Error al unificar")
		else:
			tipo = tv
		nodo = NodoAsig(nv, ne)
		return (tipo, nodo)

	@_('ID')
	def var(self, p):
		tipo = tablatipo[p.ID]
		nodo = NodoID(p.ID)
		return (tipo, nodo)

	@_('puntero ID')
	def var(self, p):
		tipo = tablatipo[p.ID]
		for i in range(p.puntero):
			tipo = tipo.elm
		nodo = NodoID(p.ID)
		for i in range(p.puntero):
			nodo = NodoPuntero(nodo)
		return (tipo, nodo)

	@_('ID vect')
	def var(self, p):
		vec, Vcont = p.vect
		tipo = tablatipo[p.ID]
		for i in range(Vcont):
			tipo = tipo.elm
		nodo = NodoID(p.ID)
		nodo = NodoArray(nodo, Vcont, vec)
		return (tipo, nodo)

	@_('sum "+" expr')
	def expr(self, p):
		ts, ns = p.sum
		te, ne = p.expr
		if(not unifica(ts, te)):
			if(ts.escribe() == "Entero" and te.escribe() == "Flotante"):
				tipo = TFloat()
				ns = Nodoitof(ns)
			else:
				if(ts.escribe() == "Flotante" and te.escribe() == "Entero"):
					tipo = TFloat()
					ne = Nodoitof(ne)
				else:
					if(ts.escribe() == "Entero" and te.escribe() == "Caracter"):
						tipo = TInt()
						ne = Nodoctoi(ne)
					else:
						if(ts.escribe() == "Caracter" and te.escribe() == "Entero"):
							tipo = TInt()
							ns = Nodoctoi(ns)
						else:
							print("Error al unificar")
		else:
			tipo = ts
		nodo = NodoSuma(ns, ne)
		return (tipo, nodo)

	@_('sum')
	def expr(self, p):
		return p.sum

	@_('factor "*" sum')
	def sum(self, p):
		tf, nf = p.factor
		ts, ns = p.sum
		if(not unifica(tf, ts)):
			if(tf.escribe() == "Entero" and ts.escribe() == "Flotante"):
				tipo = TFloat()
				nf = Nodoitof(nf)
			else:
				if(tf.escribe() == "Flotante" and ts.escribe() == "Entero"):
					tipo = TFloat()
					ns = Nodoitof(ns)
				else:
					if(tf.escribe() == "Entero" and ts.escribe() == "Caracter"):
						tipo = TInt()
						ns = Nodoctoi(ns)
					else:
						if(tf.escribe() == "Caracter" and ts.escribe() == "Entero"):
							tipo = TInt()
							nf = Nodoctoi(nf)
						else:
							print("Error al unificar")
		else:
			tipo = tf
		nodo = NodoProd(nf, ns)
		return (tipo,nodo)

	@_('factor')
	def sum(self, p):
		return p.factor

	@_('var')
	def factor(self, p):
		return p.var

	@_('num')
	def factor(self, p):
		return p.num

	@_('"(" expr ")"')
	def factor(self, p):
		return p.expr


if __name__ == "__main__":
    flex = ExamLexer()
    bison = ExamParser()
	
    while True:
        entrada = input(' > ')
        if entrada:
	        bison.parse(flex.tokenize(entrada))
    
# RAFAEL ROMÁN AGUILAR

##############################################
##                 GRAMATICA                ##
##############################################


#  entry -> line ";" entry          
#        -> Epsilon

# line   -> definition
#        -> instruction

# definition -> type {axu.h = type.s} aux

# instruction -> assign
#             -> var
#             -> "&" ID

# aux  -> aux "," {name.h = aux.h} name
#      -> name

# name -> ID {types[ID.lexval] = name.h}
#      -> pointer ID {name.s = new TipoPointer(name.h);
#                    types[ID.lexval] = name.h}
#      -> ID dim {types[ID.lexval] = name.h;
#                 name.s = new TipoArray(dim.s1,name.h)}

# dim     -> "[" NINT "]" dim {DIMC += 1;
#                             vec[DIMC] = NINT}
#         -> "[" NINT "]" {DIMC = 1;
#                         vec[Dcont] = NINT}

# pointer -> "*" pointer {POINTC += 1}
#         -> "*" {POINTC += 1}

# vector -> "[" value "]" vector {DIMC += 1;
#                                vec[DIMC] = value.s}
#        -> "[" value "]" {DIMC = 1;
#                          vec[DIMC] = value.s}
 
# value -> ID {TP = types[ID.lexval];
#              node = new NodoID(ID.lexval);
#              value.s =(TP, node)}
#       -> pointer ID {TP = types[ID.lexval];
#                      node = new NodoPointer(TP);
#                      value.s =(TP, node)}
#       -> num {value.s = num.s}

# num -> NINT {TP = new TipoInt();
#              node = new NodoCteI(NINT), num.s =(TP, node)}
#     -> NFLOAT  {TP = new TipoFloat();
#                node = new NodoCteF(NUMF);
#                num.s =(TP, node)}

# assign -> var "=" expr {TP = new Tipo(INT,CHAR,FLOAT);
#                        node = new NodoAsig(new Nodoftoi/Nodoitof/Nodoctoi/Nodoitoc);
#                        assign.s =(TP, node)}

# var -> ID {TP = types[ID.lexval];
#            node = new NodoID(ID.lexval);
#            var.s =(TP, node)}
#     -> pointer ID {TP = types[ID.lexval];
#                   node = new NodoPointer(TP);
#                   var.s =(TP, node)}
#     -> ID vector {TP = types[ID.lexval];
#                   node = new NodoArray(vector1.s,name.h);
#                   var.s =(TP, node)}

# expr -> sum "+" expr {TP = new Tipo(INT/CHAR/FLOAT);
#                       node = new NodoSuma(new Nodoftoi/Nodoitof/Nodoctoi/Nodoitoc);
#                       expr.s =(TP, node)}
#      -> sum {expr.s = sum.s}

# sum -> fact "*" sum {TP = new Tipo(INT,CHAR,FLOAT);
#        node = new NodoProd(new Nodoftoi/Nodoitof/Nodoctoi/Nodoitoc);
#        sum.s =(TP, node)}
#     -> fact {sum.s = fact.s}

# fact -> var {factor.s = sum.s}
#      -> num {factor.s = sum.s}
#      -> "(" expr ")" {factor.s = expr.s}

# type -> INT {type.s = new TipoINT();}
#      -> CHAR {type.s = new TipoCHAR();}
#      -> FLOAT {type.s = new TipoFLOAT();}


##############################################
##      GRAMATICA ADAPTADA DESCENDENTE      ##
##############################################

# entry -> line ';' entry 
#       -> Epsilon

# line -> definition 
#      -> instruction 

# defnition -> type aux

# aux  -> name aux_ 
# aux_ -> ',' name aux_
#      -> Epsilon

# name -> ID 
#      -> pointer ID 
#      -> ID dim

# type -> INT 
#      -> CHAR 
#      -> FLOAT  

# pointer -> '*' pointer 
#         -> '*'

# dim -> '[' NINT ']' dim 
#     -> '[' NINT ']'

# instruction -> assign 
#             -> var 
#             -> '&' ID

# assign -> var '=' expr

# var -> ID 
#     -> pointer ID 
#     -> ID vector

# vector -> '[' value ']' vector 
#        -> '[' value ']'

# value -> ID 
#        -> pointer ID 
#        -> num 
    
# num -> NINT 
#     -> NFLOAT
    
# expr -> sum '+' expr 
#      -> sum

# sum -> factor '*' sum 
#     -> factor 

# factor -> var 
#        -> num 
#        -> '(' expr ')'


##############################################
##                 LEXICO                   ##
##############################################

from sly import Lexer, Parser

types = {}
globalAUX = None

class LEX(Lexer):
    	
	tokens = {INT, CHAR, FLOAT, ID, NINT, NFLOAT}
	literals = { '=', '+', '[', ']', '&', '*', ',', ';',}
	
    ignore = ' \t'

	ID = r'[a-zA-Z][a-zA-Z0-9]*'
	ID['int'] = INT

	ID['char'] = CHAR

	ID['float'] = FLOAT

	@_(r'\d+')
	def NINT(self, t):
		t.value = int(t.value)
		return t

	@_(r'\d+.\d+')
	def NFLOAT(self, t):
		t.value = float(t.value)
		return t

	@_('\n+')
	def newline(self, t):
		self.lineno += t.value.count('\n')



##############################################
##                 CLASE TIPO               ##
##############################################

class Tipo():
	def escribe(self):
		pass

class TipoINT(Tipo):
	def escribe(self):
		tipo = "Entero"
		return tipo

class TipoCHAR(Tipo):
	def escribe(self):
		tipo = "Caracter"
		return tipo

class TipoFLOAT(Tipo):
	def escribe(self):
		tipo = "Flotante"
		return tipo

class TipoPointer(Tipo):
	def __init__(self, elm):
		self.elm = elm

	def escribe(self):
		tipo = "Puntero_a("+self.elm.escribe()+")"
		return tipo

class TipoArray(Tipo):
	def __init__(self, dim, elm):
		self.dim = dim
		self.elm = elm
	def escribe(self):
		tipo = "array("+str(self.dim)+","+self.elm.escribe()+")"	
		return tipo



##############################################
##               CLASE NODO                 ##
##############################################

class Nodo():
	def etiqueta(self):
		pass

class NodoID(Nodo):
	def __init__(self, nom):
		self.nom = nom
	def etiqueta(self):
		tipo = "ID("+self.nom+")"
		return tipo

class NodoPointer(Nodo):
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

def unifica(t1, t2):
	return t1.escribe() == t2.escribe()	

def escribir(t,n):
	print("El Tipo resultante de la expresión es: ",t.escribe())
	print("Y el árbol de nodos para la expresión es: ",n.etiqueta())



##############################################
##                 PARSER                   ##
##############################################

# tokens ordenados = {CHAR,FLOAT,ID,INT,NFLOAT,NINT}

class PAR(Parser):


    global tokens = None
    global tokenlist = None
    global ta = None
    global ind = 0

   def yyerror(msj):
       print("Error Sintactico",msj)

    def cuadra(obj)
        if ta.type == obj:
            ind +=1
            if ind < len(tokenlist):
                ta = tokenlist[ind]
        else:
            yyerror("en cuadra")
    # Fin de cuadra


    def factor():
        if ta.value == '*' or ta.type == tokens[2]:
            AUX = var()
            return AUX
        else:
            if ta.type == tokens[4] or ta.type == tokens[5]:
                AUX = num()
                return AUX
            else:
                if ta.value == '('
                    cuadra("(")
                    EXPR = expr()
                    cuadra(")")
                    return EXPR
                else:
                    yyerror("en factor")
        # Fin de Factor

    def type():
        if ta.type == tokens[3]: #INT
            cuadra("INT")
            TINT = TipoINT()
            return TINT
        else:
                if ta.type == tokens[0]: #CHAR
                    cuadra("CHAR")
                    TCHAR = TipoCHAR()
                    return TCHAR  
                else:
                    if ta.type == tokens[1]: #FLOAT
                        cuadra("FLOAT")
                        TFLOAT = TipoFLOAT()
                        return TFLOAT
                    else:
                        yyerror("en type")

    def sum():
        if ta.value == '*' or ta.type == tokens[2] or ta.type == tokens[4] or ta.type == tokens[5] or ta.value == '(':
            TFACTOR,NFACTOR = ta.value
            factor()
            if ind < len(tokenlist):
                cuadra("*")
                TSUM,NSUM = sum()
                if(not unifica(TFACTOR, TSUM)):
			        if(TFACTOR.escribe() == "Entero" and TSUM.escribe() == "Flotante"):
				        TP = TFloat()
				        node = Nodoitof(NFLOAT)
			        else:
				        if(TFLOAT.escribe() == "Flotante" and TSUM.escribe() == "Entero"):
					        TP = TipoFLOAT()
					        node = Nodoitof(NSUM)
				        else:
					        if(TFLOAT.escribe() == "Entero" and TSUM.escribe() == "Caracter"):
						        TP = TipoINT()
						        node = Nodoctoi(NSUM)
					        else:
						        if(tf.escribe() == "Caracter" and ts.escribe() == "Entero"):
							        tipo = TInt()
							        nf = Nodoctoi(nf)
						    
		    else:
			    TP = TFLOAT
		        node = NodoProd(NFLOAT, NSUM)
		    return (TP,node)
        else:
            yyerror("en sum")
            

    def expr():

        # NO ME HA DADO TIEMPO A TERMINAR EL RESTO DEL TRADUCTOR DESCENDENTE



if __name__ == '__main__':
    
    lexer = LEX()
    
    toks = LEX.tokens
    toks = sorted(toks)
    while True:

        data = input('Introduzca el input')
        if data:
            tokenlist = list(LEX.tokenize(data))
            ta = tokenlist[ind]
            entry()
        ind = 0

        



    
 
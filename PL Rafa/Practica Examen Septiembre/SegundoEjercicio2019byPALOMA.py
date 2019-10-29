from sly import Lexer, Parser

tabla  = {}

class Nodo():
    def escribir():
        pass
    def etiqueta():
        pass

class NodoId(Nodo):
    def __init__(self, id):
        self.id = id
    def escribir(self):
        print(self.etiqueta())
    def etiqueta(self):
        cad = "ID("+self.id+")"
        return cad
    
class NodoCteEnt(Nodo):
    def __init__(self, val):
        self.val = val
    def escribir(self):
        print(self.etiqueta())
    def etiqueta(self):
        cad = "CteEnt("+str(self.val)+")"
        return cad

class NodoCteFloat(Nodo):
    def __init__(self, val):
        self.val = val
    def escribir(self):
        print(self.etiqueta())
    def etiqueta(self):
        cad = "CteFloat("+str(self.val)+")"
        return cad

class NodoPuntero(Nodo):
    def __init__(self, n):
        self.n = n
    def escribir(self):
        print(self.etiqueta())
    def etiqueta(self):
        cad = "puntero a "+self.n.etiqueta()
        return cad

class NodoAmp(Nodo):
    def __init__(self, n):
        self.n = n
    def escribir(self):
        print(self.etiqueta())
    def etiqueta(self):
        cad = "ampersand a "+self.n.etiqueta()
        return cad

class NodoArray(Nodo):
    def __init__(self, base, ind):
        self.base = base
        self.ind = ind
    def escribir(self):
        print(self.etiqueta())
    def etiqueta(self):
        cad = "array base("+self.base.etiqueta()+") e indice ("+self.ind.etiqueta()+")"
        return cad

class NodoAsig(Nodo):
    def __init__(self, lval, rval):
        self.lval = lval
        self.rval = rval
    def escribir(self):
        print(self.etiqueta())
    def etiqueta(self):
        cad = "asignacion("+self.lval.etiqueta()+" = "+self.rval.etiqueta()+")"
        return cad

class NodoSuma(Nodo):
    def __init__(self, sum1, sum2):
        self.sum1 = sum1
        self.sum2 = sum2
    def escribir(self):
        print(self.etiqueta())
    def etiqueta(self):
        cad = "suma("+self.sum1.etiqueta()+" + "+self.sum2.etiqueta()+")"
        return cad

class NodoProd(Nodo):
    def __init__(self, fac1, fac2):
        self.fac1 = fac1
        self.fac2 = fac2
    def escribir(self):
        print(self.etiqueta())
    def etiqueta(self):
        cad = "producto("+self.fac1.etiqueta()+" * "+self.fac2.etiqueta()+")"
        return cad

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


class Tipo():
    def escribir():
        pass
    def tipo():
        pass

class TipoInt(Tipo):
    def escribir(self):
        print(self.tipo())

    def tipo(self):
        return "Entero"
    
class TipoFloat(Tipo):
    def escribir(self):
        print(self.tipo())
        
    def tipo(self):
        return "Flotante"

class TipoChar(Tipo):
    def escribir(self):
        print(self.tipo())
        
    def tipo(self):
        return "Caracter"
    
class TipoPuntero(Tipo):
    def __init__(self, elto):
        self.elto = elto

    def escribir(self):
        print(self.tipo())

    def tipo(self):
        cad = "Puntero_a("+self.elto.tipo()+")"
        return cad

class TipoArray(Tipo):
    def __init__(self, dim, elto):
        self.dim = dim
        self.elto = elto

    def escribir(self):
        print(self.tipo())

    def tipo(self):
        cad = "array("+str(self.dim)+","+self.elto.tipo()+")"
        return cad

def unifica(t1, t2):
    return t1.tipo() == t2.tipo()

def escribir(nodo, tipo):
    print("El Tipo resultante de la expresion es:", end = " ")
    tipo.escribir()
    print("Y el arbol de nodos para la expresion es:", end = " ")
    nodo.escribir()

class CalcLexer(Lexer):
    tokens = {ID, FLECHA, CTEENT, CTEFLOAT, CARACTER, ENTERO, FLOTANTE}
    ignore = ' \t'
    literals = {';', ',', '+', '&', '*', '=', '[', ']', '(', ')'}
    
    # Regular expression rules for tokens
    ID   = r'[a-zA-Z_][a-zA-Z0-9_]*'
    ID['char']  = CARACTER
    ID['int']   = ENTERO
    ID['float'] = FLOTANTE
    
    FLECHA = r'->'
    
    @_(r'\d+\.\d*')
    def CTEFOLAT(self, t):
        t.value = float(t.value)
        return t
    
    @_(r'\d+')
    def CTEENT(self, t):
        t.value = int(t.value)
        return t
    
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

    @_('defs exps')
    def entrada(self, p):
        pass
        
    @_('defi ";" defs')
    def defs(self, p):
        pass
    
    @_(' ')
    def defs(self, p):
        pass
    
    @_('tipo lista')
    def defi(self, p):
        vars = p.lista
        vars.reverse()
        for i in range(len(vars)):
            (id, elto) = vars[i]
            print(id,"=>", end = " ")
            elto.escribir()
            tabla[id] = elto
    
    @_('ENTERO')
    def tipo(self, p):
        return TipoInt()
    
    @_('FLOTANTE')
    def tipo(self, p):
        return TipoFloat()
    
    @_('CARACTER')
    def tipo(self, p):
        return TipoChar()
    
    @_('elm "," empty4 lista')
    def lista(self, p):
        vars = p.lista
        vars.append(p.elm)
        return vars
    
    @_('elm')
    def lista(self, p):
        vars = []
        vars.append(p.elm)
        return vars
    
    @_('')
    def empty4(self,p):
        return p[-3]
    
    @_('"*" empty3 elm')
    def elm(self, p):
        (id, elto) = p.elm
        tipo = TipoPuntero(elto)
        return (id, tipo)
    
    @_('ID empty2 dims')
    def elm(self, p):
        return (p.ID, p.dims)
    
    @_('')
    def empty3(self,p):
        return p[-2]
    
    @_('')
    def empty2(self,p):
        return p[-2]
    
    @_('"[" CTEENT "]" empty1 dims')
    def dims(self,p):
        tipo = TipoArray(p.CTEENT,p.dims)
        return tipo
    
    @_('')
    def dims(self,p):
        return p[-1]
    
    @_('')
    def empty1(self,p):
        return p[-4]
    
    @_('exp empty0 ";" exps')
    def exps(self,p):
        pass
    
    @_('')
    def exps(self,p):
        pass
    
    @_('')
    def empty0(self,p):
        nodo, tipo = p[-1]
        escribir(nodo, tipo)
    
    @_('lval "=" exp')
    def exp(self,p):
        nl, tl = p.lval
        ne, te = p.exp
        if(not unifica(tl, te)):
            if(tl.tipo() == "Entero" and te.tipo() == "Flotante"):
                print("hago conversion ftoi")
                tipo = TipoInt()
                ne = Nodoftoi(ne)
            else:
                if(tl.tipo() == "Flotante" and te.tipo() == "Entero"):
                    print("hago conversion itof")
                    tipo = TipoFloat()
                    ne = Nodoitof(ne)
                else:
                    if(tl.tipo() == "Entero" and te.tipo() == "Caracter"):
                        print("hago conversion ctoi")
                        tipo = TipoInt()
                        ne = Nodoctoi(ne)
                    else:
                        if(tl.tipo() == "Caracter" and te.tipo() == "Entero"):
                            print("hago conversion itoc")
                            tipo = TipoChar()
                            ne = Nodoitoc(ne)
                        else:
                            print("Error al unificar")
        else:
            tipo = tl
        nodo = NodoAsig(nl, ne)
        return (nodo, tipo)
    
    @_('sumando')
    def exp(self,p):
        return p.sumando
    
    @_('sumando "+" factor')
    def sumando(self,p):
        ns, ts = p.sumando
        nf, tf = p.factor
        if(not unifica(ts, tf)):
            if(ts.tipo() == "Entero" and tf.tipo() == "Flotante"):
                print("hago conversion itof")
                tipo = TipoFloat()
                ns = Nodoitof(ns)
            else:
                if(ts.tipo() == "Flotante" and tf.tipo() == "Entero"):
                    print("hago conversion itof")
                    tipo = TipoFloat()
                    nf = Nodoitof(nf)
                else:
                    if(ts.tipo() == "Entero" and tf.tipo() == "Caracter"):
                        print("hago conversion ctoi")
                        tipo = TipoInt()
                        nf = Nodoctoi(nf)
                    else:
                        if(ts.tipo() == "Caracter" and tf.tipo() == "Entero"):
                            print("hago conversion ctoi")
                            tipo = TipoInt()
                            ns = Nodoctoi(ns)
                        else:
                            print("Error al unificar")
        else:
            tipo = ts
        nodo = NodoSuma(ns, nf)
        return (nodo, tipo)
    
    @_('factor')
    def sumando(self,p):
        return p.factor
    
    @_('factor "*" term')
    def factor(self,p):
        nf, tf = p.factor
        nt, tt = p.term
        if(not unifica(tf, tt)):
            if(tf.tipo() == "Entero" and tt.tipo() == "Flotante"):
                print("hago conversion itof")
                tipo = TipoFloat()
                nf = Nodoitof(nf)
            else:
                if(tf.tipo() == "Flotante" and tt.tipo() == "Entero"):
                    print("hago conversion itof")
                    tipo = TipoFloat()
                    nt = Nodoitof(nt)
                else:
                    if(tf.tipo() == "Entero" and tt.tipo() == "Caracter"):
                        print("hago conversion ctoi")
                        tipo = TipoInt()
                        nt = Nodoctoi(nt)
                    else:
                        if(tf.tipo() == "Caracter" and tt.tipo() == "Entero"):
                            print("hago conversion ctoi")
                            tipo = TipoInt()
                            nf = Nodoctoi(nf)
                        else:
                            print("Error al unificar")
        else:
            tipo = tf
        nodo = NodoProd(nf, nt)
        return (nodo, tipo)
    
    @_('term')
    def factor(self,p):
        return p.term
    
    @_('lval')
    def term(self,p):
        return p.lval
    
    @_('"(" exp ")"')
    def term(self,p):
        return p.exp
    
    @_('CTEENT')
    def term(self,p):
        nodo = NodoCteEnt(p.CTEENT)
        tipo = TipoInt()
        return (nodo, tipo)
    
    @_('CTEFLOAT')
    def term(self,p):
        nodo = NodoCteFloat(p.CTEFLOAT)
        tipo = TipoFloat()
        return (nodo, tipo)
    
    @_('"*" lval')
    def lval(self,p):
        nodo, tipo = p.lval
        nodo = NodoPuntero(nodo)
        tipo = tipo.elto
        return (nodo, tipo)
    
    @_('"&" lval')
    def lval(self,p):
        nodo, tipo = p.lval
        nodo = NodoAmp(nodo)
        tipo = TipoPuntero(tipo)
        return (nodo, tipo)
    
    @_('basico')
    def lval(self,p):
        return p.basico
    
    @_('basico "[" exp "]"')
    def basico(self,p):
        nb, tb = p.basico
        ne, te = p.exp
        nodo = NodoArray(nb, ne)
        tipo = tb.elto
        return (nodo, tipo)
    
    @_('ID')
    def basico(self,p):
        nodo = NodoId(p.ID)
        tipo = tabla[p.ID]
        return (nodo, tipo)

if __name__ == '__main__':
    lexer = CalcLexer()
    parser = CalcParser()
    print("Comienza el programa:")
    while True:
        try:
            text = input('data type list > ')
        except EOFError:
            break
        if text:
            parser.parse(lexer.tokenize(text))
    print("Fin del programa")
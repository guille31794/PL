

####################################################################
#   TRABAJO REALIZADO POR JUAN RUIZ BONALD,RAFAEL ROMAN AGUILAR #
###################################################################


from sly import Lexer,Parser

class PracLexer(Lexer):
    # Set of token names.   This is always required
    tokens = { NUMBER, ID, WHILE, IF, ELSE, RETURN, SCANF, PRINTF,
               INT, PLUS, MINUS, TIMES, DIVIDE, ASSIGN,
               EQ, LT, LE, GT, GE, NE, AND, OR, NOT, STRING}


    literals = { '(', ')', '{', '}', ';', ',', '&' }

    # String containing ignored characters
    ignore = ' \t'


    # Regular expression rules for tokens
    PLUS    = r'\+'
    MINUS   = r'-'
    TIMES   = r'\*'
    DIVIDE  = r'/'
    EQ      = r'=='
    ASSIGN  = r'='
    LE      = r'<='
    LT      = r'<'
    GE      = r'>='
    GT      = r'>'
    NE      = r'!='
    AND     = r'&&'
    OR      = r'\|\|'
    NOT     = r'\!'
    STRING  = r'".*"'

    @_(r'\d+')
    def NUMBER(self, t):
        t.value = int(t.value)
        return t

    # Identifiers and keywords
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    ID['if'] = IF
    ID['else'] = ELSE
    ID['while'] = WHILE
    ID['printf'] = PRINTF
    ID['return'] = RETURN
    ID['scanf'] = SCANF
    ID['int'] = INT

    ignore_comment = r'\#.*'

    # Line number tracking
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print('Line %d: Bad character %r' % (self.lineno, t.value[0]))
        self.index += 1

global cabecera, inFunction, tabla, pila, tablaString, indiceString
inFunction = False
tabla = {}
cabecera = 4
pila = 0
tablaString = {}
indiceString = 0
indiceParaImpr = 0
        
class Nodo():
    def escribir(self):
        pass
        
class NodoFuncion(Nodo): #Nodo utilizado para las funciones
    global f_salida
    i = None
    def __init__(self, valor):
        self.i = valor
    def escribirPrincipio(self):
        f_salida.write(".text\n.globl " + self.i + "\n.type " + self.i + ", @function\n" + self.i + ":\n" )
        
        
        
class NodoInic(Nodo):
    def __init__(self):
        self.names = { }
    def escribirPrologo(self):
        f_salida.write("    pushl %ebp\n    movl %esp, %ebp\n\n")
    def escribirFinal(self):
        f_salida.write("\n    movl %ebp, %esp\n    popl %ebp\n    ret")
            

        
class NodoVariables(Nodo): #Nodo activado para almacenar las variables 
    global f_salida, tabla
    i = None
    j = None
    def __init__(self, nombre,valor):
        self.i = nombre
        self.j = valor
    def escribirInic(self):
        f_salida.write("    subl $4, %esp\n") #Funcion creada para reservar espacio
                                          #cada vez que detectamos una variabe
    def almacenarVariable(self):
        tabla[self.i] = {" " + str(self.j) + "(%ebp)"}
    def almacenarGlobal(self):
        tabla[self.i] = {str(self.i)}
    def asignaintbool(self):
        end = len(str(tabla[self.i]))
        if type(self.j) == int:
            
            f_salida.write("    movl $"+ str(self.j) + "," + str(tabla[self.i])[2:end-2] + "\n")
        else:
            if self.j == True:
                f_salida.write("    movl $1,"+str(tabla[self.i])[2:end-2]+"\n")
            else:
                f_salida.write("    movl $0,"+str(tabla[self.i])[2:end-2]+"\n")
    def asignastr(self):
        end = len(str(tabla[self.i]))
        f_salida.write("    movl "+tabla[self.j]+","+str(tabla[self.i])[2:end-2]+"\n")
    def asignaOp(self):
        end = len(str(tabla[self.i]))
        f_salida.write("    movl %eax, "+str(tabla[self.i])[2:end-2]+"\n")
    def escribirReturn(self):
        if(type(self.i)==int):
            f_salida.write("    movl $"+str(self.j)+", %eax\n")
        else:
            if(self.i!=None):
                end = len(str(tabla[self.i]))
                f_salida.write("    movl "+str(tabla[self.i])[2:end-2]+", %eax\n")



class NodoOperaciones(Nodo):
    global f_salida, tabla
    x = None
    y = None
    def __init__(self, valor1, valor2):
        self.x = valor1
        self.y = valor2

    def escribirSuma1(self): #LLamaremos a esta función cuando ninguno sea un entero
        endx = len(str(tabla[self.x]))
        endy = len(str(tabla[self.y]))
        f_salida.write("    movl " + str(tabla[self.x])[2:endx-2] + ", %eax\n")
        f_salida.write("    addl " + str(tabla[self.y])[2:endx-2] + ", %eax\n")
        eax = True

    def escribirSuma2(self): #LLamaremos a esta función cuando el primer elemento sea un entero
        
        f_salida.write("    movl $" + str(self.x) + ", %eax\n")

        if type(self.y) == int:
            f_salida.write("    addl $" + str(self.y) + ", %eax\n")
        else: #Si y fuera una global
            
            endy = len(str(tabla[self.y]))
            f_salida.write("    addl " + str(tabla[self.y])[2:endy-2] + ", %eax\n")
        eax = True

    def escribirResta1(self): #LLamaremos a esta función cuando el primer elemento NO sea un entero
        
        endx = len(str(tabla[self.x]))
        endy = len(str(tabla[self.y]))
        f_salida.write("    movl " + str(tabla[self.x])[2:endx-2] +", %eax\n")

        f_salida.write("    subl " + str(tabla[self.y])[2:endx-2] + ", %eax\n")
        eax = True


    def escribirResta2(self):#LLamaremos a esta función cuando el primer elemento sea un entero
        
          
        f_salida.write("    movl $" + str(self.x) + ", %eax\n")
        
        if type(self.y) == int:
            f_salida.write("    subl $" + str(self.y) + ", %eax\n")
        else:   
            endy = len(str(tabla[self.y]))
            f_salida.write("    subl " + str(tabla[self.y])[2:endy-2] + ", %eax\n")
        eax = True

    def escribirMulti1(self): #LLamaremos a esta función cuando el primer elemento sea un entero
        
        endx = len(str(tabla[self.x]))
        endy = len(str(tabla[self.y]))
        f_salida.write("    movl " + str(tabla[self.x])[2:endx-2] + ", %eax\n")
        f_salida.write("    imull " + str(tabla[self.y])[2:endx-2] + ", %eax\n")
        eax = True


    def escribirMulti2(self): #LLamaremos a esta función cuando el primer elemento NO sea un entero
        
        
        f_salida.write("    movl $" + str(self.x) + ", %eax\n")
        if type(self.y) == int:
            f_salida.write("    imull $" + str(self.y) + ", %eax\n")
        else:   #Si y fuera una global
            endy = len(str(tabla[self.y]))
            f_salida.write("    imull " + str(tabla[self.y])[2:endy-2] + ", %eax\n")

        eax = True
 
    def escribirDivi1(self): #LLamaremos a esta función cuando el primer elemento NO sea un entero
        
        endx = len(str(tabla[self.x]))
        endy = len(str(tabla[self.y]))
        f_salida.write("    movl " + str(tabla[self.x])[2:endx-2] + ", %eax\n")
        f_salida.write("    cdq\n")
            
        f_salida.write("    movl " + str(tabla[self.y])[2:endy-2] + ", %ecx\n")
        f_salida.write("    divl %ecx\n")
        f_salida.write("    movl %ecx, %eax\n")
        
        eax = True

    def escribirDivi2(self):#LLamaremos a esta función cuando el primer elemento sea un entero
        f_salida.write("    movl $" + str(self.x) + ", %eax\n")
        f_salida.write("    cdq\n")

        if type(self.y) == int:
            f_salida.write("    movl $" + str(self.y) + ", %ecx\n")
            f_salida.write("    divl %ecx\n")
            f_salida.write("    movl %ecx, %eax\n")
        else:   
            endy = len(str(tabla[self.y]))
            f_salida.write("    movl " + str(tabla[self.y])[2:endy-2] + ", %ecx\n")
            f_salida.write("    divl %ecx\n")
            f_salida.write("    movl %ecx, %eax\n")
        eax = True

    def escribirDivi3(self):#LLamaremos a esta función cuando el segundo es entero
        if type(self.x) == int:
            f_salida.write("    movl $" + str(self.x) + ", %eax\n")
            f_salida.write("    cdq\n")
        else:
            endx = len(str(tabla[self.x]))
            f_salida.write("    movl " + str(tabla[self.x])[2:endx-2] + ", %eax\n")
            f_salida.write("    cdq\n")

        f_salida.write("    imull $" + str(self.y) + ", %eax\n")
        f_salida.write("    divl %ecx\n")
        f_salida.write("    movl %ecx, %eax\n")
        eax = True

    def escribirAND(self):
        if type(self.x) == int:
            f_salida.write("    cmpl $"+str(self.x)+",$0\n")
            f_salida.write("    je AND\n")
        else:
            endx = len(str(tabla[self.x]))
            f_salida.write("    cmpl "+str(tabla[self.x])[2:endx-2]+",$0\n")
            f_salida.write("    je AND\n") 
            
        if type(self.y) == int:
            f_salida.write("    cmpl $"+str(self.y)+",$0\n")
            f_salida.write("    je AND\n")
        else:
            endy = len(str(tabla[self.y]))
            f_salida.write("    cmpl "+str(tabla[self.y])[2:endy-2]+",$0\n")
            f_salida.write("    je AND\n")

        f_salida.write("    movl $1,%eax\n")
        f_salida.write("    jmp F-AND\n")
        f_salida.write("AND:\n")
        f_salida.write("    movl $0,%eax\n")
        f_salida.write("F-AND:\n")
        eax = True

    def escribirOR(self):
        
        if type(self.x) == int:
            f_salida.write("    cmpl $"+str(self.x)+",$0\n")
            f_salida.write("    jne OR\n")

        else:            
            endx = len(str(tabla[self.x]))
            f_salida.write("    cmpl "+str(tabla[self.x])[2:endx-2]+",$0\n")
            f_salida.write("    jne OR\n") 
            
        if type(self.y) == int:
            endy = len(str(tabla[self.y]))
            f_salida.write("    cmpl $"+str(self.y)+",$0\n")
            f_salida.write("    jne OR\n")
        else:
            endx = len(str(tabla[self.x]))
            f_salida.write("    cmpl "+str(tabla[self.y])[2:endx-2]+",$0\n")
            f_salida.write("    jne OR\n")

        f_salida.write("    movl $0,%eax\n")
        f_salida.write("    jmp F-OR\n")
        f_salida.write("OR:\n")
        f_salida.write("    movl $1,%eax\n")
        f_salida.write("F-OR:\n")
        eax = True

    def escribirEQUAL(self):
        if type(self.x) == int:
            if type(self.y) == int:
                f_salida.write("    cmpl $"+str(self.x)+",$"+str(self.y)+"\n")
                f_salida.write("    je EQ\n")
            else:
                endx = len(str(tabla[self.x]))
                f_salida.write("    cmpl $"+str(self.x)+","+str(tabla[self.y])[2:endx-2]+"\n")
                f_salida.write("    je EQ\n")

        else:
            endx = len(str(tabla[self.x]))
            if type(self.y) == int:
                f_salida.write("    cmpl "+str(tabla[self.x])[2:endx-2]+",$"+str(self.y)+"\n")
                f_salida.write("    je EQ\n")
            else:
                endy = len(str(tabla[self.y]))
                f_salida.write("    cmpl "+str(tabla[self.x])[2:endx-2]+","+str(tabla[self.y])[2:endx-2]+"\n")
                f_salida.write("    je EQ\n")

        f_salida.write("    movl $0,%eax\n")
        f_salida.write("    jmp F-EQ\n")
        f_salida.write("EQ:\n")
        f_salida.write("    movl $1,%eax\n")
        f_salida.write("F-EQ:\n")
        eax = True


    def escribirLE(self):     
        if type(self.x) == int:
            if type(self.y) == int:
                f_salida.write("    cmpl $"+str(self.x)+",$"+str(self.y)+"\n")
                f_salida.write("    jle LE\n")
            else:
                endx = len(str(tabla[self.x]))
                f_salida.write("    cmpl $"+str(self.x)+","+str(tabla[self.y])[2:endx-2]+"\n")
                f_salida.write("    jle LE\n")

        else:
            endx = len(str(tabla[self.x]))
            if type(self.y) == int:
                f_salida.write("    cmpl "+str(tabla[self.x])[2:endx-2]+",$"+str(self.y)+"\n")
                f_salida.write("    jle LE\n")
            else:
                endy = len(str(tabla[self.y]))
                f_salida.write("    cmpl "+str(tabla[self.x])[2:endx-2]+","+str(tabla[self.y])[2:endx-2]+"\n")
                f_salida.write("    jle LE\n")
        

        f_salida.write("    movl $0,%eax\n")
        f_salida.write("    jmp F-LE\n")
        f_salida.write("LE:\n")
        f_salida.write("    movl $1,%eax\n")
        f_salida.write("F-LE:\n")
        eax = True

    def escribirLT(self):
        
        if type(self.x) == int:
            if type(self.y) == int:
                f_salida.write("    cmpl $"+str(self.x)+",$"+str(self.y)+"\n")
                f_salida.write("    jl LT\n")
            else:
                endx = len(str(tabla[self.x]))
                f_salida.write("    cmpl $"+str(self.x)+","+str(tabla[self.y])[2:endx-2]+"\n")
                f_salida.write("    jl LT\n")

        else:
            endx = len(str(tabla[self.x]))
            if type(self.y) == int:
                f_salida.write("    cmpl "+str(tabla[self.x])[2:endx-2]+",$"+str(self.y)+"\n")
                f_salida.write("    jl LT\n")
            else:
                endy = len(str(tabla[self.y]))
                f_salida.write("    cmpl "+str(tabla[self.x])[2:endx-2]+","+str(tabla[self.y])[2:endx-2]+"\n")
                f_salida.write("    jl LT\n")
        

        f_salida.write("    movl $0,%eax\n")
        f_salida.write("    jmp F-LT\n")
        f_salida.write("LT:\n")
        f_salida.write("    movl $1,%eax\n")
        f_salida.write("F-LT:\n")
        eax = True

    def escribirGE(self):
        
        if type(self.x) == int:
            if type(self.y) == int:
                f_salida.write("    cmpl $"+str(self.x)+",$"+str(self.y)+"\n")
                f_salida.write("    jge GE\n")
            else:
                endx = len(str(tabla[self.x]))
                f_salida.write("    cmpl $"+str(self.x)+","+str(tabla[self.y])[2:endx-2]+"\n")
                f_salida.write("    jge GE\n")

        else:
            endx = len(str(tabla[self.x]))
            if type(self.y) == int:
                f_salida.write("    cmpl "+str(tabla[self.x])[2:endx-2]+",$"+str(self.y)+"\n")
                f_salida.write("    jge GE\n")
            else:
                endy = len(str(tabla[self.y]))
                f_salida.write("    cmpl "+str(tabla[self.x])[2:endx-2]+","+str(tabla[self.y])[2:endx-2]+"\n")
                f_salida.write("    jge GE\n")
        

        f_salida.write("    movl $0,%eax\n")
        f_salida.write("    jmp F-GE\n")
        f_salida.write("GE:\n")
        f_salida.write("    movl $1,%eax\n")
        f_salida.write("F-GE:\n")
        eax = True

    def escribirGT(self):
        
        if type(self.x) == int:
            if type(self.y) == int:
                f_salida.write("    cmpl $"+str(self.x)+",$"+str(self.y)+"\n")
                f_salida.write("    jg GT\n")
            else:
                endx = len(str(tabla[self.x]))
                f_salida.write("    cmpl $"+str(self.x)+","+str(tabla[self.y])[2:endx-2]+"\n")
                f_salida.write("    jg GT\n")

        else:
            endx = len(str(tabla[self.x]))
            if type(self.y) == int:
                f_salida.write("    cmpl "+str(tabla[self.x])[2:endx-2]+",$"+str(self.y)+"\n")
                f_salida.write("    jg GT\n")
            else:
                endy = len(str(tabla[self.y]))
                f_salida.write("    cmpl "+str(tabla[self.x])[2:endx-2]+","+str(tabla[self.y])[2:endx-2]+"\n")
                f_salida.write("    jg GT\n")
        

        f_salida.write("    movl $0,%eax\n")
        f_salida.write("    jmp F-GT\n")
        f_salida.write("GT:\n")
        f_salida.write("    movl $1,%eax\n")
        f_salida.write("F-GT:\n")
        eax = True

    def escribirNE(self):
        
        if type(self.x) == int:
            if type(self.y) == int:
                f_salida.write("    cmpl $"+str(self.x)+",$"+str(self.y)+"\n")
                f_salida.write("    jne NE\n")
            else:
                endx = len(str(tabla[self.x]))
                f_salida.write("    cmpl $"+str(self.x)+","+str(tabla[self.y])[2:endx-2]+"\n")
                f_salida.write("    jne NE\n")

        else:
            endx = len(str(tabla[self.x]))
            if type(self.y) == int:
                f_salida.write("    cmpl "+str(tabla[self.x])[2:endx-2]+",$"+str(self.y)+"\n")
                f_salida.write("    jne NE\n")
            else:
                endy = len(str(tabla[self.y]))
                f_salida.write("    cmpl "+str(tabla[self.x])[2:endx-2]+","+str(tabla[self.y])[2:endx-2]+"\n")
                f_salida.write("    jne NE\n")
        

        f_salida.write("    movl $0,%eax\n")
        f_salida.write("    jmp F-NE\n")
        f_salida.write("NE:\n")
        f_salida.write("    movl $1,%eax\n")
        f_salida.write("F-NE:\n")
        eax = True

    def escribirNOT(self):
        
        if type(self.x) == int:
            f_salida.write("    cmpl $"+str(self.x)+",$0\n")
            f_salida.write("    je NOT\n")
        else:
            endx = len(str(tabla[self.x]))
            f_salida.write("    cmpl "+str(tabla[self.x])[2:endx-2]+",$0\n")
            f_salida.write("    je NOT\n") 

        f_salida.write("    movl $0,%eax\n")
        f_salida.write("    jmp F-NOT\n")
        f_salida.write("NOT:\n")
        f_salida.write("    movl $1,%eax\n")
        f_salida.write("F-NOT:\n")
        eax = True

    ########### empieza condicionale ############
class NodoCondicionales(Nodo):
    global f_salida
    def __init__(self):
        self.names = { }

    def escribirIFp1(self):
        f_salida.write("    cmpl $0, %eax\n")
        f_salida.write("    je final\n")
    
    def escribirIFp2(self):
        f_salida.write("final:\n")

    def escribirIF_ELSEp1(self):
        f_salida.write("    cmpl $0, %eax\n")
        f_salida.write("    je false\n")

    def escribirIF_ELSEp2(self):
        f_salida.write("    jmp final\n")
        f_salida.write("false:\n")

    def escribirIF_ELSEp3(self):
        f_salida.write("final:\n")

    def escribirWHILEp1(self):
        f_salida.write("start:\n")

    def escribirWHILEp2(self):
        f_salida.write("    cmpl $0, %eax\n")
        f_salida.write("    je final\n")

    def escribirWHILEp3(self):
        f_salida.write("    jmp start:\n")
        f_salida.write("final:\n")
        

    ########### Leer Imprimir ###############

class NodoLeerImprimir(Nodo):
    global f_salida
    def __init__(self, valor1):
        self.x = valor1

    def imprimirPush(self):
        global indiceParaImpr
        f_salida.write("    pushl "+str(self.x)+"\n")
        indiceParaImpr += 1

    def imprimirPushCadena(self):
        global indiceString,indiceParaImpr
        f_salida.write("    pushl $s"+str(indiceString)+"\n")
        indiceParaImpr += 1

    def imprimirCallP(self):
        f_salida.write("    call printf\n")

    def imprimirCallS(self):
        f_salida.write("    call scanf\n")

    def imprimirEnd(self):
        global indiceParaImpr
        f_salida.write("    addl $("+str(4*indiceParaImpr)+"), %esp\n")
        indiceParaImpr = 0

def agregarStrings(cadena):
    global f_salida
    texto = ".section .rodata"
    for i in tablaString:
        texto += "\n.LC"+str(i-1)+":\n\t.string "  + str(tablaString[i]) +"\n"

    f_salida = open(cadena, "r+")
    texto += f_salida.read()
    f_salida.close()

    f_salida = open(cadena, "w")
    f_salida.write(texto)
    f_salida.close()



class PracParser(Parser):
    tokens = PracLexer().tokens
    
    def __init__(self):
        self.names = { }
        
    @_('instruccion entrada')
    def entrada(self,p):
        pass

    @_(' ')
    def entrada(self, p):
        print(" ")
        

    ######### instruccion ########
    @_('funcion')
    def instruccion(self,p):
        pass
    
    @_('inicializacion ";"')
    def instruccion(self,p):
        pass

    @_('asignacion ";"')
    def instruccion(self,p):
        pass
        
        
    ######## contenido #####

    @_('asignacion ";" contenido')
    def contenido(self,p):
        pass

    @_('inicializacion ";" contenido')
    def contenido(self,p):
        pass

    @_('condicional contenido')
    def contenido(self,p):
        pass

    @_('retorno ";" contenido')
    def contenido(self,p):
        pass

    @_('leer ";" contenido')
    def contenido(self,p):
        pass

    @_('imprimir ";" contenido')
    def contenido(self,p):
        pass

    @_('')
    def contenido(self,p):
        pass

    ######## funcion #######
    @_('TIPO ID empty1 "(" inicializacion_cabecera ")" "{" contenido "}"')
    def funcion(self,p):
        nodo = NodoInic()
        nodo.escribirFinal()

    @_(' ') #Necesario para escribir el inicio de una función antes de que se escriba el resto de esta
    def empty1(self,p):
        global inFunction
        inFunction = True
        nodo = NodoFuncion(p[-1])
        nodo.escribirPrincipio()
        nodo = NodoInic()
        nodo.escribirPrologo()
        
    ########## leer #################
    @_('SCANF "(" STRING "," "&" ID leer_opc ")"')
    def leer(self,p):
        global tablaString, indiceString
        indiceString += 1
        tablaString[indiceString] = p.STRING
        nodo = NodoLeerImprimir(p.ID)
        nodo.imprimirPush()
        nodo.imprimirPushCadena()
        nodo.imprimirCallS()
        nodo.imprimirEnd()

    @_('"," "&" ID leer_opc')
    def leer_opc(self,p):
        nodo = NodoLeerImprimir(p.ID)
        nodo.escribirPush()

    @_('')
    def leer_opc(self,p):
        pass

############ imprimir ############
    @_('PRINTF "(" STRING imprimir_opc ")"')
    def imprimir(self,p):
        global tablaString, indiceString
        indiceString += 1
        tablaString[indiceString] = p.STRING
        nodo = NodoLeerImprimir(p.imprimir_opc)
        nodo.imprimirPushCadena()
        nodo.imprimirCallP()
        nodo.imprimirEnd()

    @_('"," "&" ID imprimir_opc')
    def imprimir_opc(self,p):
        nodo = NodoLeerImprimir(p.ID)
        nodo.escribirPush()

    @_('"," ID imprimir_opc')
    def imprimir_opc(self,p):
        nodo = NodoLeerImprimir(p.ID);
        nodo.escribirPush()

    @_(' ')
    def imprimir_opc(self,p):
        pass

    
    ######### inicializacion ########
    @_('TIPO ID empty22 resto')
    def inicializacion(self,p):
        pass

    @_('')
    def empty22(self,p):
        global inFunction, pila
        if inFunction == True:
            pila -= 4
            nodo = NodoVariables(p[-1],pila)
            nodo.escribirInic()
            nodo.almacenarVariable()
        else:
            nodo = NodoVariables(p[-1],pila)
            nodo.almacenarGlobal()
        
    @_('TIPO ID empty2 asignacion_ini resto')
    def inicializacion(self,p):
        pass

    @_('')
    def empty2(self,p):
        global inFunction, pila
        if inFunction == True:
            pila -= 4
            nodo = NodoVariables(p[-1],pila)
            nodo.escribirInic()
            nodo.almacenarVariable()
        else:
            nodo = NodoVariables(p[-1],pila)
            nodo.almacenarGlobal()
    
    @_('"," ID resto')
    def resto(self,p):
        global inFunction, pila
        if inFunction == True:
            nodo = NodoVariables(p.ID,pila)
            nodo.almacenarGlobal()
        else:
            pila -= 4
            nodo = NodoVariables(p.ID,pila)
            nodo.escribirInic()
            nodo.almacenarVariable()
    
    @_('"," ID empty2 asignacion_ini resto')
    def resto(self,p):
        pass    


    @_(' ')
    def resto(self,p):
        pass
    ######### inicializacion_cabecera ########
    @_('TIPO ID resto_cabecera')
    def inicializacion_cabecera(self,p):
        global cabecera
        cabecera += 4
        nodo = NodoVariables(p.ID,cabecera)
        nodo.almacenarVariable()

    @_(' ')
    def inicializacion_cabecera(self,p):
        pass
    
    @_('"," TIPO ID resto_cabecera')
    def resto_cabecera(self,p):
        global cabecera
        cabecera += 4
        nodo = NodoVariables(p.ID,cabecera)
        nodo.almacenarVariable()

    @_(' ')
    def resto_cabecera(self,p):
        global cabecera
        cabecera = 4
 
    ######### condicional ########
    @_('IF "(" operacionLog ")" if_ "{" contenido "}"')
    def condicional(self,p):
        nodo = NodoCondicionales()
        nodo.escribirIFp2()

    @_(' ')
    def if_(self,p):
        nodo = NodoCondicionales()
        nodo.escribirIFp1()

    @_('IF "(" operacionLog ")" if_else "{" contenido "}" fakeelse')
    def condicional(self,p):
        pass

    @_('ELSE else_ "{" contenido "}"')
    def fakeelse(self,p):
        pass

    @_(' ')
    def if_else(self,p):
        nodo = NodoCondicionales()
        nodo.escribirIF_ELSEp1()
        print("Entra por IF")

    @_(' ')
    def else_(self,p):
        nodo = NodoCondicionales()
        nodo.escribirIF_ELSEp2()
        print("Pasa por ELSE")

    @_('WHILE while_1 "(" operacionLog ")" while_2 "{" contenido "}"')
    def condicional(self,p):
        nodo = NodoCondicionales()
        nodo.escribirWHILEp3()
    
    @_(' ')
    def while_1(self,p):
        nodo = NodoCondicionales()
        nodo.escribirWHILEp1()

    @_(' ')
    def while_2(self,p):
        nodo = NodoCondicionales()
        nodo.escribirWHILEp2()

    ######### asignacion ######
    @_('ID ASSIGN operacion')
    def asignacion(self,p):
        nodo = NodoVariables(p.ID,p.operacion)
        if (type(p.operacion) == int or type(p.operacion) == bool):
            nodo.asignaintbool()
        else:
            if (type(p.operacion) == str):
                nodo.asignastr()
            else:
                nodo.asignaOp()

    @_('ASSIGN operacion')
    def asignacion_ini(self,p):      
        nodo = NodoVariables(p[-4],p.operacion)
        if (type(p.operacion) == int or type(p.operacion) == bool):
            nodo.asignaintbool()
        else:
            if (type(p.operacion) == str):
                nodo.asignastr()
            else:
                nodo.asignaOp()

    @_('operacionAri')
    def operacion(self,p):
        return p.operacionAri

    @_(' operacionLog')
    def operacion(self,p):
        return p.operacionLog

    ## operaciones aritmeticas##

    @_('sum')
    def operacionAri(self,p):
        return p.sum

    @_('sum MINUS operacionAri')
    def operacionAri(self,p):
        if type(p.sum) == int:
            nodo = NodoOperaciones(p.sum,p.operacionAri)
            nodo.escribirResta2()
        else:
            if type(p.operacionAri) == int:
                nodo = NodoOperaciones(p.operacionAri,p.sum)
                nodo.escribirResta2()
            else:
                nodo = NodoOperaciones(p.sum,p.operacionAri)
                nodo.escribirResta1()

    @_('sum PLUS operacionAri')
    def operacionAri(self,p):
        if type(p.sum) == int:
            nodo = NodoOperaciones(p.sum,p.operacionAri)
            nodo.escribirSuma2()
        else:
            if type(p.operacionAri) == int:
                nodo = NodoOperaciones(p.operacionAri,p.sum)
                nodo.escribirSuma2()
            else:
                nodo = NodoOperaciones(p.sum,p.operacionAri)
                nodo.escribirSuma1()


    @_('exprAri TIMES exprAri')
    def sum(self,p):
        if type(p.exprAri0) == int:
            nodo = NodoOperaciones(p.exprAri0,p.exprAri1)
            nodo.escribirMulti2()
        else:
            if type(p.exprAri1) == int:
                nodo = NodoOperaciones(p.exprAri1,p.exprAri0)
                nodo.escribirMulti2()
            else:
                nodo = NodoOperaciones(p.exprAri0,p.exprAri1)
                nodo.escribirMulti1()

    @_('exprAri DIVIDE exprAri')
    def sum(self,p):
        if type(p.exprAri0) == int:
            nodo = NodoOperaciones(p.exprAri0,p.exprAri1)
            nodo.escribirDivi2()
        else:
            if type(p.exprAri1) == int:
                nodo = NodoOperaciones(p.exprAri0,p.exprAri1)
                nodo.escribirDivi3()
            else:
                nodo = NodoOperaciones(p.exprAri0,p.exprAri1)
                nodo.escribirDivi1()
        return 
        

    @_('exprAri')
    def sum(self,p):
        return p.exprAri

    @_('"(" operacionAri ")"')
    def exprAri(self,p):
        return p.exprAri


    @_('factor')
    def exprAri(self,p):
        return p.factor


######### OperacionLog #######

    @_('exprLog')
    def operacionLog(self,p):
        return p.exprLog
    
    @_('factor AND exprLog')
    def exprLog(self,p):
        nodo = NodoOperaciones(p.factor,p.exprLog)
        nodo.escribirAND()

    @_('factor EQ exprLog')
    def exprLog(self,p):
        nodo = NodoOperaciones(p.factor,p.exprLog)
        nodo.escribirEQUAL()

    @_('factor OR exprLog')
    def exprLog(self,p):
        nodo = NodoOperaciones(p.factor,p.exprLog)
        nodo.escribirOR()

    @_('factor NOT exprLog')
    def exprLog(self,p):
        nodo = NodoOperaciones(p.exprLog,p.exprLog)
        nodo.escribirNOT()

    @_('factor GT exprLog')
    def exprLog(self,p):
        nodo = NodoOperaciones(p.factor,p.exprLog)
        nodo.escribirGT()

    @_('factor LT exprLog')
    def exprLog(self,p):
        nodo = NodoOperaciones(p.factor,p.exprLog)
        nodo.escribirLT()

    @_('factor NE exprLog')
    def exprLog(self,p):
        nodo = NodoOperaciones(p.factor,p.exprLog)
        nodo.escribirNE()

    @_('factor GE exprLog')
    def exprLog(self,p):
        nodo = NodoOperaciones(p.factor,p.exprLog)
        nodo.escribirGE()

    @_('factor LE exprLog')
    def exprLog(self,p):
        nodo = NodoOperaciones(p.factor,p.exprLog)
        nodo.escribirLE()

    @_('factor')
    def exprLog(self,p):
        return p.factor
        
    ######## Factor ########
    

    @_('MINUS NUMBER')
    def factor(self,p):
        return -p.NUMBER

    @_('NUMBER')
    def factor(self,p):
        return p.NUMBER

    @_('ID')
    def factor(self,p):
        return p.ID

    
    ######### retorno ########
    @_('RETURN devuelve')
    def retorno(self,p):
        pass
    
    @_('operacion')
    def devuelve(self,p):
        nodo = NodoVariables(p.operacion,p.operacion)
        nodo.escribirReturn()

    @_(' ')
    def devuelve(self,p):
        pass

    @_('INT')
    def TIPO(self,p):
        pass
 
    
  
if __name__ == '__main__':
    lexer = PracLexer()
    parser = PracParser()
    
    f_entrada = open('assembler.c','r')
    f_salida = open('main.s','w')
    option = 'assembler.c'
    with open(option, 'r') as code:
            text =  code.read()
            file = open('salida.s','w')
    try:
        if text:
            parser.parse(lexer.tokenize(text))
            file.write('###Fin del programa###')
            file.close()

            agregarStrings(cadena = 'main.s')

    except KeyboardInterrupt:
        print('Fin del programa')

from lexer import *
from nodes import *
from sly import Parser

class CalcParser(Parser):
    # Get the token list from the lexer
    tokens = CalcLexer.tokens

    # Grammar rules and actions
    @_('whatever ";" sentence')
    def sentence(self, p):
        pass
    
    @_('')
    def sentence(self, p):
        pass
    
    @_('printf')
    def whatever(self, p):
        f = open("asembler.asm", "a")
        f.write(p.printf.write())
        f.close()
        return p.printf.ret()

    @_('scanf')
    def whatever(self, p):
        f = open("asembler.asm", "a")
        f.write(p.scanf.write())
        f.close()

    @_('declaration')
    def whatever(self, p):
        pass

    @_('assign')
    def whatever(self, p):
        f = open("asembler.asm", "a")
        f.write(p.assign.write())
        f.close()
        return p.assign

    @_('SC "(" CAD store')
    def scanf(self, p):
        global stringNumber
        stringNumber += 1
        return ScanfNode(p.CAD)

    @_('"," AMPERSAND ID store')
    def store(self, p):
        scanf.append(p.ID)
    
    @_('")"')
    def store(self, p):
        pass

    @_('PR "(" CAD param')
    def printf(self, p):
        global stringNumber
        stringNumber += 1
        return PrintNode(p.CAD)

    @_('"," ID empty1 empty4 param')
    def param(self, p):
        if not p.empty1:
            Printf.append(p.ID)
        elif not p.empty4:
            Printf.append(hex(id(Variables[Pointer[p.ID]])))
        else:
            print("error:", p.ID, "not declared")

    @_('"," AMPERSAND ID empty1 empty4 param')
    def param(self, p):
        if not p.empty1:
            Printf.append(hex(id(Variables[p.ID])))
        elif not p.empty4:
            Printf.append(hex(id(Pointer[p.ID])))
        else:
            print("error:", p.ID, "not declared")

    @_('"," TIMES ID empty6 param')
    def param(self, p):
        if p.empty6:
            Printf.append(Variables[Pointer[p.ID]]) 

    @_('")"')
    def param(self, p):
        pass      
    
    @_('INT dectypes')
    def declaration(self, p):
        pass

    @_('variable')
    def dectypes(self, p):
        pass

    @_('pointer')
    def dectypes(self, p):
        pass

    @_('ID empty1 empty4 variableSeparator')
    def variable(self, p):
        if p.empty1:
            if p.empty4:
                f = open("asembler.asm", "a")
                f.write(obj.write())
                f.close()
                return obj
            else:
                print("error: conflicting types for", p.ID)
        else:
            print("Error.", p.ID, "redeclared.")
    
    @_('ID ASSIGN empty2 empty5 expr variableSeparator')
    def variable(self, p):
        if p.empty2:
            if p.empty5:
                print(type(p.expr))
                obj = AssignNode(IdNode(p.ID), p.expr.ret())
                f = open("asembler.asm", "a")
                f.write(obj.write())
                f.close()
                return obj
            else:
                print("error: conflicting types for", p.ID)
        else:
            print("Error.", p.ID, "redeclared")

    @_('TIMES ID empty1 empty4 variableSeparator')
    def pointer(self, p):
        if p.empty1:
            if p.empty4:
                obj = PointerNode(p.ID, 'NULL')
                f = open("asembler.asm", "a")
                f.write(obj.write())
                f.close()
                return obj
            else:
                print("Error:", p.ID, "redeclared")
        else:
            print("error: conflicting types for", p.ID)

    @_('TIMES ID ASSIGN empty2 empty5 AMPERSAND ID variableSeparator')
    def pointer(self, p):
        if p.empty2:
            if p.empty5:
                return PointerNode(p.ID0, p.ID1)
            else:
                print("Error:", p.ID0, "redeclared")
        else:
            print("error: conflicting types for", p.ID0)

    @_('"," dectypes')
    def variableSeparator(self, p):
        pass
    
    @_('')
    def variableSeparator(self,p):
        pass

    @_('ID ASSIGN empty3 assign')
    def assign(self, p):
        if p.empty3:
            return AssignNode(IdNode(p.ID), p.assign.ret())
        else:
            print("Error.", p.ID, "not declared")

    @_('ID ASSIGN empty4 AMPERSAND ID empty1')
    def assign(self, p):
        if not p.empty4:
            if not p.empty1:
                return PointerNode(IdNode(p.ID0), IdNode(p.ID1))
            else:
                print("error:", p.ID1, "not declared")
        else:
            print("error:", p.ID0, "not declared")

    # It last assigns between pointers

    @_('expr')
    def assign(self, p):
        f = open("asembler.asm", "a")
        f.write(p.expr.write())
        f.close()
        return p.expr

    @_('expr AND term')
    def expr(self, p):
        return AndNode(p.expr, p.term)

    @_('expr OR term')
    def expr(self, p):
        return OrNode(p.expr, p.term)

    @_('term')
    def expr(self, p):
        return p.term

    @_('term EQ logic')
    def term(self, p):
        return EqNode(p.term, p.logic)

    @_('logic')
    def term(self, p):
        return p.logic

    @_('logic NE neqExpr')
    def logic(self, p):
        return DistincNode(p.logic, p.neqExpr)

    @_('neqExpr')
    def logic(self, p):
        return p.neqExpr

    @_('neqExpr LT operator')
    def neqExpr(self, p):
        return LsNode(p.neqExpr, p.operator)

    @_('neqExpr GT operator')
    def neqExpr(self, p):
        return GrNode(p.neqExpr, p.operator)

    @_('operator')
    def neqExpr(self, p):
        if not isinstance(p.operator, IntNode):
            f = open("asembler.asm", "a")
            f.write(p.operator.write())
            f.close()
        return p.operator

    @_('operator LE operatorEQ')
    def operator(self, p):
        return LsEqNode(p.operator, p.operatorEQ)

    @_('operator GE operatorEQ')
    def operator(self, p):
        return GrEqNode(p.operator, p.operatorEQ)

    @_('operatorEQ')
    def operator(self, p):
        if not isinstance(p.operatorEQ, IntNode):
            f = open("asembler.asm", "a")
            f.write(p.operatorEQ.write())
            f.close()
        return p.operatorEQ

    @_('operatorEQ MINUS factor')
    def operatorEQ(self, p):
        return SubNode(p.operatorEQ, p.factor)

    @_('operatorEQ PLUS factor')
    def operatorEQ(self, p):
        return SumNode(p.operatorEQ, p.factor)

    @_('factor')
    def operatorEQ(self, p):
        if not isinstance(p.factor, IntNode):
            f = open("asembler.asm", "a")
            f.write(p.factor.write())
            f.close()
        return p.factor

    @_('factor TIMES cipher')
    def factor(self, p):
        return ProdNode(p.factor, p.cipher)

    @_('factor DIVIDE cipher')
    def factor(self, p):
        return DivNode(p.factor, p.cipher)

    @_('cipher')
    def factor(self, p):
        if not isinstance(p.cipher, IntNode):
            f = open("asembler.asm", "a")
            f.write(p.cipher.write())
            f.close()
        return p.cipher

    @_('MINUS cipher')
    def cipher(self, p):
        return UnaryNode(p.cipher)

    @_('NOT cipher')
    def cipher(self, p):
        return NotNode(p.cipher)

    @_('ID')
    def cipher(self, p):
        return IdNode(p.ID)

    @_('NUMBER')
    def cipher(self, p):
        return IntNode(p.NUMBER)
        

    @_('"(" assign ")"')
    def cipher(self, p):
        return AssignNode(p.assign)

    # Controls wether or not variable is declared
    # previously to declaration
    @_('')
    def empty1(self, p):
        if p[-1] in Variables:
            return False
        else:
            return True

    # Controls wether or not variable is declared
    # previously to initialization
    @_('')
    def empty2(self, p):
        if p[-2] in Variables:
            return False
        else:
            return True

    # Controls wether or not variable is declared
    # previously to assignation
    @_('')
    def empty3(self, p):
        if p[-2] in Variables:
            return True
        else:
            return False

    # Controls wether or not a variable name it's
    # a declared pointer
    @_('')
    def empty4(self, p):
        if p[-2] in Pointer:
            return False
        else:
            return True

    @_('')
    def empty5(self, p):
        if p[-3] in Pointer:
            return False
        else:
            return True
    
    @_('')
    def empty6(self, p):
        if p[-1] in Pointer:
            return True
        else:
            return False

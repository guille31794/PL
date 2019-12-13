from lexer import * # Test without from.. *
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
        return printf.ret()

    @_('scanf')
    def whatever(self, p):
        return scanf.ret()

    @_('declaration')
    def whatever(self, p):
        pass
        #return declaration.ret()

    @_('assign')
    def whatever(self, p):
        return assign.ret()

    @_('SC "(" CAD store')
    def scanf(self, p):
        return ScanfNode(CAD)

    @_('"," AMPERSAND ID store')
    def store(self, p):
        scanf.append(p.ID)
    
    @_('")"')
    def store(self, p):
        pass

    @_('PR "(" CAD param')
    def printf(self, p):
        return PrintNode(CAD)

    @_('"," ID empty1 empty4 param')
    def param(self, p):
        if not p.empty1:
            printf.append(Variables[p.ID])
        elif not p.empty4:
            printf.append(hex(id(Variables[Pointer[p.ID]])))
        else:
            print("error:", p.ID, "not declared")

    @_('"," AMPERSAND ID empty1 empty4 param')
    def param(self, p):
        if not p.empty1:
            printf.append(hex(id(Variables[p.ID])))
        elif not p.empty4:
            printf.append(hex(id(Pointer[p.ID])))
        else:
            print("error:", p.ID, "not declared")

    @_('"," TIMES ID empty6 param')
    def param(self, p):
        if p.empty6:
            return ParamNode(PointerNode(p.ID)) 

    @_('")"')
    def param(self, p):
        pass      
    
    @_('INT dectypes')
    def declaration(self, p):
        pass

    @_('variable')
    def dectypes(self, p):
        #return variable.ret()
        pass

    @_('pointer')
    def dectypes(self, p):
        #return pointer.ret()
        pass

    @_('ID empty1 empty4 variableSeparator')
    def variable(self, p):
        if p.empty1:
            if p.empty4:
                return IdNode(p.ID)
            else:
                print("error: conflicting types for", p.ID)
        else:
            print("Error.", p.ID, "redeclared.")
    
    @_('ID ASSIGN empty2 empty5 cipher variableSeparator')
    def variable(self, p):
        if p.empty2:
            if p.empty5:
                return AssignNode(IdNode(p.ID), p.cipher)
            else:
                print("error: conflicting types for", p.ID)
        else:
            print("Error.", p.ID, "redeclared")

    @_('TIMES ID empty1 empty4 variableSeparator')
    def pointer(self, p):
        if p.empty1:
            if p.empty4:
                return PointerNode(IdNode(p.ID), 'NULL')
            else:
                print("Error:", p.ID, "redeclared")
        else:
            print("error: conflicting types for", p.ID)

    @_('TIMES ID ASSIGN empty2 empty5 AMPERSAND ID variableSeparator')
    def pointer(self, p):
        if p.empty2:
            if p.empty5:
                return PointerNode(IdNode(p.ID0), IdNode(p.ID1))
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
            return AssignNode(IdNode(p.ID), p.assign)
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

    @_('expr')
    def assign(self, p):
        return p.expr.ret()

    @_('expr AND term')
    def expr(self, p):
        return AndNode(p.expr, p.term)

    @_('expr OR term')
    def expr(self, p):
        return OrNode(p.expr, p.term)

    @_('term')
    def expr(self, p):
        return p.term.ret()

    @_('term EQ logic')
    def term(self, p):
        return EqNode(p.term, p.logic)

    @_('logic')
    def term(self, p):
        return p.logic.ret()

    @_('logic NE neqExpr')
    def logic(self, p):
        return DistincNode(p.logic, p.neqExpr)

    @_('neqExpr')
    def logic(self, p):
        return p.neqExpr.ret()

    @_('neqExpr LT operator')
    def neqExpr(self, p):
        return LsNode(p.neqExpr, p.operator)

    @_('neqExpr GT operator')
    def neqExpr(self, p):
        return GrNode(p.neqExpr, p.operator)

    @_('operator')
    def neqExpr(self, p):
        return p.operator.ret()

    @_('operator LE operatorEQ')
    def operator(self, p):
        return LsEqNode(p.operator, p.operatorEQ)

    @_('operator GE operatorEQ')
    def operator(self, p):
        return GrEqNode(p.operator, p.operatorEQ)

    @_('operatorEQ')
    def operator(self, p):
        return p.operatorEQ.ret()

    @_('operatorEQ MINUS factor')
    def operatorEQ(self, p):
        return SubNode(p.operatorEQ, p.factor)

    @_('operatorEQ PLUS factor')
    def operatorEQ(self, p):
        return SumNode(p.operatorEQ, p.factor)

    @_('factor')
    def operatorEQ(self, p):
        return p.factor.ret()

    @_('factor TIMES cipher')
    def factor(self, p):
        return ProdNode(p.factor, p.cipher)

    @_('factor DIVIDE cipher')
    def factor(self, p):
        return DivNode(p.factor, p.cipher)

    @_('cipher')
    def factor(self, p):
        return p.cipher.ret()

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
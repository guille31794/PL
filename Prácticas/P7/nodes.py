import sys

Variables = {}
Pointer = {}
Printf = []
scanf = []
ebp = 0
esp = 0
stringNumber = 0

class Node():
    def ret(self):
        pass

    def write(self):
        pass

    def ebp(self):
        pass

class IntNode(Node):
    def __init__(self, val = 0):
        self.v = val 
        #self.s = "$" + str(val)

    def ret(self):
        return int(self.v)

    def write(self):
        #return self.s
        pass

class SumNode(Node):
    def __init__(self, s1, s2):
        self.v = s1.ret() + s2.ret()
        if isinstance(s1, IntNode): 
            self.s = "movl " + s1.write() + ", %eax\n"
        else:
            self.s = "movl " + str(s1.ebp()) + "(%ebp), %eax\n"
        if isinstance(s2, IntNode):
            self.s = self.s + "addl " + s2.write() + ", %eax\n"
        else:
            self.s = self.s + "addl " + str(s2.ebp()) + "(%ebp), %eax\n"

    def ret(self):
        return self.v
    
    def write(self):
        return self.s

class SubNode(Node):
    def __init__(self, s1, s2):
        self.v = s1.ret() - s2.ret()
        if isinstance(s1, IntNode):
            self.s = "movl " + s1.write() + ", %eax\n"
        else:
            self.s = "movl " + str(s1.ebp()) + "(%ebp), %eax\n"
        if isinstance(s2, IntNode):
            self.s = self.s + "subl " + s2.write() + ", %eax\n"
        else:
            self.s = self.s + "subl " + str(s2.ebp()) + "(%ebp), %eax\n"

    def ret(self):
        return self.v

    def write(self):
        return self.s

class ProdNode(Node):
    def __init__(self, s1, s2):
        self.v = s1.ret() * s2.ret()
        if isinstance(s1, IntNode):
            self.s = "movl " + s1.write() + ", %eax\n"
        else:
            self.s = "movl " + str(s1.ebp()) + "(%ebp), %eax\n"
        if isinstance(s2, IntNode):
            self.s = self.s + "imull " + s2.write() + ", %eax\n"
        else:
            self.s = self.s + "imull " + str(s2.ebp()) + "(%ebp), %eax\n" 

    def ret(self):
        return self.v

    def write(self):
        return self.s

class DivNode(Node):
    def __init__(self, s1, s2):
        self.v = int(s1.ret() / s2.ret())
        if isinstance(s1, IntNode):
            self.s = "movl " + s1.write() + ", %eax\n"
        else:
            self.s = "movl " + str(s1.ebp()) + "(%ebp), %eax\n"
        self.s = self.s + "cdq\nmovl " 
        if isinstance(s2, IntNode):
            self.s = self.s + s2.write() + ", %eax\n"
        else:
            self.s = self.s + str(s2.ebp()) + "(%ebp), %ebx\n"
        self.s = self.s + "divl %ebx\n"

    def ret(self):
        return self.v

    def write(self):
        return self.s

class UnaryNode(Node):
    def __init__(self, s):
        self.v = s.ret()
        self.s = ProdNode(s, IntNode(-1)).write()

    def ret(self):
        if self.v in Variables:
            return -Variables[self.v]
        else:
            return -self.v
    
    def write(self):
        return self.s

class AndNode(Node):
    def __init__(self, s1, s2):
        self.v1 = s1
        self.v2 = s2
        if isinstance(s1, IntNode):
            self.s = "movl " + s1.write() + ", %eax\n"
        else:
            self.s = "movl " + s1.ebp() + "(%ebp), %eax\n"
        self.s = self.s + "cmpl $0, %eax\nje false\n"
        if isinstance(s2, IntNode):
            self.s = "movl " + s2.write() + ", %eax\n"
        else:
            self.s = "movl " + s2.ebp() + "(%ebp), %eax\n"
        self.s = self.s + "cmpl $0, %eax\nje false\n"

    def ret(self):
        if self.v1.ret() and self.v2.ret():
            return 1
        else:
            return 0
    
    def write(self):
        return self.s

class OrNode(Node):
    def __init__(self, s1, s2):
        self.v1 = s1
        self.v2 = s2
        if isinstance(s1, IntNode):
            self.s = "movl " + s1.write() + ", %eax\n"
        else:
            self.s = "movl " + s1.ebp() + "(%ebp), %eax\n"
        self.s = self.s + "cmpl $0, %eax\njne false\n"
        if isinstance(s2, IntNode):
            self.s = "movl " + s2.write() + ", %eax\n"
        else:
            self.s = "movl " + s2.ebp() + "(%ebp), %eax\n"
        self.s = self.s + "cmpl $0, %eax\njne false\n"

    def ret(self):
        if self.v1.ret() or self.v2.ret():
            return 1
        else: 
            return 0
        
    def write(self):
        return self.s

class NotNode(Node):
    def __init__(self, s):
        self.v = s
        if isinstance(s, IntNode):
            self.s = "movl " + s.write() + ", %eax\n"
        else:
            self.s = "movl " + s.ebp() + "(%ebp), %eax\n"
        self.s = self.s + "cmpl $0, %eax\nje false\n"

    def ret(self):
        return int(not self.v.ret())

    def write(self):
        return self.s

class GrNode(Node):
    def __init__(self, s1, s2):
        self.v = int(s1.ret() > s2.ret())
        if isinstance(s1, IntNode):
            self.s = "movl " + s1.write() + ", %eax\n"
        else:
            self.s = "movl " + s1.ebp() + "(%ebp), %eax\n"
        if isinstance(s2, IntNode):
            self.s = self.s + "movl " + s2.write() + ", %ebx\n"
        else:
            self.s = self.s + "movl " + s2.ebp() + "(%ebp), %ebx\n"
        self.s = self.s + "cmpl %eax, %ebx\njgl true\n"

    def ret(self):
        return self.v
    
    def write(self):
        return self.s

class LsNode(Node):
    def __init__(self, s1, s2):
        self.v = int(s1.ret() < s2.ret())
        if isinstance(s1, IntNode):
            self.s = "movl " + s1.write() + ", %eax\n"
        else:
            self.s = "movl " + s1.ebp() + "(%ebp), %eax\n"
        if isinstance(s2, IntNode):
            self.s = self.s + "movl " + s2.write() + ", %ebx\n"
        else:
            self.s = self.s + "movl " + s2.ebp() + "(%ebp), %ebx\n"
        self.s = self.s + "cmpl %eax, %ebx\njll true\n"

    def ret(self):
        return self.v

    def write(self):
        return self.s

class GrEqNode(Node):
    def __init__(self, s1, s2):
        self.v1 = s1
        self.v2 = s2
        if isinstance(s1, IntNode):
            self.s = "movl " + s1.write() + ", %eax\n"
        else:
            self.s = "movl " + s1.ebp() + "(%ebp), %eax\n"
        if isinstance(s2, IntNode):
            self.s = self.s + "movl " + s2.write() + ", %ebx\n"
        else:
            self.s = self.s + "movl " + s2.ebp() + "(%ebp), %ebx\n"
        self.s = self.s + "cmpl %eax, %ebx\njgel true\n"

    def ret(self):
        return int(self.v1.ret() >= self.v2.ret())

    def write(self):
        return self.s

class LsEqNode(Node):
    def __init__(self, s1, s2):
        self.v1 = s1
        self.v2 = s2
        if isinstance(s1, IntNode):
            self.s = "movl " + s1.write() + ", %eax\n"
        else:
            self.s = "movl " + s1.ebp() + "(%ebp), %eax\n"
        if isinstance(s2, IntNode):
            self.s = self.s + "movl " + s2.write() + ", %ebx\n"
        else:
            self.s = self.s + "movl " + s2.ebp() + "(%ebp), %ebx\n"
        self.s = self.s + "cmpl %eax, %ebx\njlel true\n"

    def ret(self):
        return int(self.v1.ret() <= self.v2.ret())

    def write(self):
        return self.s

class DistincNode(Node):
    def __init__(self, s1, s2):
        self.v = int(s1.ret() != s2.ret())
        if isinstance(s1, IntNode):
            self.s = "movl " + s1.write() + ", %eax\n"
        else:
            self.s = "movl " + s1.ebp() + "(%ebp), %eax\n"
        if isinstance(s2, IntNode):
            self.s = self.s + "movl " + s2.write() + ", %ebx\n"
        else:
            self.s = self.s + "movl " + s2.ebp() + "(%ebp), %ebx\n"
        self.s = self.s + "cmpl %eax, %ebx\njnel true\n"

    def ret(self):
        return self.v

    def write(self):
        return self.s

class EqNode(Node):
    def __init__(self, s1, s2):
        self.v = int(s1.ret() == s2.ret())
        if isinstance(s1, IntNode):
            self.s = "movl " + s1.write() + ", %eax\n"
        else:
            self.s = "movl " + s1.ebp() + "(%ebp), %eax\n"
        if isinstance(s2, IntNode):
            self.s = self.s + "movl " + s2.write() + ", %ebx\n"
        else:
            self.s = self.s + "movl " + s2.ebp() + "(%ebp), %ebx\n"
        self.s = self.s + "cmpl %eax, %ebx\njel true\n"

    def ret(self):
        return self.v

    def write(self):
        return self.s

class AssignNode(Node):
    def __init__(self, id, idval):
        self.assigned = id.ret()
        if self.assigned in Variables:
            if isinstance(idval, str):
                Variables[self.assigned] = Variables[idval]
                self.s = "movl %eax," + str(id.ebp()) + "(%ebp)\n"
            else:
                # Seriously doubting
                Variables[self.assigned] = idval
                self.s = "movl $" + str(idval) + " ," + str(id.ebp()) + "(%ebp)\n"
                
        else:
            Pointer[self.assigned] = idval.ret()
            ebpPos = (len(Variables) + list(Pointer).index(self.assigned) + 1) * (-4)
            variableList = list(Variables)
            self.s = "leal " + str((variableList.index(idval.ret())+1)*(-4)) + "(%ebp), %eax\n"
            self.s = self.s + "movl %eax, " + str(ebpPos) + "(%ebp)\n"
        

    def ret(self):
        return Variables[self.assigned]

    def write(self):
        return self.s

class IdNode(Node):
    def __init__(self, id):
        if id not in Variables:
            Variables[id] = IntNode().ret()

        self.id_ = id
        # Every variable will decrease esp by itself
        global esp 
        esp = esp - 4
        self.ebp_ = esp
        self.s = "subl $4, %esp\n"
    
    def ret(self):
        return self.id_

    def id(self):
        return Variables[self.id_]

    def write(self):
        return self.s

class PointerNode(Node):
    def __init__(self, p0, p1):
        self.pointer = p0
        Pointer[self.pointer] = p1
        self.id_ = id
        global esp 
        esp = esp - 4
        self.ebp_ = esp
        self.s = "subl $4, %esp\n"
        
    def ret(self):
        return Pointer[self.pointer]
    
    def write(self):
        return self.s

class PrintNode(Node):
    def __init__(self, string):
        self.string = string[1:len(string)-1]
        Printf.reverse()
        valueList = []
        for i in Printf:
            valueList.append(Variables[i])  
        self.string = self.string % tuple(valueList)
        self.s = ""
        stackReverse = (len(Printf)+1)*4
        while len(Printf) > 0:
            aux = Printf.pop()
            if aux in Variables:
                variableList = list(Variables)
                self.s = self.s + "pushl " + str((variableList.index(aux)+1)*(-4)) + "(%ebp)\n"
            elif aux in Pointer:
                pointerList = list(Pointer)
                self.s = self.s + "pushl " + str((pointerList.index(aux)+len(Variables)+1)*(-4)) + "(%ebp)\n"
        global stringNumber
        self.s = self.s + "pushl $s" + str(stringNumber) + '\n'
        self.s = self.s + "call printf\naddl $" + str(stackReverse) + ", %esp\n"

    def ret(self):
        print(self.string)

    def write(self):
        return self.s

class ScanfNode(Node):
    def __init__(self, string):
        leng = len(scanf)
        variableList = list(Variables)
        while string.find("%d") > -1 and len(scanf) > 0:
            aux = scanf.pop()
            Variables[aux] = input()
            self.s = "leal " + str((variableList.index(aux)+1)*(-4)) + "(%ebp), %eax\n"
            self.s = self.s + "pushl %eax\n" 
            string = string.replace("%d", "", 1)
                
        if len(scanf) > 0 or string.find("%d") > -1:
            print("error: incorrect syntax")
            sys.exit()
        
        global stringNumber
        self.s = self.s + "pushl $s" + str(stringNumber) + "\n"
        self.s = self.s + "call scanf\naddl " + str(leng*(-4)) + ", %esp\n"

    def ret(self):
        pass

    def write(self):
        return self.s

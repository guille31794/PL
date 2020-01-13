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
        self.s = "$" + str(val)

    def ret(self):
        return int(self.v)

    def write(self):
        return self.s

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
        if isinstance(s2, IntNode):
            self.s = self.s + "andl %eax, " + s2.write() + '\n' 
        else:
            self.s = self.s + "andl %eax, " + s2.ebp() + "(%ebp)\n"

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
        if isinstance(s2, IntNode):
            self.s = self.s + "orl %eax, " + s2.write() + '\n' 
        else:
            self.s = self.s + "orl %eax, " + s2.ebp() + "(%ebp)\n"

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
        self.s = self.s + "negl %eax\n"

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
        Variables[id.ret()] = idval
        if isinstance(idval, IntNode):
            self.s = "movl " + idval.write() + " ," + str(id.ebp()) + "(%ebp)\n"
        else:
            # Seriously doubting
            self.s = "movl %eax," + str(id.ebp()) + "(%ebp)\n"

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
        #self.s = "subl " + str(esp) + ", %esp\n"
        self.s = "subl $4, %esp"
        # It would be possible to write a local esp to count local
        # variables and join then in only one subl instruction?
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
        
    def ret(self):
        return Pointer[self.pointer]

class PrintNode(Node):
    def __init__(self, string):
        self.string = string[1:len(string)-1]
        var_counter = 0
        try:
            if self.string.find("%d") > -1:
                var_counter = var_counter + 1
                self.string = self.string.replace("%d", str(Printf.pop()), 1)
                while self.string.find("%d") > -1:
                    var_counter = var_counter + 1
                    self.string = self.string.replace("%d", str(Printf.pop()), 1)
            elif self.string.find("%d%") > -1:
                var_counter = var_counter + 1
                self.string = self.string.replace("%d", str(Printf.pop()), 1)
                while self.string.find("%d") > -1:
                    var_counter = var_counter + 1
                    self.string = self.string.replace("%d", str(Printf.pop()), 1)
            elif self.string.find("%d ") > -1:
                var_counter = var_counter + 1
                self.string = self.string.replace("%d", str(Printf.pop()), 1)
                while self.string.find("%d") > -1:
                    var_counter = var_counter + 1
                    self.string = self.string.replace("%d", str(Printf.pop()), 1)
            elif self.string.find("%d\"") > -1:
                var_counter = var_counter + 1
                self.string = self.string.replace("%d", str(Printf.pop()), 1)
                while self.string.find("%d") > -1:
                    var_counter = var_counter + 1
                    self.string = self.string.replace("%d", str(Printf.pop()), 1)
        except IndexError:
            print("error: segmetation fault code 20502")
        global stringNumber
        self.s = "pushl $" + str(stringNumber) + '\n'
        self.s = self.s
        

    def ret(self):
        print(self.string)

    def write(self):
        return self.s

class ScanfNode(Node):
    def __init__(self, string):
        leng = len(scanf)
        while string.find("%d") > -1 and leng > 0:
            Variables[scanf.pop()] = input()
            string = string.replace("%d", "", 1)
            leng -= 1
                
        if leng > 0 or string.find("%d") > -1:
            print("error: incorrect syntax")
            sys.exit()

    def ret(self):
        pass

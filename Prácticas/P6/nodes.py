import sys

Variables = {}
Pointer = {}
Printf = []
scanf = []

class Node():
    def ret():
        pass

class IntNode(Node):
    def __init__(self, val = 0):
        self.v = val

    def ret(self):
        return int(self.v)

class SumNode(Node):
    def __init__(self, s1, s2):
        self.v = s1.ret() + s2.ret()

    def ret(self):
        return self.v

class SubNode(Node):
    def __init__(self, s1, s2):
        self.v = s1.ret() - s2.ret()

    def ret(self):
        return self.v

class ProdNode(Node):
    def __init__(self, s1, s2):
        self.v = s1.ret() * s2.ret()

    def ret(self):
        return self.v

class DivNode(Node):
    def __init__(self, s1, s2):
        self.v = int(s1.ret() / s2.ret())

    def ret(self):
        return self.v

class UnaryNode(Node):
    def __init__(self, s):
        self.v = s.ret()

    def ret(self):
        if self.v in Variables:
            return -Variables[self.v]
        else:
            return -self.v

class AndNode(Node):
    def __init__(self, s1, s2):
        self.v1 = s1
        self.v2 = s2

    def ret(self):
        if self.v1.ret() and self.v2.ret():
            return 1
        else:
            return 0

class OrNode(Node):
    def __init__(self, s1, s2):
        self.v1 = s1
        self.v2 = s2

    def ret(self):
        if self.v1.ret() or self.v2.ret():
            return 1
        else: 
            return 0

class NotNode(Node):
    def __init__(self, s):
        self.v = s

    def ret(self):
        return int(not self.s.ret())

class GrNode(Node):
    def __init__(self, s1, s2):
        self.v = int(s1.ret() > s2.ret())

    def ret(self):
        return self.v

class LsNode(Node):
    def __init__(self, s1, s2):
        self.v = int(s1.ret() < s2.ret())

    def ret(self):
        return self.v

class GrEqNode(Node):
    def __init__(self, s1, s2):
        self.v1 = s1
        self.v2 = s2

    def ret(self):
        return int(self.v1.ret() >= self.v2.ret())

class LsEqNode(Node):
    def __init__(self, s1, s2):
        self.v1 = s1
        self.v2 = s2

    def ret(self):
        return int(self.v1.ret() <= self.v2.ret())

class DistincNode(Node):
    def __init__(self, s1, s2):
        self.v = int(s1.ret() != s2.ret())

    def ret(self):
        return self.v

class EqNode(Node):
    def __init__(self, s1, s2):
        self.v = int(s1.ret() == s2.ret())

    def ret(self):
        return self.v

class AssignNode(Node):
    def __init__(self, id, idval):
        self.assigned = id.ret()
        Variables[id.ret()] = idval
        
    def ret(self):
        return Variables[self.assigned]

class IdNode(Node):
    def __init__(self, id):
        if id not in Variables:
            Variables[id] = IntNode().ret()

        self.id = id
    
    def ret(self):
        return self.id

    def id(self):
        return Variables[self.id]

class PointerNode(Node):
    def __init__(self, p0, p1):
        self.pointer = p0
        Pointer[self.pointer] = p1
        
    def ret(self):
        return Pointer[self.pointer]

class PrintNode(Node):
    def __init__(self, string):
        self.string = string[1:len(string)-1]
        try:
            if self.string.find("%d") > -1:
                self.string = self.string.replace("%d", str(Printf.pop()), 1)
                while self.string.find("%d") > -1:
                    self.string = self.string.replace("%d", str(Printf.pop()), 1)
            elif self.string.find("%d%") > -1:
                self.string = self.string.replace("%d", str(Printf.pop()), 1)
                while self.string.find("%d") > -1:
                    self.string = self.string.replace("%d", str(Printf.pop()), 1)
            elif self.string.find("%d ") > -1:
                self.string = self.string.replace("%d", str(Printf.pop()), 1)
                while self.string.find("%d") > -1:
                    self.string = self.string.replace("%d", str(Printf.pop()), 1)
            elif self.string.find("%d\"") > -1: 
                self.string = self.string.replace("%d", str(Printf.pop()), 1)
                while self.string.find("%d") > -1:
                    self.string = self.string.replace("%d", str(Printf.pop()), 1)
        except IndexError:
            print("error: segmetation fault code 20502")

    def ret(self):
        print(self.string)

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
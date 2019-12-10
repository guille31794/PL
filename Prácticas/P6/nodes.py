Variables = {}
Pointer = {}
printf = []
scanf = []

class Node():
    def ret():
        pass

class IdNode(Node):
    def __init__(self, id):
        if id not in Variables:
            Variables[id] = IntNode()

        self.id = id
    
    def ret(self):
        return Variables[id]

    def id(self):
        return self.id

class IntNode(Node):
    def __init__(self, val = 0):
        self.v = val

    def ret(self):
        return self.v

class SumNode(Node):
    def __init__(self, s1, s2)
        self.v1 = s1
        self.v2 = s2

    def ret(self):
        return self.v1 + self.v2

class SubNode(Node):
    def __init__(self, s1, s2):
        self.v1 = s1
        self.v2 = s2

    def write(self):
        return self.v1 - self.v2

class ProdNode(Node):
    def __init__(self, s1, s2):
        self.v1 = s1
        self.v2 = s2

    def ret(self):
        return self.v1 * self.v2

class DivNode(Node):
    def __init__(self, s1, s2):
        self.v1 = s1
        self.v2 = s2

    def ret(self):
        return self.v1 / self.v2

class UnaryNode(Node):
    def __init__(self, s):
        self.v = s

    def ret(self):
        return -self.v

class AndNode(Node):
    def __init__(self, s1, s2):
        self.v1 = s1
        self.v2 = s2

    def ret(self):
        if self.s1 and self.s2:
            return 1
        else:
            return 0

class OrNode(Node):
    def __init__(self, s1, s2):
        self.v1 = s1
        self.v2 = s2

    def ret(self):
        if self.v1 or self.v2:
            return 1
        else: 
            return 0

class NotNode(Node):
    def __init__(self, s):
        self.v = s

    def ret(self):
        return int(not self.s)

class GrNode(Node):
    def __init__(self, s1, s2):
        self.v1 = s1
        self.v2 = s2

    def ret(self):
        return int(self.v1 > self.v2)

class LsNode(Node):
    def __init__(self, s1, s2):
        self.v1 = s1
        self.v2 = s2

    def ret(self):
        return int(self.v1 < self.v2)

class GrEqNode(Node):
    def __init__(self, s1, s2):
        self.v1 = s1
        self.v2 = s2

    def ret(self):
        return int(self.v1 >= self.v2)

class LsEqNode(Node):
    def __init__(self, s1, s2):
        self.v1 = s1
        self.v2 = s2

    def ret(set):
        return int(self.v1 <= self.v2)

class DistincNode(Node):
    def __init__(self, s1, s2):
        self.v1 = s1
        self.v2 = s2

    def ret(self):
        return int(self.v1 != self.v2)

class EqNode(Node):
    def __init__(self, s1, s2):
        self.v1 = s1
        self.v2 = s2

    def ret(self):
        return int(self.v1 == self.v2)

class AssignNode(Node):
    def __init__(self, id, idval):
        self.assigned = id.id()
        Variables[id.id()] = idval
        
    def ret(self):
        return Variables[self.assigned]

class PointerNode(Node):
    def __init__(self, p0, p1):
        self.pointer = p0.id()
        Pointer[self.pointer] = p1.id()
        
    def ret(self):
        return Pointer[self.pointer]

class PrintNode(Node):
    def __init__(self, ):

    def ret(self):
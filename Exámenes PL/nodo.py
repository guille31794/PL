Tabla = {}

class Nodo():
	def evalua():
		pass

class nodoAsign(Nodo):
	def __init__(self,e1,e2):
		self.id = e1
		self.val = e2
		Tabla[self.id] = self.val

	def evalua(self):
		pass

class nodoPrint(Nodo):
	def __init__(self,e):
		self.val = e

	def evalua(self):
		print("Resultado es ", self.val.evalua())

class NodoId(Nodo):
	def __init__(self,e):
		self.id = e

	def evalua(self):
		return Tabla[self.id]

class NodoNum(Nodo):
	def __init__(self,e):
		self.num = e

	def evalua(self):
		return self.num

class NodoOper(Nodo):
	def __init__(self,sim,e1,e2):
		self.sim = sim
		self.oper1 = e1
		self.oper2 = e2

	def evalua(self):
		if sim == "and":
			return self.oper1.evalua and self.oper2.evalua
		if sim == "or":
			return self.oper1.evalua or self.oper2.evalua
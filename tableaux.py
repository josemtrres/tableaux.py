#-*-coding: utf-8-*-
from random import choice
##############################################################################
# Variables globales
##############################################################################

# Crea las letras minúsculas a-z
letrasProposicionales = [chr(x) for x in range(97, 123)]
# inicializa la lista de interpretaciones
listaInterpsVerdaderas = []
# inicializa la lista de hojas
listaHojas = []
# inicializa los conectivos binarios notese que el conectivo binario SII no se 
# usa pues P <-> Q es logicamente equivalente a P>Q Y Q>P
conectivosbinarios = ['Y','O','>']
negacion = ['-']

##############################################################################
# Definición de objeto tree y funciones de árboles
##############################################################################

class Tree(object):
	def __init__(self, label, left, right):
		self.left = left
		self.right = right
		self.label = label

def Inorder(f):
    # Imprime una formula como cadena dada una formula como arbol
    # Input: tree, que es una formula de logica proposicional
    # Output: string de la formula
	if f.right == None:
		return f.label
	elif f.label == '-':
		return f.label + Inorder(f.right)
	else:
		return "(" + Inorder(f.left) + f.label + Inorder(f.right) + ")"
    
def StringtoTree(A):
    # Crea una formula como tree dada una formula como cadena escrita en notacion polaca inversa
    # Input: A, lista de caracteres con una formula escrita en notacion polaca inversa
             # letrasProposicionales, lista de letras proposicionales
    # Output: formula como tree
    pila = []
    for c in A:
        if c in negacion:
            formulaAux = Tree(c, None, pila[-1])
            del pila[-1]
            pila.append(formulaAux)
        elif c in conectivosbinarios:
            formulaAux = Tree(c, pila[-1], pila[-2])
            del pila[-1]
            del pila[-1]
            pila.append(formulaAux)
        else:
            pila.append(Tree(c, None, None))
    return pila[-1]

def Inorder2Tree(A):
	if len(A) == 1:
		return Tree(A[0], None, None)
	elif A[0] == '-':
		return Tree(A[0], None, Inorder2Tree(A[1:]))
	elif A[0] == "(":
		counter = 0 #Contador de parentesis
		for i in range(1, len(A)):
			if A[i] == "(":
				counter += 1
			elif A[i] == ")":
				counter -=1
			elif (A[i] in ['Y', 'O', '>', '=']) and (counter == 0):
				return Tree(A[i], Inorder2Tree(A[1:i]), Inorder2Tree(A[i + 1:-1]))
	else:
		return -1


##############################################################################
# Definición de funciones de tableaux
##############################################################################

def imprime_hoja(H):
	cadena = "{"
	primero = True
	for f in H:
		if primero == True:
			primero = False
		else:
			cadena += ", "
		cadena += Inorder(f)
	return cadena + "}"
        
def imprime_listaHojas(L):
	for h in L:
		print(imprime_hoja(h))

def complemento(l):
    # Esta función devuelve el complemento de un literal
    # Input: l, un literal
    # Output: x, un literal
    if l[0] in conectivosbinarios:
        pass
    elif l[0] in negacion:
        a = Tree(l[1],None,None)
    else:
        a = Tree('-',None,Tree(l,None,None))
    return a

def par_complementario(l):
    for i in l:
        if i.label in conectivosbinarios:
            pass
        elif i.label in negacion:
            if i.right.label in negacion:
                pass
            else:
                a = i.right.label
                if complemento(a) in l:
                    return True
        else:
            a = i.label
            if complemento(a) in l:
                return True

def es_literal(f):
    # Esta función determina si el árbol f es un literal
    # Input: f, una fórmula como árbol
    # Output: True/False
    if f.label in negacion:
        if (f.right.label in negacion) or (f.right.label in conectivosbinarios):
            return False
        else:
            return True
    elif f.label in conectivosbinarios:
        return False
    else:
        return True

def no_literales(l):
    for h in l:
        if es_literal(h) == False:
            return True
        else:
            pass
    return False 
               
def clasificacion(f):
    if f.label in negacion:
        if f.right.label in negacion:
            return 'Alfa1'
        elif f.right.label == 'O':
            return 'Alfa3'
        elif f.right.label == '>':
            return  'Alfa4'
        elif f.right.label == 'Y':
            return  'Beta1'
    elif f.label == 'Y':
        return 'Alfa2'
    elif f.label == "O":
        return 'Beta2'
    elif f.label == '>':   
        return 'Beta3'
    
def clasifica_y_extiende(f, h):
	# Extiende listaHojas de acuerdo a la regla respectiva
	# Input: f, una fórmula como árbol
	# 		 h, una hoja (lista de fórmulas como árboles)
	# Output: no tiene output, pues modifica la variable global listaHojas

	global listaHojas

	print("Formula:", Inorder(f))
	print("Hoja:", imprime_hoja(h))

	assert(f in h), "La formula no esta en la lista!"

	clase = clasificacion(f)
	print("Clasificada como:", clase)
	assert(clase != None), "Formula incorrecta " + imprime_hoja(h)

	if clase == 'Alfa1':
	aux = [x for x in h if x != f] + [f.right.right]
	listaHojas.remove(h)
	listaHojas.append(aux)
	
	elif clase == 'Alfa2':
	aux = [x for x in h if x != f] + [f.left] + [f.right]
	listaHojas.remove(h)
	listaHojas.append(aux)
	
    	elif clase == 'Alfa3':
        aux = [x for x in h if x != f] + ["-"+ [f.left]] + ["-" + [f.right]]
        listaHojas.remove(h)
	listaHojas.append(aux)
        
    	elif clase == "Beta1":
        aux = [x for x in h if x != f] + ["-"+ [f.left]] + [x for x in h if x != f] + ["-" + [f.right]]
        listaHojas.remove(h)
	listaHojas.append(aux)
	
    	elif clase == "Beta2":
        aux = [x for x in h if x != f] + [f.left] + [x for x in h if x != f] + [f.right]
        listaHojas.remove(h)
	listaHojas.append(aux)
	
    	elif clase == "Beta3":
        aux = [x for x in h if x != f] + ["-" + [f.left]] + [x for x in h if x != f] + [f.right]
        listaHojas.remove(h)
	listaHojas.append(aux)

def Tableaux(f):

	# Algoritmo de creacion de tableau a partir de lista_hojas
	# Imput: - f, una fórmula como string en notación polaca inversa
	# Output: interpretaciones: lista de listas de literales que hacen
	#		 verdadera a f

	global listaHojas
	global listaInterpsVerdaderas

	A = StringtoTree(f)
	print(u'La fórmula introducida es:\n', Inorder(A))

	listaHojas = [[A]]

	while (len(listaHojas) > 0):
		h = choice(listaHojas)
		print("Trabajando con hoja:\n", imprime_hoja(h))
		x = no_literales(h)
		if x == None:
			if par_complementario(h):
				listaHojas.remove(h)
			else:
				listaInterpsVerdaderas.append(h)
				listaHojas.remove(h)
		else:
			clasifica_y_extiende(x, h)

	return listaInterpsVerdaderas


f = Inorder2Tree('-(rYs)')

h = [f, Inorder2Tree('-p')] 

listaHojas = [h]

clasifica_y_extiende(f, h)

imprime_listaHojas(listaHojas)

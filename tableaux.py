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
        if c in letrasProposicionales:
            pila.append(Tree(c, None, None))
        elif c in negacion:
            formulaAux = Tree(c, None, pila[-1])
            del pila[-1]
            pila.append(formulaAux)
        elif c in conectivosbinarios:
            formulaAux = Tree(c, pila[-1], pila[-2])
            del pila[-1]
            del pila[-1]
            pila.append(formulaAux)
    return pila[-1]


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

def par_complementario(l):
	# Esta función determina si una lista de solo literales
	# contiene un par complementario
	# Input: l, una lista de literales
	# Output: True/False
	return False

def es_literal(f):

    if f.label in letrasProposicionales:
        return True
    if f.label in negacion:
        if f.right.label in negacion:
            return False
        else:
            return es_literal(f.right)
    elif f.label in conectivosbinarios:
        return False

def no_literales(l):
    for h in l:
        if es_literal(h) == False:
            return True
        else:
            pass
    return True 
               

def clasifica_y_extiende(f):
	# clasifica una fórmula como alfa o beta y extiende listaHojas
	# de acuerdo a la regla respectiva
	# Input: f, una fórmula como árbol
	# Output: no tiene output, pues modifica la variable global listaHojas
	global listaHojas
    
def Tableaux(f):

    # Algoritmo de creacion de tableau a partir de lista_hojas
    # Imput: - f, una fórmula como string en notación polaca inversa
    # Output: interpretaciones: lista de listas de literales que hacen
    #         verdadera a f
    global listaHojas
    global listaInterpsVerdaderas

    A = StringtoTree(f)
    listaHojas = [[A]]

    return listaInterpsVerdaderas


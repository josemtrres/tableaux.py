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
I = []
aux = {}
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

for a in letrasproposicionales:
    aux[a] = 1
I.append(aux)

for a in letrasProposicionales:
    I_aux = [i for i in I]
    for i in I_aux:
        aux1 = {}
        for b in letrasProposicionales:
            if a == b:
                aux1[b] = 1 - i[b]
            else:
                aux1[b] = i[b]
        I.append(aux1)
    
def VI(f,I):
    if f.label in letrasProposicionales:
        return I[f.label]
    if f.label in negacion:
        return (1-VI(f.right, I))
    if f.label  == 'Y':
        return (VI(f.left, I)* VI(f.right, I))
    if f.label == 'O':
        return max((VI(f.left, I), VI(f.right, I)))
    if f.label == '>':
        return max(1-VI(f.left,I), VI(f.right,I))
    if f.label == '<->':
        return 1-pow((VI(f.left, I) - VI(f.right)), 2)
    
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
	# Esta función determina si el árbol f es un literal
	# Input: f, una fórmula como árbol
	# Output: True/False
    if f.label in letrasProposicionales:
        return True
    if f.label in negacion:
        return True
    elif f.label in conectivosbinarios:
        return False

def no_literales(l):
	# Esta función determina si una lista de fórmulas contiene
	# solo literales
	# Input: l, una lista de fórmulas como árboles
	# Output: None/f, tal que f no es literal
	return False

def clasifica_y_extiende(f):
	# clasifica una fórmula como alfa o beta y extiende listaHojas
	# de acuerdo a la regla respectiva
	# Input: f, una fórmula como árbol
	# Output: no tiene output, pues modifica la variable global listaHojas
	global listaHojas

def Tableaux(f):

	# Algoritmo de creacion de tableau a partir de lista_hojas
	# Input: - f, una fórmula como string en notación polaca inversa
	# Output: interpretaciones: lista de listas de literales que hacen
	#		 verdadera a f
	global listaHojas
	global listaInterpsVerdaderas

	A = StringtoTree(f)
	listaHojas = [[A]]

	return listaInterpsVerdaderas

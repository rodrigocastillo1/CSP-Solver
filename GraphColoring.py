#GraphColoring.py
#Proyecto CSPSolver
#Autor: Castillo Alcántara Rodrigo

import numpy
import math


class Node:
	def __init__(self, name, color = None):
		self.name = name 				#Se trata del nombre del grafo con el cual se identifica
		self.color = color 				#Se trata del color del grafo con el cual se genera
		self.coordinates = () 			#Tupla con las coordenadas en x e y del nodo para la implementación gráfica

class Graph:
	def __init__(self, fich):
		self.nodes = [] 										#Se trata de una lista de los nodos que ya tienen asignado un color
		self.links = Graph.AdjacencyDict(self, fich) 			#Se trata del diccionario en el que se precisan los enlaces
		self.order = len(self.links) 							#Número de nodos del grafo dado por la cantidad de claves en el diccionario de self.links
		self.chromatic_number = Graph.ChromaticNumber(self) 	#El mínimo número de colores con los cuales se puede pintar un grafo
		self.chromatic_list = Graph.ChromaticList(self)			#Lista (Dominio) de colores con los cuales se pinta un grafo, determinada según el número cromático

	def isAvailable(self, new_node): 										#Función que indica si un color para un nodo está disponible
		for adj_node in self.links.get(new_node.name):						#Por cada "nombre" de nodo adyacente al que se recibió como parámetro en el diccionario de nodos adyacentes 
			for node in self.nodes: 										#Por cada nodo en la lista de nodos que ya fueron asignados
				if adj_node == node.name and node.color == new_node.color: 	#Si el nombre del nodo adyacente es el mismo que el que se está iterando y el color de dicho nodo es el mismo que el color del nodo que se pasó como parámetro
					return False 											#Retornamos "False" que indicará que ya existe un nodo adyacente con el mismo color que el nodo que ingresó como parámetro
		return True 														#Si se recorrieron todos los nodos y no existen nodos adyacentes aún coloreados o si ninguno de estos tiene el mismo color que el se está ingresando retornamos "True", es decir: es un color válido

	def AdjacencyMatrix(self): 										#Genera la matríz de adyacencia del grafo
		nodes = self.links.keys() 									#Genera una lista con los nodos que contiene el diccionario de nodos del grafo
		rows_list = [] 												#Lista en la que se almacenan los renglones de la matríz de adyacencia
		for row_node in nodes: 										#Por cada nodo renglón en la lista de nodos:
			row_elements_list = [] 									#Lista de los elementos del renglón
			for column_node in nodes: 								#Por cada nodo de columna en la lista de nodos:
				if column_node in self.links.get(row_node): 		#Si el nodo columna se encuentra en la lista de nodos asociados del nodo renglón
					row_elements_list.append(1) 					#Ingresamos un 1 en la lista del renglón
				else: 												#Sino:
					row_elements_list.append(0) 					#Ingresamos un cero a la lista
			rows_list.append(row_elements_list) 					#Cada que cambiamos de renglón ingresamos la lista del renglón anterior
		adj_matrix = numpy.mat(rows_list) 							#Cuando se terminan de iterar todos los renglones: generamos la matríz de adyacencia con ellos
		return adj_matrix 											#Regresamos la matríz de adyacencia

	def ChromaticNumber(self): 															#Función que determina el número cromático de un grafo
		adj_matrix = Graph.AdjacencyMatrix(self) 										#Generamos la matríz de adyacencia del grafo
		eigen_values = list(numpy.linalg.eigvals(adj_matrix)) 							#Generamos la lista de los eigenvalores de la matriz de adyacencia
		if max(eigen_values) == 0 and min(eigen_values) == 0: return 1 				 	#Si se introducen grafos en los que todos los nodos son independientes entonces los eigenvalores serán cero, en ese caso el número de colores será 1
		chromatic_number = math.ceil(1 - (max(eigen_values)/min(eigen_values))) 		#Calculamos el número cromático de la diferencia de 1 y la división del eigenvalor máximo y mínimo. Transformamos a este entero con la función techo "ceil"
		return chromatic_number 														#Retornamos el número cromático

	def ChromaticList(self): 												#Función para generar la lista de colores mínimos con los que se puede llenar un grafo
		available_colors = ["blue", "red", "green", "yellow", "cian"] 		#Tenemos definida ya una lista de colores disponibles. Esta lista tiene unicamente atendiendo a la solución del problema de los cinco colores que dice que cualquier grafo se puede colorear con cinco colores. Podrían agregarse más en caso de que se encuentre un caso extra
		return available_colors[:self.chromatic_number] 					#Regresamos una sublista de la lista de colores dispoibles desde el primero hasta el que está en la posición "número cromático"

	def AdjacencyDict(self, file_name):										#Función para generar el diccionario de nodos adyacentes del grafo, esta es la información principal del grafo
		adjacency_dict = {} 												#Inicialiazamos un diccionario
		fich = open(file_name, "r") 										#Abrimos el archivo en el cual está contenida la información del grafo
		for line in fich.readlines(): 										#Por cada linea en la lista de lineas del archivo:
			keyAndValues = line.split(":") 									#Generamos una lista cuyo primer elemento es el el nodo "clave", el segundo es una cadena con los nodos adyacentes separados por comas
			if len(keyAndValues) <= 1:
				values = []
			else:
				values = keyAndValues[1].split(",") 							#Generamos una lista de valores que contendrá a los nodos adyacentes en forma de cadena
			adjacency_dict[int(keyAndValues[0])] = [int(node) for node in values] 		#Ingresamos ahora los elementos al diccionario de adyacencia cuya clave será el valor entero del nodo y cuyo valor será la lista generada en la linea anterior pero con enteros
		fich.close() 														#Cerramos el archivo
		return adjacency_dict 												#Retornamos el diccionario de adyacencia
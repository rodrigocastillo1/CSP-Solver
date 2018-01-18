#GraphColoring-pygame.py
#Proyecto CSPSolver
#Autor: Castillo Alcántara Rodrigo

import pygame
from pygame.locals import *
import sys
import math
import numpy
import GraphColoring
import csp_Solver

SCREEN_WIDTH = 640 				#Ancho de la ventana en pixeles
SCREEN_HEIGHT = 640 			#Altura de la ventana en pixeles

#Diccionario de colores con sus tuplas RBG para usarlos con facilidad
colors = {"white":(255,255,255), "red":(255,0,0), "green":(0,255,0), "blue":(0,0,255), "black":(0,0,0), "yellow":(255, 255, 0), "cian":(0, 255, 255)}

def toScreenCoordSys(point): 			#Función que convierte coordenadas cartesianas a coordenadas de la ventana
	return (int(SCREEN_WIDTH/2 + point[0]), int(SCREEN_HEIGHT/2 - point[1])) 	#Retornamos una tupla de un punto con x e y

def toCartesianCoordSys(point): 		#Función que convierte coordenadas de la ventana a coordenadas cartesianas
	return (int(point[0] - SCREEN_WIDTH/2), int(-point[1] + SCREEN_HEIGHT/2)) 	#Retorna una tupla de un punto con x e y

def middlePoint(point1, point2): 								#Función para encontrar el punto medio. Recibe coordenadas cartesianas
	return ((point1[0]+point2[0])/2, (point1[1]+point2[1])/2) 	#Retorna una tupla con el valor del punto medio de un segmento en coordenadas cartesianas

def pointsDistance(point1, point2): 										#Función para obtener la distancia entre dos puntos. Recibe coordenadas cartesianas
	return numpy.linalg.norm(numpy.array(point1) - numpy.array(point2)) 	#Hace uso de las funciones de algebra lineal de numpy, retorna la norma del segmento que recibe

def rotation(point, angle): 						#Función que calcula las coordenadas del siguiente punto aplicando una transformación lineal a las coordenadas de un punto inicial. Recibe el punto en coordenadas cartesianas
	rotation_matrix = numpy.mat([[math.cos(math.radians(angle)), -1*math.sin(math.radians(angle))], 	#Matríz de rotación de un punto respecto al origen en un determinado ángulo 
						[math.sin(math.radians(angle)), math.cos(math.radians(angle))]]) 				
	point_vector = numpy.mat([[point[0]], [point[1]]]) 					#Obtenemos el vector columna del punto que entro por consola, esto para operarlo con la matríz de rotación
	new_point = rotation_matrix * point_vector 							#Encontramos el nuevo punto, resultado de aplicar la transformación anterior al multiplicar la matríz de rotación por el vector columna del punto original
	return (int(new_point[0,0]), int(new_point[1,0])) 					#Retornamos el nuevo punto por medio de una tupla. Está en coordenadas cartesianas

def AddCoordinatesToNodes(point, graph): 						#Función para llenar el atributo de coordenadas a cada nodo del grafo
	for node in graph.nodes: 									#Por cada nodo en la lista de nodos del grafo:
		node.coordinates = toScreenCoordSys(point) 				#Las coordenadas del primer nodo estarán dadas por el primer punto que se pasó como parámetro
		point = rotation(point, 360/len(graph.nodes)) 			#Después se calculan las coordenadas del siguiente punto por medio de la función de rotación, pasando el punto inicial y el ángulo que estará en función de la cantidad de nodos que tenga el grafo, formando un polígono

def getRadius(graph, y_coord): 									#Función para encontrar el radio de los nodos que se dibujarán
	if graph.order <= 2: 										#Si el orden del grafo es menor o igual a dos:
		radius = 100 											#Damos un radio constante de 100
	else: 														#Sino:
		#El radio será igual a la mitad de la distancia que exista entre la recta secante a la circunferencia del grafo que pase por dos nodos separados por un tercer nodo entre ellos
		#y dicho punto medio. Así, si tenemos a los puntos a, b, c colocados en dicho orden, el radio será: 1/2(distancia entre b y la recta ac)
		radius = int(pointsDistance(graph.nodes[1].coordinates, middlePoint(graph.nodes[0].coordinates, graph.nodes[2].coordinates))/2)
		origin_circle_distance = radius + y_coord 						#Calculamos la distancia que existe desde el origen de nuestro "sistema cartesiano" y el punto final del primer círculo dibujado
		if origin_circle_distance > SCREEN_HEIGHT/2: 					#Si esta distancia es mayor a lo que mide la mitad de la pantalla entónces una parte de nuestro círculo quedará fuera de la pantalla, por lo cual tenemos que hacer más pequeño el radio
			while origin_circle_distance > SCREEN_HEIGHT/2 - 10: 		#Mientras la distancia de la que se habló anteriormente siga siendo mayor que la mitad de la ventana, el círculo seguirá dibujandose fuera de la ventana, para lo cual:
				radius -= 1 											#Vamos decrementando el radio hasta que se adecue a un tamaño que no lo haga salirse de la ventana
				origin_circle_distance = radius + y_coord 				#Calculamos la nueva distancia del origen hasta el centro del círculo con el nuevo radio, así sabremos si ya se trata de un radio adecuado
	return radius 														#Retornamos el radio

def GraphDrawer(graph): 												#Función para dibujar el grafo
	pygame.init() 														#Iniciamos pygame
	screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) 	#Creamos el objeto screen, que será la ventana y que tendrá por medidas a los pixeles que definimos al inicio
	pygame.display.set_caption("Graph Coloring") 						#Escribimos un título adecuado para la ventana
	y_coord = (SCREEN_HEIGHT/2) - (SCREEN_HEIGHT/2)/graph.order 		#Calculamos la coordenada en y del punto inicial del grafo, que estará dado según la cantidad de nodos que se tengan en el grafo.  
	AddCoordinatesToNodes((0, y_coord), graph) 							#Añadimos las coordenadas a los nodos del grafo, eviando como parámetro a las coordenadas el primer nodo
	radius = getRadius(graph, y_coord) 									#Obtenemos el radio de los nodos, el cual estará adecuado según la cantidad de nodos
	pygame.display.flip() 												#Actualizamos la ventana

	while True: 														#Ciclo de la ventana activa
		screen.fill((colors.get("white"))) 								#"Coloreamos" a la ventana de color blanco, accediendo por medio de su clave en el diccionario de colores
		for event in pygame.event.get(): 								#En este for se iteran los eventos que suceden en la ventana
			if event.type == pygame.QUIT: 								#Si se presiona la "cruz" de cerrar ventana:
				sys.exit() 												#La ventana se cerrara y terminará el programa

		#DIBUJAR LINEAS
		for node in graph.nodes: 										#Por cada nodo en la lista de nodos del grafo:
			for adj_node_name in graph.links.get(node.name): 			#Por cada nombre de la lista de nodos adyacentes al nodo que estamos iterando:
				for n in graph.nodes: 									#Por cada nodo en la lista de nodos del grafo:
					if adj_node_name == n.name: 						#Si el nombre del nodo adyacente es el mismo que el nombre del nodo que se itera en el último for:
						pygame.draw.aaline(screen, colors.get("black"), node.coordinates, n.coordinates) 	#Dibujamos una línea de color negro desde las coordenadas del centro del primer nodo hasta las coordenadas del centro del nodo en el que estamos iterando

		#DIBUJAR NODOS
		for node in graph.nodes: 										#Por cada nodo en la lista de nodos del grafo
			pygame.draw.circle(screen, colors.get(node.color), node.coordinates, radius) 	#Dibujamos un círculo del color que el nodo tenga en su atributo "color" que pasaremos al diccionario de colores para obtener, con centro en las coordenadas del nodo y con el radio calculado anteriormente

		pygame.display.update() 										#Actualizamos la ventana


#DICCIONARIOS DE PRUEBA
links = {"A":["B", "D"],
		"B":["A", "C", "D", "E"], 
		"C":["B", "E", "F"],
		"D":["A", "B", "E", "G"],
		"E":["B", "C", "D", "F", "G", "H"],
		"F":["C", "E", "H", "I"],
		"G":["D", "E", "H"],
		"H":["E", "F", "G", "I"],
		"I":["F", "H"]}

links2 = {"A":["B"],
		"B":["A", "C"],
		"C":["B"]}

links3 = {"A":["B", "C", "D"],
		"B":["A", "C", "E"],
		"C":["A", "B", "D", "E"],
		"D":["A", "C", "E"],
		"E":["B", "C", "D"]}

links4 = {0:[1], 1:[0], 2:[]}

links5 = {"A":["B", "C"], "B":["A", "C", "D"], "C":["A", "B", "D"], "D":["B", "C"]}

links10 = {"A":["B", "D", "E"],
		"B":["A", "C", "D", "E", "F"], 
		"C":["B", "E", "F"],
		"D":["A", "B", "E", "G", "H"],
		"E":["A", "B", "C", "D", "F", "G", "H", "I"],
		"F":["B", "C", "E", "H", "I"],
		"G":["D", "E", "H"],
		"H":["D", "E", "F", "G", "I"],
		"I":["E", "F", "H"]}

links6 = {0:[1, 3, 4],
		1:[0, 2, 3, 4, 5], 
		2:[1, 4, 5],
		3:[0, 1, 4, 6, 7],
		4:[0, 1, 2, 3, 5, 6, 7, 8],
		5:[1, 2, 4, 7, 8],
		6:[3, 4, 7],
		7:[3, 4, 5, 6, 8],
		8:[4, 5, 7]}

links7 = {0:[]}


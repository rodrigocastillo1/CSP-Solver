#GraphColoring-pygame.py
#Proyecto CSPSolver
#Autor: Castillo Alcántara Rodrigo

import pygame
from pygame.locals import *
import sys
import NQueens

SCREEN_WIDTH = 640 				#Ancho de la ventana en pixeles
SCREEN_HEIGHT = 640 			#Altura de la ventana en pixeles

#Diccionario de colores con sus tuplas RBG para usarlos con facilidad
colors = {"white":(255,255,255), "black":(0,0,0)}

def ChessDrawer(chess): 												#Función para dibujar el ajedrez
	pygame.init() 														#Iniciamos pygame
	screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) 	#Creamos el objeto screen, que será la ventana y que tendrá por medidas a los pixeles que definimos al inicio
	pygame.display.set_caption("Graph Coloring") 						#Escribimos un título adecuado para la ventana
	x_side = int(SCREEN_WIDTH/chess.order) 									#Definimos la longitud del lado vertical de los cuadros para dibujar al tablero
	y_side = int(SCREEN_HEIGHT/chess.order)									#Definimos la longitud del lado horizontal de los cuadros para dibujar al tablero
	queen_image = pygame.image.load("queen.png").convert_alpha() 			#Creación del objeto imagen para la reina, al final se pone"convert_alpha" para indicar un fondo transparente
	queen_image = pygame.transform.smoothscale(queen_image, (int(SCREEN_WIDTH/chess.order), int(SCREEN_HEIGHT/chess.order))) 	#Redimensionado del objeto anterior según el orden del tablero

	pygame.display.flip() 												#Actualizamos la ventana

	while True: 														#Ciclo de la ventana activa
		screen.fill((colors.get("white"))) 								#"Coloreamos" a la ventana de color blanco, accediendo por medio de su clave en el diccionario de colores
		for event in pygame.event.get(): 								#En este for se iteran los eventos que suceden en la ventana
			if event.type == pygame.QUIT: 								#Si se presiona la "cruz" de cerrar ventana:
				sys.exit() 												#La ventana se cerrara y terminará el programa

		#Ciclo para dibujar el tablero
		for x in range(0, chess.order): 								#Iteramos el valor de x entre 0 y el orden del tablero
			for y in range(0, chess.order): 							#Iteramos el valor de y entre 0 y el orden del tablero
				if (x % 2) - (y % 2) == 0: color = "black" 				#Si la resta del residuo de x entre 2 menos el residuo de y menos 2 es igual a cero, asignamos el color negro
				else: color = "white" 									#Sino asignamos el color blanco
				pygame.draw.rect(screen, colors.get(color), [x*(y_side), y*(x_side), y_side, x_side]) 	#Dibujamos el rectángulo según el color, y las coordenadas que vamos iterando en los ciclos, así como el tamaño del lado que estará dado según el orden del tablero

		#Ciclo para colocar a las reinas en la posición que deben estar
		for queen in chess.queens: 										#Por cada reina en la lista de reinas del tablero
			screen.blit(queen_image, (queen.x*x_side, queen.y*y_side)) 	#Insertamos la imagen de la reina en la posición que debe tener, según las coordenadas de la reina

		pygame.display.update() 										#Actualizamos la ventana

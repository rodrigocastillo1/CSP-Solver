#main_CSP_Solver.py
#Proyecto CSPSolver
#Autor: Castillo Alcántara Rodrigo

import csp_Solver
import ChessDrawing_pygame
import GraphColoring_pygame
import sys

argv = sys.argv 	#Le damos el nombre de argv para usarlo con mayor facilidad
def main(): 										#Función principal
	if validations() == False: 				#Se hacen las validaciones necesarias y en caso de que alguna de estas no se cumpla se retorna False
		sys.exit() 									#Lo que nos lleva a dar un mensaje de error y salir del programa
	csp = argv[1] 									#Asignamos el nombre de csp al argumento 1 por simple facilidad en el manejo de nombres
	csp_info = argv[2] 								#Asignamos la información que tenemos del problema
	print("Información introducida con éxto. Generando solución...") 	#Damos un mensaje de que ha sido correcta la información introducida y se comienza a generar la solución
	problem_solved = csp_Solver.CSP_Solver(csp, csp_info) 				#Asignamos la solucion del problema que está dada según el algoritmo de solución de CSP's, a esta se le pasa el problema a resolver y la información inicial
	if csp == "NQueens": 											#Ya con la solución, pasaremos a presentarla gráficamente. Vemos que si el problema es el de la N reinas:
		ChessDrawing_pygame.ChessDrawer(problem_solved) 			#Mandamos a llamar a la función que representa gráficamente a la solución, le damos a esta el problema resuelto
	elif csp == "GraphColoring": 									#Si el problema es el de coloreado de grafos:
		GraphColoring_pygame.GraphDrawer(problem_solved) 			#Llamamos a la función para representar el problema resuelto


def validations(): 											#Función de validaciones
	available_problems = ["NQueens", "GraphColoring"] 		#Damos una lista de problemas disponibles para resolver
	if len(argv) < 3 or len(argv) > 3: 						#Primero validamos que se tengan todos los parámetros necesarios
		print("Exceso o déficit de argumentos. Ingrese: python3 main_CSP_Solver.py \"problema\" \"informacion del problema\" ") #Si no se cumple damos un mensaje
		return False 										#Retornamos False
	csp = argv[1] 											#Sino entonces asignamos a csp el argumento en la posición 1, esto por simple uso de nombres
	if csp not in available_problems: 						#Si el csp no está en la lista de problemas a resolver disponibles:
		return False 										#Retornamos False
	elif csp == "NQueens":									#Si el csp es el de las reinas:
		chessboard_order = int(argv[2]) 					#Asignamos el orden del tablero como el parámetro 2 desde consola
		if chessboard_order <= 0 or chessboard_order > 19 or chessboard_order == 2 or chessboard_order == 3: 	#Si el parámetro es menor a 0 o es mayor a 19 o es 2 o 3 (para los cuales no hay solución):
			print("Cantidad de reinas no permitida. Ingrese un número dentro dentro de [1, 19] excepto 2 y 3. No existe solución para los dos últimos") #Damos un mensaje de error
			return False 									#Retornamos False
	elif csp == "GraphColoring": 							#Si el problema es el del coloreado de grafos:
		file_name = argv[2] 								#Tomamos al nombre del archivo como file_name por simple facilidad en el manejo de variables
		try: 												#Tratamos de abrir y cerrarel archivo
			fich = open(file_name, "r") 					#Abrirlo en modo lectura
			fich.close() 									#Cerrarlo normalmente
		except: 											#Si ocurre algún problema en este proceso entonces:
			print("Archivo no encontrado. Asegurese que el archivo este dentro de la carpeta del programa") 	#Damos un mensaje de error
			return False 									#Retornamos False
	return True 											#Si ninguna de las codiciones anteriores se cumple entonces retornamos True que implicará que todas las validaciones se satisfacieron adecuadamente

main() 			#Mandamos a llamar a la función principal
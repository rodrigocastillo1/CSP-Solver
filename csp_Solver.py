#csp_Solver.py
#Proyecto CSPSolver
#Autor: Castillo Alcántara Rodrigo

import NQueens
import GraphColoring


def CSP_Solver(csp, csp_info): 												#Función envolvente para la función Real_CSP_Solver, determina además el valor de las variables generales para dicha función
	if csp == "NQueens": 													#Si el problema que se está pasando en el de las N reinas:
		environment = NQueens.ChessBoard(int(csp_info)) 					#El "entorno" en el que se desarrolla el problema es el tablero de ajedrez
		obj = NQueens.Queen 												#El objeto general que será ingresado en las listas de solución de problema será uno de la Clase "Queen"
		object_list = environment.queens 									#La lista de objetos será la lista de reinas colocadas del tablero
		domain = range(0, environment.order) 								#El dominio para la solución del problema será una lista de números de 0 hasta el número de reinas que se quiere colocar
		isConsistent = NQueens.ChessBoard.isAvailable 						#El método general con el cual se determinará si una posible solución es válida será el método isAvailable de la clase ChessBoard
	
	elif csp == "GraphColoring": 											#Si el problema que se está pasando es el de coloreado de grafos:
		environment = GraphColoring.Graph(csp_info) 						#El entorno será el grafo, generado según el dato que se proporcionó, en este caso el archivo
		obj = GraphColoring.Node 											#El objeto general que será ingresado en las listas de solución será un nodo de la clase "Node"
		object_list = environment.nodes 									#La lista de objetos será la lista de nodos coloreados del grafo
		domain = environment.chromatic_list 								#El dominio para la solución del problema será la lista de colores generada según el número cromático
		isConsistent = GraphColoring.Graph.isAvailable 						#El método general con el cual se determinará si un nodo es una solución correcta será el método isAvailable de la clase Graph
	
	Real_CSP_Solver(environment, obj, object_list, domain, isConsistent, 0) 	#Con estas asignaciones mandamos mandamos a llamar a la función que resolverá al problema
	return environment 		#Regresamos el entorno ya completado después de las asignaciones de la función anterior

def Real_CSP_Solver(environment, obj, object_list, domain, isConsistent, num): 		#Función Back Track para la solución general de los problemas de coloreado de grafos y n reinas
	if len(object_list) == environment.order: 										#Si el tamaño de la lista de objetos es igual a la cantidad de objetos a asignar entonces está terminada la función
		return True 																#Retornamos True
	for element in domain: 															#Si no se cumple: por cada elemento dentro del dominio para la solución del problema:
		new_object = obj(num, element) 												#Generamos una posible solución con dicho elemento del dominio
		if isConsistent(environment, new_object): 									#Determinamos si dicho elemento es consistente para llegar a la solución del problema
			object_list.append(new_object) 											#Si se cumple que es consistente entonces ingresamos el elemento a la lista de objetos asignados
			if Real_CSP_Solver(environment, obj, object_list, domain, isConsistent, num+1) == False: 	#Hacemos una llamada recursiva de la función enviando como parámetro al siguiente elemento en la lista de posibles soluciones y se realiza todo el proceso anterior nuevamente
				object_list.pop() 													#En caso de que la asignación anterior retorne False entonces no se cumplió que ningun elemento generado con los datos del dominio era viable para una solución por lo tanto retorna False en cuyo caso sacamos al último elemento asignado en la lista de soluciones y regresamos a ese ciclo
			else: return True 														#Sino, entonces retornará True que indica que se ha completado la asignación regresando e ignorando las instrucciones de todas las entradas recursivas anteriores
	return False 																	#En caso de que se haya iterado en todos los elementos del dominio y ningún objeto generado haya cumplido ser un elemento viable para la solución del problema entonces retornamos True que será una bandera para saber cuando sacar al último elemento y continuar generando posibles soluciones



#Se presenta la implementación del mismo algoritmo para cada problema por separado
#Estas fueron las primeras implementaciones, de ahí se logró generalizar a una función: Real_CSP_Solver
"""def nQueens(chessboard, row):									#Función recursiva para encontrar las posiciones de las reinas en el tablero de ajedrez
	if len(chessboard.queens) == chessboard.order:					#Caso base: si el número de reinas en la lista de reinas del tablero es el mismo que el orden del tablero:
		return True													#RetornamosTrue, que servirá para diferenciar de cuando estamos regresando a cambiar la posición de una reina y cuando queremos salir de la función
	for column in range(0, chessboard.order):						#Por cada columna en el tablero, desde 0 hasta n (orden):
		o_pair = Queen(row, column)									#Creamos el par ordenado que será un objeto de la clase "Queen" con las coordenadas el renglón y columna en que estamos
		if ChessBoard.isAvailable(chessboard, o_pair):				#Si el par ordenado que acabamos de crear está disponible (no ocupado ni amenzado) en el tablero:
			chessboard.queens.append(o_pair)						#Metemos el par ordenado creado en la lista de reinas del tablero
			if nQueens(chessboard, row+1) == False:					#Hacemos la llamada recursiva, mandando al siguiente renglón del cual estamos usando para colocar la siguiente reina. Se hace la coomparación para saber si el intento de poner una reina falló o si se completó el acomodo
				chessboard.queens.pop()								#En caso de que haya fallado el acomodo, sacamos a la última reina que estuvo en la lista de reinas. Continuamos con el ciclo for
			else: return True 										#En caso de que se retorne True (debido a que ya se terminaron de colocar las piezas -línea 3 de la función-) se retorna True para regresar de cada llamada a la función sin afectar a las reinas
	return False 													#En caso de que se haya terminado de iterar todas las columnas y no se haya encontrado alguna casilla válida retornamos False, que significa que se debe eliminar la última reina en la lista y regresar a seguir buscando

def graphColoring(graph, node_num):									#Función recursiva para encontrar los colores de los nodos en el grafo
	colors = ["blue", "red", "green"] 								#Lista de colores disponibles para el coloreado
	if len(graph.nodes) == graph.order:								#Caso base: si el número nodos coloreados en la lista de nodos del grafo es el mismo que la cantidad de nodos (orden) del grafo:
		return True													#Retornamos True, que servirá para diferenciar de cuando estamos regresando a cambiar el color de un nodo y cuando queremos salir de la función
	for color in colors:											#Por cada color en la lista de colores:
		new_node = Node(chr(node_num), color)						#Creamos el nodo que será un objeto de la clase "Node" con su nombre (según código ASCII) y el color que se está iterando
		if Graph.isAvailable(graph, new_node):						#Si el nodo que acabamos de crear tiene un color disponible (que ningún nodo adyacente lo tiene (ni Obama)) en el grafo:
			graph.nodes.append(new_node)							#Metemos el nodo creado en la lista de nodos coloreados del grafo
			if graphColoring(graph, node_num+1) == False:			#Hacemos la llamada recursiva, mandando la siguiente letra (en código ASCII) del cual estamos usando para nombrar al siguiente nodo. Se hace la coomparación para saber si el intento de insetar un nuevo nodo falló o si se completó
				graph.nodes.pop()									#En caso de que para ningún color se puede crear un nuevo nodo: sacamos al último nodo que estuvo en la lista de nodos. Continuamos con el ciclo for en el que se quedó iterando
			else: return True 										#En caso de que se retorne True (debido a que ya se colorearon todos los nodos -línea 3 de la función-) se retorna True para regresar de cada llamada a la función sin afectar a la lista de nodos
	return False													#En caso de que se haya terminado de iterar todos los colores y no se haya encontrado ningun color válido retornamos False, que significa que se debe eliminar al último nodo en la lista y regresar a seguir buscando
"""
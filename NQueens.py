#NQueens.py
#Proyecto CSPSolver
#Autor: Castillo Alcántara Rodrigo

class Queen:						#Clase "Reina", se constituye por un par ordenado que es su posición en el tablero.
	def __init__(self, x, y):		#Pasamos como parámetro la posición en x & en y de la reina
		self.x = x					#Inicializamos así a la reina.
		self.y = y


class ChessBoard:								#Clase "Tablero de ajedrez", tiene una lista de las posiciones disponibles del tablero
	def __init__(self, order):					#Pasamos como parámetro el orden del tablero, es decir la cantidad de cuadros que tiene por lado
		self.order = order						#Le damos el orden es decir, el número de cuadros por lado
		self.queens = []						#Esta lista será la lista en las cuales tendrá ubicadas a las reinas

	def isAvailable(self, o_pair):									#Función que indica si una posible posición de reina está dispoible o no
		for queen in self.queens:									#Por cada reina en la lista de reinas del tablero
			if queen.x == o_pair.x or queen.y == o_pair.y:			#Si el par ordenado tiene la misma coordenada en x o y que alguna de las reinas entonces la casilla está en la misma columna o renglón
				return False										#Retornamos False
			if abs(queen.y - o_pair.y) == abs(o_pair.x - queen.x):	#Este pequeño algoritmo determina si el par ordenado se encuentra en la misma diagonal que una reina
				return False										#En caso afirmativo retorna False
		return True													#En caso de que el par ordenado no se encuentre en ninguna de las posiciones no permitidas se retorna True

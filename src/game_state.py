
'''
Game State: clase que guarda el estado del tablero.
'''
class GameState:

    '''
    Función de inicialización de las varialbes.
    - board: guarda las posiciones de cada pieza en el tablero
    - current_player: guarda el jugador que le toca mover en el turno actual
    '''
    def __init__(self):
        self.board = [
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        ]

        self.current_player = 'white'
    
    '''
    Convierte una posición en nomenclatura de ajedrez a posición x, y del tablero
    - pos: posición en nomencaltura de ajedrez (ej. e4)
    - return x, y: coordenadas de la matriz tablero
    '''
    def chess_to_coords(self, pos):
        x = ord(pos[0]) - ord('a')
        y = 8 - int(pos[1])
        return (x, y)

    '''
    Convierte una posición x, y del tablero a nomenclatura de ajedrez
    - x, y: coordenadas del tablero
    - return pos: posición en nomenclatura de ajedrez
    '''
    def coord_to_chess(self, x, y):
        return f"{chr(ord('a') + x)}{8 - y}"
    
    '''
    Aplica un movimiento a la matriz tablero
    - move: movimiento en noomenclatura uci (ej. "e2e4")
    '''
    def update_board(self, origen, destino):
        x1, y1 = origen
        x2, y2 = destino

        self.board[y2][x2] = self.board[y1][x1]
        self.board[y1][x1] = '.'

    '''
    Comprueva si una posición del tablero esta vacía
    - pos: posición en nomenclatura de ajedrez
    - return: booleano que es true si la posición está vacía y false en caso contrario
    '''
    def is_empty(self, x, y):
        return self.board[y][x] == '.'
    
    # Verifica si una coordenada es válida
    def coordenada_valida(self, x, y):
        return 0 <= x < 8 and 0 <= y < 8
    
    # Devuelve los vecinos (arriba, abajo, izq, der)
    def vecinos(self, x, y):
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx, ny = x + dx, y + dy
            if self.coordenada_valida(nx, ny):
                yield nx, ny
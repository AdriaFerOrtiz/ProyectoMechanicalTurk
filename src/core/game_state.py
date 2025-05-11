
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
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
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
    def update_board(self, move):
        from_pos, to_pos = move[:2], move[2:]
        x1, y1 = self.chess_to_coords(from_pos)
        x2, y2 = self.chess_to_coords(to_pos)

        self.board[y2][x2] = self.board[y1][x1]
        self.board[y1][x1] = ' '

    '''
    Comprueva si una posición del tablero esta vacía
    - pos: posición en nomenclatura de ajedrez
    - return: booleano que es true si la posición está vacía y false en caso contrario
    '''
    def is_empty(self, pos):
        x, y = self.chess_to_coords(pos)
        return self.board[y][x] == ' '
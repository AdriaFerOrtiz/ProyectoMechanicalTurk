from game_state import GameState
import time
import requests

'''
Central Module: clase que controla el estado de la partida y se comunica con el resto de módulos.
'''
class CentralModule:

    '''
    Función de inicialización de las varialbes.
    - game_state: objeto de la clase GameState que guarda el estado de la partida en cada iteración
    - ia_endpoint: dirección con la que se comunica el módulo central con el módulo del modelo de IA
    - vision_module: objeto de la clase Vision Module que se encarga del procesado de las imágenes del tablero
    - movement_module: objeto de la clase Movement Module que se encarga de realizar los movimientos del robot
    '''
    def __init__(self):
        self.game_state = GameState()
        self.ia_endpoint = "https://tu-api-ia.com/move"
        #self.vision_module = VisionModule()
        #self.movement_module = MovementModule()

    '''
    Calcula rutas en L (horizontal → vertical o viceversa) que pueda realizar el robot para mover una pieza
    - form_pos: posición inicial de la pieza
    - to_pos: posición final de la pieza
    - return: lista con los caminos en L disponibles
    '''
    def calculate_orthogonal_path(self, from_pos, to_pos):
        from_x, from_y = self.game_state.chess_to_coords(from_pos)
        to_x, to_y = self.game_state.chess_to_coords(to_pos)
        
        # Opción 1: Horizontal → Vertical
        path1 = []
        step_x = 1 if to_x > from_x else -1
        if from_x != to_x:
            for x in range(from_x, to_x + step_x, step_x):
                path1.append((x, from_y))
        step_y = 1 if to_y > from_y else -1
        if from_y != to_y:
            for y in range(from_y, to_y + step_y, step_y):
                path1.append((to_x, y))
        
        # Opción 2: Vertical → Horizontal
        path2 = []
        if from_y != to_y:
            for y in range(from_y, to_y + step_y, step_y):
                path2.append((from_x, y))
        if from_x != to_x:
            for x in range(from_x, to_x + step_x, step_x):
                path2.append((x, to_y))
        
        return [path1, path2]

    '''
    Busca una ruta para realizar el movimiento de la pieza que no tenga obstaculos
    - form_pos: posición inicial de la pieza
    - to_pos: posición final de la pieza
    - return: primer camino encontrado sin obstaculos
    '''
    def find_valid_path(self, from_pos, to_pos):
        possible_paths = self.calculate_orthogonal_path(from_pos, to_pos)
        for path in possible_paths:
            if all(self.game_state.is_empty(self.game_state.coord_to_chess(x, y)) for (x, y) in path[1:]):
                return path
        return None

    '''
    Realiza un movimiento de la partida, gestionando el tablero virtual y movimiento del robot
    - move: movimiento en noomenclatura uci (ej. "e2e4")
    '''
    def execute_robot_move(self, move):
        from_pos, to_pos = move[:2], move[2:]
        path = self.find_valid_path(from_pos, to_pos)

        if path is None:
            blocking_piece_pos = self.find_blocking_piece(from_pos, to_pos)
            safe_pos = self.find_empty_position_nearby(blocking_piece_pos)
            self.game_state.update_board(f"{blocking_piece_pos}{safe_pos}")
            self.movement_module.move_piece(f"{blocking_piece_pos}{safe_pos}")
            time.sleep(1)
            path = self.find_valid_path(from_pos, to_pos)
            self.game_state.update_board(f"{safe_pos}{blocking_piece_pos}")
            self.movement_module.move_piece(f"{safe_pos}{blocking_piece_pos}")

        for i in range(len(path) - 1):
            step_move = f"{self.game_state.coord_to_chess(*path[i])}{self.game_state.coord_to_chess(*path[i+1])}"
            self.movement_module.move_piece(step_move)
        self.game_state.update_board(move)

    '''
    Encuentra la pieza que bloquea el camino
    - form_pos: posición inicial de la pieza
    - to_pos: posición final de la pieza
    - return: devuelve la posición de la pieza que obstaculiza el camino
    '''
    def find_blocking_piece(self, from_pos, to_pos):
        paths = self.calculate_orthogonal_path(from_pos, to_pos)
        for path in paths:
            for (x, y) in path[1:]:
                if not self.game_state.is_empty(self.game_state.coord_to_chess(x, y)):
                    return self.game_state.coord_to_chess(x, y)

    '''
    Busca una casilla vacía en las casillas adyacentes
    - pos: posición en nomencaltura de ajedrez (ej. e4)
    - return: cooredenadas de la casilla vacía
    '''
    def find_empty_position_nearby(self, pos):
        x, y = self.game_state.chess_to_coords(pos)
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < 8 and 0 <= new_y < 8 and self.game_state.is_empty(self.game_state.coord_to_chess(new_x, new_y)):
                return self.game_state.coord_to_chess(new_x, new_y)
        raise Exception("No hay casillas vacías cerca")

    def request_ai_move(self):
        """Solicita un movimiento a la IA."""
        fen = self._board_to_fen()  # Implementa esta función
        response = requests.post(self.ia_endpoint, json={"fen": fen})
        return response.json()["move"]
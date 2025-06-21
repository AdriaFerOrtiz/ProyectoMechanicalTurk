from game_state import GameState
from collections import deque
from motor_control import ejecutar_movimiento_completo

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

    # BFS para encontrar un camino libre de obstáculos (solo en casillas vacías)
    def encontrar_camino_simple(self, origen, destino):
        visitado = set()
        cola = deque()
        cola.append((origen, []))

        while cola:
            (x, y), camino = cola.popleft()
            if (x, y) == destino:
                return camino + [(x, y)]

            if (x, y) in visitado:
                continue
            visitado.add((x, y))

            for nx, ny in self.game_state.vecinos(x, y):
                if self.game_state.is_empty(nx, ny) or (nx, ny) == destino:
                    cola.append(((nx, ny), camino + [(x, y)]))

        return None  # No se encontró camino
    
    def detectar_bloqueadores(self, origen, destino):
        """Detecta qué piezas bloquean el camino directo entre origen y destino"""
        visitado = set()
        cola = deque()
        cola.append((origen, []))

        bloqueadores = set()

        while cola:
            (x, y), camino = cola.popleft()
            if (x, y) == destino:
                return list(bloqueadores)

            if (x, y) in visitado:
                continue
            visitado.add((x, y))

            for nx, ny in self.game_state.vecinos(x, y):
                if not self.game_state.is_empty(nx, ny) and (nx, ny) != destino:
                    bloqueadores.add((nx, ny))
                elif self.game_state.is_empty(nx, ny) or (nx, ny) == destino:
                    cola.append(((nx, ny), camino + [(x, y)]))

        return list(bloqueadores)

    def buscar_casilla_temporal(self, bloqueador, max_depth=2):
        """Busca casillas vacías accesibles desde la posición del bloqueador en 1 o 2 movimientos"""
        visitado = set()
        cola = deque()
        cola.append((bloqueador, []))
        resultados = []

        while cola:
            (x, y), camino = cola.popleft()
            if len(camino) > max_depth:
                continue
            if (x, y) != bloqueador and self.game_state.is_empty(x, y):
                resultados.append((camino + [(x, y)]))

            for nx, ny in self.game_state.vecinos(x, y):
                if (nx, ny) not in visitado and self.game_state.is_empty(nx, ny):
                    visitado.add((nx, ny))
                    cola.append(((nx, ny), camino + [(nx, ny)]))
        return resultados

    
    def mover_temporalmente_y_continuar(self, origen, destino):
        bloqueadores = self.detectar_bloqueadores(origen, destino)

        if not bloqueadores:
            print("No hay bloqueadores directos.")
            return None

        candidatos_validos = []

        for bloqueador in bloqueadores:
            caminos_temporales = self.buscar_casilla_temporal(bloqueador, max_depth=2)

            for camino in caminos_temporales:
                if not camino:
                    continue

                destino_temporal = camino[-1]
                self.game_state.update_board(bloqueador, destino_temporal)

                # Reintentamos encontrar el camino original ahora sin el bloqueador
                camino_principal = self.encontrar_camino_simple(origen, destino)

                # Revertimos
                self.game_state.update_board(destino_temporal, bloqueador)

                camino.pop()
                camino.insert(0, bloqueador)
                if camino_principal:
                    candidatos_validos.append({
                        "bloqueador": bloqueador,
                        "camino_temporal": camino,
                        "camino_principal": camino_principal,
                        "num_movimientos_temporales": len(camino),
                    })

        if not candidatos_validos:
            print("Ningún bloqueador pudo despejar el camino.")
            return None

        # Elegimos el que despeja el camino con menos movimientos temporales
        mejor = min(candidatos_validos, key=lambda x: x["num_movimientos_temporales"])

        return {
            "temporal": mejor["camino_temporal"],
            "principal": mejor["camino_principal"]
        }
    
def movimiento_completo(tablero, origen, destino):
    modulo = CentralModule()
    modulo.game_state.board = tablero
    origen = modulo.game_state.chess_to_coords(origen)
    destino = modulo.game_state.chess_to_coords(destino)

    camino = modulo.encontrar_camino_simple(origen, destino)
    if camino:
        print("Camino encontrado:", camino)
        modulo.game_state.update_board(origen, destino)
        ejecutar_movimiento_completo(camino)
    else:
        resultado = modulo.mover_temporalmente_y_continuar(origen, destino)

        if resultado:
            print("Instrucciones:")
            print("1. Mover bloqueador temporal:", resultado["temporal"])
            print("2. Ejecutar movimiento principal:", resultado["principal"])
            print("3. Volver a dejar la pieza en su lugar.")
            modulo.game_state.update_board(origen, destino)
            ejecutar_movimiento_completo(resultado["principal"], resultado["temporal"])
        else:
            print("No se pudo resolver la obstrucción.")
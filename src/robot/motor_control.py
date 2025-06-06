import time

def generar_instrucciones_movimiento(camino):
    """
    Convierte una lista de coordenadas [(fila, col), ...] en instrucciones 'w', 'a', 's', 'd'
    """

    instrucciones = []
    for i in range(1, len(camino)):
        f1, c1 = camino[i - 1]
        f2, c2 = camino[i]

        if f2 < f1:
            instrucciones.append('w')  # subir
        elif f2 > f1:
            instrucciones.append('s')  # bajar
        elif c2 > c1:
            instrucciones.append('d')  # derecha
        elif c2 < c1:
            instrucciones.append('a')  # izquierda
        else:
            raise ValueError(f"Movimiento inválido de {camino[i-1]} a {camino[i]}")

    return instrucciones

def generar_camino_simple(origen, destino):
    """
    Devuelve una lista de coordenadas que forman un camino simple
    de origen a destino en movimientos rectilíneos (primero vertical, luego horizontal).
    """
    camino = [origen]
    fila_origen, col_origen = origen
    fila_destino, col_destino = destino

    # Movimiento vertical
    paso_f = 1 if fila_destino > fila_origen else -1
    for f in range(fila_origen + paso_f, fila_destino + paso_f, paso_f):
        camino.append((f, col_origen))

    # Movimiento horizontal
    paso_c = 1 if col_destino > col_origen else -1
    for c in range(col_origen + paso_c, col_destino + paso_c, paso_c):
        camino.append((fila_destino, c))

    return camino

def enviar_a_robot(letra):
    # Ejemplo: enviar por puerto serie
    print(f"Enviando al robot: {letra}")

def ejecutar_movimiento_completo(camino_principal, camino_bloqueador=None, origen_robot=(4, 4), delay=0.5):
    """
    Ejecuta uno o dos movimientos encadenados desde una posición de origen.
    - camino_bloqueador: si existe, se mueve primero la pieza que obstruye.
    - camino_principal: movimiento final deseado.
    - origen_robot: casilla base del robot (por defecto e4 = (4, 4))
    """

    # Función auxiliar para enviar los movimientos de un camino
    def mover(camino, comentario=""):
        if not camino or len(camino) < 2:
            print(f"[ERROR] Camino no válido para {comentario}")
            return camino[-1] if camino else None
        instrucciones = generar_instrucciones_movimiento(camino)
        print(f"[DEBUG] Movimiento ({comentario}): {camino}")
        for letra in instrucciones:
            enviar_a_robot(letra)
            time.sleep(delay)
        return camino[-1]

    # 1. Movimiento del bloqueador si existe
    if camino_bloqueador:
        # Mover desde origen a la primera casilla del bloqueador
        camino_hacia_bloqueador = generar_camino_simple(origen_robot, camino_bloqueador[0])
        mover(camino_hacia_bloqueador, "hacia bloqueador")

        # Mover el bloqueador
        pos_final_bloqueador = mover(camino_bloqueador, "bloqueador")

        # 2. Movimiento directo a la pieza principal (sin volver al origen)
        camino_hacia_principal = generar_camino_simple(pos_final_bloqueador, camino_principal[0])
        mover(camino_hacia_principal, "hacia principal")

    else:
        # Si no hay bloqueador, ir desde origen a la pieza principal
        camino_hacia_principal = generar_camino_simple(origen_robot, camino_principal[0])
        mover(camino_hacia_principal, "hacia principal")

    # 3. Mover la pieza principal
    pos_final_principal = mover(camino_principal, "pieza principal")

    # 5. Devolver la pieza bloqueadora a su lugar (si existe)
    if camino_bloqueador:
        # Ir desde el origen al lugar temporal del bloqueador
        camino_ir_bloqueador = generar_camino_simple(pos_final_principal, camino_bloqueador[-1])
        mover(camino_ir_bloqueador, "ir a bloqueador temporal")

        # Volver a su posición original
        camino_revertido = list(reversed(camino_bloqueador))
        mover(camino_revertido, "devolver bloqueador")

        # 4. Volver al origen desde la pieza principal
        camino_regreso = generar_camino_simple(camino_bloqueador[0], origen_robot)
        mover(camino_regreso, "regreso al origen")
    else:
        # 4. Volver al origen desde la pieza principal
        camino_regreso = generar_camino_simple(pos_final_principal, origen_robot)
        mover(camino_regreso, "regreso al origen")

    print("[INFO] Movimiento completo realizado.")

import cv2
import numpy as np

# =============================================================================
# CONFIGURACIÓN
# =============================================================================

GREEN_CORNERS_HSV = [[[35, 50, 50], [85, 255, 255]]]  # Rangos de color verde
MIN_CONTOUR_AREA = 0  # Área mínima para detección de esquinas
MASK = GREEN_CORNERS_HSV

# =============================================================================
# FUNCIONES DE PROCESAMIENTO
# =============================================================================


def preprocess_image(img):
    """Aplica preprocesamiento a la imagen"""
    blurred = cv2.GaussianBlur(img, (7, 7), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    return hsv


def create_mask(hsv_img):
    """Crea máscara para detectar colores verdes"""
    lower_green = np.array(MASK[0][0])
    upper_green = np.array(MASK[0][1])
    
    mask = cv2.inRange(hsv_img, lower_green, upper_green)
    
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (25,25))
    closed_mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    final_mask = cv2.morphologyEx(closed_mask, cv2.MORPH_OPEN, kernel)
    
    return final_mask


def find_corners(img, mask):
    """Encuentra las esquinas verdes en la imagen"""
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    corners = []
    
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > MIN_CONTOUR_AREA:
            perimeter = cv2.arcLength(cnt, True)
            circularity = 4 * np.pi * area / (perimeter**2) if perimeter > 0 else 0
            
            if circularity > 0.65:
                M = cv2.moments(cnt)
                if M["m00"] != 0:
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    corners.append([cX, cY])
    
    return np.array(corners, dtype=np.float32)


def order_corners(corners):
    """Ordena las esquinas en sentido horario"""
    if len(corners) < 4:
        return None
    
    center = np.mean(corners, axis=0)
    ordered = sorted(corners, 
                   key=lambda p: (np.arctan2(p[1]-center[1], p[0]-center[0]) + 2*np.pi) % (2*np.pi))
    return np.array(ordered[:4], dtype=np.float32)


def transform_board(img, corners):
    """Aplica transformación de perspectiva al tablero"""
    side = max(img.shape[:2])
    dst_pts = np.array([[0,0], [side,0], [side,side], [0,side]], dtype=np.float32)
    M = cv2.getPerspectiveTransform(corners, dst_pts)
    warped = cv2.warpPerspective(img, M, (side, side))
    return warped


def crop_board(warped_img, margin_pct=0.05):
    """
    Recorta el área del tablero usando un margen porcentual igual en todos los bordes.
    :param warped_img: Imagen a recortar (numpy array)
    :param margin_pct: Margen a recortar en cada borde (porcentaje, por ejemplo 0.1 para 10%)
    :return: Imagen recortada
    """
    h, w = warped_img.shape[:2]

    # Calcula los píxeles a recortar según el porcentaje
    margin_y = int(h * margin_pct)
    margin_x = int(w * margin_pct)

    # Calcula los límites asegurando que no se salga de la imagen
    y1 = margin_y
    y2 = h - margin_y
    x1 = margin_x
    x2 = w - margin_x

    # Recorta la imagen
    return warped_img[y1:y2, x1:x2]


def divide_board(board_img):
    """Divide el tablero en casillas individuales"""
    h, w = board_img.shape[:2]
    cell_size = h // 8
    cells = []
    board_with_grid = board_img.copy()
    
    for row in range(8):
        for col in range(8):
            y1 = row * cell_size
            y2 = (row + 1) * cell_size
            x1 = col * cell_size
            x2 = (col + 1) * cell_size
            
            cv2.rectangle(board_with_grid, (x1, y1), (x2, y2), (0, 255, 0), 3)
            cell = board_img[y1:y2, x1:x2]
            cells.append(cell)
    
    return board_with_grid, cells


def crop_and_divide_board(img, margin_pct=0.08, debug=False):
    """
    Detecta el tablero, corrige perspectiva, recorta y divide en 64 casillas.
    :param img: Imagen de entrada (numpy array, BGR)
    :param margin_pct: Porcentaje de recorte en cada borde (ej: 0.08 para 8%)
    :param debug: Si True, muestra la primera casilla extraída
    :return: Lista de 64 imágenes (casillas)
    """
    hsv_img = preprocess_image(img)
    mask = create_mask(hsv_img)
    corners = find_corners(img, mask)
    ordered_corners = order_corners(corners)

    if ordered_corners is None:
        raise ValueError("No se detectaron suficientes esquinas verdes (se necesitan 4)")

    warped = transform_board(img, ordered_corners)
    board = crop_board(warped, margin_pct)
    _, cells = divide_board(board)

    return cells


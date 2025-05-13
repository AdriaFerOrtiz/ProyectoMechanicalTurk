import cv2
import numpy as np
import matplotlib.pyplot as plt

# =============================================================================
# CONFIGURACIÓN
# =============================================================================

IMG_NAME = "img/board1.jpeg"  # Nombre de la imagen a procesar
GREEN_CORNERS_HSV = [[[35, 50, 50], [85, 255, 255]]]  # Rangos de color verde
MIN_CONTOUR_AREA = 0  # Área mínima para detección de esquinas
DEBUG_MODE = False  # Activar para mostrar imágenes de debug
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

    if debug:
        plt.imshow(cv2.cvtColor(cells[0], cv2.COLOR_BGR2RGB))
        plt.title('Casilla 0')
        plt.axis('off')
        plt.show()

    return cells

# =============================================================================
# EJECUCIÓN PRINCIPAL
# =============================================================================


# Cargar imagen
if DEBUG_MODE:
    img = cv2.imread(IMG_NAME)
    if img is None:
        print(f"No se pudo cargar la imagen: {IMG_NAME}")
        exit()

    # Procesamiento
    hsv_img = preprocess_image(img)
    MASK = create_mask(hsv_img)

    # Debug: Mostrar imágenes del proceso
    if DEBUG_MODE:
        plt.figure(figsize=(18, 12))
        
        # Imagen original
        plt.subplot(2, 2, 1)
        plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        plt.title('Imagen Original')
        plt.axis('off')
        
        # Imagen HSV
        plt.subplot(2, 2, 2)
        plt.imshow(cv2.cvtColor(hsv_img, cv2.COLOR_HSV2RGB))
        plt.title('Imagen HSV')
        plt.axis('off')
        
        # Máscara verde
        plt.subplot(2, 2, 3)
        plt.imshow(MASK, cmap='gray')
        plt.title('Máscara Verde')
        plt.axis('off')
        
        # Máscara aplicada a imagen original
        masked_img = cv2.bitwise_and(img, img, mask=MASK)
        plt.subplot(2, 2, 4)
        plt.imshow(cv2.cvtColor(masked_img, cv2.COLOR_BGR2RGB))
        plt.title('Imagen con Máscara Verde Aplicada')
        plt.axis('off')
        
        plt.tight_layout()
        plt.show()

    # Continuar con el procesamiento
    corners = find_corners(img, MASK)
    ordered_corners = order_corners(corners)

    if ordered_corners is None:
        print("No se detectaron suficientes esquinas verdes (se necesitan 4)")
        exit()

    # Dibujar esquinas detectadas
    img_with_corners = img.copy()
    for (x, y) in ordered_corners.astype(int):
        cv2.circle(img_with_corners, (x, y), 20, (0, 255, 0), -1)

    # Transformar y dividir tablero
    warped = transform_board(img, ordered_corners)
    board = crop_board(warped)
    board_with_grid, cells = divide_board(board)
    ""
    # Visualización final
    plt.figure(figsize=(18, 8))

    plt.subplot(1, 2, 1)
    plt.imshow(cv2.cvtColor(img_with_corners, cv2.COLOR_BGR2RGB))
    plt.title('Esquinas Verdes Detectadas')
    plt.axis('off')

    plt.subplot(1, 2, 2)
    plt.imshow(cv2.cvtColor(board_with_grid, cv2.COLOR_BGR2RGB))
    plt.title('Tablero Dividido')
    plt.axis('off')

    plt.tight_layout()
    plt.show()

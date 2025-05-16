import cv2
import numpy as np
import matplotlib.pyplot as plt

def apply_filters(cell):
    # Redimensiona la imagen si lo necesitas (por ejemplo, 64x64)
    cell = cv2.resize(cell, (64, 64))
    # Filtro: escala de grises
    gray = cv2.cvtColor(cell, cv2.COLOR_BGR2GRAY)
    # Filtro: binarización adaptativa
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY, 11, 2)
    # Filtro: gradiente Sobel
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    sobel = cv2.magnitude(sobelx, sobely)
    sobel = np.uint8(np.clip(sobel, 0, 255))
    # Filtro: Canny
    canny = cv2.Canny(gray, 100, 200)
    # Filtro: canal V de HSV
    hsv = cv2.cvtColor(cell, cv2.COLOR_BGR2HSV)
    v = hsv[:, :, 2]
    # Stack de canales (puedes elegir los que quieras)
    filtered = np.stack([gray, thresh, sobel, canny, v], axis=-1)
    return filtered

def augment_filters(cell):
    # Redimensiona la imagen si lo necesitas (por ejemplo, 64x64)
    cell = cv2.resize(cell, (64, 64))
    augmented = []
    # Imagen original
    augmented.append(cell)
    # Escala de grises
    gray = cv2.cvtColor(cell, cv2.COLOR_BGR2GRAY)
    gray = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)  # Para mantener 3 canales
    augmented.append(gray)
    # Binarización
    thresh = cv2.adaptiveThreshold(cv2.cvtColor(cell, cv2.COLOR_BGR2GRAY), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY, 11, 2)
    thresh = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
    augmented.append(thresh)
    # Sobel
    sobelx = cv2.Sobel(cv2.cvtColor(cell, cv2.COLOR_BGR2GRAY), cv2.CV_64F, 1, 0, ksize=3)
    sobely = cv2.Sobel(cv2.cvtColor(cell, cv2.COLOR_BGR2GRAY), cv2.CV_64F, 0, 1, ksize=3)
    sobel = cv2.magnitude(sobelx, sobely)
    sobel = np.uint8(np.clip(sobel, 0, 255))
    sobel = cv2.cvtColor(sobel, cv2.COLOR_GRAY2BGR)
    augmented.append(sobel)
    # Canny
    canny = cv2.Canny(cv2.cvtColor(cell, cv2.COLOR_BGR2GRAY), 100, 200)
    canny = cv2.cvtColor(canny, cv2.COLOR_GRAY2BGR)
    augmented.append(canny)
    augmented = np.array(augmented)
    return augmented

def all_filters_and_rotations(cell):
    """
    Aplica varios filtros a la imagen y, para cada filtro, añade también
    las versiones rotadas (90°, 180°, 270°) y sus versiones volteadas horizontalmente (flip).
    Devuelve una lista de imágenes (todas en RGB, 64x64x3).
    """
    cell = cv2.resize(cell, (64, 64))
    filtered = []

    # Siempre convierte a RGB para compatibilidad con Keras
    cell_rgb = cv2.cvtColor(cell, cv2.COLOR_BGR2RGB)
    filtered.append(cell_rgb)

    # Escala de grises (convertida a 3 canales RGB)
    gray = cv2.cvtColor(cell, cv2.COLOR_BGR2GRAY)
    gray_rgb = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)
    filtered.append(gray_rgb)

    # Binarización (convertida a 3 canales RGB)
    thresh = cv2.adaptiveThreshold(
        cv2.cvtColor(cell, cv2.COLOR_BGR2GRAY), 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
    )
    thresh_rgb = cv2.cvtColor(thresh, cv2.COLOR_GRAY2RGB)
    filtered.append(thresh_rgb)

    # Sobel (convertida a 3 canales RGB)
    sobelx = cv2.Sobel(cv2.cvtColor(cell, cv2.COLOR_BGR2GRAY), cv2.CV_64F, 1, 0, ksize=3)
    sobely = cv2.Sobel(cv2.cvtColor(cell, cv2.COLOR_BGR2GRAY), cv2.CV_64F, 0, 1, ksize=3)
    sobel = cv2.magnitude(sobelx, sobely)
    sobel = np.uint8(np.clip(sobel, 0, 255))
    sobel_rgb = cv2.cvtColor(sobel, cv2.COLOR_GRAY2RGB)
    filtered.append(sobel_rgb)

    # Canny (convertida a 3 canales RGB)
    canny = cv2.Canny(cv2.cvtColor(cell, cv2.COLOR_BGR2GRAY), 100, 200)
    canny_rgb = cv2.cvtColor(canny, cv2.COLOR_GRAY2RGB)
    filtered.append(canny_rgb)

    # Para cada imagen filtrada, genera las rotaciones y sus flips
    augmented = []
    for img in filtered:
        # Rotaciones
        rotations = [
            img,
            cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE),
            cv2.rotate(img, cv2.ROTATE_180),
            cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
        ]
        for rot in rotations:
            augmented.append(rot)  # original rotada
            flipped = cv2.flip(rot, 1)  # flip horizontal
            augmented.append(flipped)

    return augmented  # Lista de imágenes (cada una 64x64x3 RGB)
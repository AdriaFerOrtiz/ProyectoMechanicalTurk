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

import cv2
import numpy as np
import random

def get_basic_filters(cell):
    # Filtros básicos (RGB, gris, binarización, sobel, canny)
    cell_rgb = cv2.cvtColor(cell, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(cell, cv2.COLOR_BGR2GRAY)
    gray_rgb = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY, 11, 2)
    thresh_rgb = cv2.cvtColor(thresh, cv2.COLOR_GRAY2RGB)
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    sobel = cv2.magnitude(sobelx, sobely)
    sobel = np.uint8(np.clip(sobel, 0, 255))
    sobel_rgb = cv2.cvtColor(sobel, cv2.COLOR_GRAY2RGB)
    canny = cv2.Canny(gray, 100, 200)
    canny_rgb = cv2.cvtColor(canny, cv2.COLOR_GRAY2RGB)
    return [cell_rgb, gray_rgb, thresh_rgb, sobel_rgb, canny_rgb]

def get_rotations_and_flips(img):
    # Rotaciones y flips
    rotations = [
        img,
        cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE),
        cv2.rotate(img, cv2.ROTATE_180),
        cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    ]
    augmented = []
    for rot in rotations:
        augmented.append(rot)
        augmented.append(cv2.flip(rot, 1))  # flip horizontal
    return augmented

def apply_all_augmentations(cell):
    # Tamaño estándar
    cell = cv2.resize(cell, (64, 64))
    all_augmented = []

    # Filtros básicos
    filtered = get_basic_filters(cell)

    # Parámetros para traslaciones, zoom, shear y rotaciones pequeñas
    translations = [(-5,0), (5,0), (0,-5), (0,5), (0,0)]  # izquierda, derecha, arriba, abajo, sin mover
    zooms = [0.9, 1.0, 1.1]  # zoom-out, original, zoom-in
    shears = [-10, 0, 10]    # cizalladura en grados
    small_rotations = [-5, 0, 5]  # pequeñas rotaciones

    # Para cada filtro básico
    for fimg in filtered:
        # Rotaciones y flips
        for rimg in get_rotations_and_flips(fimg):
            # Traslaciones
            for tx, ty in translations:
                M = np.float32([[1, 0, tx], [0, 1, ty]])
                timg = cv2.warpAffine(rimg, M, (64, 64), borderMode=cv2.BORDER_REFLECT)
                # Zooms
                for zoom in zooms:
                    if zoom == 1.0:
                        zimg = timg.copy()
                    else:
                        h, w = timg.shape[:2]
                        new_h, new_w = int(h * zoom), int(w * zoom)
                        zimg = cv2.resize(timg, (new_w, new_h))
                        if zoom < 1:
                            pad_h = (h - new_h) // 2
                            pad_w = (w - new_w) // 2
                            zimg = cv2.copyMakeBorder(zimg, pad_h, h - new_h - pad_h, pad_w, w - new_w - pad_w, cv2.BORDER_REFLECT)
                        else:
                            crop_h = (new_h - h) // 2
                            crop_w = (new_w - w) // 2
                            zimg = zimg[crop_h:crop_h + h, crop_w:crop_w + w]
                    # Shear
                    for shear in shears:
                        M_shear = np.float32([[1, np.tan(np.radians(shear)), 0], [0, 1, 0]])
                        s_img = cv2.warpAffine(zimg, M_shear, (64, 64), borderMode=cv2.BORDER_REFLECT)
                        # Pequeñas rotaciones
                        for angle in small_rotations:
                            if angle == 0:
                                rot_img = s_img.copy()
                            else:
                                M_rot = cv2.getRotationMatrix2D((32, 32), angle, 1)
                                rot_img = cv2.warpAffine(s_img, M_rot, (64, 64), borderMode=cv2.BORDER_REFLECT)
                            # Fotométricas y efectos
                            # Brillo
                            hsv = cv2.cvtColor(rot_img, cv2.COLOR_RGB2HSV)
                            for bright in [0.8, 1.0, 1.2]:
                                hsv_b = hsv.copy()
                                hsv_b[:,:,2] = np.clip(hsv_b[:,:,2] * bright, 0, 255)
                                bright_img = cv2.cvtColor(hsv_b, cv2.COLOR_HSV2RGB)
                                # Contraste
                                for contrast in [0.8, 1.0, 1.2]:
                                    c_img = np.clip((bright_img - 128) * contrast + 128, 0, 255).astype(np.uint8)
                                    # Saturación
                                    hsv_c = cv2.cvtColor(c_img, cv2.COLOR_RGB2HSV)
                                    for sat in [0.8, 1.0, 1.2]:
                                        hsv_c2 = hsv_c.copy()
                                        hsv_c2[:,:,1] = np.clip(hsv_c2[:,:,1] * sat, 0, 255)
                                        sat_img = cv2.cvtColor(hsv_c2, cv2.COLOR_HSV2RGB)
                                        # Blur y ruido
                                        blur_img = cv2.GaussianBlur(sat_img, (3,3), 0)
                                        noise = np.random.normal(0, 10, blur_img.shape).astype(np.uint8)
                                        noisy_img = cv2.add(blur_img, noise)
                                        # Oclusión (random erasing)
                                        occ_img = noisy_img.copy()
                                        if random.random() < 0.3:
                                            h, w, _ = occ_img.shape
                                            se = np.random.uniform(0.02, 0.1) * h * w
                                            re = np.random.uniform(0.3, 3.3)
                                            he = int(np.sqrt(se * re))
                                            we = int(np.sqrt(se / re))
                                            if he < h and we < w:
                                                xe = np.random.randint(0, w - we)
                                                ye = np.random.randint(0, h - he)
                                                occ_img[ye:ye+he, xe:xe+we, :] = np.random.randint(0, 255, (he, we, 3))
                                        # Sombra artificial
                                        shadow_img = occ_img.copy()
                                        if random.random() < 0.2:
                                            h, w = shadow_img.shape[:2]
                                            top_x, bot_x = np.random.randint(0, w, 2)
                                            shadow_mask = np.zeros_like(shadow_img[:,:,0])
                                            X_m = np.mgrid[0:h, 0:w][1]
                                            shadow_mask[((X_m - top_x) * (bot_x - top_x) >= 0)] = 1
                                            alpha = np.random.uniform(0.5, 0.85)
                                            shadow_img[shadow_mask == 1] = (shadow_img[shadow_mask == 1] * alpha).astype(np.uint8)
                                        all_augmented.append(shadow_img)
    return all_augmented

# --- AUMENTOS EXTRA (opcional) ---

def augment_image(img):
    """
    Aplica una transformación aleatoria (traslación, zoom, brillo, contraste, ruido, blur) a la imagen.
    """
    img_aug = img.copy()
    h, w = img.shape[:2]

    # Traslación aleatoria
    if random.random() < 0.3:
        tx, ty = random.randint(-5, 5), random.randint(-5, 5)
        M = np.float32([[1, 0, tx], [0, 1, ty]])
        img_aug = cv2.warpAffine(img_aug, M, (w, h), borderMode=cv2.BORDER_REFLECT)

    # Zoom aleatorio
    if random.random() < 0.3:
        scale = random.uniform(0.9, 1.1)
        new_size = int(64 * scale)
        img_zoom = cv2.resize(img_aug, (new_size, new_size))
        if scale < 1.0:
            pad = (64 - new_size) // 2
            img_aug = cv2.copyMakeBorder(img_zoom, pad, 64-new_size-pad, pad, 64-new_size-pad, cv2.BORDER_REFLECT)
        else:
            crop = (new_size - 64) // 2
            img_aug = img_zoom[crop:crop+64, crop:crop+64]

    # Brillo y contraste aleatorio
    if random.random() < 0.3:
        alpha = random.uniform(0.8, 1.2)  # contraste
        beta = random.randint(-20, 20)    # brillo
        img_aug = cv2.convertScaleAbs(img_aug, alpha=alpha, beta=beta)

    # Ruido gaussiano
    if random.random() < 0.2:
        noise = np.random.normal(0, 10, img_aug.shape).astype(np.uint8)
        img_aug = cv2.add(img_aug, noise)

    # Blur
    if random.random() < 0.2:
        img_aug = cv2.GaussianBlur(img_aug, (3,3), 0)

    return img_aug

def all_filters_rotations_and_augmentation(cell, extra_per_base=2):
    """
    Devuelve las 40 imágenes base (filtros+rotaciones+flip) y, para cada una,
    un pequeño número de aumentos extra (por defecto 2).
    """
    base_imgs = all_filters_and_rotations(cell)
    augmented = base_imgs.copy()
    for img in base_imgs:
        for _ in range(extra_per_base):
            augmented.append(augment_image(img))
    return augmented
import numpy as np
from crop_board import crop_and_divide_board
from aply_filters import apply_filters, augment_filters, all_filters_and_rotations

def predict_board_position(img, model, margin_pct=0.05):
    """
    Dada una imagen de un tablero, devuelve la posición predicha (lista de 64 etiquetas).
    :param img: imagen del tablero (BGR)
    :param model: modelo CNN entrenado
    :param margin_pct: margen para recorte de tablero
    :return: lista de 64 etiquetas predichas
    """
    # 1. Divide la imagen en 64 casillas
    cells = crop_and_divide_board(img, margin_pct=margin_pct, debug=False)
    
    # 2. Aplica los mismos filtros/preprocesado que en el entrenamiento
    X_pred = [apply_filters(cell) for cell in cells]
    X_pred = np.array(X_pred) / 255.0  # Normaliza igual que en el entrenamiento
    
    # 3. Predice las clases
    preds = model.predict(X_pred)
    class_indices = np.argmax(preds, axis=1)
    
    # 4. Decodifica los índices a etiquetas de piezas
    idx_to_piece = {
        0: '.', 1: 'P', 2: 'N', 3: 'B', 4: 'R', 5: 'Q', 6: 'K',
        7: 'p', 8: 'n', 9: 'b', 10: 'r', 11: 'q', 12: 'k'
    }
    predicted_labels = [idx_to_piece[idx] for idx in class_indices]
    
    return predicted_labels

import numpy as np
from crop_board import crop_and_divide_board
from aply_filters import apply_filters, augment_filters

def predict_board_position_tta(img, model, margin_pct=0.05):
    """
    Predice la posición del tablero usando test-time augmentation (TTA).
    Para cada celda genera varias versiones aumentadas, promedia las predicciones
    y elige la clase más probable.
    """
    # 1. Divide la imagen en 64 casillas
    cells = crop_and_divide_board(img, margin_pct=margin_pct, debug=False)

    all_preds = []
    for cell in cells:
        # Genera versiones aumentadas (incluye la original)
        augmented_cells = augment_filters(cell)
        # Preprocesa y normaliza
        aug_X = np.array([apply_filters(aug_cell) for aug_cell in augmented_cells]) / 255.0
        # Predice para cada augmentación
        preds = model.predict(aug_X, verbose=0)  # (n_aug, n_classes)
        # Promedia las predicciones
        mean_pred = np.mean(preds, axis=0)  # (n_classes,)
        all_preds.append(mean_pred)

    all_preds = np.array(all_preds)  # (64, n_classes)
    class_indices = np.argmax(all_preds, axis=1)

    idx_to_piece = {
        0: '.', 1: 'P', 2: 'N', 3: 'B', 4: 'R', 5: 'Q', 6: 'K',
        7: 'p', 8: 'n', 9: 'b', 10: 'r', 11: 'q', 12: 'k'
    }
    predicted_labels = [idx_to_piece[idx] for idx in class_indices]
    return predicted_labels


def predict_board_position_all_filters_rotations(img, model, margin_pct=0.05):
    """
    Predice la posición del tablero usando test-time augmentation (TTA) consistente con el entrenamiento
    con all_filters_and_rotations: para cada celda, aplica todos los filtros y rotaciones,
    promedia las predicciones y elige la clase más probable.
    """
    # 1. Divide la imagen en 64 casillas
    cells = crop_and_divide_board(img, margin_pct=margin_pct, debug=False)

    all_preds = []
    for cell in cells:
        # Genera todas las versiones aumentadas (filtros + rotaciones)
        augmented_cells = all_filters_and_rotations(cell)  # Lista de imágenes (N, 64, 64, 3)
        # Preprocesa y normaliza (si apply_filters es necesario, si no, puedes omitirlo)
        aug_X = np.array([aug_cell for aug_cell in augmented_cells]) / 255.0
        # Predice para cada augmentación
        preds = model.predict(aug_X, verbose=0)  # (N, n_classes)
        # Promedia las predicciones
        mean_pred = np.mean(preds, axis=0)  # (n_classes,)
        all_preds.append(mean_pred)

    all_preds = np.array(all_preds)  # (64, n_classes)
    class_indices = np.argmax(all_preds, axis=1)

    idx_to_piece = {
        0: '.', 1: 'P', 2: 'N', 3: 'B', 4: 'R', 5: 'Q', 6: 'K',
        7: 'p', 8: 'n', 9: 'b', 10: 'r', 11: 'q', 12: 'k'
    }
    predicted_labels = [idx_to_piece[idx] for idx in class_indices]
    return predicted_labels
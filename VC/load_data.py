from aply_filters import apply_filters, augment_filters, all_filters_and_rotations, apply_all_augmentations, all_filters_rotations_and_augmentation
import os
import cv2
from crop_board import crop_and_divide_board
import numpy as np

def load_dataset(dataset_folder, margin_pct=0.05):
    """
    Carga imágenes de tableros y sus etiquetas desde una carpeta.
    Devuelve dos listas: imágenes de casillas y etiquetas.
    """
    X = []  # Imágenes de casillas
    y = []  # Etiquetas (ground truth)
    
    for fname in os.listdir(dataset_folder):
        if fname.endswith('.jpeg') or fname.endswith('.png'):
            img_path = os.path.join(dataset_folder, fname)
            txt_path = img_path.rsplit('.', 1)[0] + '.txt'
            
            if not os.path.exists(txt_path):
                print(f"Ground truth no encontrado para {img_path}")
                continue

            # Carga imagen y divide en casillas
            img = cv2.imread(img_path)
            if img is None:
                print(f"No se pudo leer {img_path}")
                continue
            cells = crop_and_divide_board(img, margin_pct=margin_pct, debug=False)
            
            # Carga etiquetas
            with open(txt_path, 'r') as f:
                labels = f.read().strip().split()
                if len(labels) != 64:
                    print(f"Ground truth incorrecto en {txt_path}")
                    continue

            # Añade cada casilla y su etiqueta
            for cell, label in zip(cells, labels):
                X.append(cell)
                y.append(label)
    
    return X, y


def load_dataset_with_filters(dataset_folder, margin_pct=0.05):
    X = []
    y = []
    for fname in os.listdir(dataset_folder):
        if fname.endswith('.jpeg') or fname.endswith('.png'):
            img_path = os.path.join(dataset_folder, fname)
            txt_path = img_path.rsplit('.', 1)[0] + '.txt'
            if not os.path.exists(txt_path):
                continue
            img = cv2.imread(img_path)
            if img is None:
                continue
            cells = crop_and_divide_board(img, margin_pct=margin_pct, debug=False)
            with open(txt_path, 'r') as f:
                labels = f.read().strip().split()
                if len(labels) != 64:
                    continue
            for cell, label in zip(cells, labels):
                filtered = apply_filters(cell)
                X.append(filtered)
                y.append(label)
    return np.array(X), np.array(y)


def load_augmented_dataset(dataset_folder, margin_pct=0.05):
    X = []
    y = []
    for fname in os.listdir(dataset_folder):
        if fname.endswith('.jpeg') or fname.endswith('.png'):
            img_path = os.path.join(dataset_folder, fname)
            txt_path = img_path.rsplit('.', 1)[0] + '.txt'
            if not os.path.exists(txt_path):
                continue
            img = cv2.imread(img_path)
            if img is None:
                continue
            cells = crop_and_divide_board(img, margin_pct=margin_pct, debug=False)
            with open(txt_path, 'r') as f:
                labels = f.read().strip().split()
                if len(labels) != 64:
                    continue
            for cell, label in zip(cells, labels):
                augmented_cells = augment_filters(cell)
                for aug_cell in augmented_cells:
                    X.append(aug_cell)
                    y.append(label)
    return np.array(X), np.array(y)


def load_dataset_with_all_filters_and_rotations(dataset_folder, margin_pct=0.05):
    """
    Carga imágenes de tableros y sus etiquetas desde una carpeta.
    Para cada celda, aplica todos los filtros y rotaciones definidos en all_filters_and_rotations.
    Devuelve dos arrays: imágenes aumentadas y etiquetas correspondientes.
    """
    X = []  # Imágenes aumentadas de casillas
    y = []  # Etiquetas (ground truth)

    for fname in os.listdir(dataset_folder):
        if fname.endswith('.jpeg') or fname.endswith('.png'):
            img_path = os.path.join(dataset_folder, fname)
            txt_path = img_path.rsplit('.', 1)[0] + '.txt'
            if not os.path.exists(txt_path):
                print(f"Ground truth no encontrado para {img_path}")
                continue

            # Carga imagen y divide en casillas
            img = cv2.imread(img_path)
            if img is None:
                print(f"No se pudo leer {img_path}")
                continue
            cells = crop_and_divide_board(img, margin_pct=margin_pct, debug=False)

            # Carga etiquetas
            with open(txt_path, 'r') as f:
                labels = f.read().strip().split()
                if len(labels) != 64:
                    print(f"Ground truth incorrecto en {txt_path}")
                    continue

            # Aplica filtros y rotaciones a cada celda
            for cell, label in zip(cells, labels):
                augmented_cells = all_filters_and_rotations(cell)
                for aug_cell in augmented_cells:
                    X.append(aug_cell)
                    y.append(label)
    return np.array(X), np.array(y)

def load_fully_augmented_dataset(dataset_folder, margin_pct=0.05):
    """
    Carga imágenes de tableros y sus etiquetas desde una carpeta.
    Para cada celda, aplica todos los filtros y augmentaciones definidos en apply_all_augmentations.
    Devuelve dos arrays: imágenes aumentadas y etiquetas correspondientes.
    """
    X = []  # Imágenes aumentadas de casillas
    y = []  # Etiquetas (ground truth)

    for fname in os.listdir(dataset_folder):
        if fname.endswith('.jpeg') or fname.endswith('.png'):
            img_path = os.path.join(dataset_folder, fname)
            txt_path = img_path.rsplit('.', 1)[0] + '.txt'
            if not os.path.exists(txt_path):
                print(f"Ground truth no encontrado para {img_path}")
                continue

            # Carga imagen y divide en casillas
            img = cv2.imread(img_path)
            if img is None:
                print(f"No se pudo leer {img_path}")
                continue
            cells = crop_and_divide_board(img, margin_pct=margin_pct, debug=False)

            # Carga etiquetas
            with open(txt_path, 'r') as f:
                labels = f.read().strip().split()
                if len(labels) != 64:
                    print(f"Ground truth incorrecto en {txt_path}")
                    continue

            # Aplica augmentación exhaustiva a cada celda
            for cell, label in zip(cells, labels):
                augmented_cells = apply_all_augmentations(cell)
                for aug_cell in augmented_cells:
                    X.append(aug_cell)
                    y.append(label)
    return np.array(X), np.array(y)

def load_augmented_dataset(dataset_folder, margin_pct=0.05, extra_per_base=2):
    """
    Carga imágenes de tableros y sus etiquetas desde una carpeta.
    Para cada celda, aplica los filtros y augmentaciones definidos en all_filters_rotations_and_augmentation.
    Devuelve dos arrays: imágenes aumentadas y etiquetas correspondientes.
    """
    X = []
    y = []

    for fname in os.listdir(dataset_folder):
        if fname.endswith('.jpeg') or fname.endswith('.png'):
            img_path = os.path.join(dataset_folder, fname)
            txt_path = img_path.rsplit('.', 1)[0] + '.txt'
            if not os.path.exists(txt_path):
                print(f"Ground truth no encontrado para {img_path}")
                continue

            img = cv2.imread(img_path)
            if img is None:
                print(f"No se pudo leer {img_path}")
                continue

            cells = crop_and_divide_board(img, margin_pct=margin_pct, debug=False)

            with open(txt_path, 'r') as f:
                labels = f.read().strip().split()
                if len(labels) != 64:
                    print(f"Ground truth incorrecto en {txt_path}")
                    continue

            for cell, label in zip(cells, labels):
                augmented_cells = all_filters_rotations_and_augmentation(cell, extra_per_base=extra_per_base)
                for aug_cell in augmented_cells:
                    X.append(aug_cell)
                    y.append(label)
    return np.array(X), np.array(y)
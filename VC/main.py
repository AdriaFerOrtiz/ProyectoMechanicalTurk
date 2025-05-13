import cv2
import numpy as np
from tensorflow.keras.models import load_model
import matplotlib.pyplot as plt

# Importa tus funciones de predicción
from prediction import (
    predict_board_position,
    predict_board_position_tta,
    predict_board_position_all_filters_rotations
)

def predict_and_print_board(img_path, model_path, predict_func, margin_pct=0.05, show_img=False, print_board=True):
    """
    Carga el modelo y la imagen, predice el tablero y, opcionalmente, lo imprime por pantalla.
    
    Args:
        img_path (str): Ruta de la imagen del tablero.
        model_path (str): Ruta del modelo Keras.
        predict_func (callable): Función de predicción a usar.
        margin_pct (float): Margen para recorte del tablero.
        show_img (bool): Si True, muestra la imagen original.
        print_board (bool): Si True, imprime el tablero predicho.
    
    Returns:
        list: Lista de 64 etiquetas predichas.
    """
    # Cargar modelo
    model = load_model(model_path)
    
    # Cargar imagen
    img = cv2.imread(img_path)
    if img is None:
        raise ValueError(f"No se pudo cargar la imagen: {img_path}")
    
    # Mostrar imagen si se solicita
    if show_img:
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        plt.imshow(img_rgb)
        plt.axis('off')
        plt.title("Imagen de entrada")
        plt.show()
    
    # Predecir
    predicted_labels = predict_func(img, model, margin_pct=margin_pct)
    
    # Imprimir tablero si se solicita
    if print_board:
        print("\nTablero predicho:")
        for i in range(8):
            print(' '.join(predicted_labels[i*8:(i+1)*8]))
    
    return predicted_labels

# Ejemplo de uso:
if __name__ == "__main__":
    img_path = "img/board1.jpeg"
    model_path = "my_model_28160.h5"
    predicted_labels = predict_and_print_board(
        img_path,
        model_path,
        predict_board_position_all_filters_rotations,  # Cambia aquí la función si quieres otro método
        margin_pct=0.05,
        show_img=True,    # Cambia a False si no quieres mostrar la imagen
        print_board=True  # Cambia a False si no quieres imprimir el tablero
    )

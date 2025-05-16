import argparse
import numpy as np
from tensorflow.keras import layers, models
from sklearn.model_selection import train_test_split
from load_data import load_augmented_dataset, load_dataset_with_filters, load_dataset, load_dataset_with_all_filters_and_rotations

import tensorflow as tf

# Para guardar el modelo en Cloud Storage
def save_model_to_gcs(model, gcs_path):
    # Si la ruta es gs://..., usa tf.keras.models.save_model directamente
    model.save(gcs_path)

piece_to_idx = {
    '.': 0, 'P': 1, 'N': 2, 'B': 3, 'R': 4, 'Q': 5, 'K': 6,
    'p': 7, 'n': 8, 'b': 9, 'r': 10, 'q': 11, 'k': 12
}

def encode_labels(y):
    return np.array([piece_to_idx[label] for label in y])

def main(data_path, model_output_path):
    # Carga los datos (puede ser una ruta local o gs://)
    X, y = load_dataset_with_all_filters_and_rotations(data_path, margin_pct=0.05)
    print(f"Total de imágenes aumentadas: {len(X)}")
    y_enc = encode_labels(y)
    X = X / 255.0

    X_train, X_test, y_train, y_test = train_test_split(X, y_enc, test_size=0.2, random_state=42)

    model = models.Sequential([
        layers.Conv2D(32, (3,3), activation='relu', input_shape=X_train.shape[1:]),
        layers.MaxPooling2D((2,2)),
        layers.Conv2D(64, (3,3), activation='relu'),
        layers.MaxPooling2D((2,2)),
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dense(13, activation='softmax')  # 13 clases
    ])

    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    model.fit(X_train, y_train, epochs=10, validation_data=(X_test, y_test))

    # Guarda el modelo en Cloud Storage o localmente
    save_model_to_gcs(model, model_output_path)
    print(f"Modelo guardado en: {model_output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_path', type=str, required=True, help='Ruta a la carpeta de imágenes (puede ser gs://...)')
    parser.add_argument('--model_output_path', type=str, required=True, help='Ruta de salida del modelo (puede ser gs://...)')
    args = parser.parse_args()

    main(args.data_path, args.model_output_path)

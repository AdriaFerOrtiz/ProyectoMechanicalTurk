import os
import tempfile
import cv2
import numpy as np
from tensorflow.keras.models import load_model
from flask import jsonify
from prediction import predict_board_position_all_filters_rotations

MODEL_PATH = 'my_model.h5'
model = None

def get_model():
    global model
    if model is None:
        model = load_model(MODEL_PATH)
    return model

def parse_image(request):
    if 'file' not in request.files:
        return None, "No file part"
    file = request.files['file']
    if file.filename == '':
        return None, "No selected file"
    temp = tempfile.NamedTemporaryFile(delete=False)
    file.save(temp.name)
    img = cv2.imread(temp.name)
    os.unlink(temp.name)
    if img is None:
        return None, "Cannot read image"
    return img, None

def predict_chessboard(request):
    # --- CORS preflight ---
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }
        return ('', 204, headers)
    # --- Fin CORS preflight ---

    if request.method != 'POST':
        headers = {'Access-Control-Allow-Origin': '*'}
        return jsonify({'error': 'Use POST'}), 405, headers

    img, error = parse_image(request)
    if error:
        headers = {'Access-Control-Allow-Origin': '*'}
        return jsonify({'error': error}), 400, headers

    model = get_model()
    labels = predict_board_position_all_filters_rotations(img, model, margin_pct=0.05)
    board = [labels[i*8:(i+1)*8] for i in range(8)]

    headers = {'Access-Control-Allow-Origin': '*'}
    return jsonify({'board': board}), 200, headers

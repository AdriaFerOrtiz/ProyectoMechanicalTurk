from flask import Flask, request, jsonify
from flask_cors import CORS  
from modulo_central import movimiento_completo
import time

app = Flask(__name__)
CORS(app)  # ✅ Permite CORS desde cualquier origen

@app.route("/mover", methods=["POST"])
def mover_pieza():
    data = request.get_json()
    movimiento = data.get("movimiento")
    estado_tablero = data.get("estado_tablero")

    if not movimiento or not estado_tablero:
        return jsonify({"error": "Faltan datos"}), 400

    origen = movimiento[:2]
    destino = movimiento[2:4]

    movimiento_completo(estado_tablero, origen, destino)

    return jsonify({"status": "ok", "mensaje": f"Movimiento simulado: {origen} -> {destino}"}), 200

if __name__ == "__main__":
    app.run(port=5000)
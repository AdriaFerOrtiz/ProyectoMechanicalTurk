from flask import Flask, request, jsonify
import chess
import chess.engine
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
STOCKFISH_PATH = "./stockfish/stockfish"

def tablero_a_fen(tablero):
    fen_filas = []
    for fila in tablero:
        elementos = fila.strip().split()
        fen_fila = ""
        vacias = 0
        for elem in elementos:
            pieza_fen = elem
            if pieza_fen == ".":
                vacias += 1
            else:
                if vacias > 0:
                    fen_fila += str(vacias)
                    vacias = 0
                fen_fila += pieza_fen
        if vacias > 0:
            fen_fila += str(vacias)
        fen_filas.append(fen_fila)
    fen = "/".join(fen_filas)
    fen += " b - - 0 1"
    return fen

@app.route("/", methods=["POST"])
def analizar():
    data = request.get_json()
    tablero = data.get("tablero")
    if not tablero:
        return jsonify({"error": "No se envió el tablero"}), 400

    fen = tablero_a_fen(tablero)
    board = chess.Board(fen)

    engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)
    info = engine.analyse(board, chess.engine.Limit(depth=15))
    score = info["score"].black()
    best_move = info["pv"][0]
    engine.quit()

    if score.is_mate():
        eval_str = f"Mate en {score.mate()}"
    else:
        eval_cp = score.score() / 100
        eval_str = f"{eval_cp:+.2f}"

    return jsonify({
        "fen": fen,
        "evaluacion": eval_str,
        "mejor_movimiento": best_move.uci()
    })

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
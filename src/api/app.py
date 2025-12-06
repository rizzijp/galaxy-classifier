from flask import Flask, request, jsonify
import pickle
import numpy as np
from PIL import Image
import io
import sqlite3
import datetime
import os
from huggingface_hub import hf_hub_download


app = Flask(__name__)

REPO_ID = "rocio2125/paisajes"
FILENAME = "paisajes.pkl"


# DESCARGA DESDE HUGGINGFACE y CARGA DEL MODELO

def load_model_from_hf():
    print("Descargando/cargando modelo desde HuggingFace…")
    model_path = hf_hub_download(
        repo_id=REPO_ID,
        filename=FILENAME,
        cache_dir="./model_cache"   # opcional, donde guardar el modelo
    )

    with open(model_path, "rb") as f:
        model = pickle.load(f)

    print("Modelo cargado correctamente.")
    return model

model = load_model_from_hf()

#   CONFIGURAR BASE DE DATOS

DB_PATH = "../database/predictions.db"

def init_db():
    """
    Crea la base de datos y la tabla si no existen.
    """
    # Crear archivo si no existe
    if not os.path.exists(DB_PATH):
        open(DB_PATH, "w").close()

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            filename TEXT,
            prediction TEXT
        )
    """)
    conn.commit()
    conn.close()


def save_prediction(filename, prediction):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO predictions (timestamp, filename, prediction) VALUES (?, ?, ?)",
        (datetime.datetime.now().isoformat(), filename, str(prediction))
    )
    conn.commit()
    conn.close()


# Llamar a init_db() al arrancar
init_db()



#   PREPROCESADO DE IMAGEN

def preprocess_image(image_bytes):
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    img = img.resize((100, 100))  # Tamaño esperado por el modelo
    img_arr = np.array(img) / 255.0
    img_arr = np.expand_dims(img_arr, axis=0)
    return img_arr



#   ENDPOINT 1: PREDICCIÓN

@app.route("/predict", methods=["POST"])
def predict():

    if "image" not in request.files:
        return jsonify({"error": "Debes enviar una imagen"}), 400

    image_file = request.files["image"]
    image_bytes = image_file.read()
    processed_img = preprocess_image(image_bytes)

    prediction = model.predict(processed_img)
    pred_value = prediction.tolist()

    # Guardar en BD
    save_prediction(image_file.filename, pred_value)

    return jsonify({
        "filename": image_file.filename,
        "prediction": pred_value
    })



#   ENDPOINT 2: CONSULTAR PREDICCIONES

@app.route("/predictions", methods=["GET"])
def get_predictions():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, timestamp, filename, prediction FROM predictions")
    rows = c.fetchall()
    conn.close()

    results = []
    for r in rows:
        results.append({
            "id": r[0],
            "timestamp": r[1],
            "filename": r[2],
            "prediction": r[3]
        })

    return jsonify(results)


#   ENDPOINT 3: CONSULTAR UNA PREDICCIÓN POR ID

@app.route("/predictions/<int:prediction_id>", methods=["GET"])
def get_prediction_by_id(prediction_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, timestamp, filename, prediction FROM predictions WHERE id = ?", (prediction_id,))
    row = c.fetchone()
    conn.close()

    if row is None:
        return jsonify({"error": "Predicción no encontrada"}), 404

    result = {
        "id": row[0],
        "timestamp": row[1],
        "filename": row[2],
        "prediction": row[3]
    }

    return jsonify(result)


#   ENDPOINT 4: BORRAR TODAS LAS PREDICCIONES

@app.route("/predictions/delete", methods=["DELETE"])
def delete_all_predictions():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM predictions")
        conn.commit()
        conn.close()

        return jsonify({"message": "All predictions deleted"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
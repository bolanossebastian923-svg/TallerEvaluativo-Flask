from flask import Flask, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# Conexión con MongoDB Atlas
cliente = MongoClient(os.getenv("MONGO_URI"))

db = cliente["CURSOS_CTPI_2026-SEBASTIAN"]

coleccion = db["APRENDICES_BOLANOS"]


@app.route('/api/')
def inicio():
    return jsonify({
        "mensaje": "API funcionando correctamente"
    })
@app.route('/api/cantidadAprendices')
def cantidad_aprendices():
    cantidad = coleccion.count_documents({})

    return jsonify({
        "CantidadAprendices": cantidad
    })

if __name__ == '__main__':
    app.run(debug=True, port=8000)
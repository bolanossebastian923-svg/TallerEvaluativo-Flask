from flask import Flask, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.json.ensure_ascii = False

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


@app.route('/api/aprendices/TECNICO')
def aprendices_por_nivel():
    resultado = coleccion.aggregate([
        {
            "$group": {
                "_id": "$NIVEL_DE_FORMACION",
                "cantidad": {"$sum": 1}
            }
        }
    ])
    datos = []
    for registro in resultado:
        datos.append({
            "nivel_formacion": registro["_id"],
            "cantidad": registro["cantidad"]
        })
    return jsonify(datos)


@app.route('/api/programas/TEGNOLOGOS')
def programas_tecnologos():

    resultado = coleccion.distinct("PROGRAMA", {
        "NIVEL_DE_FORMACION": "TECNÓLOGO"
    })

    return jsonify(resultado)



if __name__ == '__main__':
    app.run(debug=True, port=8000)

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
    return jsonify({"mensaje": "API funcionando correctamente"})


@app.route('/api/cantidadAprendices')
def cantidad_aprendices():
    return jsonify({"CantidadAprendices": coleccion.count_documents({})})


@app.route('/api/aprendices/TECNICO')
def aprendices_por_nivel():
    resultado = coleccion.aggregate([
        {"$group": {"_id": "$NIVEL_DE_FORMACION", "cantidad": {"$sum": 1}}}
    ])
    datos = []
    for registro in resultado:
        datos.append({"nivel_formacion": registro["_id"], "cantidad": registro["cantidad"]})
    return jsonify(datos)


@app.route('/api/programas/TEGNÓLOGOS')
def programas_tecnologos():
    resultado = coleccion.distinct("PROGRAMA", {"NIVEL_DE_FORMACION": "TECNÓLOGO"})
    return jsonify(resultado)


@app.route('/api/aprendices/ADSO')
def aprendices_adso():
    resultado = coleccion.find(
        {"PROGRAMA": "ANALISIS Y DESARROLLO DE SOFTWARE.", "ESTADO_APRENDIZ": "Certificado"},
        {"_id": 0, "FICHA": 1, "NOMBRE": 1, "PRIMER_APELLIDO": 1,
         "SEGUNDO_APELLIDO": 1, "ESTADO_APRENDIZ": 1}
    )
    datos = []
    for aprendiz in resultado:
        datos.append(aprendiz)
    return jsonify(datos)


@app.route('/api/aprendicesPorFicha/<int:ficha>/<int:cantidad>')
def aprendices_por_ficha(ficha, cantidad):
    resultado = coleccion.find(
        {"FICHA": ficha, "ESTADO_APRENDIZ": "Por certificar"},
        {"_id": 0, "FICHA": 1, "PROGRAMA": 1, "NUMERO_DOCUMENTO": 1,
         "NOMBRE": 1, "PRIMER_APELLIDO": 1, "SEGUNDO_APELLIDO": 1}
    ).sort("PRIMER_APELLIDO", -1).limit(cantidad)

    datos = []
    for aprendiz in resultado:
        datos.append(aprendiz)
    return jsonify(datos)

@app.route('/api/aprendices/TerminadaUnificacion')
def aprendices_terminada_unificacion():
    resultado = coleccion.find({"PROGRAMA": "ANALISIS Y DESARROLLO DE SOFTWARE.", "ESTADO_FICHA": "Terminada por unificación"}, 
                               {"_id": 0, "FICHA": 1, "NUMERO_DOCUMENTO": 1, "NOMBRE": 1, "PRIMER_APELLIDO": 1, "SEGUNDO_APELLIDO": 1})
    datos = []
    for aprendiz in resultado:
        datos.append(aprendiz)
    return jsonify(datos)

@app.route('/api/aprendices/PowerBI')
def aprendices_power_bi():
    resultado = coleccion.find({"PROGRAMA": "VISUALIZACION DE DATOS USANDO POWER BI"}, 
                               {"_id": 0, "PROGRAMA": 1, "FICHA": 1, "NOMBRE": 1, "PRIMER_APELLIDO": 1, "SEGUNDO_APELLIDO": 1})
    datos = []
    for aprendiz in resultado:
        datos.append(aprendiz)
    return jsonify(datos)

if __name__ == '__main__':
    app.run(debug=True, port=8000)

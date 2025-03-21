from flask import Flask, request, jsonify, render_template, url_for
import csv
import json
import mysql.connector

app = Flask(__name__, static_folder='static', template_folder='templates')

# Configurar conexión con MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456",
    database="coquito_amarillo_db"
)
cursor = db.cursor()

# Ruta principal (Página de inicio)
@app.route('/')
def home():
    return render_template('index.html')

# Ruta para mostrar la página de evaluación
@app.route('/evaluacion')
def mostrar_formulario():
    return render_template('evaluacion.html')

# Otras rutas para navegación
@app.route('/nosotros')
def nosotros():
    return render_template('nosotros.html')

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

# Ruta para recibir datos y guardarlos en MySQL, CSV y JSON
@app.route('/guardar', methods=['POST'])
def guardar_datos():
    datos = request.json  # Recibe datos en formato JSON

    # Guardar en MySQL
    sql = "INSERT INTO Encuesta (nombre, edad, categoria, puntuacion) VALUES (%s, %s, %s, %s)"
    valores = (datos['nombre'], datos['edad'], datos['categoria'], datos['puntuacion'])
    cursor.execute(sql, valores)
    db.commit()

    # Guardar en CSV
    with open('evaluacion.csv', mode='a', newline='') as file:
        escritor = csv.writer(file)
        escritor.writerow([datos['nombre'], datos['edad'], datos['categoria'], datos['puntuacion']])

    # Guardar en JSON
    with open('evaluacion.json', 'a') as file:
        json.dump(datos, file)
        file.write("\n")

    return jsonify({"mensaje": "Datos guardados correctamente"}), 200

# Ejecutar el servidor Flask
if __name__ == '__main__':
    app.run(debug=True)

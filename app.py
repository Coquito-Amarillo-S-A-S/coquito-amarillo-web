from flask import Flask, request, jsonify, render_template
from flask_cors import CORS  # 🔹 Importa CORS
import csv
import json
import mysql.connector

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

# Rutas para renderizar páginas
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/evaluacion')
def mostrar_formulario():
    return render_template('evaluacion.html')

@app.route('/nosotros')
def nosotros():
    return render_template('nosotros.html')

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

# Ruta para recibir datos y guardarlos
@app.route('/guardar', methods=['POST'])
def guardar_datos():
    try:
        # Recibir los datos del formulario
        datos = request.form.to_dict()
        print("📥 Datos recibidos:", datos)

        # Verificar que los datos no están vacíos
        if not datos:
            return jsonify({"error": "No se recibieron datos"}), 400

        # Conversión de datos (números como enteros)
        datos_convertidos = {k: (int(v) if v.isdigit() else v) for k, v in datos.items()}

        # Conectar a MySQL
        try:
            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="123456",
                database="coquito_amarillo_db"
            )
            cursor = db.cursor()
            print("✅ Conexión exitosa a MySQL")
        except mysql.connector.Error as err:
            print("❌ Error conectando a MySQL:", err)
            return jsonify({"error": f"Error en la base de datos: {str(err)}"}), 500

        # Guardar en MySQL
        sql = """INSERT INTO evaluaciones (salud, dinero, amor, trabajo, familia, ocio, crecimiento, espiritualidad, fecha)
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        valores = (
            datos_convertidos['salud'], datos_convertidos['dinero'], datos_convertidos['amor'], 
            datos_convertidos['trabajo'], datos_convertidos['familia'], datos_convertidos['ocio'], 
            datos_convertidos['crecimiento'], datos_convertidos['espiritualidad'], datos_convertidos['fecha']
        )

        cursor.execute(sql, valores)
        db.commit()
        cursor.close()
        db.close()
        print("✅ Datos guardados en MySQL")

        # Guardar en CSV
        with open('evaluacion.csv', mode='a', newline='') as file:
            escritor = csv.writer(file)
            escritor.writerow(list(valores))  # Convertimos la tupla en lista
        print("✅ Datos guardados en CSV")

        # Guardar en JSON
        try:
            with open('evaluacion.json', 'r') as file:
                lista_datos = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            lista_datos = []

        lista_datos.append(datos_convertidos)
        with open('evaluacion.json', 'w') as file:
            json.dump(lista_datos, file, indent=4)
        print("✅ Datos guardados en JSON")

        return jsonify({"mensaje": "Datos guardados correctamente"}), 200

    except Exception as e:
        print("❌ Error:", str(e))
        return jsonify({"error": str(e)}), 500

# Ejecutar el servidor Flask
if __name__ == '__main__':
    app.run(debug=True)

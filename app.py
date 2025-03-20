from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# Configurar conexión a MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456",
    database="coquito_amarillo_db"
)
cursor = db.cursor()

# Ruta de prueba
@app.route("/")
def home():
    return "Bienvenido a la API de la Rueda de la Vida"

# Ruta para recibir y guardar datos de la evaluación
@app.route("/guardar", methods=["POST"])
def guardar_evaluacion():
    data = request.json  # Recibe JSON con los valores de la rueda
    categorias = ["salud", "dinero", "amor", "trabajo", "familia", "ocio", "crecimiento", "espiritualidad"]
    
    # Verificar que todas las categorías existan en la data
    if not all(c in data for c in categorias):
        return jsonify({"error": "Faltan datos en la evaluación"}), 400
    
    # Insertar datos en la base de datos
    sql = """
    INSERT INTO evaluaciones (salud, dinero, amor, trabajo, familia, ocio, crecimiento, espiritualidad)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    valores = tuple(data[c] for c in categorias)
    
    try:
        cursor.execute(sql, valores)
        db.commit()
        return jsonify({"mensaje": "Datos guardados correctamente"}), 201
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500

# Ejecutar la app en modo depuración
if __name__ == "__main__":
    app.run(debug=True)

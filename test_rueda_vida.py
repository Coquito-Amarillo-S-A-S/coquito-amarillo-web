import pytest
import io
import sys
from rueda_de_la_vida import obtener_datos, guardar_datos

def test_validacion_entrada(monkeypatch):
    inputs = iter(["", "0", "11", "5"])  # Simula entradas inválidas y válidas
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    
    nombre, edad, ocupacion, categorias, valores = obtener_datos()
    
    assert valores[-1] == 5  # Debe aceptar el último valor válido

def test_guardado_archivo():
    nombre, edad, ocupacion = "Juan", "25", "Estudiante"
    categorias = ["Salud"]
    valores = [8]
    
    guardar_datos(nombre, edad, ocupacion, categorias, valores)
    
    with open("rueda_vida.txt", "r", encoding="utf-8") as file:
        contenido = file.read()
    
    assert "Nombre: Juan" in contenido
    assert "Salud: 8" in contenido

# Guardar resultados en un archivo de texto
if __name__ == "__main__":
    with open("resultados_pruebas.txt", "w", encoding="utf-8") as f:
        sys.stdout = f  # Redirigir la salida estándar al archivo
        pytest.main(["-v"])
        sys.stdout = sys.__stdout__  # Restaurar la salida estándar original

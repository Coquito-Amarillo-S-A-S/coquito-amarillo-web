import matplotlib.pyplot as plt
import numpy as np
import os

def obtener_datos():
    print("Responde en una escala del 1 al 10")
    categorias = ["Salud", "Dinero", "Amor", "Familia", "Trabajo", "Diversión", "Desarrollo Personal", "Espiritualidad"]
    valores = []
    
    nombre = input("Nombre: ")
    edad = input("Edad: ")
    ocupacion = input("Ocupación: ")
    
    for categoria in categorias:
        while True:
            try:
                valor = input(f"Puntúa {categoria} (1-10): ")
                if not valor:
                    raise ValueError("No puede estar vacío.")
                valor = int(valor)
                if 1 <= valor <= 10:
                    valores.append(valor)
                    break
                else:
                    print("Error: Debes ingresar un número entre 1 y 10.")
            except ValueError as e:
                print(f"Error: Entrada no válida. {e}")
    
    return nombre, edad, ocupacion, categorias, valores

def guardar_datos(nombre, edad, ocupacion, categorias, valores):
    with open("rueda_vida.txt", "w") as file:
        file.write(f"Nombre: {nombre}\n")
        file.write(f"Edad: {edad}\n")
        file.write(f"Ocupación: {ocupacion}\n")
        file.write("\nRespuestas:\n")
        for i in range(len(categorias)):
            file.write(f"{categorias[i]}: {valores[i]}\n")

def graficar_rueda(categorias, valores, nombre):
    angulos = np.linspace(0, 2 * np.pi, len(categorias), endpoint=False).tolist()
    valores += valores[:1]  # Cerrar la rueda
    angulos += angulos[:1]
    
    fig, ax = plt.subplots(figsize=(6,6), subplot_kw={"projection": "polar"})
    ax.fill(angulos, valores, color='blue', alpha=0.4)
    ax.plot(angulos, valores, color='blue', linewidth=2)
    ax.set_yticklabels([])
    ax.set_xticks(angulos[:-1])
    ax.set_xticklabels(categorias)
    plt.title(f"Rueda de la Vida - {nombre}")
    
    # Guardar la imagen
    output_dir = "graficas"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    plt.savefig(os.path.join(output_dir, f"rueda_vida_{nombre}.png"))
    plt.show()

if __name__ == "__main__":
    nombre, edad, ocupacion, categorias, valores = obtener_datos()
    guardar_datos(nombre, edad, ocupacion, categorias, valores)
    graficar_rueda(categorias, valores, nombre)

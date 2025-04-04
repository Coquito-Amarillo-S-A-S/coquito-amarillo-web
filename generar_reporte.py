from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generar_pdf():
    c = canvas.Canvas("informe_pruebas.pdf", pagesize=letter)
    c.setFont("Helvetica", 12)

    c.drawString(100, 750, "INFORME DE PRUEBAS - Rueda de la Vida")
    c.drawString(100, 730, "--------------------------------------")

    with open("resultados_pruebas.txt", "r") as f:
        lineas = f.readlines()
    
    y = 700
    for linea in lineas:
        c.drawString(100, y, linea.strip())
        y -= 20  # Espaciado entre líneas
    
    c.save()
    print("Informe generado: informe_pruebas.pdf")

if __name__ == "__main__":
    generar_pdf()

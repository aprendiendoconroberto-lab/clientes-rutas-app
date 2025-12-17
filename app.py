from flask import Flask, render_template
import csv

app = Flask(__name__)

def leer_rutas_activas():
    rutas = []
    with open("data/rutas.csv", newline="", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            if fila["activo"].lower() == "true":
                rutas.append(fila)
    return rutas

@app.route("/")
def home():
    rutas = leer_rutas_activas()
    return render_template("index.html", rutas=rutas)

if __name__ == "__main__":
    app.run()

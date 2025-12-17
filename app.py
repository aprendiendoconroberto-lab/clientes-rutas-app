from flask import Flask, render_template, request, redirect
import csv
from datetime import datetime

app = Flask(__name__)

RUTAS_CSV = "data/rutas.csv"
CLIENTES_CSV = "data/clientes.csv"


def leer_rutas_activas():
    rutas = []
    with open(RUTAS_CSV, newline="", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            if fila["activo"].lower() == "true":
                rutas.append(fila)
    return rutas


def obtener_ruta_por_id(ruta_id):
    with open(RUTAS_CSV, newline="", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            if fila["ruta_id"] == ruta_id:
                return fila
    return None


def generar_cliente_id():
    return f"C{int(datetime.now().timestamp())}"


@app.route("/", methods=["GET", "POST"])
def home():
    rutas = leer_rutas_activas()

    if request.method == "POST":
        nombre = request.form.get("nombre_cliente")
        ruta_id = request.form.get("ruta_id")
        nota = request.form.get("nota")

        ruta = obtener_ruta_por_id(ruta_id)

        if ruta is None:
            return "Error: ruta no encontrada", 400

        cliente_id = generar_cliente_id()

        with open(CLIENTES_CSV, "a", newline="", encoding="utf-8") as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow([
                cliente_id,
                nombre,
                "",                      # lat
                "",                      # lng
                "",                      # foto_url
                nota,
                ruta["ruta_id"],
                ruta["nombre_ruta"],
                ruta["dia_semana"],
                "vendedor",              # creado_por (temporal)
                datetime.now().isoformat(),
                "ALTA"
            ])

        return redirect("/")

    return render_template("index.html", rutas=rutas)


if __name__ == "__main__":
    app.run()

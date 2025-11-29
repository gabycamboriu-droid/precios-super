# app.py
from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# ---------------------------------------------------------
# Función para buscar el precio en Coto
# ---------------------------------------------------------
def buscar_en_coto(ean):
    try:
        url = f"https://www.cotodigital.com.ar/sitios/cdigi/browse?q={ean}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        # Buscamos el precio: en Coto está dentro de <span class="price">
        price_tag = soup.find("span", class_="price")
        if price_tag:
            precio_texto = price_tag.get_text().strip()
            # Convertimos a número quitando $ y puntos
            precio_num = int("".join(filter(str.isdigit, precio_texto)))
            return precio_num
        else:
            return None
    except Exception as e:
        print("Error buscando en Coto:", e)
        return None

# ---------------------------------------------------------
# Ruta para consultar precios por código de barras
# ---------------------------------------------------------
@app.route("/precio/<ean>", methods=["GET"])
def obtener_precio(ean):
    coto = buscar_en_coto(ean)

    respuesta = {
        "ean": ean,
        "supermercados": {
            "Coto": coto
        }
    }
    return jsonify(respuesta)

# ---------------------------------------------------------
# Ruta de prueba
# ---------------------------------------------------------
@app.route("/")
def index():
    return jsonify({"status": "API funcionando"})

if __name__ == "__main__":
    app.run(debug=True)

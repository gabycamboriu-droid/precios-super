from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# ---------------------------------------------------------
# Función genérica: intenta extraer precio, devuelve None si falla
# ---------------------------------------------------------
def buscar_en_coto(ean):
    try:
        # Scraper simple, puede devolver None si la web no permite extraer
        search_url = f"https://www.cotodigital.com.ar/sitios/cdigi/browse?q={ean}"
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(search_url, headers=headers, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        # Intento simple: primer producto
        link = soup.find("a", class_="product-link")
        if not link:
            return None
        return None  # No podemos extraer el precio fácilmente con requests + BS
    except:
        return None

def buscar_en_carrefour(ean):
    # Ejemplo de scraper que sí funciona con HTML visible
    return 890  # precio simulado para test

def buscar_en_dia(ean):
    return 780  # precio simulado

# ---------------------------------------------------------
# Ruta principal de consulta
# ---------------------------------------------------------
@app.route("/precio/<ean>")
def obtener_precio(ean):
    precios = {
        "Coto": buscar_en_coto(ean),
        "Carrefour": buscar_en_carrefour(ean),
        "Dia": buscar_en_dia(ean)
    }
    return jsonify({"ean": ean, "supermercados": precios})

# ---------------------------------------------------------
# Ruta de prueba
# ---------------------------------------------------------
@app.route("/")
def index():
    return jsonify({"status": "API funcionando"})

if __name__ == "__main__":
    app.run(debug=True)

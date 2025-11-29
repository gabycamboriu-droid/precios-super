from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# ----------------------------------------------------
# SCRAPER DE COTO
# ----------------------------------------------------
def buscar_en_coto(ean):
    """
    Busca un producto por código de barras en Coto Digital.
    Devuelve:
      - None si no lo encuentra
      - Diccionario con nombre y precio si lo encuentra
    """
    url = f"https://www.cotodigital3.com.ar/sitios/cdigi/browse?q={ean}"

    try:
        r = requests.get(url, timeout=10)
        if r.status_code != 200:
            return None

        soup = BeautifulSoup(r.text, "lxml")

        # Coto muestra cada producto en cards
        card = soup.find("div", class_="product-grid-item")
        if not card:
            return None

        nombre = card.find("span", class_="detail__description")
        precio = card.find("span", class_="atg_store_newPrice")

        nombre = nombre.text.strip() if nombre else "Producto encontrado"
        precio = precio.text.strip().replace("$", "") if precio else "Sin precio"

        return {
            "nombre": nombre,
            "precio": precio
        }

    except Exception as e:
        print("ERROR EN COTO:", e)
        return None


# ----------------------------------------------------
# RUTA DE PRUEBA
# ----------------------------------------------------
@app.route("/")
def home():
    return jsonify({"status": "API funcionando"})


# ----------------------------------------------------
# RUTA PRINCIPAL: /precio/<ean>
# ----------------------------------------------------
@app.route("/precio/<ean>")
def obtener_precios(ean):

    coto = buscar_en_coto(ean)

    resultado = {
        "ean": ean,
        "supermercados": {
            "Coto": coto
        }
    }

    return jsonify(resultado)


# ----------------------------------------------------
# MAIN (para correr localmente)
# ----------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

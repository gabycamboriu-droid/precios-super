# app.py
from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# ---------------------------------------------------------
# Función para buscar el precio en Coto con varios selectores
# ---------------------------------------------------------
def buscar_en_coto(ean):
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        
        # 1️⃣ Página de búsqueda
        search_url = f"https://www.cotodigital.com.ar/sitios/cdigi/browse?q={ean}"
        r = requests.get(search_url, headers=headers, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        
        # Intentamos varios selectores para el link del producto
        product_link_tag = (
            soup.find("a", class_="product-link") or
            soup.find("a", class_="productTitle") or
            soup.find("a", class_="product") or
            soup.find("a", href=True)
        )
        if not product_link_tag:
            return None

        product_url = "https://www.cotodigital.com.ar" + product_link_tag.get("href")

        # 2️⃣ Página de producto
        r2 = requests.get(product_url, headers=headers, timeout=10)
        r2.raise_for_status()
        soup2 = BeautifulSoup(r2.text, "html.parser")

        # Intentamos varios selectores para el precio
        price_selectors = [
            ("span", "price"),
            ("span", "product-price"),
            ("div", "product-price"),
            ("div", "price")
        ]
        precio_num = None
        for tag, class_name in price_selectors:
            price_tag = soup2.find(tag, class_=class_name)
            if price_tag:
                precio_texto = price_tag.get_text().strip()
                # Convertimos a número quitando símbolos y puntos
                precio_num = int("".join(filter(str.isdigit, precio_texto)))
                break  # encontramos un precio válido

        return precio_num

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

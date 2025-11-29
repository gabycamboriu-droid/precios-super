from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# --------------------------
# Scraper Coto (no funciona bien con requests)
# --------------------------
def buscar_en_coto(ean):
    # Por ahora no podemos obtener precio con requests
    return None

# --------------------------
# Scraper Carrefour
# --------------------------
def buscar_en_carrefour(ean):
    try:
        search_url = f"https://www.carrefour.com.ar/supermercado/buscar?q={ean}"
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(search_url, headers=headers, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        
        # Buscamos primer producto
        product = soup.find("div", class_="product-item") or soup.find("div", class_="product")
        if not product:
            return None

        # Intentamos encontrar el precio
        price_tag = product.find("span", class_="product-price") or product.find("span", class_="price")
        if price_tag:
            precio_texto = price_tag.get_text().strip()
            precio_num = int("".join(filter(str.isdigit, precio_texto)))
            return precio_num
        return None
    except:
        return None

# --------------------------
# Scraper Día
# --------------------------
def buscar_en_dia(ean):
    try:
        search_url = f"https://www.diaonline.com.ar/buscar?q={ean}"
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(search_url, headers=headers, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        
        # Primer producto
        product = soup.find("div", class_="product-item") or soup.find("div", class_="product")
        if not product:
            return None

        # Precio
        price_tag = product.find("span", class_="price") or product.find("span", class_="product-price")
        if price_tag:
            precio_texto = price_tag.get_text().strip()
            precio_num = int("".join(filter(str.isdigit, precio_texto)))
            return precio_num
        return None
    except:
        return None

# --------------------------
# Ruta principal de consulta
# --------------------------
@app.route("/precio/<ean>")
def obtener_precio(ean):
    precios = {
        "Coto": buscar_en_coto(ean),
        "Carrefour": buscar_en_carrefour(ean),
        "Dia": buscar_en_dia(ean)
    }
    return jsonify({"ean": ean, "supermercados": precios})

# --------------------------
# Ruta de prueba
# --------------------------
@app.route("/")
def index():
    return jsonify({"status": "API funcionando"})

if __name__ == "__main__":
    app.run(debug=True)

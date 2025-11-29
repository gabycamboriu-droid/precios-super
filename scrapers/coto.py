import requests
from bs4 import BeautifulSoup

def buscar_en_coto(ean):
    url = f"https://www.cotodigital.com.ar/sitios/cdigi/browse?q={ean}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    resp = requests.get(url, headers=headers, timeout=10)

    if resp.status_code != 200:
        return {"error": "Coto no respondió"}

    soup = BeautifulSoup(resp.text, "lxml")

    # Cada producto está en la clase "product-item"
    items = soup.select(".product-item")

    if not items:
        return {"error": "Producto no encontrado"}

    # Tomamos el primero (el más relevante)
    item = items[0]

    # Nombre del producto
    nombre = item.select_one(".product-name")
    nombre = nombre.get_text(strip=True) if nombre else "Sin nombre"

    # Precio
    precio_elem = item.select_one(".atg_store_newPrice")
    if precio_elem:
        precio = precio_elem.get_text(strip=True)
    else:
        precio = None

    return {
        "nombre": nombre,
        "precio": precio
    }

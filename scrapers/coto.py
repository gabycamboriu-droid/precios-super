import requests
from bs4 import BeautifulSoup

def buscar_en_coto(ean):
    url = f"https://www.cotodigital.com.ar/sitios/cdigi/browse?q={ean}"
    r = requests.get(url, timeout=10)
    if r.status_code != 200:
        return None

    soup = BeautifulSoup(r.text, "lxml")

    # precio
    precio_tag = soup.select_one(".atg_store_newPrice")
    if not precio_tag:
        return None

    precio = precio_tag.get_text(strip=True).replace("$", "").replace(",", ".")

    # nombre
    nombre_tag = soup.select_one(".atg_store_productListingName a")
    nombre = nombre_tag.get_text(strip=True) if nombre_tag else "Producto"

    return {
        "super": "Coto",
        "producto": nombre,
        "precio": float(precio)
    }

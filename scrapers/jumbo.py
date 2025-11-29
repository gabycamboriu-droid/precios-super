import requests
from bs4 import BeautifulSoup

def precio_jumbo(ean):
    try:
        url = f"https://www.jumbo.com.ar/busqueda?q={ean}"
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        tag = soup.select_one(".valtech-product-price__value")
        if tag:
            return float(tag.text.replace("$", "").replace(".", "").replace(",", ".").strip())
        return None
    except:
        return None

import requests
from bs4 import BeautifulSoup

def precio_carrefour(ean):
    try:
        url = f"https://www.carrefour.com.ar/catalogsearch/result/?q={ean}"
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        tag = soup.select_one("span.price")
        if tag:
            return float(tag.text.replace("$", "").replace(",", "").strip())
        return None
    except:
        return None

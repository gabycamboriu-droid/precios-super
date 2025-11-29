import requests
from bs4 import BeautifulSoup

def precio_coto(ean):
    try:
        url = f"https://www.cotodigital.com.ar/sitios/cdigi/browse?q={ean}"
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        price_tag = soup.select_one(".atg_store_newPrice")
        if price_tag:
            return float(price_tag.text.replace("$", "").replace(",", ".").strip())
        return None
    except:
        return None

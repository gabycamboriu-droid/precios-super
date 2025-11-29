import requests
from bs4 import BeautifulSoup

def precio_dia(ean):
    try:
        url = f"https://diaonline.supermercadosdia.com.ar/catalogsearch/result/?q={ean}"
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        tag = soup.select_one(".price")
        if tag:
            return float(tag.text.replace("$", "").replace(",", "").strip())
        return None
    except:
        return None

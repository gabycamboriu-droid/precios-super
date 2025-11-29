from flask import Flask, jsonify, request
#from scrapers.coto import precio_coto
from scrapers.carrefour import precio_carrefour
from scrapers.dia import precio_dia
from scrapers.jumbo import precio_jumbo
from scrapers.coto import buscar_en_coto


app = Flask(__name__)

@app.route("/precio/<ean>", methods=["GET"])
def precio(ean):
    resultados = {
        "ean": ean,
        "precios": {
            "Coto": precio_coto(ean),
            "Carrefour": precio_carrefour(ean),
            "Dia": precio_dia(ean),
            "Jumbo": precio_jumbo(ean)
        }
    }
    return jsonify(resultados)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "API funcionando"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

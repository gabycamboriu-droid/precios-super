from flask import Flask, jsonify
from scrapers.coto import buscar_en_coto

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"status": "ok", "message": "API de precios funcionando"})

@app.route("/precio/<ean>")
def precio(ean):
    resultados = []

    # Coto
    try:
        datos_coto = buscar_en_coto(ean)
        if datos_coto:
            resultados.append(datos_coto)
    except Exception as e:
        print("Error en Coto:", e)

    return jsonify({
        "ean": ean,
        "resultados": resultados
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

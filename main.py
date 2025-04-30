
from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

def get_amadeus_token():
    url = "https://test.api.amadeus.com/v1/security/oauth2/token"
    payload = {
        "grant_type": "client_credentials",
        "client_id": os.getenv("AMADEUS_CLIENT_ID"),
        "client_secret": os.getenv("AMADEUS_CLIENT_SECRET")
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(url, data=payload, headers=headers)
    response.raise_for_status()
    return response.json()["access_token"]

@app.route("/api/voos", methods=["GET"])
def buscar_voos():
    origem = request.args.get("origem", "GRU")
    destino = request.args.get("destino", "JFK")
    data = request.args.get("data", "2025-08-15")
    try:
        token = get_amadeus_token()
        headers = {"Authorization": f"Bearer {token}"}
        params = {
            "originLocationCode": origem,
            "destinationLocationCode": destino,
            "departureDate": data,
            "adults": 1,
            "nonStop": True,
            "max": 5
        }
        url = "https://test.api.amadeus.com/v2/shopping/flight-offers"
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        voos = []
        for offer in data.get("data", []):
            itinerario = offer["itineraries"][0]["segments"][0]
            preco = offer["price"]["total"]
            voos.append({
                "cia": itinerario["carrierCode"],
                "saida": itinerario["departure"]["at"],
                "chegada": itinerario["arrival"]["at"],
                "preco": f"USD {preco}"
            })
        return jsonify({
            "origem": origem,
            "destino": destino,
            "data": data,
            "voos": voos
        })
    except Exception as e:
        return jsonify({"erro": "Falha ao buscar voos", "detalhe": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)

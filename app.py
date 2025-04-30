from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Rota principal
@app.route("/")
def home():
    return jsonify({"mensagem": "🚀 API Amadeus ativa e funcionando!"})

# Pegar token de acesso
def get_amadeus_token():
    url = "https://test.api.amadeus.com/v1/security/oauth2/token"
    payload = {
        "grant_type": "client_credentials",
        "client_id": os.getenv("AMADEUS_API_KEY"),
        "client_secret": os.getenv("AMADEUS_API_SECRET")
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(url, data=payload, headers=headers)
    return response.json()["access_token"]

# Rota para consultar voos
@app.route("/voos")
def voos():
    origem = request.args.get("origem")
    destino = request.args.get("destino")
    data = request.args.get("data")

    if not origem or not destino or not data:
        return jsonify({"erro": "Parâmetros 'origem', 'destino' e 'data' são obrigatórios."}), 400

    token = get_amadeus_token()

    url = f"https://test.api.amadeus.com/v2/shopping/flight-offers"
    params = {
        "originLocationCode": origem,
        "destinationLocationCode": destino,
        "departureDate": data,
        "adults": 1,
        "nonStop": "false",
        "max": 3
    }

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers, params=params)
    return jsonify(response.json())

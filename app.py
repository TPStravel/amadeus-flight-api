from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"mensagem": "🚀 API Amadeus ativa e funcionando!"})

@app.route('/api/voos')
def buscar_voos():
    origem = request.args.get('origem')
    destino = request.args.get('destino')
    data = request.args.get('data')

    token_url = "https://test.api.amadeus.com/v1/security/oauth2/token"
    client_id = os.getenv("AMADEUS_CLIENT_ID")
    client_secret = os.getenv("AMADEUS_CLIENT_SECRET")

    token_response = requests.post(token_url, data={
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret
    })

    access_token = token_response.json().get("access_token")
    headers = {"Authorization": f"Bearer {access_token}"}

    search_url = "https://test.api.amadeus.com/v2/shopping/flight-offers"
    params = {
        "originLocationCode": origem,
        "destinationLocationCode": destino,
        "departureDate": data,
        "adults": 1
    }

    response = requests.get(search_url, headers=headers, params=params)
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(debug=True)
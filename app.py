@app.route("/voos")
def voos():
    origem = request.args.get("origem")
    destino = request.args.get("destino")
    data = request.args.get("data")

    if not origem or not destino or not data:
        return jsonify({"erro": "Parâmetros 'origem', 'destino' e 'data' são obrigatórios."}), 400

    token = get_amadeus_token()
    url = "https://test.api.amadeus.com/v2/shopping/flight-offers"
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
    data = response.json()

    voos = []
    for offer in data.get("data", []):
        seg = offer["itineraries"][0]["segments"][0]
        voos.append({
            "companhia": offer["validatingAirlineCodes"][0],
            "aero_origem": seg["departure"]["iataCode"],
            "aero_destino": seg["arrival"]["iataCode"],
            "partida": seg["departure"]["at"],
            "chegada": seg["arrival"]["at"],
            "preco": offer["price"]["total"],
            "moeda": offer["price"]["currency"]
        })

    return jsonify(voos)

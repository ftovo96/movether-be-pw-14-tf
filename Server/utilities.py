from flask import jsonify

# Trasforma i dati in json e aggiunge gli headers.
# Riutilizzata per evitare codice duplicato e di
# dimenticare di aggiungere gli headers.
def sendResponse(data):
    response = jsonify(data)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response
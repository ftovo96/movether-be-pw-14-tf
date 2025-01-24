import json
from flask import Blueprint, jsonify, request
from . import loginQuery

login_api = Blueprint('login_api', __name__)

@login_api.route('/login', methods=['POST'])
def perform_login_api():
    data = json.loads(request.data)
    email = data['email']
    password = data['password']
    user = loginQuery.login(email, password)
    if user is not None:
        result = {
            "user": user,
            "result": "OK"
        }
    else:
        result = {
            "user": None,
            "result": "KO"
        }
    response = jsonify(result)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

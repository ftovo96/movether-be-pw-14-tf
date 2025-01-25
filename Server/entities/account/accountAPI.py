import json
from flask import Blueprint, jsonify, request
from . import accountQuery
import utilities

account_api = Blueprint('account_api', __name__)

@account_api.route('/login', methods=['POST'])
def perform_login_api():
    data = json.loads(request.data)
    email = data['email']
    password = data['password']
    user = accountQuery.login(email, password)
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
    return utilities.sendResponse(result)

@account_api.route('/register', methods=['POST'])
def create_account_api():
    data = json.loads(request.data)
    name = data['name']
    surname = data['surname']
    email = data['email']
    password = data['password']
    user = accountQuery.createAccount(name, surname, email, password)
    result = {
        "user": user,
        "result": "OK"
    }
    return utilities.sendResponse(result)

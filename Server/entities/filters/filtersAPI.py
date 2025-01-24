from flask import Blueprint, jsonify, request
from . import filtersQuery

filters_api = Blueprint('filters_api', __name__)

@filters_api.route("/sports", methods=['GET'])
def sports_api():
    result = filtersQuery.getSports()
    response = jsonify(result)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@filters_api.route("/locations", methods=['GET'])
def locations_api():
    result = filtersQuery.getLocations()
    response = jsonify(result)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response
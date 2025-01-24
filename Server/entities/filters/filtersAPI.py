from flask import Blueprint, jsonify, request
from . import filtersQuery
import utilities

filters_api = Blueprint('filters_api', __name__)

@filters_api.route("/sports", methods=['GET'])
def sports_api():
    result = filtersQuery.getSports()
    return utilities.sendResponse(result)

@filters_api.route("/locations", methods=['GET'])
def locations_api():
    result = filtersQuery.getLocations()
    return utilities.sendResponse(result)
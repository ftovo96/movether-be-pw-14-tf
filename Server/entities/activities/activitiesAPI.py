import json
from flask import Blueprint, jsonify, request
from . import activitiesQuery

activities_api = Blueprint('activities', __name__)

# @account_api.route("/account")
# def accountList():
#     return "list of accounts"

@activities_api.route("/activities", methods=['GET'])
def get_activities_api():
    params = {
        "search": request.args.get('search') or '',
        "sport": request.args.get('sport') or '',
        "location": request.args.get('location') or '',
        "companyId": request.args.get('companyId') or None,
        "userId": request.args.get('userId') or 0,
    }
    result = activitiesQuery.getActivities(params)
    response = jsonify(result)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@activities_api.route('/activities/<activityId>')
def activities_for_reservation_api(activityId):
    userId = request.args.get('userId') or 0
    result = activitiesQuery.getActivitiesForReservation(activityId, userId)
    response = jsonify(result)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@activities_api.route('/reserveActivity', methods=['POST'])
def reserve_activity_api():
    data = json.loads(request.data)
    params = {
        "activityId": data['activityId'],
        "partecipants": data['partecipants'],
        "userId": data['userId'] or None,
    }
    result = activitiesQuery.reserveActivity(params)
    response = jsonify(result)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response
import json
from flask import Blueprint, jsonify, request
from . import reservationsQuery
import utilities

reservations_api = Blueprint('reservations_api', __name__)

@reservations_api.route('/link-reservations', methods=['POST'])
def link_reservations_api():
    data = json.loads(request.data)
    userId = data['userId']
    reservationIds = data['reservationIds']
    result = reservationsQuery.linkReservations(userId, reservationIds)
    return utilities.sendResponse(result)

@reservations_api.route('/reservation-options/<reservationId>')
def activities_for_reservation_edit_api(reservationId):
    result = reservationsQuery.activitiesForReservationEdit(reservationId)
    return utilities.sendResponse(result)

@reservations_api.route('/reservations/<reservationId>', methods=['DELETE'])
def delete_reservation_api(reservationId):
    wasDeleted = False
    if reservationId:
        reservationsQuery.deleteReservation(reservationId)
        wasDeleted = True
    result = {
        "result": 'OK' if wasDeleted else 'KO',
    }
    return utilities.sendResponse(result)

@reservations_api.route('/reservations/<reservationId>', methods=['PUT'])
def update_reservation_api(reservationId):
    data = json.loads(request.data)
    params = {
        "reservationId": reservationId,
        "activityId": data['activityId'],
        "partecipants": data['partecipants'],
        "userId": data['userId'] or None,
    }
    result = reservationsQuery.updateReservation(params)
    return utilities.sendResponse(result)

@reservations_api.route("/reservations", methods=['GET'])
def get_reservations_api():
    userId = request.args.get('userId') or None
    if (userId is None):
        result = []
    else:
        params = {
            "userId": userId,
            "search": request.args.get('search') or '',
            "sport": request.args.get('sport') or '',
            "location": request.args.get('location') or '',
        }
        result = reservationsQuery.getReservations(params)
    return utilities.sendResponse(result)

@reservations_api.route('/reservations/<reservationId>', methods=['GET'])
def get_reservation_api(reservationId):
    params = {
        "reservationId": reservationId,
    }
    result = reservationsQuery.getReservation(params)
    return utilities.sendResponse(result)

@reservations_api.route("/get-reservation-by-code", methods=['GET'])
def get_reservation_by_code_api():
    reservationId = request.args.get('id') or None
    securityCode = request.args.get('securityCode') or None
    params = {
        "reservationId": reservationId,
        "securityCode": securityCode,
    }
    result = reservationsQuery.getReservationByCode(params)
    return utilities.sendResponse(result)
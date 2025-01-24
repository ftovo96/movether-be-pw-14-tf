from flask import Flask, jsonify, request, redirect
import json
from queries import login, activities, reservations, feedbacks, filters, rewards

app = Flask(__name__)

@app.route("/")
def redirectToActivities():
    return redirect('static/activities/activities.html')

@app.route('/login', methods=['POST', 'GET'])
def login_api():
    data = json.loads(request.data)
    email = data['email']
    password = data['password']
    user = login.login(email, password)
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

@app.route("/activities", methods=['GET'])
def activities_api():
    params = {
        "search": request.args.get('search') or '',
        "sport": request.args.get('sport') or '',
        "location": request.args.get('location') or '',
        "companyId": request.args.get('companyId') or None,
        "userId": request.args.get('userId') or 0,
    }
    result = activities.getActivities(params)
    response = jsonify(result)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/activities/<activityId>')
def activities_for_reservation_api(activityId):
    userId = request.args.get('userId') or 0
    result = activities.getActivitiesForReservation(activityId, userId)
    response = jsonify(result)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/reserveActivity', methods=['POST'])
def reserve_activity_api():
    data = json.loads(request.data)
    params = {
        "activityId": data['activityId'],
        "partecipants": data['partecipants'],
        "userId": data['userId'] or None,
    }
    result = acitivities.reserveActivity(params)
    response = jsonify(result)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/link-reservations', methods=['POST'])
def link_reservations_api():
    data = json.loads(request.data)
    userId = data['userId']
    reservationIds = data['reservationIds']
    result = reservations.linkReservations(userId, reservationIds)
    response = jsonify(result)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/reservations/<reservationId>')
def activities_for_reservation_edit_api(reservationId):
    result = reservations.activitiesForReservationEdit(reservationId)
    response = jsonify(result)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/deleteReservation/<reservationId>', methods=['DELETE'])
def delete_reservation_api(reservationId):
    wasDeleted = False
    if reservationId:
        reservations.deleteReservation(reservationId)
        wasDeleted = True
    result = {
        "result": 'OK' if wasDeleted else 'KO',
    }
    response = jsonify(result)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/updateReservation/<reservationId>', methods=['PUT'])
def update_reservation_api(reservationId):
    data = json.loads(request.data)
    params = {
        "reservationId": reservationId,
        "activityId": data['activityId'],
        "partecipants": data['partecipants'],
        "userId": data['userId'] or None,
    }
    result = reservations.updateReservation(params)
    response = jsonify(result)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route("/reservations", methods=['GET'])
def reservations_api():
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
        result = reservations.getReservations(params)
    response = jsonify(result)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route("/feedbacks/<companyId>", methods=['GET'])
def feedbacks_api(companyId):
    result = feedbacks.getFeedbacks(companyId)
    response = jsonify(result)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route("/send-feedback/<reservationId>", methods=['POST'])
def set_feedback_api(reservationId):
    data = json.loads(request.data)
    params = {
        "reservationId": reservationId,
        "feedbackScore": data['score'],
        "feedbackMessage": data['message'] or None,
        "userId": data['userId'] or None,
    }
    result = feedbacks.setFeedback(params)
    response = jsonify(result)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route("/sports", methods=['GET'])
def sports_api():
    result = filters.getSports()
    response = jsonify(result)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route("/locations", methods=['GET'])
def locations_api():
    result = filters.getLocations()
    response = jsonify(result)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route("/rewards", methods=['GET'])
def rewards_api():
    result = rewards.getRewards()
    response = jsonify(result)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route("/redeemed-rewards", methods=['GET'])
def redeemed_rewards_api():
    userId = request.args.get('userId') or None
    if (userId is None):
        result = []
    else:
        result = rewards.getRedeemedRewards(userId)
    response = jsonify(result)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route("/user-points", methods=['GET'])
def user_points_api():
    userId = request.args.get('userId') or None
    if (userId is None):
        result = {
            "points": 0
        }
    else:
        result = rewards.getUserPoints(userId)
    response = jsonify(result)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route("/redeem-reward", methods=['POST'])
def redeem_reward_api():
    data = json.loads(request.data)
    rewardId = data['rewardId'] or None
    userId = data['userId'] or None
    if (userId is None or rewardId is None):
        result = None
    else:
        result = rewards.redeemReward(userId, rewardId)
    response = jsonify(result)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

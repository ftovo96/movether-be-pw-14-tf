from flask import Flask, jsonify, request, redirect
import json
import queries

app = Flask(__name__)

@app.route("/")
def hello_world():
    return redirect('static/activities/activities.html')

@app.route('/login', methods=['POST', 'GET'])
def login_api():
    print(request.data)
    data = json.loads(request.data)
    email = data['email']
    password = data['password']
    user = queries.login(email, password)
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
    result = queries.getActivities(params)
    response = jsonify(result)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/activities/<activityId>')
def activities_for_reservation_api(activityId):
    userId = request.args.get('userId') or 0
    result = queries.getActivitiesForReservation(activityId, userId)
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
    result = queries.reserveActivity(params)
    response = jsonify(result)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/link-reservations', methods=['POST'])
def link_reservations_api():
    data = json.loads(request.data)
    userId = data['userId']
    reservationIds = data['reservationIds']
    result = queries.linkReservations(userId, reservationIds)
    response = jsonify(result)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/reservations/<reservationId>')
def activities_for_reservation_edit_api(reservationId):
    result = activitiesForReservationEdit(reservationId)
    response = jsonify(result)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/deleteReservation/<reservationId>', methods=['DELETE'])
def delete_reservation_api(reservationId):
    wasDeleted = False
    if reservationId:
        queries.deleteReservation(reservationId)
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
    result = queries.updateReservation(params)
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
        result = queries.getReservations(params)
    response = jsonify(result)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

# @app.route("/reservations_history", methods=['GET'])
# def reservations_history_api():
#     user_id = request.args.get('userId') or None
#     if (user_id is None):
#         response = jsonify([])
#         response.headers.add("Access-Control-Allow-Origin", "*")
#         return response
#     search = request.args.get('search') or ''
#     sport = request.args.get('sport') or ''
#     location = request.args.get('location') or ''
#     connection = sqlite3.connect(databaseName)
#     connection.row_factory = sqlite3.Row
#     cursor = connection.cursor()
#     query = f""" SELECT *,
#         FEEDBACK.id as FEEDBACK_ID,
#         COMPANY.id as COMPANY_ID,
#         COMPANY.name as COMPANY_NAME
#         FROM RESERVATION
#         LEFT JOIN ACTIVITY AS ACT
#         ON RESERVATION.activity_id = ACT.id
#         LEFT JOIN COMPANY
#         ON COMPANY.id = ACT.id
#         LEFT JOIN FEEDBACK
#         ON RESERVATION.id = FEEDBACK.reservation_id
#         WHERE (
#             user_id = '{user_id}' AND
#             DATE(date) < DATE('now') AND
#             ACT.SPORT LIKE '%{sport}%' AND
#             ACT.LOCATION LIKE '%{location}%' AND
#             COMPANY.name LIKE '%{search}%'
#         )
#     """
#     cursor.execute(query)
#     reservations = cursor.fetchall()
#     connection.close()
#     print(reservations)
#     result = []
#     for reservation in reservations:
#         print(reservation)
#         res = {
#             "id": reservation["id"],
#             "activity_id": reservation["activity_id"],
#             "partecipants": reservation["partecipants"],
#             "sport": reservation["sport"],
#             "date": reservation["date"],
#             "time": reservation["time"],
#             "location": reservation["location"],
#             "feedback_id": reservation["feedback_id"],
#             "score": reservation["score"],
#             "message": reservation["message"],
#             "company_id": reservation["company_id"],
#             "company_name": reservation["company_name"],
#         }
#         print(res)
#         result.append(res)
#     # return result
#     response = jsonify(result)
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     return response

@app.route("/feedbacks/<companyId>", methods=['GET'])
def feedbacks_api(companyId):
    result = queries.getFeedbacks(companyId)
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
    result = queries.setFeedback(params)
    response = jsonify(result)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route("/sports", methods=['GET'])
def sports_api():
    result = queries.getSports()
    response = jsonify(result)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route("/locations", methods=['GET'])
def locations_api():
    result = queries.getLocations()
    response = jsonify(result)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route("/rewards", methods=['GET'])
def rewards_api():
    result = queries.getRewards()
    response = jsonify(result)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route("/redeemed-rewards", methods=['GET'])
def redeemed_rewards_api():
    userId = request.args.get('userId') or None
    if (userId is None):
        result = []
    else:
        result = queries.getRedeemedRewards(userId)
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
        result = queries.getUserPoints(userId)
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
        result = queries.redeemReward(userId, rewardId)
    response = jsonify(result)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

from flask import Flask, jsonify, request, make_response, redirect, url_for
import json
import sqlite3
import random
import time

app = Flask(__name__)

databaseName = "test-db.db"

@app.route("/")
def hello_world():
    # return "<p>Hello, World!</p>"
    return redirect('static/activities/activities.html')

@app.route('/login', methods=['POST', 'GET'])
def login_api():
    # user = login(request.form['email'], request.form['password'])
    print(request.data)
    data = json.loads(request.data)
    email = data['email']
    password = data['password']
    # print(email)
    # user = login('mario.rossi@gmail.com', 'password123')
    user = login(email, password)
    # if user is not None:
    #     return {
    #         "user": user,
    #         "result": "OK"
    #     }
    # else:
    #     return {
    #         "user": None,
    #         "result": "KO"
    #     }
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
    # if user is not None:
    #     response.set_cookie('userId', str(user["id"]))
    #     response.set_cookie('userFullName', user["name"] + ' ' + user["surname"])
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route("/activities", methods=['GET'])
def activities_api():
    search = request.args.get('search') or ''
    sport = request.args.get('sport') or ''
    location = request.args.get('location') or ''
    companyId = request.args.get('companyId') or None
    userId = request.args.get('userId') or 0
    connection = sqlite3.connect('test-db.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    query = f""" SELECT 
        ACT.id as ID,
        ACT.location as LOCATION,
        ACT.sport as SPORT,
        ACT.date as ACT_DATE, 
        (
            SELECT GROUP_CONCAT(time, '; ') 
            FROM ACTIVITY
            WHERE ACT.date = ACTIVITY.date
        ) as ACT_TIMES,
        ACT.max_partecipants,
        ACT.allow_anonymous,
        COMPANY.id as COMPANY_ID,
        COMPANY.name as COMPANY_NAME,
        (
            SELECT count(ACTIVITY.id)
            FROM ACTIVITY
            LEFT JOIN RESERVATION
            ON RESERVATION.activity_id = ACTIVITY.id
            WHERE (
                RESERVATION.validated = "False" AND
                RESERVATION.user_id = {userId} AND
                ACTIVITY.company_id = ACT.company_id AND
                ACTIVITY.date > DATE('now', '-30 day')
            )
        ) as BAN_COUNT
        FROM ACTIVITY as ACT
        LEFT JOIN COMPANY
        ON ACT.company_id = COMPANY.id
        WHERE (
            ACT.SPORT LIKE '%{sport}%' AND
            ACT.LOCATION LIKE '%{location}%' AND
            COMPANY.name LIKE '%{search}%' AND
            ACT.date >=  DATE('now')
        """
    if companyId is not None:
        query += f"""AND COMPANY.id = {companyId}"""
    query += f"""
        )
        GROUP BY ACT.date
        ORDER BY 
            date(ACT.date) DESC,
            ACT.time DESC
    """
    cursor.execute(query)
    activities = cursor.fetchall()
    connection.close()
    # print(activities)
    result = []
    for activity in activities:
        act = {
            "id": activity["id"],
            "location": activity["location"],
            "sport": activity["sport"],
            "date": activity["act_date"],
            "times": activity["act_times"],
            "max_partecipants": activity["max_partecipants"],
            "company_id": activity["company_id"],
            "company_name": activity["company_name"],
            "isBanned": activity["ban_count"] >= 3,
        }
        if activity["allow_anonymous"] == "True":
            act["allowAnonymous"] = "true"
        elif activity["allow_anonymous"] == "False":
            act["allowAnonymous"] = "false"
        # print(act)
        result.append(act)
    response = jsonify(result)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/activities/<activity_id>')
def activities_for_reservation(activity_id):
    connection = sqlite3.connect(databaseName)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    user_id = request.args.get('userId') or 0
    query = f""" SELECT *,
        (
            SELECT COALESCE(SUM(RESERVATION.partecipants), 0)
            FROM RESERVATION
            WHERE (
                RESERVATION.user_id != {user_id} AND
                RESERVATION.activity_id = ACT.id
            )
        ) AS reserved_partecipants,
        (
            SELECT RESERVATION.id
            FROM RESERVATION
            WHERE (
                RESERVATION.user_id = {user_id} AND
                RESERVATION.activity_id = ACT.id
            )
        ) AS reservation_id
        FROM ACTIVITY as ACT
        WHERE date = (
            SELECT DATE
            FROM ACTIVITY
            WHERE ID = {activity_id}
        )
    """
    cursor.execute(query)
    activities = cursor.fetchall()
    connection.close()
    # print(activities)
    result = []
    for activity in activities:
        act = {
            "id": activity["id"],
            "time": activity["time"],
            "availablePartecipants": activity["max_partecipants"] - activity["reserved_partecipants"],
            "reservationId": activity["reservation_id"],
        }
        # print(act)
        result.append(act)
    response = jsonify(result)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response
# @app.route('/activities/<activity_id>')
# def show_post(activity_id):
#     connection = sqlite3.connect(databaseName)
#     connection.row_factory = sqlite3.Row
#     cursor = connection.cursor()
#     user_id = request.args.get('userId') or 0
#     query = f""" SELECT 
#         ACT.id as ID,
#         ACT.location as LOCATION,
#         ACT.sport as SPORT,
#         ACT.date as ACT_DATE, 
#         (
#             SELECT GROUP_CONCAT(time, '; ') 
#             FROM ACTIVITY
#             WHERE ACT.date = ACTIVITY.date
#         ) as ACT_TIMES,
#         ACT.max_partecipants,
#         (
#             SELECT COALESCE(SUM(RESERVATION.partecipants), 0)
#             FROM RESERVATION
#             WHERE RESERVATION.activity_id = {activity_id} AND
#             RESERVATION.user_id != {user_id}
#         ) AS reserved_partecipants,
#         COMPANY.id as COMPANY_ID,
#         COMPANY.name as COMPANY_NAME
#         FROM ACTIVITY as ACT
#         LEFT JOIN COMPANY
#         ON ACT.company_id = COMPANY.id
#         WHERE ACT.ID = {activity_id}
#     """
#     cursor.execute(query)
#     activity = cursor.fetchone()
#     connection.close()
#     result = {
#         "id": activity["id"],
#         "location": activity["location"],
#         "sport": activity["sport"],
#         "date": activity["act_date"],
#         "times": activity["act_times"],
#         "max_partecipants": activity["max_partecipants"],
#         "reserved_partecipants": activity["reserved_partecipants"],
        
#         "company_id": activity["company_id"],
#         "company_name": activity["company_name"]
#     }
#     response = jsonify(result)
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     return response

@app.route('/reserveActivity', methods=['POST'])
def reserveActivity():
    connection = sqlite3.connect(databaseName)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    data = json.loads(request.data)
    activityId = data['activityId']
    partecipants = data['partecipants']
    userId = data['userId'] or None
    # reservationId = data['reservationId']
    # Elimino eventuale vecchia prenotazione
    # if reservationId:
    query = f"""
        DELETE FROM RESERVATION
        WHERE ACTIVITY_ID = {activityId}
    """
    cursor.execute(query)
    connection.commit()
    # Creo prenotazione
    securityCode = str(hash(random.random()))[0:8]
    query = f"""
        INSERT INTO RESERVATION (activity_id, user_id, security_code, partecipants) 
        VALUES (?,?,?,?)
    """
    cursor.execute(query, (activityId, userId, securityCode, partecipants))
    # query = f"""
    #         SELECT * FROM RESERVATION
    #         WHERE ID = {cursor.lastrowid}
    #     """
    query = f""" SELECT *,
        (
            SELECT sport
            FROM ACTIVITY
            WHERE ACTIVITY.id = RES.activity_id
        ) as sport_abc,
        (
            SELECT SUM(RESERVATION.partecipants)
            FROM RESERVATION
            WHERE (
                RESERVATION.activity_id = RES.activity_id
            )
        ) as requested_partecipants,
        COMPANY.id AS COMPANY_ID,
        COMPANY.name AS COMPANY_NAME
        FROM RESERVATION as RES
        LEFT JOIN ACTIVITY as ACT
        ON RES.activity_id = ACT.id
        LEFT JOIN COMPANY
        ON ACT.company_id = COMPANY.id
        WHERE RES.id = {cursor.lastrowid}
    """
    cursor.execute(query)
    reservation = cursor.fetchone()
    result = {
        "id": reservation["id"],
        "securityCode": reservation["security_code"],
        "activity_id": reservation["activity_id"],
        "partecipants": reservation["partecipants"],
        "max_partecipants": reservation["max_partecipants"],
        "requested_partecipants": reservation["requested_partecipants"],
        "available_partecipants": reservation["max_partecipants"] - reservation["requested_partecipants"] + reservation["partecipants"],
        "sport": reservation["sport"],
        "sport_abc": reservation["sport_abc"],
        "date": reservation["date"],
        "time": reservation["time"],
        "location": reservation["location"],
        "company_id": reservation["company_id"],
        "company_name": reservation["company_name"],
    }
    connection.commit()
    connection.close()
    response = jsonify(result)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/link-reservations', methods=['POST'])
def link_reservations_api():
    print("Reservations")
    data = json.loads(request.data)
    userId = data['userId']
    reservationIds = data['reservationIds']
    print(userId)
    print(reservationIds)


    connection = sqlite3.connect(databaseName)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    queryIds = ','.join(['?'] * len(reservationIds))
    query = f""" 
        UPDATE RESERVATION
        SET user_id = {userId}
        WHERE 
            user_id IS NULL AND
            id IN ({queryIds})
     """
    cursor.execute(query, reservationIds)
    updatedRows = cursor.rowcount
    connection.commit()
    connection.close()
    result = {
        "result": "OK",
        "linkedReservations": updatedRows,
    }
    # return result
    response = jsonify(result)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/reservations/<reservationId>')
def activities_for_reservation_edit(reservationId):
    connection = sqlite3.connect(databaseName)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    # user_id = request.args.get('userId') or 0
    query = f""" SELECT *,
        (
            SELECT COALESCE(SUM(RESERVATION.partecipants), 0)
            FROM RESERVATION
            WHERE (
                RESERVATION.activity_id = ACT.id AND
                RESERVATION.id != {reservationId}
            )
        ) AS reserved_partecipants,
        (
            SELECT RESERVATION.id
            FROM RESERVATION
            WHERE (
                RESERVATION.activity_id = ACT.id
            )
        ) AS reservation_id
        FROM ACTIVITY as ACT
        WHERE 
            date = (
                SELECT DATE
                FROM ACTIVITY
                WHERE ID = (
                    SELECT RESERVATION.activity_id
                    FROM RESERVATION
                    WHERE RESERVATION.id = {reservationId}
                )
            ) AND
            (
                ACT.ID IN (
                    SELECT RESERVATION.activity_id
                    FROM RESERVATION
                    WHERE RESERVATION.id = {reservationId}
                ) OR
                ACT.ID NOT IN (
                    SELECT RESERVATION.activity_id
                    FROM RESERVATION
                )
            )
            
    """
    cursor.execute(query)
    activities = cursor.fetchall()
    connection.close()
    # print(activities)
    result = []
    for activity in activities:
        act = {
            "id": activity["id"],
            "time": activity["time"],
            "availablePartecipants": activity["max_partecipants"] - activity["reserved_partecipants"],
            "reservationId": activity["reservation_id"],
        }
        # print(act)
        result.append(act)
    response = jsonify(result)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/deleteReservation/<reservationId>', methods=['DELETE'])
def deleteReservation(reservationId):
    connection = sqlite3.connect(databaseName)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    if reservationId:
        query = f"""
            DELETE FROM RESERVATION
            WHERE ID = {reservationId}
        """
        cursor.execute(query)
        connection.commit()
        wasDeleted = True
    result = {
        "result": 'OK' if wasDeleted else 'KO',
    }
    connection.close()
    response = jsonify(result)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/updateReservation/<reservationId>', methods=['PUT'])
def updateReservation(reservationId):
    connection = sqlite3.connect(databaseName)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    data = json.loads(request.data)
    activityId = data['activityId']
    partecipants = data['partecipants']
    userId = data['userId'] or None
    # Non serve fare controlli su altre prenotazioni già effettuate
    # per la stessa attività ad un orario diverso perchè
    # non sono selezionabili dall'utente



    # activityReservationId = data['reservationId']
    # Elimino eventuale vecchia prenotazione (ma solo se
    # è diversa da quella che andrei a modificare)
    # if activityReservationId is None or activityReservationId != reservationId:
    # query = f"""
    #     DELETE FROM RESERVATION
    #     WHERE ID = {reservationId}
    # """
    # cursor.execute(query)
    # connection.commit()
    # if (activityReservationId):
    # Creo prenotazione
    # securityCode = str(hash(random.random()))[0:8]
    # query = f"""
    #     INSERT INTO RESERVATION (activity_id, user_id, security_code, partecipants) 
    #     VALUES (?,?,?,?)
    # """
    # cursor.execute(query, (activityId, userId, securityCode, partecipants))
    # else:
    # Modifico prenotazione esistente
    query = f"""
        UPDATE RESERVATION 
        SET
            activity_id = {activityId},
            user_id = {userId},
            partecipants = {partecipants} 
        WHERE ID = {reservationId}
    """
    cursor.execute(query)
    connection.commit()
    query = f"""
            SELECT * FROM RESERVATION
            WHERE ID = {reservationId}
        """
    cursor.execute(query)
    reservation = cursor.fetchone()
    result = {
        "id": reservation["id"],
        "securityCode": reservation["security_code"],
    }
    connection.close()
    response = jsonify(result)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route("/reservations", methods=['GET'])
def reservations_api():
    user_id = request.args.get('userId') or None
    if (user_id is None):
        response = jsonify([])
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response
    search = request.args.get('search') or ''
    sport = request.args.get('sport') or ''
    location = request.args.get('location') or ''
    connection = sqlite3.connect(databaseName)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    # query = f""" SELECT *,
    #     (
    #         SELECT sport
    #         FROM ACTIVITY
    #         WHERE ACTIVITY.id = RES.activity_id
    #     ) as sport_abc,
    #     (
    #         SELECT SUM(partecipants)
    #         FROM ACTIVITY
    #         WHERE ACTIVITY.id = ACT.id
    #     ) as requested_partecipants
    #     FROM RESERVATION as RES
    #     LEFT JOIN ACTIVITY as ACT
    #     ON RES.activity_id = ACT.id
    #     WHERE (
    #         user_id = '{user_id}' AND
    #         DATE(date) >= DATE('now')
    #     )
    # """

    query = f""" SELECT *,
        (
            SELECT sport
            FROM ACTIVITY
            WHERE ACTIVITY.id = RES.activity_id
        ) as sport_abc,
        (
            SELECT SUM(RESERVATION.partecipants)
            FROM RESERVATION
            WHERE (
                RESERVATION.activity_id = RES.activity_id
            )
        ) as requested_partecipants,
        COMPANY.id AS COMPANY_ID,
        COMPANY.name AS COMPANY_NAME,
        FEEDBACK.id AS FEEDBACK_ID
        FROM RESERVATION as RES
        LEFT JOIN ACTIVITY as ACT
        ON RES.activity_id = ACT.id
        LEFT JOIN COMPANY
        ON ACT.company_id = COMPANY.id
        LEFT JOIN FEEDBACK
        ON RES.id = FEEDBACK.reservation_id
        WHERE (
            user_id = '{user_id}' AND
            --DATE(date) >= DATE('now') AND
            ACT.SPORT LIKE '%{sport}%' AND
            ACT.LOCATION LIKE '%{location}%' AND
            COMPANY.name LIKE '%{search}%'
        )
        ORDER BY 
            date(ACT.date) DESC,
            ACT.time DESC
    """
    cursor.execute(query)
    reservations = cursor.fetchall()
    connection.close()
    print(reservations)
    result = []
    for reservation in reservations:
        res = {
            "id": reservation["id"],
            "activity_id": reservation["activity_id"],
            "partecipants": reservation["partecipants"],
            "max_partecipants": reservation["max_partecipants"],
            "requested_partecipants": reservation["requested_partecipants"],
            "available_partecipants": reservation["max_partecipants"] - reservation["requested_partecipants"] + reservation["partecipants"],
            "sport": reservation["sport"],
            "sport_abc": reservation["sport_abc"],
            "date": reservation["date"],
            "time": reservation["time"],
            "location": reservation["location"],
            "company_id": reservation["company_id"],
            "company_name": reservation["company_name"],
            "feedbackId": reservation["feedback_id"],
        }
        if reservation["validated"] == "True":
            res["validated"] = "true"
        elif reservation["validated"] == "False":
            res["validated"] = "false"
        print(res)
        result.append(res)
    # return result
    response = jsonify(result)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route("/reservations_history", methods=['GET'])
def reservations_history_api():
    user_id = request.args.get('userId') or None
    if (user_id is None):
        response = jsonify([])
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response
    search = request.args.get('search') or ''
    sport = request.args.get('sport') or ''
    location = request.args.get('location') or ''
    connection = sqlite3.connect(databaseName)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    query = f""" SELECT *,
        FEEDBACK.id as FEEDBACK_ID,
        COMPANY.id as COMPANY_ID,
        COMPANY.name as COMPANY_NAME
        FROM RESERVATION
        LEFT JOIN ACTIVITY AS ACT
        ON RESERVATION.activity_id = ACT.id
        LEFT JOIN COMPANY
        ON COMPANY.id = ACT.id
        LEFT JOIN FEEDBACK
        ON RESERVATION.id = FEEDBACK.reservation_id
        WHERE (
            user_id = '{user_id}' AND
            DATE(date) < DATE('now') AND
            ACT.SPORT LIKE '%{sport}%' AND
            ACT.LOCATION LIKE '%{location}%' AND
            COMPANY.name LIKE '%{search}%'
        )
    """
    cursor.execute(query)
    reservations = cursor.fetchall()
    connection.close()
    print(reservations)
    result = []
    for reservation in reservations:
        print(reservation)
        res = {
            "id": reservation["id"],
            "activity_id": reservation["activity_id"],
            "partecipants": reservation["partecipants"],
            "sport": reservation["sport"],
            "date": reservation["date"],
            "time": reservation["time"],
            "location": reservation["location"],
            "feedback_id": reservation["feedback_id"],
            "score": reservation["score"],
            "message": reservation["message"],
            "company_id": reservation["company_id"],
            "company_name": reservation["company_name"],
        }
        print(res)
        result.append(res)
    # return result
    response = jsonify(result)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route("/feedbacks/<companyId>", methods=['GET'])
def feedbacks_api(companyId):
    connection = sqlite3.connect(databaseName)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    query = f""" SELECT *,
        USER.name AS USER_NAME,
        USER.surname AS USER_SURNAME
        FROM FEEDBACK
        LEFT JOIN RESERVATION
        ON FEEDBACK.reservation_id = RESERVATION.id
        LEFT JOIN ACTIVITY
        ON RESERVATION.activity_id = ACTIVITY.id
        LEFT JOIN COMPANY
        ON COMPANY.id = ACTIVITY.company_id
        LEFT JOIN USER
        ON USER.id = RESERVATION.user_id
        WHERE COMPANY.id = '{companyId}'
        ORDER BY date DESC
        LIMIT 3
    """
    cursor.execute(query)
    feedbacks = cursor.fetchall()
    connection.close()
    print(feedbacks)
    result = []
    for feedback in feedbacks:
        print(feedback)
        res = {
            "id": feedback["id"],
            "score": feedback["score"],
            "message": feedback["message"],
            "timestamp": feedback["timestamp"] * 1000,
            "companyId": feedback["activity_id"],
            "companyName": feedback["name"],
        }
        if (feedback["user_name"] is not None):
            res["userName"] = feedback["user_name"] + ' ' + feedback["user_surname"][0:1] + '.'
        else:
            res["userName"] = "Anonimo"
        print(res)
        result.append(res)
    # return result
    response = jsonify(result)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route("/send-feedback/<reservationId>", methods=['POST'])
def set_feedback_api(reservationId):
    data = json.loads(request.data)
    feedbackScore = data['score']
    feedbackMessage = data['message'] or None
    userId = data['userId'] or None
    timestamp = int(time.time())
    connection = sqlite3.connect(databaseName)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    query = f"""
        INSERT INTO FEEDBACK (reservation_id, score, message, timestamp) 
        VALUES (?,?,?,?)
    """
    cursor.execute(query, (reservationId, feedbackScore, feedbackMessage, timestamp))
    connection.commit()
    query = f""" SELECT *
        FROM FEEDBACK
        WHERE id = {cursor.lastrowid}
    """
    cursor.execute(query)
    feedback = cursor.fetchone()
    connection.close()
    print(feedback)
    result = {
        "id": feedback["id"],
        "score": feedback["score"],
        "message": feedback["message"],
        "timestamp": feedback["timestamp"] * 1000,
    }
    response = jsonify(result)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route("/sports", methods=['GET'])
def sports_api():
    connection = sqlite3.connect(databaseName)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    query = f""" SELECT DISTINCT SPORT
        FROM ACTIVITY
        ORDER BY SPORT ASC
        """
    cursor.execute(query)
    activitySports = cursor.fetchall()
    connection.close()
    result = []
    for activitySport in activitySports:
        result.append(activitySport["sport"])
    response = jsonify(result)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route("/locations", methods=['GET'])
def locations_api():
    connection = sqlite3.connect(databaseName)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    query = f""" SELECT DISTINCT LOCATION
        FROM ACTIVITY
        ORDER BY LOCATION ASC
        """
    cursor.execute(query)
    activityLocations = cursor.fetchall()
    connection.close()
    result = []
    for activityLocation in activityLocations:
        result.append(activityLocation["location"])
    response = jsonify(result)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route("/rewards", methods=['GET'])
def rewards_api():
    user_id = request.args.get('userId') or None
    if (user_id is None):
        response = jsonify([])
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response
    connection = sqlite3.connect(databaseName)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    query = f""" SELECT *
        FROM REWARD
    """
    cursor.execute(query)
    reservations = cursor.fetchall()
    connection.close()
    print(reservations)
    result = []
    for reservation in reservations:
        res = {
            "id": reservation["id"],
            "description": reservation["description"],
        }
        print(res)
        result.append(res)
    # return result
    response = jsonify(result)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route("/redeemed-rewards", methods=['GET'])
def redeemed_rewards_api():
    user_id = request.args.get('userId') or None
    if (user_id is None):
        response = jsonify([])
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response
    connection = sqlite3.connect(databaseName)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    query = f""" SELECT *
        FROM REDEEMED_REWARD
        LEFT JOIN REWARD
        ON REWARD.id = REDEEMED_REWARD.reward_id
        WHERE user_id = {user_id}
    """
    cursor.execute(query)
    reservations = cursor.fetchall()
    connection.close()
    print(reservations)
    result = []
    for reservation in reservations:
        res = {
            "description": reservation["description"],
            "code": reservation["code"],
        }
        print(res)
        result.append(res)
    # return result
    response = jsonify(result)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route("/user-points", methods=['GET'])
def user_points_api():
    userId = request.args.get('userId') or None
    if (userId is None):
        response = jsonify({
            "points": 0
        })
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response
    connection = sqlite3.connect(databaseName)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    query = f""" SELECT COUNT(id) as points
        FROM RESERVATION
        WHERE (
            user_id = {userId} AND
            validated = 'True'
        )
    """
    cursor.execute(query)
    points = cursor.fetchone()["points"]
    query = f""" SELECT COUNT(id) as points
        FROM REDEEMED_REWARD
        WHERE user_id = {userId}
    """
    cursor.execute(query)
    usedPoints = cursor.fetchone()["points"]
    connection.close()
    print(points)
    print(usedPoints)
    userPoints = points - (usedPoints * 10)
    if userPoints < 0:
        userPoints = 0
    result = {
        "points": userPoints
    }
    # return result
    response = jsonify(result)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route("/redeem-reward", methods=['POST'])
def redeem_reward_api():
    data = json.loads(request.data)
    rewardId = data['rewardId'] or None
    userId = data['userId'] or None
    if (userId is None or rewardId is None):
        response = jsonify(None)
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response
    connection = sqlite3.connect(databaseName)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    redeemCode = str(hash(random.random()))[0:10]
    query = f"""
        INSERT INTO REDEEMED_REWARD (reward_id, user_id, code) 
        VALUES (?,?,?)
    """
    cursor.execute(query, (rewardId, userId, redeemCode))
    connection.commit()
    query = f""" SELECT *
        FROM REDEEMED_REWARD
        WHERE id = {cursor.lastrowid}
    """
    cursor.execute(query)
    redeemedReward = cursor.fetchone()
    connection.close()
    print(redeemedReward)
    result = {
        "code": redeemedReward["code"]
    }
    response = jsonify(result)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

def login(email, password):
    connection = sqlite3.connect(databaseName)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    print(f"Login utente con email {email} e password {password}") 
    userLoginQuery = f""" SELECT * 
        FROM USER 
        WHERE id = (
            SELECT user_id 
            FROM LOGIN 
            WHERE email = '{email}' AND 
            password = '{password}'
        )"""
    cursor.execute(userLoginQuery)
    user = cursor.fetchone()
    connection.close()
    print(user)
    if user:
        return {
            "id": user["id"],
            "name": user["name"],
            "surname": user["surname"],
        }
    else:
        return None
from flask import Flask, jsonify, request, make_response
import json
import sqlite3

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

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
    connection = sqlite3.connect('app.db')
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
        COMPANY.id as COMPANY_ID,
        COMPANY.name as COMPANY_NAME
        FROM ACTIVITY as ACT
        LEFT JOIN COMPANY
        ON ACT.company_id = COMPANY.id
        WHERE (
            ACT.SPORT LIKE '%{sport}%' AND
            ACT.LOCATION LIKE '%{location}%' AND
            COMPANY.name LIKE '%{search}%'
        """
    if companyId is not None:
        query += f"""AND COMPANY.id = {companyId}"""
    query += f"""
        )
        GROUP BY ACT.date
        ORDER BY date(ACT.date) DESC
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
            "company_name": activity["company_name"]
        }
        # print(act)
        result.append(act)
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
    connection = sqlite3.connect('app.db')
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
        COMPANY.name AS COMPANY_NAME
        FROM RESERVATION as RES
        LEFT JOIN ACTIVITY as ACT
        ON RES.activity_id = ACT.id
        LEFT JOIN COMPANY
        ON ACT.company_id = COMPANY.id
        WHERE (
            user_id = '{user_id}' AND
            DATE(date) >= DATE('now') AND
            ACT.SPORT LIKE '%{sport}%' AND
            ACT.LOCATION LIKE '%{location}%' AND
            COMPANY.name LIKE '%{search}%'
        )
        ORDER BY date(ACT.date) DESC
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
        }
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
    connection = sqlite3.connect('app.db')
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

@app.route("/feedbacks", methods=['GET'])
def feedbacks_api():
    company_id = 2
    connection = sqlite3.connect('app.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    query = f""" SELECT *,
        USER.name AS USER_NAME
        FROM FEEDBACK
        LEFT JOIN RESERVATION
        ON FEEDBACK.reservation_id = RESERVATION.id
        LEFT JOIN ACTIVITY
        ON RESERVATION.activity_id = ACTIVITY.id
        LEFT JOIN COMPANY
        ON COMPANY.id = ACTIVITY.company_id
        LEFT JOIN USER
        ON USER.id = RESERVATION.user_id
        WHERE COMPANY.id = '{company_id}'
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
            "company_id": feedback["activity_id"],
            "company_name": feedback["name"],
        }
        if (feedback["user_name"] is not None):
            res["user_name"] = feedback["user_name"]
        else:
            res["user_name"] = "Anonimo"
        print(res)
        result.append(res)
    # return result
    response = jsonify(result)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route("/set_feedback", methods=['POST'])
def set_feedback_api():
    feedbacks = []
    return [feedback.to_json() for feedback in feedbacks]

@app.route("/sports", methods=['GET'])
def sports_api():
    connection = sqlite3.connect('app.db')
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
    connection = sqlite3.connect('app.db')
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


def login(email, password):
    connection = sqlite3.connect('app.db')
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
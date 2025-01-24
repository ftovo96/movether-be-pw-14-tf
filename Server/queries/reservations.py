import sqlite3
from queries import config

# Collega le prenotazioni (eseguite con utente anonimo)
# all'utente passato in input
def linkReservations(userId, reservationIds):
    connection = sqlite3.connect(config.databaseName)
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
    return result

# Restituisce le attività collegate alla prenotazione
# (usata per la modifica di una prenotazione)
def activitiesForReservationEdit(reservationId):
    connection = sqlite3.connect(config.databaseName)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
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
    result = []
    for activity in activities:
        act = {
            "id": activity["id"],
            "time": activity["time"],
            "availablePartecipants": activity["max_partecipants"] - activity["reserved_partecipants"],
            "reservationId": activity["reservation_id"],
        }
        result.append(act)
    return result

    # Elimina la prenotazione
def deleteReservation(reservationId):
    connection = sqlite3.connect(config.databaseName)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    query = f"""
        DELETE FROM RESERVATION
        WHERE ID = {reservationId}
    """
    cursor.execute(query)
    connection.commit()
    connection.close()
    return reservationId

# Aggiorna la prenotazione
def updateReservation(params):
    connection = sqlite3.connect(config.databaseName)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    # Non serve fare controlli su altre prenotazioni già effettuate
    # per la stessa attività ad un orario diverso perchè
    # non sono selezionabili dall'utente
    query = f"""
        UPDATE RESERVATION 
        SET
            activity_id = {params["activityId"]},
            user_id = {params["userId"]},
            partecipants = {params["partecipants"]} 
        WHERE ID = {params["reservationId"]}
    """
    cursor.execute(query)
    connection.commit()
    query = f"""
            SELECT * FROM RESERVATION
            WHERE ID = {params["reservationId"]}
        """
    cursor.execute(query)
    reservation = cursor.fetchone()
    connection.close()
    result = {
        "id": reservation["id"],
        "securityCode": reservation["security_code"],
    }
    return result

# Restituisce le prenotazioni eseguite dall'utente
def getReservations(params):
    connection = sqlite3.connect(config.databaseName)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
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
            user_id = '{params["userId"]}' AND
            --DATE(date) >= DATE('now') AND
            ACT.SPORT LIKE '%{params["sport"]}%' AND
            ACT.LOCATION LIKE '%{params["location"]}%' AND
            COMPANY.name LIKE '%{params["search"]}%'
        )
        ORDER BY 
            date(ACT.date) DESC,
            ACT.time DESC
    """
    cursor.execute(query)
    reservations = cursor.fetchall()
    connection.close()
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
        result.append(res)
    return result

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
#     connection = sqlite3.connect(config.databaseName)
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
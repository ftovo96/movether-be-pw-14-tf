import sqlite3
from entities import config

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
            activity_id = ?,
            user_id = ?,
            partecipants = ?
        WHERE ID = {params["reservationId"]}
    """
    cursor.execute(query, (params["activityId"], params["userId"], params["partecipants"]))
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
            ACT.SPORT LIKE '%{params["sport"]}%' AND
            ACT.LOCATION LIKE '%{params["location"]}%' """
    if params["search"]:
        query += f"""AND (COMPANY.name LIKE '%{params["search"]}%' """
        if not params["sport"]:
            query += f"""OR ACT.SPORT LIKE '%{params["search"]}%' """
        if not params["location"]:
            query += f"""OR ACT.LOCATION LIKE '%{params["search"]}%' """
        query += f""")"""
    query += """)
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

# Restituisce la prenotazione con l'id specificato
def getReservation(params):
    connection = sqlite3.connect(config.databaseName)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    print(params)
    print(params)
    print(params)
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
            RES.id = '{params["reservationId"]}'
        )
    """
    cursor.execute(query)
    reservation = cursor.fetchone()
    connection.close()
    result = {
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
        result["validated"] = "true"
    elif reservation["validated"] == "False":
        result["validated"] = "false"
    print(result)
    return result

# Restituisce le prenotazioni eseguite dall'utente
def getReservationByCode(params):
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
            RES.id = '{params["reservationId"]}' AND
            RES.security_code = '{params["securityCode"]}'
        )
    """
    cursor.execute(query)
    reservation = cursor.fetchone()
    connection.close()
    result = {
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
        result["validated"] = "true"
    elif reservation["validated"] == "False":
        result["validated"] = "false"
    print(result)
    return result
import sqlite3
import random
import time

databaseName = "test-db.db"

# Verifica le credenziali dell'utente. Se sono giuste vengono
# restituiti i dati dell'utente.
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

# Restituisce la lista delle attività
def getActivities(params):
    connection = sqlite3.connect(databaseName)
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
                RESERVATION.user_id = {params["userId"]} AND
                ACTIVITY.company_id = ACT.company_id AND
                ACTIVITY.date > DATE('now', '-30 day')
            )
        ) as BAN_COUNT
        FROM ACTIVITY as ACT
        LEFT JOIN COMPANY
        ON ACT.company_id = COMPANY.id
        WHERE (
            ACT.SPORT LIKE '%{params["sport"]}%' AND
            ACT.LOCATION LIKE '%{params["location"]}%' AND
            COMPANY.name LIKE '%{params["search"]}%' AND
            ACT.date >=  DATE('now')
        """
    if params["companyId"] is not None:
        query += f"""AND COMPANY.id = {params["companyId"]}"""
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
        result.append(act)
    return result

# Restituisce la lista di attività collegate all'activityId
# (per ogni orario di un'attività viene creata una riga diversa sul database)
def getActivitiesForReservation(activityId, userId):
    connection = sqlite3.connect(databaseName)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    query = f""" SELECT *,
        (
            SELECT COALESCE(SUM(RESERVATION.partecipants), 0)
            FROM RESERVATION
            WHERE (
                RESERVATION.user_id != {userId} AND
                RESERVATION.activity_id = ACT.id
            )
        ) AS reserved_partecipants,
        (
            SELECT RESERVATION.id
            FROM RESERVATION
            WHERE (
                RESERVATION.user_id = {userId} AND
                RESERVATION.activity_id = ACT.id
            )
        ) AS reservation_id
        FROM ACTIVITY as ACT
        WHERE date = (
            SELECT DATE
            FROM ACTIVITY
            WHERE ID = {activityId}
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

def reserveActivity(params):
    connection = sqlite3.connect(databaseName)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    # Elimino eventuale vecchia prenotazione
    if params["activityId"]:
        query = f"""
            DELETE FROM RESERVATION
            WHERE ACTIVITY_ID = {params["activityId"]}
        """
        cursor.execute(query)
    # Creo prenotazione
    securityCode = str(hash(random.random()))[0:8]
    query = f"""
        INSERT INTO RESERVATION (activity_id, user_id, security_code, partecipants) 
        VALUES (?,?,?,?)
    """
    cursor.execute(query, (params["activityId"], params["userId"], securityCode, params["partecipants"]))
    # Ottengo i dati della prenotazione appena creata
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
    connection.commit()
    connection.close()
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
    return result

# Collega le prenotazioni (eseguite con utente anonimo)
# all'utente passato in input
def linkReservations(userId, reservationIds):
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
    return result

# Restituisce le attività collegate alla prenotazione
# (usata per la modifica di una prenotazione)
def activitiesForReservationEdit(reservationId):
    connection = sqlite3.connect(databaseName)
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
    connection = sqlite3.connect(databaseName)
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
    connection = sqlite3.connect(databaseName)
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
    connection = sqlite3.connect(databaseName)
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

# Restituisce gli ultimi 3 feedback di una palestra
def getFeedbacks(companyId):
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
        ON USER.id = RESERVATION.user_id"""
    if companyId:
        query += f" WHERE COMPANY.id = '{companyId}' "
    query += f"""
        ORDER BY date DESC
        LIMIT 3
    """
    cursor.execute(query)
    feedbacks = cursor.fetchall()
    connection.close()
    result = []
    for feedback in feedbacks:
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
        result.append(res)
    return result

# Salva un nuovo feedback
def setFeedback(params):
    connection = sqlite3.connect(databaseName)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    timestamp = int(time.time())
    query = f"""
        INSERT INTO FEEDBACK (reservation_id, score, message, timestamp) 
        VALUES (?,?,?,?)
    """
    cursor.execute(query, (params["reservationId"], params["feedbackScore"], params["feedbackMessage"], timestamp))
    connection.commit()
    query = f""" SELECT *
        FROM FEEDBACK
        WHERE id = {cursor.lastrowid}
    """
    cursor.execute(query)
    feedback = cursor.fetchone()
    connection.close()
    result = {
        "id": feedback["id"],
        "score": feedback["score"],
        "message": feedback["message"],
        "timestamp": feedback["timestamp"] * 1000,
    }
    return result

# Restituisce la lista degli sport
def getSports():
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
    return result

# Restituisce la lista dei luoghi in cui si svolgono le attività
def getLocations():
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
    return result

# Restituisce la lista dei premi
def getRewards():
    connection = sqlite3.connect(databaseName)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    query = f""" SELECT *
        FROM REWARD
    """
    cursor.execute(query)
    reservations = cursor.fetchall()
    connection.close()
    result = []
    for reservation in reservations:
        res = {
            "id": reservation["id"],
            "description": reservation["description"],
        }
        result.append(res)
    return result

# Restituisce la lista dei premi riscattati dall'utente
def getRedeemedRewards(userId):
    connection = sqlite3.connect(databaseName)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    query = f""" SELECT *
        FROM REDEEMED_REWARD
        LEFT JOIN REWARD
        ON REWARD.id = REDEEMED_REWARD.reward_id
        WHERE user_id = {userId}
    """
    cursor.execute(query)
    reservations = cursor.fetchall()
    connection.close()
    result = []
    for reservation in reservations:
        res = {
            "description": reservation["description"],
            "code": reservation["code"],
        }
        result.append(res)
    return result

# Restitusce il numero di punti accumulati dall'utente
def getUserPoints(userId):
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
    userPoints = points - (usedPoints * 10)
    if userPoints < 0:
        userPoints = 0
    result = {
        "points": userPoints
    }
    return result

# Riscatta un premio
def redeemReward(userId, rewardId):
    connection = sqlite3.connect(databaseName)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    redeemedRewardCode = str(hash(random.random()))[0:10]
    query = f"""
        INSERT INTO REDEEMED_REWARD (reward_id, user_id, code) 
        VALUES (?,?,?)
    """
    cursor.execute(query, (rewardId, userId, redeemedRewardCode))
    connection.commit()
    query = f""" SELECT *
        FROM REDEEMED_REWARD
        WHERE id = {cursor.lastrowid}
    """
    cursor.execute(query)
    redeemedReward = cursor.fetchone()
    connection.close()
    result = {
        "code": redeemedReward["code"]
    }
    return result
import sqlite3
import random
from entities import config

# Restituisce la lista delle attività
def getActivities(params):
    connection = sqlite3.connect(config.databaseName)
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
    connection = sqlite3.connect(config.databaseName)
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

# Prenota l'attività
def reserveActivity(params):
    connection = sqlite3.connect(config.databaseName)
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
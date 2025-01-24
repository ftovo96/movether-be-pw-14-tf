import sqlite3
import time
from queries import config

# Restituisce gli ultimi 3 feedback di una palestra
def getFeedbacks(companyId):
    connection = sqlite3.connect(config.databaseName)
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
    connection = sqlite3.connect(config.databaseName)
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
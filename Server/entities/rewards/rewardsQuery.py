import sqlite3
import random
from entities import config

# Restituisce la lista dei premi
def getRewards():
    connection = sqlite3.connect(config.databaseName)
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
    connection = sqlite3.connect(config.databaseName)
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
    connection = sqlite3.connect(config.databaseName)
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
    userPoints = points - usedPoints
    if userPoints < 0:
        userPoints = 0
    result = {
        "points": userPoints
    }
    return result

# Riscatta un premio
def redeemReward(userId, rewardId):
    connection = sqlite3.connect(config.databaseName)
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
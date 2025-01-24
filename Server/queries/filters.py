import sqlite3
from queries import config

# Restituisce la lista degli sport delle attività
def getSports():
    connection = sqlite3.connect(config.databaseName)
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
    connection = sqlite3.connect(config.databaseName)
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
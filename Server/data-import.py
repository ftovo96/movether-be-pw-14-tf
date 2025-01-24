import csv
import sqlite3
from entities import config

def importUsers():
    fileName = "users"
    createTableQuery = """ CREATE TABLE USER (
                id INTEGER PRIMARY KEY,
                name CHAR(50) NOT NULL,
                surname CHAR(50) NOT NULL
            ); """
    insertDataQuery = "INSERT INTO USER VALUES (?,?,?)"
    importTableData("USER", fileName, createTableQuery, insertDataQuery)

def importLogins():
    fileName = "logins"
    createTableQuery = """ CREATE TABLE LOGIN (
                id INTEGER PRIMARY KEY,
                user_id INTEGER NOT NULL,
                email CHAR(120) NOT NULL,
                password CHAR(255) NOT NULL
            ); """
    insertDataQuery = "INSERT INTO LOGIN (user_id, email, password) VALUES (?,?,?)"
    importTableData("LOGIN", fileName, createTableQuery, insertDataQuery)

def importCompanies():
    fileName = "companies"
    createTableQuery = """ CREATE TABLE COMPANY (
                id INTEGER PRIMARY KEY,
                name CHAR(100) NOT NULL,
                description CHAR(1000)
            ); """
    insertDataQuery = "INSERT INTO COMPANY VALUES (?,?,?)"
    importTableData("COMPANY", fileName, createTableQuery, insertDataQuery)

def importActivities():
    fileName = "activities"
    createTableQuery = """ CREATE TABLE ACTIVITY (
                id INTEGER PRIMARY KEY,
                company_id INTEGER NOT NULL,
                sport CHAR(50) NOT NULL,
                date CHAR(10) NOT NULL,
                time CHAR(5) NOT NULL,
                max_partecipants INTEGER NOT NULL,
                location CHAR(1000) NOT NULL,
                description CHAR(1000),
                allow_anonymous BOOLEAN NOT NULL
            ); """
    insertDataQuery = "INSERT INTO ACTIVITY (id, sport, date, time, max_partecipants, description, location, company_id, allow_anonymous) VALUES (?,?,?,?,?,?,?,?,?)"
    importTableData("ACTIVITY", fileName, createTableQuery, insertDataQuery)

def importReservations():
    fileName = "reservations"
    createTableQuery = """ CREATE TABLE RESERVATION (
                id INTEGER PRIMARY KEY,
                activity_id INTEGER NOT NULL,
                user_id INTEGER,
                security_code CHAR(8) NOT NULL,
                partecipants INTEGER NOT NULL,
                validated BOOLEAN
            ); """
    insertDataQuery = "INSERT INTO RESERVATION (id, activity_id, user_id, security_code, partecipants, validated) VALUES (?,?,?,?,?,?)"
    importTableData("RESERVATION", fileName, createTableQuery, insertDataQuery)

def importFeedbacks():
    fileName = "feedbacks"
    createTableQuery = """ CREATE TABLE FEEDBACK (
                id INTEGER PRIMARY KEY,
                reservation_id INTEGER NOT NULL,
                score INTEGER NOT NULL,
                message CHAR(1000),
                timestamp INTEGER NOT NULL
            ); """
    insertDataQuery = "INSERT INTO FEEDBACK (reservation_id, score, message, timestamp) VALUES (?,?,?,?)"
    importTableData("FEEDBACK", fileName, createTableQuery, insertDataQuery)

def importRewards():
    fileName = "rewards"
    createTableQuery = """ CREATE TABLE REWARD (
                id INTEGER PRIMARY KEY,
                description CHAR(1000)
            ); """
    insertDataQuery = "INSERT INTO REWARD VALUES (?,?)"
    importTableData("REWARD", fileName, createTableQuery, insertDataQuery)

def importRedeemedRewards():
    fileName = "redeemed_rewards"
    createTableQuery = """ CREATE TABLE REDEEMED_REWARD (
                id INTEGER PRIMARY KEY,
                reward_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                code CHAR(10) NOT NULL
            ); """
    insertDataQuery = "INSERT INTO REDEEMED_REWARD (reward_id, user_id, code) VALUES (?,?,?)"
    importTableData("REDEEMED_REWARD", fileName, createTableQuery, insertDataQuery)

def importTableData(tableName, fileName, createTableQuery, insertDataQuery):
    connection = sqlite3.connect(config.databaseName)
    cursor = connection.cursor()
    cursor.execute(f"DROP TABLE IF EXISTS {tableName}")
    cursor.execute(createTableQuery)
    # Apro file csv con i dati
    with open(f"data/{fileName}.csv") as fp:
        reader = csv.reader(fp, delimiter=",", quotechar='"')
        for i, row in enumerate(reader):
            if i == 0:
                continue
            print(row)
            # Inserisco dati nella tabella
            cursor.execute(insertDataQuery, row)
    # Salvo modifiche alla tabella
    connection.commit()
    connection.close()
    print(f"Imported {tableName}!\n\n")

def printTableData(tableName):
    print(f"{tableName}:")
    connection = sqlite3.connect(config.databaseName)
    cursor = connection.cursor()
    userQuery = f""" SELECT * FROM {tableName}"""
    data = cursor.execute(userQuery)
    for row in data: 
        print(row)
    connection.close()
    print("\n************************************\n")


importUsers()
importLogins()
importCompanies()
importActivities()
importReservations()
importFeedbacks()
importRewards()
importRedeemedRewards()

printTableData("USER")
printTableData("LOGIN")
printTableData("COMPANY")
printTableData("ACTIVITY")
printTableData("RESERVATION")
printTableData("FEEDBACK")
printTableData("REWARD")
printTableData("REDEEMED_REWARD")

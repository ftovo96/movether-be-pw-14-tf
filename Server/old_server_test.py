
import sqlite3
 
# try:
   
#     # Connect to DB and create a cursor
#     sqliteConnection = sqlite3.connect('sql.db')
#     cursor = sqliteConnection.cursor()
#     print('DB Init')
 
#     # Write a query and execute it with cursor
#     query = 'select sqlite_version();'
#     cursor.execute(query)
 
#     # Fetch and output result
#     result = cursor.fetchall()
#     print('SQLite Version is {}'.format(result))
 
#     # Close the cursor
#     cursor.close()
 
# # Handle errors
# except sqlite3.Error as error:
#     print('Error occurred - ', error)
 
# # Close DB Connection irrespective of success
# # or failure
# finally:
   
#     if sqliteConnection:
#         sqliteConnection.close()
#         print('SQLite Connection closed')


import sqlite3
 
# Connecting to sqlite
# connection object
connection = sqlite3.connect('app.db')
 
# cursor object
cursor = connection.cursor()
 
# Drop the GEEK table if already exists.
# cursor.execute("DROP TABLE IF EXISTS GEEK")
 

cursor.execute("DROP TABLE IF EXISTS USER")
cursor.execute("DROP TABLE IF EXISTS LOGIN")
cursor.execute("DROP TABLE IF EXISTS FEEDBACK")
cursor.execute("DROP TABLE IF EXISTS COMPANY")
cursor.execute("DROP TABLE IF EXISTS ACTIVITY")
cursor.execute("DROP TABLE IF EXISTS RESERVATION")

# Creazione tabelle
# Creazione tabella USER
table = """ CREATE TABLE USER (
            id INTEGER PRIMARY KEY,
            name CHAR(50) NOT NULL,
            surname CHAR(50) NOT NULL
        ); """
cursor.execute(table)

# Creazione tabella LOGIN
table = """ CREATE TABLE LOGIN (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            email CHAR(120) NOT NULL,
            password CHAR(255) NOT NULL
        ); """
cursor.execute(table)

# Creazione tabella FEEDBACK
table = """ CREATE TABLE FEEDBACK (
            id INTEGER PRIMARY KEY,
            reservation_id INTEGER NOT NULL,
            score INTEGER NOT NULL,
            message CHAR(1000)
        ); """
cursor.execute(table)

# Creazione tabella COMPANY
table = """ CREATE TABLE COMPANY (
            id INTEGER PRIMARY KEY,
            name CHAR(100) NOT NULL,
            description CHAR(1000)
        ); """
cursor.execute(table)

# Creazione tabella ACTIVITY
table = """ CREATE TABLE ACTIVITY (
            id INTEGER PRIMARY KEY,
            company_id INTEGER NOT NULL,
            sport CHAR(50) NOT NULL,
            date CHAR(10) NOT NULL,
            time CHAR(5) NOT NULL,
            max_partecipants INTEGER NOT NULL,
            location CHAR(1000) NOT NULL,
            description CHAR(1000)
        ); """
cursor.execute(table)

# Creazione tabella RESERVATION
table = """ CREATE TABLE RESERVATION (
            id INTEGER PRIMARY KEY,
            activity_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            security_code CHAR(8) NOT NULL,
            partecipants INTEGER NOT NULL
        ); """
cursor.execute(table)

# Popolazione dati tabelle
# Popolazione tabella COMPANY
company1 = {'id': 1, 'name': 'Benessere 24/7', 'descrizione': 'Per stare bene tutti i giorni!' }
company2 = {'id': 2, 'name': 'Passione running', 'descrizione': 'Una corsa al giorno toglie il medico di torno!' }
company3 = {'id': 3, 'name': 'Tennis lovers', 'descrizione': None }
cursor.execute('''INSERT INTO COMPANY (id, name, description) VALUES (?,?,?)''', (company1['id'], company1['name'], company1['descrizione']))
cursor.execute('''INSERT INTO COMPANY (id, name, description) VALUES (?,?,?)''', (company2['id'], company2['name'], company2['descrizione']))
cursor.execute('''INSERT INTO COMPANY (id, name, description) VALUES (?,?,?)''', (company3['id'], company3['name'], company3['descrizione']))
# Display data inserted 
print("Data Inserted in COMPANY: ") 
data = cursor.execute('''SELECT * FROM COMPANY''') 
for row in data: 
    print(row) 
print("") 

# Popolazione tabella USER
user1 = {'id': 1, 'name': 'Mario', 'surname': 'Rossi' }
user2 = {'id': 2, 'name': 'Luigi', 'surname': 'Verdi' }
user3 = {'id': 3, 'name': 'Rosa', 'surname': 'Bianchi' }
cursor.execute('''INSERT INTO USER VALUES (?,?,?)''', (user1['id'], user1['name'], user1['surname']))
cursor.execute('''INSERT INTO USER VALUES (?,?,?)''', (user2['id'], user2['name'], user2['surname']))
cursor.execute('''INSERT INTO USER VALUES (?,?,?)''', (user3['id'], user3['name'], user3['surname']))
# Display data inserted 
print("Data Inserted in USER: ") 
data = cursor.execute('''SELECT * FROM USER''') 
for row in data: 
    print(row)
print("") 

# Popolazione tabella LOGIN
userLogin1 = {'email': 'mario.rossi@gmail.com', 'password': 'password123' }
userLogin2 = {'email': 'rosa.bianchi@gmail.com', 'password': 'password456' }
cursor.execute('''INSERT INTO LOGIN (user_id, email, password) VALUES (?,?,?)''', (user1['id'], userLogin1['email'], userLogin1['password']))
cursor.execute('''INSERT INTO LOGIN (user_id, email, password) VALUES (?,?,?)''', (user3['id'], userLogin2['email'], userLogin2['password']))
# Display data inserted 
print("Data Inserted in LOGIN: ") 
data = cursor.execute('''SELECT * FROM LOGIN''') 
for row in data: 
    print(row) 
print("") 

# Popolazione tabella ACTIVITY
activity1a = {'id': 1, 'sport': 'RUNNING', 'date': '2025-01-11', 'time': '10:30', 'max_partecipants': 10, 'description': 'Vieni a correre con noi!', 'location': 'Bosco "Parco Nazionale del Circeo" (Sabaudia)', 'company_id': company2['id'] }
activity1b = {'id': 2, 'sport': 'RUNNING', 'date': '2025-01-11', 'time': '15:30', 'max_partecipants': 10, 'description': 'Vieni a correre con noi!', 'location': 'Bosco "Parco Nazionale del Circeo" (Sabaudia)', 'company_id': company2['id'] }
activity1c = {'id': 3, 'sport': 'RUNNING', 'date': '2025-01-11', 'time': '17:30', 'max_partecipants': 10, 'description': 'Vieni a correre con noi!', 'location': 'Bosco "Parco Nazionale del Circeo" (Sabaudia)', 'company_id': company2['id'] }

activity2 = {'id': 4, 'sport': 'TENNIS', 'date': '2025-01-15', 'time': '16:00', 'max_partecipants': 4, 'description': 'Partecipa ad una partita per familiarizzare con questo sport', 'location': 'Giardini Latina', 'company_id': company3['id'] }

activity3a = {'id': 5, 'sport': 'BODYBUILDING', 'date': '2025-01-18', 'time': '10:00', 'max_partecipants': 8, 'description': 'Vieni a sollevare in compagnia!', 'location': 'Sede palestra', 'company_id': company1['id'] }
activity3b = {'id': 6, 'sport': 'BODYBUILDING', 'date': '2025-01-18', 'time': '16:00', 'max_partecipants': 12, 'description': 'Vieni a sollevare in compagnia!', 'location': 'Sede palestra', 'company_id': company1['id'] }

cursor.execute('''INSERT INTO ACTIVITY (id, company_id, sport, date, time, max_partecipants, location, description) VALUES (?,?,?,?,?,?,?,?)''', (activity1a['id'], activity1a['company_id'], activity1a['sport'], activity1a['date'], activity1a['time'], activity1a['max_partecipants'], activity1a['location'], activity1a['description']))
cursor.execute('''INSERT INTO ACTIVITY (id, company_id, sport, date, time, max_partecipants, location, description) VALUES (?,?,?,?,?,?,?,?)''', (activity1b['id'], activity1b['company_id'], activity1b['sport'], activity1b['date'], activity1b['time'], activity1b['max_partecipants'], activity1b['location'], activity1b['description']))
cursor.execute('''INSERT INTO ACTIVITY (id, company_id, sport, date, time, max_partecipants, location, description) VALUES (?,?,?,?,?,?,?,?)''', (activity1c['id'], activity1c['company_id'], activity1c['sport'], activity1c['date'], activity1c['time'], activity1c['max_partecipants'], activity1c['location'], activity1c['description']))

cursor.execute('''INSERT INTO ACTIVITY (id, company_id, sport, date, time, max_partecipants, location, description) VALUES (?,?,?,?,?,?,?,?)''', (activity2['id'], activity2['company_id'], activity2['sport'], activity2['date'], activity2['time'], activity2['max_partecipants'], activity2['location'], activity2['description']))

cursor.execute('''INSERT INTO ACTIVITY (id, company_id, sport, date, time, max_partecipants, location, description) VALUES (?,?,?,?,?,?,?,?)''', (activity3a['id'], activity3a['company_id'], activity3a['sport'], activity3a['date'], activity3a['time'], activity3a['max_partecipants'], activity3a['location'], activity3a['description']))
cursor.execute('''INSERT INTO ACTIVITY (id, company_id, sport, date, time, max_partecipants, location, description) VALUES (?,?,?,?,?,?,?,?)''', (activity3b['id'], activity3b['company_id'], activity3b['sport'], activity3b['date'], activity3b['time'], activity3b['max_partecipants'], activity3b['location'], activity3b['description']))
# Display data inserted 
print("Data Inserted in ACTIVITY: ") 
data = cursor.execute('''SELECT * FROM ACTIVITY''') 
for row in data: 
    print(row) 
print("") 


# Popolazione tabella RESERVATION
reservation1 = {'id': 1, 'activity_id': activity1a['id'], 'user_id': user1['id'], 'security_code': 'a1b2c3d4', 'partecipants': 2 }
reservation2 = {'id': 2, 'activity_id': activity1a['id'], 'user_id': user2['id'], 'security_code': 'd5b1c5g6', 'partecipants': 1 }
reservation3 = {'id': 3, 'activity_id': activity1a['id'], 'user_id': user3['id'], 'security_code': 'f4b6v3h9', 'partecipants': 1 }

reservation4 = {'id': 4, 'activity_id': activity1c['id'], 'user_id': user3['id'], 'security_code': 'h4b4c4d8', 'partecipants': 1 }
reservation5 = {'id': 5, 'activity_id': activity1c['id'], 'user_id': user2['id'], 'security_code': 'k7b7c0j6', 'partecipants': 1 }

reservation6 = {'id': 6, 'activity_id': activity3b['id'], 'user_id': user1['id'], 'security_code': 'h4h4h4d3', 'partecipants': 1 }
reservation7 = {'id': 7, 'activity_id': activity3b['id'], 'user_id': user2['id'], 'security_code': 'g7h7c0j7', 'partecipants': 4 }


cursor.execute('''INSERT INTO RESERVATION (id, activity_id, user_id, security_code, partecipants) VALUES (?,?,?,?,?)''', (reservation1['id'], reservation1['activity_id'], reservation1['user_id'], reservation1['security_code'], reservation1['partecipants']))
cursor.execute('''INSERT INTO RESERVATION (id, activity_id, user_id, security_code, partecipants) VALUES (?,?,?,?,?)''', (reservation2['id'], reservation2['activity_id'], reservation2['user_id'], reservation2['security_code'], reservation2['partecipants']))
cursor.execute('''INSERT INTO RESERVATION (id, activity_id, user_id, security_code, partecipants) VALUES (?,?,?,?,?)''', (reservation3['id'], reservation3['activity_id'], reservation3['user_id'], reservation3['security_code'], reservation3['partecipants']))

cursor.execute('''INSERT INTO RESERVATION (id, activity_id, user_id, security_code, partecipants) VALUES (?,?,?,?,?)''', (reservation4['id'], reservation4['activity_id'], reservation4['user_id'], reservation4['security_code'], reservation4['partecipants']))
cursor.execute('''INSERT INTO RESERVATION (id, activity_id, user_id, security_code, partecipants) VALUES (?,?,?,?,?)''', (reservation5['id'], reservation5['activity_id'], reservation5['user_id'], reservation5['security_code'], reservation5['partecipants']))

cursor.execute('''INSERT INTO RESERVATION (id, activity_id, user_id, security_code, partecipants) VALUES (?,?,?,?,?)''', (reservation6['id'], reservation6['activity_id'], reservation6['user_id'], reservation6['security_code'], reservation6['partecipants']))
cursor.execute('''INSERT INTO RESERVATION (id, activity_id, user_id, security_code, partecipants) VALUES (?,?,?,?,?)''', (reservation7['id'], reservation7['activity_id'], reservation7['user_id'], reservation7['security_code'], reservation7['partecipants']))
# Display data inserted 
print("Data Inserted in RESERVATION: ") 
data = cursor.execute('''SELECT * FROM RESERVATION''') 
for row in data: 
    print(row) 
print("") 

# Popolazione tabella FEEDBACK
feedback1 = {'reservation_id': reservation1['id'], 'score': 4, 'message': 'Ottima!' }
feedback2 = {'reservation_id': reservation2['id'], 'score': 5, 'message': 'Tosta ma divertente' }
feedback3 = {'reservation_id': reservation3['id'], 'score': 5, 'message': None }

feedback4 = {'reservation_id': reservation4['id'], 'score': 3, 'message': None }
feedback5 = {'reservation_id': reservation7['id'], 'score': 5, 'message': 'Parteciperò anche alla prossima!' }


cursor.execute('''INSERT INTO FEEDBACK (reservation_id, score, message) VALUES (?,?,?)''', (feedback1['reservation_id'], feedback1['score'], feedback1['message']))
cursor.execute('''INSERT INTO FEEDBACK (reservation_id, score, message) VALUES (?,?,?)''', (feedback2['reservation_id'], feedback2['score'], feedback2['message']))
cursor.execute('''INSERT INTO FEEDBACK (reservation_id, score, message) VALUES (?,?,?)''', (feedback3['reservation_id'], feedback3['score'], feedback3['message']))
cursor.execute('''INSERT INTO FEEDBACK (reservation_id, score, message) VALUES (?,?,?)''', (feedback4['reservation_id'], feedback4['score'], feedback4['message']))
cursor.execute('''INSERT INTO FEEDBACK (reservation_id, score, message) VALUES (?,?,?)''', (feedback5['reservation_id'], feedback5['score'], feedback5['message']))

# Display data inserted 
print("Data Inserted in FEEDBACK: ") 
data = cursor.execute('''SELECT * FROM FEEDBACK''') 
for row in data: 
    print(row) 
print("") 


# Query
# Login utente con email e password
print(f"Login utente con email {userLogin2['email']} e password {userLogin2['password']}") 
userLoginQuery = f""" SELECT * 
    FROM USER 
    WHERE id = (
        SELECT user_id 
        FROM LOGIN 
        WHERE email = '{userLogin2['email']}' AND 
        password = '{userLogin2['password']}'
    )"""
data = cursor.execute(userLoginQuery)
for row in data: 
    print(row) 
print("") 

# Get dati utente dopo login
print(f"Get dati utente dopo login") 
userLoginQuery = f""" SELECT 
    USER.id AS ID,
    USER.name AS NOME,
    USER.surname AS COGNOME,
    LOGIN.email AS EMAIL
    FROM USER 
    FULL JOIN LOGIN
    ON USER.id = LOGIN.user_id
    WHERE USER.id = (
        SELECT user_id 
        FROM LOGIN 
        WHERE email = '{userLogin2['email']}' AND 
        password = '{userLogin2['password']}'
    )"""
data = cursor.execute(userLoginQuery)
for row in data: 
    print(row) 
print("") 

# Query attività RUNNING
print(f"Attività prenotabili di RUNNING") 
# userLoginQuery = f""" SELECT 
#     ACT.id as ID,
#     ACT.date as DATA, 
#     (
#         SELECT count(time) 
#         FROM ACTIVITY as ACTIVITY2
#         WHERE ACT.company_id = ACTIVITY2.company_id
#     ) as ORARI,
#     COMPANY.name as PALESTRA
#     FROM ACTIVITY as ACT
#     LEFT JOIN COMPANY
#     ON ACT.company_id = COMPANY.id
#     WHERE ACT.sport = 'RUNNING'
#     GROUP BY ACT.date"""
userLoginQuery = f""" SELECT 
    ACT.id as ID,
    ACT.date as DATA, 
    (
        SELECT GROUP_CONCAT(time, '; ') 
        FROM ACTIVITY
        WHERE ACT.date = ACTIVITY.date
    ) as ORARI,
    COMPANY.name as PALESTRA
    FROM ACTIVITY as ACT
    LEFT JOIN COMPANY
    ON ACT.company_id = COMPANY.id
    WHERE ACT.sport = 'RUNNING'
    GROUP BY ACT.date"""
data = cursor.execute(userLoginQuery)
for row in data: 
    print(row) 
print("") 

# Query di tutte le attività
print(f"Query di tutte le attività") 
# userLoginQuery = f""" SELECT 
#     ACT.id as ID,
#     ACT.date as DATA, 
#     (
#         SELECT count(time) 
#         FROM ACTIVITY as ACTIVITY2
#         WHERE ACT.company_id = ACTIVITY2.company_id
#     ) as ORARI,
#     COMPANY.name as PALESTRA
#     FROM ACTIVITY as ACT
#     LEFT JOIN COMPANY
#     ON ACT.company_id = COMPANY.id
#     WHERE ACT.sport = 'RUNNING'
#     GROUP BY ACT.date"""
userLoginQuery = f""" SELECT 
    ACT.id as ID,
    ACT.sport as SPORT,
    ACT.date as DATA, 
    (
        SELECT GROUP_CONCAT(time, '; ') 
        FROM ACTIVITY
        WHERE ACT.date = ACTIVITY.date
    ) as ORARI,
    COMPANY.name as PALESTRA
    FROM ACTIVITY as ACT
    LEFT JOIN COMPANY
    ON ACT.company_id = COMPANY.id
    GROUP BY ACT.date"""
data = cursor.execute(userLoginQuery)
for row in data: 
    print(row) 
print("") 

# Query feedback di una palestra
print(f"Query feedback di una palestra") 
userLoginQuery = f""" SELECT 
    FBCK.score as PUNTEGGIO,
    FBCK.message as MESSAGGIO,
    RESERVATION.activity_id as ATTIVITA,
    RESERVATION.user_id as UTENTE,
    (
        SELECT COMPANY.id
        FROM COMPANY
        FULL JOIN ACTIVITY
        WHERE COMPANY.id = ACTIVITY.company_id AND
        ACTIVITY.id = RESERVATION.activity_id
    ) as ID_PALESTRA,
    (
        SELECT name
        FROM COMPANY
        FULL JOIN ACTIVITY
        WHERE COMPANY.id = ACTIVITY.company_id AND
        ACTIVITY.id = RESERVATION.activity_id
    ) as NOME_PALESTRA
    FROM FEEDBACK AS FBCK
    LEFT JOIN RESERVATION
    ON FBCK.reservation_id = RESERVATION.id
    WHERE ID_PALESTRA = 2
    """
data = cursor.execute(userLoginQuery)
for row in data: 
    print(row) 
print("") 



print("Table is Ready")

connection.commit()
 
# Close the connection
connection.close()

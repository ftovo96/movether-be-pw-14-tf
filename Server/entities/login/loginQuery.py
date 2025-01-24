import sqlite3
from entities import config

# Verifica le credenziali dell'utente. Se sono giuste vengono
# restituiti i dati dell'utente.
def login(email, password):
    connection = sqlite3.connect(config.databaseName)
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
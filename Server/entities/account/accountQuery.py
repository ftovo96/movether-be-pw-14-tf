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

# Crea un nuovo account.
# Se creato vengono restituiti i dati dell'utente.
def createAccount(name, surname, email, password):
    connection = sqlite3.connect(config.databaseName)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    # Creo utente
    query = f"""
        INSERT INTO USER (name, surname) 
        VALUES (?,?)
    """
    cursor.execute(query, (name, surname))
    # Ottengo dati nuovo utente (mi serve l'id)
    query = f""" SELECT *
        FROM USER
        WHERE id = {cursor.lastrowid}
    """
    cursor.execute(query)
    user = cursor.fetchone()
    # Creo il login associato al nuovo utente
    query = f"""
        INSERT INTO LOGIN (user_id, email, password) 
        VALUES (?,?,?)
    """
    cursor.execute(query, (user["id"], email, password))
    connection.commit()
    connection.close()
    result = {
        "id": user["id"],
        "name": name,
        "surname": surname,
        "email": email,
    }
    return result
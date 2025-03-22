import sqlite3
import random
from entities import config

# Restituisce la lista delle palestre
def getCompanies():
    connection = sqlite3.connect(config.databaseName)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    query = f""" SELECT *
        FROM COMPANY
    """
    cursor.execute(query)
    companies = cursor.fetchall()
    connection.close()
    result = []
    for company in companies:
        res = {
            "id": company["id"],
            "name": company["name"],
            "description": company["description"],
        }
        result.append(res)
    return result

# Restituisce la palestra con l'id specificato
def getCompany(companyId):
    connection = sqlite3.connect(config.databaseName)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    query = f""" SELECT * 
        FROM COMPANY 
        WHERE id = '{companyId}'"""
    cursor.execute(query)
    company = cursor.fetchone()
    connection.close()
    if company:
        return {
            "id": company["id"],
            "name": company["name"],
            "description": company["description"],
        }
    else:
        return None

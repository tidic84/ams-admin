import sqlite3
import os
import sys
from datetime import datetime, timedelta
import json

def connect_to_db():
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'archivage/archive.db')
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"Erreur de connexion à la base de données: {e}")
        sys.exit(1)

def fetch_last_data():
    conn = connect_to_db()
    cursor = conn.cursor()

    cursor.execute("SELECT MAX(timestamp) as latest_time FROM sondes")
    result = cursor.fetchone()
    latest_time = (datetime.fromisoformat(result['latest_time']) - timedelta(minutes=1))

    query = """
    SELECT * FROM sondes 
    WHERE timestamp >= ?
    ORDER BY timestamp DESC
    """
    cursor.execute(query, (latest_time,))
    crises_data = cursor.fetchall()
    print(f"Enregistrements: {len(crises_data)}")

    filtered = []
    for row in crises_data:
        try:
            row_dict = dict(row)
            if isinstance(row_dict['data'], str):
                filtered.append({
                    **row_dict,
                    "data": json.loads(row_dict['data'])
                })
        except (json.JSONDecodeError, ValueError, KeyError) as e:
            print(f"Erreur traitement: {row}, erreur : {e}")
    return filtered

def fetch_data():
    conn = connect_to_db()
    cursor = conn.cursor()

    query = """
    SELECT * FROM sondes 
    ORDER BY timestamp DESC
    """
    cursor.execute(query)
    crises_data = cursor.fetchall()
    print(f"Enregistrements: {len(crises_data)}")

    filtered = []
    for row in crises_data:
        try:
            row_dict = dict(row)
            if isinstance(row_dict['data'], str):
                filtered.append({
                    **row_dict,
                    "data": json.loads(row_dict['data'])
                })
        except (json.JSONDecodeError, ValueError, KeyError) as e:
            print(f"Erreur traitement: {row}, erreur : {e}")
    return filtered

def fetch_alert():
    conn = connect_to_db()
    cursor = conn.cursor()

    query = """
    SELECT * FROM cert_alert
    ORDER BY date DESC
    LIMIT 1
    """

    cursor.execute(query)

    result = cursor.fetchone()
    if result:
        return dict(result)
    return None

if __name__ == "__main__":
    res = {
        "last_data": fetch_last_data(),
        "data": fetch_data(),
        "alert": fetch_alert()
    }
    print(json.dumps(res))
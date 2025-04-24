import datetime
import json
import os
import subprocess
import sys 

def archiv_alert(conn, alert):
    cursor = conn.cursor()
    alert['date_archiv'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    cursor.execute("SELECT * FROM cert_alert WHERE id = ?", (alert['id'],))
    existing = cursor.fetchone()
    
    if existing:
        cursor.execute('''
        UPDATE cert_alert 
        SET title = ?, date = ?, status = ?, date_archiv = ?
        WHERE id = ?
        ''', (alert['title'], alert['date'], alert['status'], alert['date_archiv'], alert['id']))
        print(f"Alerte {alert['id']} mise à jour")
    else:
        cursor.execute('''
        INSERT INTO cert_alert (id, title, date, status, date_archiv)
        VALUES (?, ?, ?, ?, ?)
        ''', (alert['id'], alert['title'], alert['date'], alert['status'], alert['date_archiv']))
        print(f"Nouvelle alerte {alert['id']} ajoutée à la base de données")
    
    conn.commit()


def clean_old_alert(conn, days_to_keep=30):
    cursor = conn.cursor()
    
    limit_date = (datetime.datetime.now() - datetime.timedelta(days=days_to_keep)).strftime('%Y-%m-%d %H:%M:%S')
    
    cursor.execute("SELECT id FROM cert_alert WHERE date_archiv < ?", (limit_date,))
    old_alert = cursor.fetchall()
    
    if old_alert:
        cursor.execute("DELETE FROM cert_alert WHERE date_archiv < ?", (limit_date,))
        conn.commit()
        print(f"{len(old_alert)} alertes obsolètes supprimées")


def get_all_alert(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, date, status, date_archiv FROM cert_alert ORDER BY date_archiv DESC")
    
    alert = []
    for row in cursor.fetchall():
        alert.append({
            'id': row[0],
            'title': row[1],
            'date': row[2],
            'status': row[3],
            'date_archiv': row[4]
        })
    
    return alert 

def parse():
    try:
        result = subprocess.run(['python3', os.path.join(os.path.dirname(__file__), '../parser/cert.py')], 
                       capture_output=True, text=True)
        return json.loads(result.stdout)
    except Exception as e:
        print(f"Erreur lors de l'exécution du parser: {e}", file=sys.stderr)
        return None
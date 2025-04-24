import sqlite3
import os
import alert as cert
import sondes as sond

def init_database(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cert_alert (
        id TEXT PRIMARY KEY,
        title TEXT,
        date TEXT,
        status TEXT,
        date_archiv TEXT
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sondes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sonde_name TEXT,
        data TEXT,
        timestamp TEXT,
        hostname TEXT
    )
    ''')
    
    conn.commit()
    return conn

def main():
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'archive.db')
    conn = init_database(db_path)
    try:
        alert = cert.parse()
        
        if alert:
            cert.archiv_alert(conn, alert)
            print(f"Archivage de l'alerte CERT terminé.")
        else:
            print("Aucune alerte CERT.")
        
        sondes_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../sondes')
        sondes = sond.discover_sondes(sondes_dir)
        if sondes:
            for sonde_path in sondes:
                sonde_name = os.path.basename(sonde_path)                
                data = sond.execute_sonde(sonde_path)
                if data:
                    sond.archiv_sondes(conn, sonde_name, data)
            
            sond.clean_old_sondes(conn)
            cert.clean_old_alert(conn)
            
            print(f"Archivage terminé.")
        else:
            print("Aucune sonde trouvée")
    finally:
        conn.close()

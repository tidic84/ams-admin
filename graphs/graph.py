import sqlite3
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import json
import sys

def connect_to_db():
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../archivage/archive.db')
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"Erreur de connexion à la base de données: {e}")
        sys.exit(1)

def fetch_cpu_data(conn, days=1):
    cursor = conn.cursor()
    query = """
    SELECT timestamp, json_extract(data, '$.cpu') as cpu_value
    FROM sondes
    WHERE sonde_name = 'cpu.py'
    AND timestamp >= datetime('now', ?)
    """
    params = [f'-{days} days']

    query += " ORDER BY timestamp"
    
    cursor.execute(query, params)
    return cursor.fetchall()

def fetch_ram_data(conn, days=1):
    cursor = conn.cursor()
    query = """
    SELECT timestamp, json_extract(data, '$.ram') as ram_value
    FROM sondes
    WHERE sonde_name = 'ram.py'
    AND timestamp >= datetime('now', ?)
    """
    params = [f'-{days} days']
    
    query += " ORDER BY timestamp"
    
    cursor.execute(query, params)
    return cursor.fetchall()

def fetch_disk_data(conn, days=1):
    cursor = conn.cursor()
    query = """
    SELECT timestamp, json_extract(data, '$.disk') as disk_value
    FROM sondes
    WHERE sonde_name = 'disk.py'
    AND timestamp >= datetime('now', ?)
    """
    params = [f'-{days} days']

    query += " ORDER BY timestamp"
    
    cursor.execute(query, params)
    return cursor.fetchall()

def generate_graphs(days=1):
    conn = connect_to_db()
    try:
        cpu_data = fetch_cpu_data(conn, days)
        ram_data = fetch_ram_data(conn, days)
        disk_data = fetch_disk_data(conn, days)
        
        output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img')
        os.makedirs(output_dir, exist_ok=True)
        
        title_suffix = f"({days} {'jour' if days == 1 else 'jours'})"
        
        if cpu_data:
            times_cpu = [datetime.fromisoformat(row['timestamp']) for row in cpu_data]
            values_cpu = [row['cpu_value'] for row in cpu_data]
            
            plt.figure(figsize=(12, 6))
            plt.plot(times_cpu, values_cpu, 'r-', label='Utilisation CPU (%)')
            plt.title(f"Utilisation CPU {title_suffix}")
            plt.xlabel('Date et heure')
            plt.ylabel('Pourcentage (%)')
            plt.grid(True)
            plt.ylim(0, 100)
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
            plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
            plt.gcf().autofmt_xdate()
            plt.legend()
            
            filename = f"cpu.png"
            plt.savefig(os.path.join(output_dir, filename))
            plt.close()
            print(f"Graphique CPU généré: {filename}")
        
        if ram_data:
            times_ram = [datetime.fromisoformat(row['timestamp']) for row in ram_data]
            values_ram = [row['ram_value'] for row in ram_data]
            
            plt.figure(figsize=(12, 6))
            plt.plot(times_ram, values_ram, 'b-', label='Utilisation RAM (%)')
            plt.title(f"Utilisation RAM {title_suffix}")
            plt.xlabel('Date et heure')
            plt.ylabel('Pourcentage (%)')
            plt.grid(True)
            plt.ylim(0, 100)
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
            plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
            plt.gcf().autofmt_xdate()
            plt.legend()
            
            filename = f"ram.png"
            plt.savefig(os.path.join(output_dir, filename))
            plt.close()
            print(f"Graphique RAM généré: {filename}")
        
        if disk_data:
            times_disk = [datetime.fromisoformat(row['timestamp']) for row in disk_data]
            values_disk = [row['disk_value'] for row in disk_data]
            
            plt.figure(figsize=(12, 6))
            plt.plot(times_disk, values_disk, 'g-', label='Utilisation Disque (%)')
            plt.title(f"Utilisation Disque {title_suffix}")
            plt.xlabel('Date et heure')
            plt.ylabel('Pourcentage (%)')
            plt.grid(True)
            plt.ylim(0, 100)
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
            plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
            plt.gcf().autofmt_xdate()
            plt.legend()
            
            filename = f"disk.png"
            plt.savefig(os.path.join(output_dir, filename))
            plt.close()
            print(f"Graphique Disque généré: {filename}")        
    finally:
        conn.close()

def main():    
    try:
        with open(os.path.join(os.path.dirname(__file__), 'config.json'), 'r') as f:
            config = json.load(f)
    except Exception as e:
        print(f"Erreur lecture config: {e}")
        return []
    
    generate_graphs(config.get('days', 1))
    print("Génération des graphiques terminée.")

if __name__ == "__main__":
    main()
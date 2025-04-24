import glob
import subprocess
import json
import datetime
import os
import sys

def discover_sondes(sondes_dir):
    py_sondes = glob.glob(os.path.join(sondes_dir, "*.py"))
    sh_sondes = glob.glob(os.path.join(sondes_dir, "*.sh"))
    return py_sondes + sh_sondes

def execute_sonde(sonde_path):
    try:
        if sonde_path.endswith('.py'):
            result = subprocess.run(['python3', sonde_path], capture_output=True, text=True)
        elif sonde_path.endswith('.sh'):
            result = subprocess.run(['bash', sonde_path], capture_output=True, text=True)
        else:
            return None
        
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        print(f"Erreur {sonde_path}: JSON valide.")
        return None
    except Exception as e:
        print(f"Erreur {sonde_path}: {e}")
        return None

def archiv_sondes(conn, sonde_name, data):
    cursor = conn.cursor()
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    hostname = os.uname()[1]
    
    cursor.execute('''
    INSERT INTO sondes (sonde_name, data, timestamp, hostname)
    VALUES (?, ?, ?, ?)
    ''', (sonde_name, json.dumps(data), timestamp, hostname))
    
    conn.commit()
    print(f"{sonde_name} stockée")

def clean_old_sondes(conn, days_to_keep=7):
    cursor = conn.cursor()
    limit_date = (datetime.datetime.now() - datetime.timedelta(days=days_to_keep)).strftime('%Y-%m-%d %H:%M:%S')
    
    cursor.execute("SELECT COUNT(*) FROM sondes WHERE timestamp < ?", (limit_date,))
    count = cursor.fetchone()[0]
    
    if count > 0:
        cursor.execute("DELETE FROM sondes WHERE timestamp < ?", (limit_date,))
        conn.commit()
        print(f"{count} lignes supprimées")
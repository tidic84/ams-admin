import sqlite3
import os
from datetime import datetime, timedelta
import json
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'mail'))
from sendmail import sendMail

def detect_crises(db_path):
    try:
        with open(os.path.join(os.path.dirname(__file__), 'config.json'), 'r') as f:
            config = json.load(f)
    except Exception as e:
        print(f"Erreur lecture config: {e}")
        return []
    try:
        with sqlite3.connect(db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute("SELECT MAX(timestamp) as latest_time FROM sondes")
            result = cursor.fetchone()
            latest_time = (datetime.fromisoformat(result['latest_time']) - timedelta(minutes=1))

            query = """
            SELECT * FROM sondes 
            WHERE timestamp >= ?
            AND (json_extract(data, '$.cpu') > ? 
                OR json_extract(data, '$.ram') > ?
                OR json_extract(data, '$.disk') > ?)
            ORDER BY timestamp DESC
            """
            cursor.execute(query, (latest_time, config['cpu'], config['ram'], config['disk']))
            crises_data = cursor.fetchall()
            print(f"Enregistrements: {len(crises_data)}")

            filtered_crises = []
            for row in crises_data:
                try:
                    row_dict = dict(row)
                    if isinstance(row_dict['data'], str):
                        filtered_crises.append({
                            **row_dict,
                            "data": json.loads(row_dict['data'])
                        })
                except (json.JSONDecodeError, ValueError, KeyError) as e:
                    print(f"Erreur traitement: {row}, erreur : {e}")

            return filtered_crises

    except sqlite3.Error as e:
        print(f"Erreur accès db: {e}")
        return []

def main():
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../archivage/archive.db')
    crises = detect_crises(db_path)

    if crises:
        print(f"Crises détectées: {len(crises)}")
        
        # Lecture du template
        template_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'template.txt')
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                mail = f.read()
        except FileNotFoundError:
            print("Template non trouvé, utilisation du template par défaut")
            mail = "Une crise a été détectée dans la base de données.\n"
            mail += "Veuillez vérifier la base de données pour plus de détails."

        # Préparation des détails des crises
        crisis_details = ""
        hosts = []
        
        for crisis in crises:
            if 'hostname' in crisis:
                if crisis['hostname'] not in hosts:
                    hosts.append(crisis['hostname'])
                
                data_str = json.dumps(crisis['data'], indent=2) if isinstance(crisis['data'], dict) else str(crisis['data'])
                
                crisis_details += f"Sonde : {crisis.get('sonde_name', 'N/A')}\n"
                crisis_details += f"Date : {crisis.get('timestamp', 'N/A')}\n"
                crisis_details += f"Host : {crisis.get('hostname', 'N/A')}\n"
                crisis_details += f"Données : {data_str}\n\n"

        mail = mail.replace('[DETAILS]', crisis_details)
        mail = mail.replace('[DATE]', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        mail = mail.replace('[HOTES]', ', '.join(hosts))
        mail = mail.replace('[NB_CRISES]', str(len(crises)))

        if hosts:
            subject = "Crise détectée dans "
            for host in hosts:
                subject += host + ", "
            subject = subject[:-2]
            
            print(f"Envoi d'un e-mail d'alerte pour {len(hosts)} hôtes")
            sendMail(subject, mail, "cedricsephanh@gmail.com")
        else:
            print("Aucun hôte spécifié dans les données de crise")
    else:
        print("Aucune crise détectée")
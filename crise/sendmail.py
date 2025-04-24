import smtplib
import ssl
from dotenv import load_dotenv
from email.mime.text import MIMEText
import os

# Charger les variables d'environnement
load_dotenv(os.path.join(os.path.dirname(__file__), '../.env'))

def sendMail(objet, text, email):
    server = smtplib.SMTP(os.environ.get("SMTP_SERVER")+":"+ os.environ.get("SMTP_PORT"))
    login = os.environ.get("SMTP_LOGIN") 
    password = os.environ.get("SMTP_PASSWORD") 

    sender_email = login  
    receiver_email = email 

    message = MIMEText(text, "plain")
    message["Subject"] = objet
    message["From"] = sender_email
    message["To"] = receiver_email

    try:
        server.ehlo()
        server.starttls()
        server.login(login, password)  
        server.sendmail(message["From"], message["To"], message.as_string())   

        print('Mail envoyé.')
    except Exception as e:
        print(f'Erreur envoi mail: {e}')
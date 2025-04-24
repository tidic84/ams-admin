# Projet d'Administration

## Description
Un outil d'administration développé en Python pour gérer et analyser les données.

## Installation
1. Cloner le repository
2. Si requis: Créer un environnement virtuel Python :
```bash
python -m venv venv
source venv/bin/activate
```
3. Installer les dépendances :
```bash
pip install -r requirements.txt
```

## Configuration
Activer le crontab:
```
crontab -e
```
puis inserer cette ligne: le premier chiffre étant les minutes d'intervalle.
```
*/5 * * * * python3 /chemin/vers/main.py >> /chemin/vers/logs.txt
```

Remplir le .env avec les valeurs: 
```
SMTP_LOGIN=<email>
SMTP_PASSWORD=<motdepasse>
SMTP_SERVER=<serveur smtp>
SMTP_PORT=<port smtp>
```

## Utilisation
Pour lancer l'application :
```bash
python3 main.py
```

Pour lancer le serveur web:
```bash
python3 web/server.py
```

## Template pour le mail
```
Il y a [NB_CRISES] crises détectés aujourd'hui le [DATE] sur [HOTES].

Voici les détails: 
[DETAILS]
Veuillez vérifier la base de données pour plus de détails.
```
- `[DETAILS]` affiche l'ensemble des crises avec tous ses détails.
- `[DATE]` affiche la date de l'execution du script avec les secondes.
- `[HOTES]` affiche le ou les hotes qui ont une alerte.
- `[NB_CRISES]` affiche le nombre de crises

## Details des scripts
- `main.py` est exécuté par le crontab et appelle les scripts d'archivage, puis de détection des crises et enfin la génération des graphes.
- - `archivage.py` sert a archiver les données du serveur. Il execute les script sondes et alert
- - ╰ `sondes.py` sert a appeller les sondes dans le dossier sonde.
- - ╰ `alert.py` sert a appeller le parser
- - ╰ -- `cert.py` est un parseur qui va chercher la dernière alert cert
- - `graph.py` génère des graphiques a partir des données de la db.
- - `crises.py` cherche dans la db les alertes récentes qui pourraient depasser le seuil. Et envoie un mail a l'administrateur si la situation est critique.


import os
import sys
import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), 'archivage'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'graph/graph'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'crise'))
import archivage
import graphs.graph as graph
import crise

date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print("\n------------------------------------")
print(f"{date} - Début de l'archivage")
# Archivage
try:
    archivage.main()
except Exception as e:
    print(f"Erreur dans le module archivage: {e}")

# Verifier si il y a une crise
print(f"\n{date} - Début de la vérification de crise")
try:
    crise.main()
except Exception as e:
    print(f"Erreur dans le module crise: {e}")

# Generation du graphique
print(f"\n{date} - Début de la génération du graphique")
try:
    graph.main()
except Exception as e:
    print(f"Erreur dans le module graph: {e}")
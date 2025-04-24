import psutil
import time
import threading
import multiprocessing
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import math
import argparse
import os

# Variables globales pour le suivi
cpu_percentages = []
timestamps = []
test_running = False

def cpu_intensive_task(duration=60, intensity=80):
    """Fonction qui sollicite le CPU à un niveau d'intensité paramétrable"""
    start_time = time.time()
    end_time = start_time + duration
    
    print(f"Démarrage du test CPU pour {duration} secondes avec intensité {intensity}%...")
    
    while time.time() < end_time:
        # Phase de calcul intensif
        work_time = (intensity / 100) * 0.1  # Temps de travail proportionnel à l'intensité
        work_end = time.time() + work_time
        
        while time.time() < work_end:
            # Calculs intensifs
            for i in range(10000):
                math.factorial(100)
                math.sin(i) * math.cos(i)
                pow(i, i % 5)
        
        # Phase de repos si l'intensité est inférieure à 100%
        if intensity < 100:
            sleep_time = 0.1 - work_time
            time.sleep(max(0, sleep_time))
    
    return "Test CPU terminé"

def start_cpu_test(duration, cores, intensity):
    """Démarre le test CPU sur plusieurs cœurs"""
    global test_running
    test_running = True
    
    processes = []
    for i in range(cores):
        p = multiprocessing.Process(target=cpu_intensive_task, args=(duration, intensity))
        processes.append(p)
        p.start()
        print(f"Processus {i+1} démarré")
    
    # Attendre que tous les processus se terminent
    for p in processes:
        p.join()
    
    test_running = False
    print("Test de charge CPU terminé")

def monitor_cpu():
    """Surveille l'utilisation CPU et sauvegarde les données"""
    while True:
        cpu_percent = psutil.cpu_percent(interval=1)
        current_time = time.time()
        
        cpu_percentages.append(cpu_percent)
        timestamps.append(current_time)
        
        # Limiter la taille des listes pour éviter une utilisation mémoire excessive
        if len(cpu_percentages) > 3600:  # Conserver 1 heure de données max
            cpu_percentages.pop(0)
            timestamps.pop(0)
        
        # Si aucun test n'est en cours et qu'on a collecté au moins 10s de données, on peut arrêter
        if not test_running and len(cpu_percentages) > 10:
            break

def save_cpu_graph(output_dir="./graphs"):
    """Sauvegarde un graphique de l'utilisation CPU"""
    os.makedirs(output_dir, exist_ok=True)
    
    # Convertir les timestamps en valeurs relatives (secondes depuis le début)
    relative_times = [t - timestamps[0] for t in timestamps]
    
    plt.figure(figsize=(12, 6))
    plt.plot(relative_times, cpu_percentages, 'r-', label='Utilisation CPU (%)')
    plt.title("Test de charge CPU")
    plt.xlabel('Temps (secondes)')
    plt.ylabel('Utilisation CPU (%)')
    plt.grid(True)
    plt.ylim(0, 100)
    plt.legend()
    
    filename = f"cpu_test_{int(time.time())}.png"
    filepath = os.path.join(output_dir, filename)
    plt.savefig(filepath)
    plt.close()
    print(f"Graphique CPU sauvegardé: {filepath}")

def main():
    parser = argparse.ArgumentParser(description='Outil de test et surveillance CPU')
    parser.add_argument('-d', '--duree', type=int, default=60, 
                        help='Durée du test en secondes (défaut: 60)')
    parser.add_argument('-c', '--coeurs', type=int, default=multiprocessing.cpu_count(),
                        help=f'Nombre de cœurs à utiliser (défaut: {multiprocessing.cpu_count()})')
    parser.add_argument('-i', '--intensite', type=int, default=80,
                        help='Intensité de la charge CPU en pourcentage (défaut: 80)')
    
    args = parser.parse_args()
    
    # Démarrer la surveillance CPU dans un thread séparé
    monitor_thread = threading.Thread(target=monitor_cpu)
    monitor_thread.start()
    
    # Démarrer le test CPU
    start_cpu_test(args.duree, args.coeurs, args.intensite)
    
    # Attendre que la surveillance se termine
    monitor_thread.join()
    
    # Sauvegarder le graphique

if __name__ == "__main__":
    main()
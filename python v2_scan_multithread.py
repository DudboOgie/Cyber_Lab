import socket
import time
from concurrent.futures import ThreadPoolExecutor
from functools import partial

# --- Fonction de scan d'un port unique ---
def scan_port(target, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.1)
    result = s.connect_ex((target, port))
    if result == 0:
        print(f"[+] PORT {port} : OUVERT")
    s.close()

# --- Programme principal ---
print("--- SCANNER DE PORTS V2 (MULTITHREAD) ---")
target = input("Entrez l'IP à scanner : ")

# Chronomètre — on note l'heure de départ
debut = time.time()

print(f"Lancement du scan sur {target} (ports 1-1024)...")

# On fige le paramètre target dans la fonction
scan_cette_cible = partial(scan_port, target)

# On lance 50 threads en parallèle
with ThreadPoolExecutor(max_workers=50) as executor:
    executor.map(scan_cette_cible, range(1, 1025))

# Chronomètre — on calcule le temps écoulé
fin = time.time()
duree = round(fin - debut, 2)

print(f"Scan terminé en {duree} secondes.")
input("Appuyez sur Entrée pour quitter...")

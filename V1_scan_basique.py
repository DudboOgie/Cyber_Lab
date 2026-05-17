import socket

# Configuration de la cible
print("--- SCANNER DE PORTS (LABORATOIRE) ---")
target = input("Entrez l'IP a scanner (ex: 127.0.0.1) : ")

print(f"Lancement du scan sur {target}...")

# Boucle de scan sur les 100 premiers ports
for port in range(1, 101):
    # On cree une "prise" (socket)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.1) # Rapidite du test
    
    # On tente la connexion
    result = s.connect_ex((target, port))
    
    if result == 0:
        print(f"[+] PORT {port} : OUVERT")
    
    s.close()

print("Scan termine.")
input("Appuyez sur Entree pour quitter...")
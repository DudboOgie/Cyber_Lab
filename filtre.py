import socket

# On cree un serveur de filtrage simplifie
def demarrer_filtre():
    # Ecoute sur toutes les interfaces (0.0.0.0) sur un port test (ex: 8080)
    host = '0.0.0.0'
    port = 8080
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(1)
    
    print(f"--- FILTRE ACTIF SUR LE PORT {port} ---")
    print("En attente de donnees a filtrer...")

    while True:
        conn, addr = s.accept()
        data = conn.recv(1024)
        if data:
            # Ici on simule le filtrage : on affiche ce qu'on reçoit
            print(f"[*] Paquet recu de {addr[0]}")
            print(f"[!] Contenu : {data.decode('utf-8', errors='ignore')}")
        conn.close()

if __name__ == "__main__":
    try:
        demarrer_filtre()
    except KeyboardInterrupt:
        print("\nArret du filtrage.")
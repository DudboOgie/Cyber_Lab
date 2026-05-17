import socket
import json
import datetime
from concurrent.futures import ThreadPoolExecutor

def scan_port(target, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        result = s.connect_ex((target, port))
        if result == 0:
            try:
                s.send(b'HEAD / HTTP/1.0\r\n\r\n')
                banner = s.recv(1024).decode('utf-8', errors='ignore').strip()
            except:
                banner = ""
            s.close()
            return {"port": port, "statut": "ouvert", "banner": banner}
        s.close()
        return None
    except:
        return None

def main():
    target = input("Cible a scanner : ")
    print(f"\nDémarrage du scan sur {target}")
    
    debut = datetime.datetime.now()
    resultats = []
    
    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = [executor.submit(scan_port, target, port) for port in range(1, 65536)]
        for future in futures:
            result = future.result()
            if result:
                print(f"[+] PORT {result['port']} : OUVERT | {result['banner'][:50] if result['banner'] else ''}")
                resultats.append(result)
                
    fin = datetime.datetime.now()
    duree = (fin - debut).seconds
    
    horodatage = debut.strftime("%Y%m%d_%H%M%S")
    nom_fichier = f"scan_{target}_{horodatage}.json"
    
    rapport = {
        "cible": target,
        "date": str(debut),
        "duree_secondes": duree,
        "ports_ouverts": len(resultats),
        "resultats": resultats
    }
    
    with open(nom_fichier, 'w') as f:
        json.dump(rapport, f, indent=4)
        
    print(f"\nScan terminé en {duree}s")
    print(f"Ports ouverts : {len(resultats)}")
    print(f"Rapport sauvegardé : {nom_fichier}")

if __name__ == "__main__":
    main()
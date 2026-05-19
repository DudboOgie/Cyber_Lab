import socket
import argparse
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

def scan_port(target, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1.0)
        result = sock.connect_ex((target, port))
        
        if result == 0:
            try:
                sock.send(b"Hello\r\n")
                banniere = sock.recv(1024).decode('utf-8', errors='ignore').strip()
            except Exception:
                banniere = "Inconnue"
                
            sock.close()
            return {"port": port, "statut": "ouvert", "banniere": banniere or "Inconnue"}
        sock.close()
        return None
    except Exception:
        return None

def main(target, ports_range, workers=50):
    try:
        target_ip = socket.gethostbyname(target)
    except socket.gaierror:
        print(f"[-] Impossible de résoudre l'hôte : {target}")
        return

    print("-" * 60)
    print(f" Scan en cours sur la cible : {target_ip} ({target})")
    print(f" Début du scan : {datetime.now()}")
    print("-" * 60)

    if "-" in ports_range:
        debut_p, fin_p = map(int, ports_range.split("-"))
        ports_to_scan = list(range(debut_p, fin_p + 1))
    else:
        ports_to_scan = [int(p) for p in ports_range.split(",")]

    print(f"[+] Volume : {len(ports_to_scan)} ports à analyser | Threads alloués : {workers}")
    
    debut = datetime.now()
    resultats = []

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(scan_port, target_ip, port) for port in ports_to_scan]
        
        for future in futures:
            res = future.result()
            if res:
                print(f"[+] PORT {res['port']:<5} : {res['statut'].upper()} | {res['banniere']}")
                resultats.append(res)

    fin = datetime.now()
    duree = (fin - debut).total_seconds()
    
    print("-" * 60)
    print(f"[+] Scan terminé en {round(duree, 2)} secondes.")
    print(f"[+] Synthèse : {len(resultats)} port(s) identifié(s) ouvert(s).")
    print("-" * 60)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scanner de ports Python optimisé.")
    parser.add_argument("target", help="Hôte cible (IP ou nom de domaine)")
    parser.add_argument("--ports", required=True, help="Ports à scanner (ex: 22,80 ou 1-1024)")
    parser.add_argument("--threads", type=int, default=50, help="Nombre de threads simultanés")
    
    args = parser.parse_args()
    main(args.target, args.ports, args.threads)
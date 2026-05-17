#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import json
import argparse
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

def scan_port(target, port, timeout=0.5):
    """
    Scanne un port TCP unique et tente une capture de bannière (Banner Grabbing).
    Garantit la fermeture de la socket via un gestionnaire de contexte (with).
    """
    # Payload de stimulation par défaut (HTTP)
    payload = b'HEAD / HTTP/1.0\r\n\r\n'
    
    # Utilisation de 'with' pour éviter les fuites de descripteurs de fichiers (file descriptors)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(timeout)
        result = s.connect_ex((target, port))
        
        if result == 0:
            banner = ""
            try:
                # Tentative de stimulation pour obtenir une bannière de couche Application
                s.send(payload)
                banner = s.recv(1024).decode('utf-8', errors='ignore').strip()
            except Exception:
                # Si le protocole n'attend pas de stimulation (ex: SSH), on tente une écoute directe
                try:
                    banner = s.recv(1024).decode('utf-8', errors='ignore').strip()
                except Exception:
                    banner = "Inconnue (Pas de réponse applicative)"
            
            return {
                "port": port,
                "statut": "ouvert",
                "banniere": banner if banner else "Ouvert (Bannière vide)"
            }
    return None

def parse_ports(port_range_str):
    """
    Analyse la chaîne de caractères des ports pour retourner une liste d'entiers.
    Prend en charge les formats : '80', '22,80,443' ou '1-1024'.
    """
    ports = []
    if '-' in port_range_str:
        try:
            start, end = map(int, port_range_str.split('-'))
            ports = list(range(start, end + 1))
        except ValueError:
            raise argparse.ArgumentTypeError(f"Format de plage de ports invalide : {port_range_str}")
    elif ',' in port_range_str:
        try:
            ports = [int(p.strip()) for p in port_range_str.split(',')]
        except ValueError:
            raise argparse.ArgumentTypeError(f"Format de liste de ports invalide : {port_range_str}")
    else:
        try:
            ports = [int(port_range_str)]
        except ValueError:
            raise argparse.ArgumentTypeError(f"Port unique invalide : {port_range_str}")
    return ports

def main(target, port_range, workers, output_file=None):
    """
    Orchestrateur principal du scan réseau.
    Gère la parallélisation et la journalisation des résultats.
    """
    print(f"\n[+] Initialisation de l'audit sur la cible : {target}")
    
    try:
        ports_to_scan = parse_ports(port_range)
    except Exception as e:
        print(f"[-] Erreur de configuration : {e}")
        return

    print(f"[+] Volume : {len(ports_to_scan)} ports à analyser | Threads alloués : {workers}")
    
    debut = datetime.now()
    resultats = []

    # Utilisation de ThreadPoolExecutor pour optimiser les performances d'I/O réseau
    with ThreadPoolExecutor(max_workers=workers) as executor:
        # Cartographie des tâches en tâche de fond
        futures = [executor.submit(scan_port, target, port) for port in ports_to_scan]
        
        for future in futures:
            res = future.result()
            if res:
                print(f"    [!] Port {res['port']} : {res['statut'].upper()} | Bannière : {res['banniere']}")
                resultats.append(res)

    fin = datetime.now()
    duree = (fin - debut).total_seconds()
    
    # Structuration du rapport selon un formalisme d'ingénierie
    rapport = {
        "cible": target,
        "date_generation": str(debut),
        "duree_execution_secondes": round(duree, 2),
        "metriques": {
            "ports_analyses": len(ports_to_scan),
            "ports_ouverts": len(resultats)
        },
        "resultats": resultats
    }

    print(f"\n[+] Scan terminé en {round(duree, 2)} secondes.")
    print(f"[+] Synthèse : {len(resultats)} port(s) identifié(s) ouvert(s).")

    # Logique d'exportation étanche
    if output_file:
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(rapport, f, indent=4, ensure_ascii=False)
            print(f"[+] Succès : Rapport d'audit consigné dans '{output_file}'")
        except IOError as e:
            print(f"[-] Erreur critique lors de l'écriture du rapport : {e}")

if __name__ == "__main__":
    # Configuration du parseur d'arguments CLI (Command Line Interface)
    parser = argparse.ArgumentParser(
        description="Outil d'audit réseau unifié - Scanner de ports TCP multi-threadé avec capture de bannières.",
        epilog="Usage sécurisé dans le cadre de laboratoires de tests ou d'autorisations explicites."
    )
    
    # Définition des commutateurs (arguments)
    parser.add_argument("-t", "--target", required=True, type=str, help="Adresse IP ou FQDN de la cible (Ex: 127.0.0.1)")
    parser.add_argument("-p", "--ports", default="1-1024", type=str, help="Périmètre de ports. Formats acceptés : '80', '22,80,443', '1-1024' (Défaut: 1-1024)")
    parser.add_argument("-w", "--workers", default=50, type=int, help="Capacité de parallélisation / Nombre de threads (Défaut: 50)")
    parser.add_argument("-o", "--output", type=str, help="Chemin d'export du livrable au format JSON (Optionnel)")

    # Extraction des variables saisies par l'opérateur
    args = parser.parse_args()

    # Transmission à l'orchestrateur
    main(
        target=args.target,
        port_range=args.ports,
        workers=args.workers,
        output_file=args.output
    )
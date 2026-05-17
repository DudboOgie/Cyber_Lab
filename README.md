# Laboratoire d'Audit Réseau - Scanner TCP Multi-threadé

## Description du Projet
Ce projet implémente un outil d'audit réseau unifié permettant de cartographier la couche Transport (TCP) d'une cible spécifiée. Développé de manière modulaire, il intègre une logique de parallélisation pour optimiser les performances de scan, une brique de capture de bannières (*banner grabbing*) pour identifier les services applicatifs, et un système d'exportation étanche des artefacts.

## Architecture du Laboratoire
L'environnement est structuré selon les standards d'isolation de l'ingénierie logicielle :

* `src/` : Contient le code source modulaire de l'application (`network_scanner.py`).
* `data/` : Zone étanche locale dédiée à la consignation des rapports d'audit (fichiers `.json`), exclue du suivi de version pour prévenir toute fuite de données (*data leak*).
* `.gitignore` : Configuration des filtres d'exclusion pour Git.

## Fonctionnalités Majeures
1. **Gestion Dynamique des Arguments (CLI) :** Paramétrage complet via le terminal grâce au module `argparse`.
2. **Optimisation I/O Bound :** Utilisation de `ThreadPoolExecutor` pour la parallélisation des requêtes de connexion.
3. **Capture de Bannières (Banner Grabbing) :** Tentative de stimulation applicative pour identifier les versions des services distants.
4. **Fermeture Sécurisée des Ressources :** Implémentation de gestionnaires de contexte (`with`) sur les sockets TCP pour éviter les fuites de descripteurs de fichiers (*file descriptor leaks*).

## Utilisation Opérationnelle

### Prérequis
* Python 3.x
* Environnement Linux / WSL (recommandé)

### Syntaxe des Commandes
L'outil s'exécute à l'aide de commutateurs standards :

```bash
python3 src/network_scanner.py -t <IP_CIBLE> -p <PORTS> -w <THREADS> -o <FICHIER_EXPORT>
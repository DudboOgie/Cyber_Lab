# Laboratoire d'Audit Réseau - Scanner TCP Multi-threadé

## Description du Projet

L'objectif de ce projet est de concevoir un scanner de ports TCP fonctionnel en Python. 
Ce script permet d'analyser une adresse IP ou un nom de domaine cible afin d'identifier les ports ouverts et de déterminer quels services y sont potentiellement actifs.

Dans un premier temps, nous avons configuré l'infrastructure réseau pour tester le script en toute sécurité. 
Nous avons ensuite écrit le code en utilisant la bibliothèque `socket` de Python pour tenter des connexions sur une plage de ports définie.

La suite du projet consiste à optimiser ce scanner en y intégrant le multi-threading afin d'accélérer la vitesse d'exécution des scans, et à ajouter une gestion des erreurs plus robuste pour traiter les cas de timeout ou de ports filtrés.

## Architecture du Laboratoire
L'environnement est structuré selon les standards d'isolation de l'ingénierie logicielle :

* `src/` : Contient le code source modulaire de l'application (`network_scanner.py`).
* `data/` : Zone étanche locale dédiée à la consignation des rapports d'audit (fichiers `.json`), exclue du suivi de version   **  pour empêcher toute fuite de données**.
* `.gitignore` : Configuration des filtres d'exclusion pour Git.

## Fonctionnalités Majeures
1. **Gestion Dynamique des Arguments (CLI) : Paramétrage complet via le terminal grâce au module argparse.
2. **Optimisation I/O Bound : Utilisation de ThreadPoolExecutor pour paralléliser les requêtes de connexion et accélérer le scan.
3. **Capture de Bannières (Banner Grabbing) : Sollicitation applicative pour identifier les versions des services distants.
4. **Fermeture Sécurisée des Ressources : Implémentation de gestionnaires de contexte (with) sur les prises TCP pour éviter les fuites de descripteurs de fichiers.

## Utilisation Opérationnelle

### Prérequis
* Python 3.x
* Environnement Linux / WSL (recommandé)

### Syntaxe des Commandes
L'outil s'exécute à l'aide de commutateurs standards :

```bash
python3 src/network_scanner.py -t <IP_CIBLE> -p <PORTS> -w <THREADS> -o <FICHIER_EXPORT>

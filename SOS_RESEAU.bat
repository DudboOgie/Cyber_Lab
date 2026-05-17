@echo off
echo --- NETTOYAGE RESEAU ET DEV EN COURS ---

:: 1. Fermeture brutale de WSL (souvent le coupable)
wsl --shutdown
echo WSL arrete.

:: 2. Nettoyage du cache DNS
ipconfig /flushdns
echo Cache DNS vide.

:: 3. Reset des interfaces reseau (Winsock)
netsh winsock reset
netsh int ip reset
echo Interfaces reseau reinitialisees.

echo ---------------------------------------
echo NETTOYAGE TERMINE ! 
echo CONSEIL : Redemarrez votre ordinateur maintenant.
pause
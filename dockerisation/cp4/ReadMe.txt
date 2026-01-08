Jusqu'à maintenant (cp1-cp3), on téléchargeait à chaque fois le modèle et toutes les ressources dès qu'on demandait à notre programme de se configurer. On voudrait donc mettre en place un système de cache pour éviter les appels réseaux et téléchargements inutiles.

Le dossier ia/downloads permet de stocker les modèles en local et de les utiliser en priorité. 

Le dossier ia/save permet de stocker la configuration (ce que Google a renvoyé lors du téléchargement des ressources) du modèle.

Les modèles du dossier ia/graphs sont ensuite utilisés s'ils existent déjà.

Ce système de cache est rendu possible par les lignes 129-140 du fichier ia/classify.py

Lorsqu'on lance le serveur, la ligne suivante dans le fichier go : docker run -v ./zzz:/app/saves --name ia ia 
permet de récupérer les modèles dans le répertoire zzz pour les mettre dans le dossier saves du docker

On peut également sur la page web suivant le lien du serveur (par exemple http://172.17.0.2/) pour avoir une partie graphique.

Dossier contenant l'ensemble des étapes pour le TD de mise en production d'un réseau

L'idée générale est de prendre un réseau non personnel et de le transformer

Le réseau provient d'un collab de google
On va le structurer en deux parties : initialisation, classification
On va mettre un serveur web pour l'utiliser
On va le ranger dans un container 
On va mettre un cache pour conserver les poids 
On va construire un frontal en springboot qui va rediriger les requêtes vers le container
On va containeriser le frontal et déployer en docker compose
On va construire dans un container (java et maven disparaissent de la machine hôte)

Il faudra des outils sur la machine et des images à précharger pour gagner du temps
lors des démos.

preload est un script qui va tenter de charger les besoins
deux options exclusives et une obligatoire:
-d : on utilise le docker présent et au pire on charge un docker obsolete (cp7 ne sera pas testable)
-e : on force l'utilisation de docker engine, si une version obsolete est présente on la retire

par defaut on fait aucune option et on affiche le help avec un suicide


-----------------------------------------------------------------------

STRUCTURE DU PROJET :
Chaque dossier cp1-cp7 est un checkpoint, c'est-à-dire une version du projet de cp1 (la moins avancée) à cp7 (la plus avancée).
Dans la racine des dossiers cp1-cp7, il y a un fichier ReadMe.txt avec les commandes à utiliser pour lancer le réseau de neurones ou encore les modifications apportées par rapport à la version suivante ou alors ce qu'il manque à la version actuelle et sera ajoutée à la version suivante (c'est globalement la motivation du checkpoint actuel et du prochain checkpoint).

-----------------------------------------------------------------------

MOTIVATION DU PROJET :
On souhaite industrialiser la mise en route d'un modèle/d'un ensemble de modèles d'IA (ici récupéré sur Tensorflow Hub pour classifier des images) en le mettant dans un docker. On souhaite donc à terme créer un docker avec le modèle et un autre qui récupère les informations saisies par l'utilisateur (notamment l'image qu'il souhaite classifier et le modèle qu'il souhaite utiliser). On souhaite également créer un serveur Springboot sur un docker pour avoir un joli site web pour que l'utilisateur puisse utiliser les modèles d'ia et saisir des informations facilement (l'image à classifier et le modèle utilisé notamment).
On ne souhaite pas s'occuper de la partie "entraînement de l'IA"; on se moque donc de comment elle a été entraînée, on veut simplement pouvoir la configurer initialement et la rendre disponible auprès d'utilisateurs.

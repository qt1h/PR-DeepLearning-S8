Il faut d'abord (télécharger si besoin) et lancer les images nécessaires avec le fichier go dans un terminal:
./go

Ensuite pour lancer le serveur Springboot on peut utiliser la commande docker-compose up

Problème : On souhaite ne rien installer directement sur notre machine pour ne pas la polluer (mais on peut installer les dépendances dans les dockers, ex: Python). Cependant le JDK et JRE Java (qui sont utilisés par Springboot) sont directement inclus dans le docker, on va donc automatiser le téléchargement du jdk (?) et jre nécessaires pour le lancement de notre serveur springboot avant de les compiler dans le docker (comme ça il n'y aura que les fichiers compilés dans notre image, par contre il faut que ça compile correctement sinon le docker aurait des problèmes) --> voir cp7 (notamment le fichier nn/Dockerfile)

Dans le src/java du dossier ia/nn avec le serveur springboot, on ne peut pas mettre les 2 fichiers FirstNNController.java et NNController.java (ils sont dans le dossier assets/) car ils ont tous les 2 les mêmes routages (avec les requêtes classify et validate en POST), on doit donc supprimer l'un des 2 fichiers. On supprime donc le FirstNNController.java comme c'était une implémentation de base un peu naïve du réseau.

Pour installer les dépendances et lancer le serveur springboot : 
cd /home/sombra/Documents/Deep Learning (2A IR S8)/Projet Deep Learning/dockerisation/cp5/ia/nn
mvn package

Il faut lancer le docker avec python dessus :
docker run -p 9081:80 -v ./zzz:/app/saves --name ia ia &

Problème : Springboot ne tourne pas dans un docker, ce sera donc le point d'amélioration de cp6



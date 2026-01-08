On reprend le code du fichier classify.py de cp2/ia et on souhaite configrer un site web qui bascule entre configuration du réseau de neurones et classification (envoi d'une image par un utilisateur dans le réseau de neurones). Pour cela le prof utilise flask (il aurait pu utiliser Django mais trop lourd pour ce projet...).

On peut utiliser 2 commandes spéciales en envoyant des requêtes POST au serveur s'il tourne :
	On lance le serveur avec un terminal et le fichier "go" : ./go
	Dans un autre terminal, on peut utiliser les commandes :
		curl -X POST http://172.17.0.2/config					// Permet de configurer le réseau de neurones (?)
		curl -X POST http://172.17.0.2/validate					// Permet de classifier l'image choisie par défaut, permet de tester rapidement le réseau de neurones
		curl -X POST http://172.17.0.2/validate?id=1				// Permet de classifier l'image avec id=1 (elle est sélectionnée à partir du tableau validation_image_map dans le fichier main.py du dossier cp3/ia )
		curl -X POST http://172.17.0.2/validate?id=2
		curl -X POST -F '@picture=banana.jpg' http://172.17.0.2/classify	// Permet de classifier une image (ici on prend l'image banana.jpg à la racine du dossier dockerisation). /!\ Le lien devrait marcher mais il doit y avoir une faute de frappe dans l'argument de la picture

# Le jeu du Président

## Contexte

Ce jeu est le résultat d'un projet Python de B3 collaboratif, réalisé à 2 personnes.
L'objectif était de programmer un jeu du président et de produire une interface, a minima 
en ligne de commande.
Il était évalué notre maîtrise de la Programmation Orientée Objet en Python, notre
capacité à produire du code propre et structuré. Des points étaient rajoutés si nous
mettions en place une batterie de tests unitaires conséquente, une interface graphique,
ou une base de données.

## Règles du jeu

Le président (aussi appelé le troufion) est un jeu de cartes rapide et amusant, au cours duquel la hiérarchie des joueurs changera à chaque manche. Le vainqueur d'une manche devient le président, alors que le perdant est proclamé troufion. Une fois que vous maitriserez les règles de base, vous pourrez essayer différentes variantes de ce jeu très populaire. <br>
Règles du jeu :

 - Ce jeu se joue de 3 à 6 joueurs.
 - Lors du premier tour, le joueur possédant la dame de coeur commence.
 - L'ensemble des cartes sont distribuées aux joueurs de la manière la plus homogène.
 - Ce jeu se joue par tours. Tant que quelqu'un peut et veut jouer, le tour continue et tourne dans le sens horaire.
 - Le premier joueur choisit des cartes d'une même valeur et les pose sur la tables.
 - Suite à celà, chaque joueur doit fournir autant de cartes que le joueur précédent des cartes dun' valeur supérieure ou égale.
 - Un joueur a le droit de sauter son tour et reprendre le tour d'après.
 - Un tour est fini lorsque plus personne ne joue. C'est alors le dernier à avoir joué qui ouvre la manche suivante. Ou si un joueur pose un ou plusieurs deux. Ce qui mets immédiatement fin au tour.
 - L'objectif est d'être le premier à ne plus avoir de cartes. Ce joueur est alors déclaré président de la manche.
 - Les joueurs restants continuent à jouer jusqu'à ce qu'il n'y ait plus qu'une joueur qui ait des cartes en main, il est alors déclaré 'troufion'

On décide alors ou non de jouer une nouvelle manche. Ce sera le troufion qui ouvrira la partie.

## Organisation du code

L'application est divisée en 3 couches (modèle, vue et contrôleur). L'utilisation d'un tel
_design pattern_ permet de bien cloisonner les différentes fonctionnalités de l'application.
Cela permet d'avoir, par exemple, une couche métier indépendante de la couche interface utilsateur.
On peut donc plus facilement ajouter une autre interface que celle déjà présente, sans avoir 
à se soucier de la logique métier.

#### Le model (_model.py_)

Il contient la logique métier. Toutes les classes qui permettent de décrire l'état du jeu
(_Card_, _Trick_, _PresidentGame_,...), ainsi que les méthodes qui modifient cet état
(ajouter des cartes à un joueur, ajouter des cartes au pli en cours,...). <br>

#### Le controller (_controller.py_)

Il traite les informations transmises par les utilisateurs au _model_ et retourne la 
réponse, sous forme d'un Data Transfer Object (DTO), ou les erreurs à l'utilisateur.
L'utilisation d'un DTO permet de ne retourner que l'information strictement nécessaire
à l'affichage de la partie et non pas tout le jeu. On interdit ainsi que l'utilisateur
puisse modifier les informations de jeu en accédant à l'objet jeu (_PresidentGame_)
directement.

#### La view (_view.py_)

L'interface utilisateur est en ligne de commande. Elle gère l'interaction avec l'utilisateur
et transmet la requête au controller.

#### Autres

On définit par ailleurs des exceptions spécifiques aux erreurs que peut faire l'utilisateur 
(envoi d'une requête qui n'est pas valable dans la forme ou qui ne respecte pas les règles du jeu)
dans _exception.py_.

On implémente la gestion de ces erreurs dans le fichier _util.py_.

Dans _main.py_, on instancie une interface en ligne de commande pour lancer le jeu.

## États du jeu actuellement (09/12/2023) et fix à apporter

- Tous les éléments de la classe métier sont présents. Il n'y a rien à ajouter pour que
le jeu puisse marcher dans une première version (sans règle additionnelle).
- Le jeu se lance, demande aux utilisateurs s'ils veulent jouer ou passer, mais des bugs
continuent d'exister au niveau du _controller_ et du _model_, faisant planter le jeu
assez rapidement. La première chose à faire est de fix ces bugs pour qu'une partie puisse
se terminer.
- Il n'existe pas actuellement de menu qui permette de paramétrer sa partie. Il faudrait
donc implémenter des classes _CommandLineMenu_ et _MenuController_ qui permettent à 
l'utilisateur de choisir le nombre de joueurs que l'utilisateur veut pour sa partie et en
combien de manches il veut jouer.
- Il faudrait également ajouter des tests unitaires, notamment pour le modèle et le contrôleur.
Il y a peu de tests sur les classes et méthodes du modèle et aucune sur le contrôleur.
- Une simple interface en ligne de commandes, c'est un peu triste et il faudrait ajouter
une interface graphique (avec Pygame, Qt ou Tkinter).

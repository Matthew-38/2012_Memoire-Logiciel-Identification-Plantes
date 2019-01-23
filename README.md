# 2012_Memoire-Logiciel-Identification-Plantes
Pour mon mémoire de L4, j'ai programmé un logiciel prototype en Python pour l'identification des plantes

# Contexte
Il s'agit de mon projet de mémoire pour mon quatrième et dernière année de Licence Science à NUI Galway. Cependant cette version n'est pas la même. Après mes examens et ma soutenance de mémoire , j'ai décidé de réecrire et améliorer ce logiciel afin de le rendre plus utile, surtout en prennant compte des suggestions et critiques que j'ai eu dans la soutenance. 
Et lorsque le prototype pour mon mémoire comprennait comme exemple les espèces de la famille Fabaceae, pour la deuxième version, j'ai choisit un groupe plus divers : les arbres et arbrisseaux de l'Irlande. 

# Usage

Pour lancer cette programme Python, il faut obligatoirement avoir Python Imaging Library (PIL, et non pas PILLOW) et Tkinter installé. J'ai essayé de faire en sorte que le logiciel marche dans Python 2.7 et 3.4 mais l'installation de PIL n'est pas la même dans les deux cas :

Python 2.7 : sudo apt-get install python-pil
Python3 : sudo apt-get install python3-pil.imagetk

Pour Windows, il existe une version un peu different (pour que certaines fonctionallités comme le scroll souris marchent). Merci de me demander si vous avez pas Linux et vous voulez tester ceci. Mais si vous voulez le voir marcher simplement, vous pouvez télécharger le binaire Windows dans le fichier ZIP. Avec ceci vous voyez pas le code, mais l'avantage est qu'il n'y a pas besoin d'installer des modules/bibliothèques etc. 

# Tutoriel
1. Admettons qu'on as un arbre comme ceci : https://cdn11.bigcommerce.com/s-999jbj41m8/products/112/images/3162/beech__24524.1483234259__00225.1515640010.500.750.jpg
Avec des feuilles comme ceux-ci : www.organicfacts.net/wp-content/uploads/beechtree.jpg
Et qu'on veut l'identifier. Or on sait déjà que ça appartient à l'ordre Fagales.
2. Commencez la programme (voir Usage plus haut).
3. Sur la liste gauche, on va selectionner des characters. Premièrement "Fagales" comme Order. Puis "tree" comme structure.
4. En consultant la deuxième image, on peut constater quelques choses sur les feuilles. Premièrement la forme elliptique. En défilant la liste, vous trouverez Leaf comme titre de section. Cliquer sur + pour montrer les options. Maintenant plus loin on trouve "Lf(let) Shape" (explication d'anglais : leaf (lf pour court)=feuille, leaflet=foliole (petite feuille)). Dans les options, on peut cliquer sur Chooser pour ouvrir une nouvelle fenêtre avec le choix de forme. On peut donc choisir Eliptic et "Okay" pour revenir. 
5. Vous constaterez déjà que la liste des "Possible Species" change. Celles qui devient orange ou rouge sont moins probable. On va essayer d'éliminter autant que possible.
6. Encore dans la section Leaf, on va cliquer sur "unsure" à côté de Leaves. Ici on a quelques images qui s'affiche, mais rien ne correspond à notre image, donc on choisit "Definitely Not Listed", Okay.
7. Enfin, un dernier : Sous Leaf Observation : None of the above.
8. Maintenant il reste seulement une option verte comme espèce. Mais déjà on peut cliquer sur les autres pour voir leur image, et puis "Highlight Mismatching Characters" pour voir ce qui ne correspond pas en Orange (c'est pas toujours visible dans la fenêtre principale, donc essayez plusieurs).
9. Enfin cliquer sur Fagus sylvatica et View Details. Dans la nouvelle fenêtre on peut voir que les photos correspond, et on peut lire quelques informations dessous. Il s'agit bien de beech (l'hêtre). Dans la liste des espèces semblable, on trouve Carpinus betulus, et c'est vrai que les gens prennent ce dernier pour des hêtres. Plus bas, on à la possibilité de comparer l'hêtre avec des autres espèces. Je vous invite à selectionner "Carpinus betulus". On voit les caracters semblables en vert, les autres en blanc.
10. Merci de me signaler des bugs ou problèmes que vous trouvez. 

# Porting pour version 3
Quand j'écrivais le code de cette programme, ce n'étais pas facile d'installer PIL pour Python 3, donc j'ai fait le choix d'utiliser Python 2.7. Mais maintenant je voulais le rendre compatible avec les deux, ce qui n'est pas très compliqué. Il faut faire un "try...except ImportError:.." pour les modules à importer avec les versions correspondantes à chaque version de Python. Ici on peut trouver une liste de modules avec les équivalents dans chaque version : http://python3porting.com/stdlib.html

Puis il faut s'assurer de quelques autres petits trucs, par exemple devision "/" en Python 2.7 donne un int, mais en Python 3, ça donne un float. Pour un int dans les deux cas, il suffit d'utiliser "//" partout. 

# Limitations
Il me semble que j'étais trop ambitious avec ce projet, et j'ai mis tant de caractères et de fonctionalités dedans qu'il n'est pas si évident non seulement de l'utiliser, mais aussi ça augment le travail de définir les profils pour chaque espèce. En somme ce projet est beaucoup plus grand que je n'avais imaginé. Pour l'amèner à quelque chose de vraiment utile, il faudrait :
1. Y consacrer beaucoup, beaucoup de temps
2. Mettre en ordre le code que j'ai écrit, éliminer les bugs, le rendre plus stable etc.
3. Passer de Tkinter à un autre GUI plus moderne pour que ça soit plus attractif. 

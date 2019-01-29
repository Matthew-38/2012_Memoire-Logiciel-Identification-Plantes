# Bachelor Thesis Project - A plant Identification Programme in Python
For my Bachelor Thesis at the end of my 4th year of science at NUI Galway, in 2012, I programmed a desktop application prototype in Python for helping identify plants.
[Version française en bas]

# Background
The version here is an updated version (June 2012). After my exams and thesis submission, I decided to recreate and improve this application to make it more useful, especially by taking into consideration the suggestions and feedback from the examinors. Whereas the prototype for my thesis used as pilot plant group the species of Fabaceae found in Ireland, for this second version I chose a more diverse group: Irish shrubs and trees in general.

# Usage
Two options exist, as a binary under Windows (recommended for testing), or using Python interpreter for the source code, under Linux

1. Windows Binary
To run this program and see what it is like, download the ZIP file containing the binary (FloraDiversa.exe) and complementary files, unzip them and run the exe. No special libraries are need, all is included.

2. Linux (as source code)
To launch this Python program as source, it is essential to have Python Imaging Library (PIL, not PILLOW) and Tkinter installed. I tried to make it so that this application will work with both Python 2.7 and Python 3.4, but the installation of PIL is not the same in both cases:

Python 2.7 : sudo apt-get install python-pil
31
Python 3 : sudo apt-get install python3-pil.imagetk

For the windows _source_, I have a separate file (not included), which allows functions like correct mouse wheel scrolling. If you want to test this under Windows as source (with the libraries installed), let me know and I can add the Windows source code.

# Tutorial
1. Let's suppose that we have a tree like in this image: https://cdn11.bigcommerce.com/s-999jbj41m8/products/112/images/3162/beech__24524.1483234259__00225.1515640010.500.750.jpg
With leaves like these: www.organicfacts.net/wp-content/uploads/beechtree.jpg
And we want to identify it. But we already know it belongs to the order Fagales.
2. Start the program (see instructions above)
3. In the list on the left, we are going to select the characters which correspond. Firstly, "Fagales" as the answer for Order. Then "tree" as structure.
4. Looking at the second image, we can note a few things about the leaves. Firstly their form is elliptic. Scrolling down, we can find the section for Leaf, and expanding it we can choose "Lf(let) Shape" (=leaf or leaflet). Clicking on "Chooser" opens a new window with images. We can then choose the one corresponding ("Elliptic"). Click ok to return.
5. You will have already noticed the list of possible species (right) changes. Some become orange or red (indicating decreased probability). We will try to eliminate some more.
6. Still under the section of "Leaf", we can click on "Unsure" to the right of "Leaves", at the beginning. This also opens a new window, allowing us to compare with some images presented. We can then observe that none seem to match, so select "Definitely Not Listed". Okay.
7. And one more: Under "Leaf Observations", "None of the above"
8. Now there remains just one green option. But we can click on the others (orange, red) to see their image. Further we can click "Highlight mismatching characteristics" to see why this species is selected against by which characters (the characters are not always visable in the current view on the left, so try a few species to get the idea).
9. Finally click on "Fagus sylvatica" in green, and click details to open a new window. Here we can see that the photos correspond. It is indeed the beech tree. We can also see the similar species, including Carpinus betulus (it is a common mixup, people thinking that this is a beech). Below we have the possibility to compare the beech with another species. I suggest you try to compare it with Carpinus betulus. You will see the characters which are similar highlighted in green, the others in white. It turns out they are not actually that similar!
10. Let me know if you have any difficulties, or you find some bugs.

# Porting for Python 3
When I was writing this second version of the application, it was not easy to install PIL for Python 3. So I converted my code to make it work with Python 2.7. But now I would like to make it compatible with both, so that you can try it most easily. This turns out to not be so difficult. Firstly it is important to import equivalent libraries (which have different names), using a "try...except ImportError:.." statement. Here you can find a list of equivalents for each version of Python: http://python3porting.com/stdlib.html

There are several other important things to adjust too. For example, dedision with "/" in Python 2.7 gives an int, but in Python 3 it gives a float (which causes problems if it is then used as an index of a list, for example!). To get around this, we can just use "//" everywhere, which will always return an int (rounded). 

The result is a version of code which works with both Python versions!

# Limitations
It seems that I was too ambitious with this project, and I put so many characters for each plant, and so many application features, that it is not so easy to use the application, but also it increases hugely the work needed to define the profiles of each species. The result was much bigger than I had imagined. So, to make this application really useful, I would need to:
1. Dedicate much more time. A lot!
2. Organise and clean up the code that I wrote then, remove bugs, add better commentary and make the program more stable.
3. Change the GUI. Tkinter is handy but it would be much nicer with a more modern looking and adaptable GUI, like GTK.


"Normal people... believe that if it ain't broke, don't fix it. Engineers believe that if it ain't broke, it doesn't have enough features yet."
                                                                                                      - Scott Adams

#############################################################################################################################
# [Version Française]


# 2012_Memoire-Logiciel-Identification-Plantes
Pour mon mémoire de L4, j'ai programmé un logiciel prototype en Python pour l'identification des plantes

# Contexte
Il s'agit de mon projet de mémoire pour mon quatrième et dernière année de Licence Science à NUI Galway. Cependant cette version n'est pas la même. Après mes examens et ma soutenance de mémoire , j'ai décidé de réecrire et améliorer ce logiciel afin de le rendre plus utile, surtout en prennant compte des suggestions et critiques que j'ai eu dans la soutenance. 
Et lorsque le prototype pour mon mémoire comprennait comme exemple les espèces de la famille Fabaceae, pour la deuxième version, j'ai choisit un groupe plus divers : les arbres et arbrisseaux de l'Irlande. 

# Usage

Pour lancer cette programme Python, il faut obligatoirement avoir Python Imaging Library (PIL, et non pas PILLOW) et Tkinter installé. J'ai essayé de faire en sorte que le logiciel marche dans Python 2.7 et 3.4 mais l'installation de PIL n'est pas la même dans les deux cas :

Python 2.7 : sudo apt-get install python-pil
Python 3 : sudo apt-get install python3-pil.imagetk

Pour Windows, il existe une version un peu different (pour que certaines fonctionallités comme le scroll souris marchent). Merci de me demander si vous avez pas Linux et vous voulez tester ceci. Mais si vous voulez le voir marcher simplement, vous pouvez télécharger le binaire Windows dans le fichier ZIP. Avec ceci vous voyez pas le code, mais l'avantage est qu'il n'y a pas besoin d'installer des modules/bibliothèques etc. 

# Tutoriel
1. Admettons qu'on as un arbre comme ceci : https://cdn11.bigcommerce.com/s-999jbj41m8/products/112/images/3162/beech__24524.1483234259__00225.1515640010.500.750.jpg
Avec des feuilles comme ceux-ci : www.organicfacts.net/wp-content/uploads/beechtree.jpg
Et qu'on veut l'identifier. Or on sait déjà que ça appartient à l'ordre Fagales.
2. Commencez la programme (voir Usage plus haut).
3. Sur la liste gauche, on va selectionner des characters. Premièrement "Fagales" comme Order. Puis "tree" comme structure.
4. En consultant la second image (lien ci-dessus), on peut constater quelques choses sur les feuilles. Premièrement la forme elliptique. En défilant la liste, vous trouverez Leaf comme titre de section. Cliquer sur + pour montrer les options. Maintenant plus loin on trouve "Lf(let) Shape" (explication d'anglais : leaf (lf pour court)=feuille, leaflet=foliole (petite feuille)). Dans les options, on peut cliquer sur Chooser pour ouvrir une nouvelle fenêtre avec le choix de forme. On peut donc choisir Eliptic et "Okay" pour revenir. 
5. Vous constaterez déjà que la liste des "Possible Species" change. Celles qui devient orange ou rouge sont moins probable. On va essayer d'éliminter autant que possible.
6. Encore dans la section Leaf, on va cliquer sur "unsure" à côté de Leaves. Ici on a quelques images qui s'affiche, mais rien ne correspond à notre image, donc on choisit "Definitely Not Listed", Okay.
7. Enfin, un dernier : Sous Leaf Observation : None of the above.
8. Maintenant il reste seulement une option verte comme espèce. Mais déjà on peut cliquer sur les autres pour voir leur image, et puis "Highlight Mismatching Characters" pour voir ce qui ne correspond pas en Orange (c'est pas toujours visible dans la fenêtre principale, donc essayez plusieurs).
9. Enfin cliquer sur Fagus sylvatica et View Details. Dans la nouvelle fenêtre on peut voir que les photos correspondent, et on peut lire quelques informations dessous. Il s'agit bien de beech (l'hêtre). Dans la liste des espèces semblable, on trouve Carpinus betulus, et c'est vrai que les gens prennent ce dernier pour des hêtres. Plus bas, on à la possibilité de comparer l'hêtre avec des autres espèces. Je vous invite à selectionner "Carpinus betulus". On voit les caracters semblables en vert, les autres en blanc.
10. Merci de me signaler des bugs ou problèmes que vous trouvez. 

# Porting pour version 3
Quand j'écrivais le code de cette programme, ce n'étais pas facile d'installer PIL pour Python 3, donc j'ai fait le choix d'utiliser Python 2.7. Mais maintenant je voulais le rendre compatible avec les deux, ce qui n'est pas très compliqué. Il faut faire un "try...except ImportError:.." pour les modules à importer avec les versions correspondantes à chaque version de Python. Ici on peut trouver une liste de modules avec les équivalents dans chaque version : http://python3porting.com/stdlib.html

Puis il faut s'assurer de quelques autres petits trucs, par exemple devision "/" en Python 2.7 donne un int, mais en Python 3, ça donne un float. Pour un int dans les deux cas, il suffit d'utiliser "//" partout. 

# Limitations
Il me semble que j'étais trop ambitious avec ce projet, et j'ai mis tant de caractères et de fonctionalités dedans qu'il n'est pas si évident non seulement de l'utiliser, mais aussi ça augment le travail de définir les profils pour chaque espèce. En somme ce projet est beaucoup plus grand que je n'avais imaginé. Pour l'amèner à quelque chose de vraiment utile, il faudrait :
1. Y consacrer beaucoup, beaucoup de temps
2. Mettre en ordre le code que j'ai écrit, éliminer les bugs, le rendre plus stable etc.
3. Passer de Tkinter à un autre GUI plus moderne pour que ça soit plus attractif. 

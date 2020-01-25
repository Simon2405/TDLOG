# TDLOG
Développement d'une interface graphique pour le traitement d'image numérique.

# Comment faire ?
1. Vérifier que vous possédez une version suffisante de python (3.7.3), que le module PIL (6.2.1) est installé, que vous disposez de PyQT (5).

# Structure du programme

Le fichier principal est le fichier Menu.py, il comprend la classe Window contenant l'interface et ses différentes options.
Le fichier Method.py regroupe des fonctionnalités externe à la classe relatifs au chargement des images.
Les descriptifs des menus sont stockés dans les fichiers YAML du dossier YAML.
Le fichier Interface C-Python contient le code C++ contient la fonction clear, on y trouve les fichiers CMake ainsi que le header pybind. La bibliothèque python associée se trouve dans le dossier build.
Les icônes sont optionnels et se trouve dans le dossier icone

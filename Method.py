# -*- coding: utf-8 -*-
"""
    Created on Fri Jan  3 16:22:24 2020
    
    @author: -
    """

import numpy as np
import os.path
from PIL import Image, ImageQt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel

RAW = ".raw"
TIF = ".tif"

#Variable globale pour un événement
clic = (0,0)

def createLabel(window, ref) :
    """Crée et renvoie un Qlabel contenant l'image placés à l'adresse window.ImagePath[ref]"""
    label = QLabel()
    
    if (window.imageExtensions[ref] == RAW) :
        global_raw_file = open(window.imagePaths[ref], "rb")
        image_binaries = np.fromfile(global_raw_file, dtype=np.uint8, count=window.imageDims[ref][0]*window.imageDims[ref][1], offset = window.imageDims[ref][0]*window.imageDims[ref][1]*window.imageSlice)
        buffer = Image.frombuffer("I",window.imageDims[ref][0:2],image_binaries.astype("I"), "raw", "I", 0, 1)
        file = buffer.convert("L")
    
    if (window.imageExtensions[ref] == TIF) :
        correctPathForTif(window,ref)
        file = Image.open(window.imagePaths[ref])
    
    label.setPixmap(QPixmap.fromImage(ImageQt.ImageQt(file)))
    return label

def correctPathForTif(window, ref) :
    """Lorsqu'on manipule des fichier .tif, le changement de couche pose des problèmes car, contrairement au fichiers .raw, il n'existe pas de facon d'accéder à une image en particulier comme on le fait avec np.fromfile. Il faut, à partir de la couche sélectionnée, récupérer la bonne image et donc le bon path. Cette fonction est là pour ca : on opère "chirurgicalement" le path actuel (qui ne correspond pas forcément au path vers l'image de la couche sélectionnée) pour qu'il deviennent le path vers la couche sélectionnée. Notons que cette fonction part du principe (et c'est en effet le cas) que tous les fichiers .tif qu'on utilisera poru cette interface graphique ont un path qui possède la structure suivante : prefix_xyz.tif ou xyz est le numéro de la couche """
    try :
        assert(window.imageExtensions[ref]==TIF)
        newpath, extension = os.path.splitext(window.imagePaths[ref])
        slice = list('0' + '0' + str(window.imageSlice))
        newpath = list(newpath)
        newpath[(len(newpath)-3):len(newpath)] = slice[(len(slice)-3):len(slice)]
        newpath = "".join(newpath) + extension
        window.imagePaths[ref] = newpath
    
    except AssertionError :
        window.statusBar().showMessage("wrong extension")

def zoom(image,x1,y1,x2,y2) :
    new_image=image.crop((x1,y1,x2,y2))
    dx = abs(x1-x2)
    dy = abs(y1-y2)
    if dx > dy :
        factor = 500//dx
    else :
        factor = 500//dy
    new_image=new_image.resize((factor*dx,factor*dy),Image.ANTIALIAS)

return new_image

### Beaucoup de trucs qui vont pas dans la lecture d'image : on peut pas lire du 16bits : https://github.com/python-pillow/Pillow/issues/2970 = pet etre une solution en passant par du 32 bit, https://askcodez.com/python-et-tiff-16-bits.html

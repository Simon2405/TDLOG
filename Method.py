# -*- coding: utf-8 -*-
"""
    Created on Fri Jan  3 16:22:24 2020
    
    @author: -
    """

import numpy as np
from PIL import Image, ImageQt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel

#Dimension d'un fichier.raw
Nx=600
Ny=500
Nz=400

RAW = "raw"
TIF = "tif"

#Variable globale pour un événement
clic = (0,0)

def createLabel(window, ref) :
    """Crée et renvoie un Qlabel, l'image à l'adresse window.refImagePath"""
    label = QLabel()
    if (window.imageExtensions[ref] == RAW) :
        file = choose_slice(window.imageSlices[ref],window.imagePaths[ref])
    if (window.imageExtensions[ref] == TIF) :
        file = Image.open(window.imagePaths[ref])
    label.setPixmap(QPixmap.fromImage(ImageQt.ImageQt(file)))
    return label

def choose_slice(n,path) :
    """Cette fonction permet d'afficher une image en 2D à partir d'un fichier .raw
        et d'une coupe n donnée"""
    i=1
    scene_infile = open(path,"rb")
    scene_image_array = np.fromfile(scene_infile,dtype=np.uint8,count=Nx*Ny)
    scene_image = Image.frombuffer("I",[Nx,Ny], scene_image_array.astype("I"),"raw","I",0,1)
    if n>Nz :
        return "Index trop grand"
    if n<1 :
        return "Index trop petit"
    while i<n :
        scene_image_array = scene_image_array = np.fromfile(scene_infile,dtype=np.uint8,count=600*500)
        scene_image = Image.frombuffer("I",[Nx,Ny],
                                       scene_image_array.astype("I"),
                                       "raw","I",0,1)
        i=i+1
    return scene_image.convert("L")

def next_slice(n,path) :
    return choose_slice(n+1,path)

def previous_slice(n,path) :
    return choose_slice(n-1,path)

def zoom(image,x1,y1,x2,y2) :
    new_image=image.crop((x1,y1,x2,y2))
    new_image=new_image.resize((600,600),Image.ANTIALIAS)
    return new_image

def mousePressEvent(self, event):
    clic = (event.x(),event.y())


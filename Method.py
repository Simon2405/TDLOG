# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 16:22:24 2020

@author: -
"""
import matplotlib as plt
import numpy as np
from PyQt5.QtGui import QPixmap
from PIL import Image, ImageQt

#Dimension d'un fichier.raw
Nx=600
Ny=500
Nz=400

"""Cette fonction permet d'afficher une image en 2D à partir d'un fichier .raw
 et d'une coupe n donnée"""
def choose_slice(n,path) :
    i=1
    scene_infile = open(path,"rb")
    scene_image_array = np.fromfile(scene_infile,dtype=np.uint8,count=Nx*Ny)
    scene_image = Image.frombuffer("I",[Nx,Ny],
    scene_image_array.astype("I"),
    "raw","I",0,1)
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

def open_image(path) :
    return choose_slice(1,path)
 
def zoom(image,x1,y1,x2,y2) :     
    new_image=image.crop((x1,y1,x2,y2))
    new_image=new_image.resize((600,600),Image.ANTIALIAS)
    return new_image

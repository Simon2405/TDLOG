# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 09:42:07 2020

@author: simon
"""


import sys
import yaml
import Method
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QMainWindow, QMenu, QAction, QPushButton
from PyQt5.Qt import QIcon
from PyQt5.QtGui import QPixmap
from PIL import ImageQt

app = QApplication.instance() 
if not app: # On ne peut avoir qu'une seule instance de QApplication ouverte à la fois
    app = QApplication(sys.argv)

#Variable globale correspondant à la slice d'observation
n=200

path = "C:/Users/simon/OneDrive/Documents/Projet TDLog/fichiers_TDLOG/beton_def_8b.raw"

class Window(QMainWindow) : # QMainWindow offre un cadre propice au développement d'une fenêtre utilisateur
    def __init__(self):
        QMainWindow.__init__(self)

        # Initialisation de la fenêtre
        self.setWindowTitle("CMV_3D") # titre
        self.resize(600,600) # taille 
        self.move(400,100) # position
        
        self.__createFileMenu()
    
        label = QLabel()
        image = Method.choose_slice(n,path)
        label.setPixmap(QPixmap.fromImage(ImageQt.ImageQt(image)))
        
        self.setCentralWidget(label)
        
    def __createFileMenu(self) :
        path = "Fichiers YAML/File.txt"    
        with open(path) as file:
            data = yaml.full_load(file)
        mainMenu = self.menuBar()
        Menu = mainMenu.addMenu("File")    
        for i in range(len(data)) :
            if data[i]=={'Kind': 'Separator'} :
                Menu.addSeparator()
            else :    
                act_i = QAction("unknown", self)
                if data[i]["Image"]=="None" :
                    act_i = QAction(data[i]["Title"], self)
                else :
                    act_i = QAction(QIcon(data[i]["Image"]), data[i]["Title"], self)
                print(data[i]["Title"])
                act_i.setShortcut(data[i]["Shortcut"])
                act_i.setStatusTip(data[i]["Status"]) 
                if data[i]["Method"] != " " :
                    print(data[i]["Method"]=="self.nxt_slice")
                    cmd = data[i]["Method"]
                    act_i.triggered.connect(cmd)
                Menu.addAction(act_i)
     
    #slots
    
        
    def nxt_slice(self) :
        global n
        n=n+10
        label = QLabel()
        image = Method.next_slice(n,path)
        label.setPixmap(QPixmap.fromImage(ImageQt.ImageQt(image)))
        self.setCentralWidget(label)
                   
              
if __name__ == '__main__' :
    fen = Window()
    fen.show()
    app.exec_()        
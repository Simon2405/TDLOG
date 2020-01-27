import sys
import yaml
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMainWindow, QMenu, QAction, QPushButton
from PyQt5.QtGui import QPixmap
from PyQt5.Qt import QIcon

from PIL import Image, ImageQt # pour installer la librairie PIL, tapper 'conda install PIL' dans un terminal

app = QApplication.instance()
if not app: # On ne peut avoir qu'une seule instance de QApplication ouverte à la fois
    app = QApplication(sys.argv)


class Window(QMainWindow) : # QMainWindow offre un cadre propice au développement d'une fenêtre utilisateur
    def __init__(self):
        QMainWindow.__init__(self)
        
        # Initialisation de la fenêtre
        self.setWindowTitle("CMV_3D") # titre
        self.resize(600,600) # taille
        self.move(400,100) # position
        
        # Initialisation de la barre de menu
        self.__createFileMenu()
        self.__createReferenceMenu()
        self.__createImageProcessingMenu()
        self.__createViewMenu()
        self.__createPointsMenu()
        self.__createAreaOperationsMenu()
        
        self.statusBar().showMessage("Welcome !")
        
        # Chargement d'une image
        label = QLabel()
        image = Image.open('/Users/Simon/Documents/Projet TDLog/fichiers_TDLOG/beton_def_8b/beton_def_8b_000.tif')
        label.setPixmap(QPixmap.fromImage(ImageQt.ImageQt(image)))
        self.setCentralWidget(label)
    
    
    def __createFileMenu(self) :
        # On définit les différents actions possible pour le menu File
        with open("Fichiers YAML/File.txt") as file:
            data = yaml.full_load(file)
        mainMenu = self.menuBar()
        file = mainMenu.addMenu("&File")
        for i in range(len(data)) :
            if data[i]=={'Kind': 'Separator'} :
                file.addSeparator()
            else :
                act_i = QAction("unknown", self)
                if data[i]["Image"]=="None" :
                    act_i = QAction(data[i]["Title"], self)
                else :
                    act_i = QAction(QIcon(data[i]["Image"]), data[i]["Title"], self)
                act_i.setShortcut(data[i]["Shortcut"])
                act_i.setStatusTip(data[i]["Status"])
                
                file.addAction(act_i)

                    def __createReferenceMenu(self) :
                        
                        with open("Fichiers YAML/Reference.txt") as file:
                            data = yaml.full_load(file)
                                mainMenu = self.menuBar()
                                reference = mainMenu.addMenu("&Reference")
                                for i in range(len(data)) :
                                    if data[i]=={'Kind': 'Separator'} :
                                        reference.addSeparator()
                                            else :
                                                act_i = QAction("unknown", self)
                                                if data[i]["Image"]=="None" :
                                                    act_i = QAction(data[i]["Title"], self)
                                                        else :
                                                            act_i = QAction(QIcon(data[i]["Image"]), data[i]["Title"], self)
                                                                act_i.setShortcut(data[i]["Shortcut"])
                                                                act_i.setStatusTip(data[i]["Status"])
                                                                
                                                                    reference.addAction(act_i)
                                                                        
                                                                        
                                                                        def __createImageProcessingMenu(self) :
                                                                            
                                                                            with open("Fichiers YAML/ImageProcessing.txt") as file:
                                                                                data = yaml.full_load(file)
                                                                                    mainMenu = self.menuBar()
                                                                                    ImageProcessing = mainMenu.addMenu("&Image Processing")
                                                                                    for i in range(len(data)) :
                                                                                        if data[i]=={'Kind': 'Separator'} :
                                                                                            ImageProcessing.addSeparator()
                                                                                                else :
                                                                                                    act_i = QAction("unknown", self)
                                                                                                    if data[i]["Image"]=="None" :
                                                                                                        act_i = QAction(data[i]["Title"], self)
                                                                                                            else :
                                                                                                                act_i = QAction(QIcon(data[i]["Image"]), data[i]["Title"], self)
                                                                                                                    act_i.setShortcut(data[i]["Shortcut"])
                                                                                                                    act_i.setStatusTip(data[i]["Status"])
                                                                                                                    
                                                                                                                        ImageProcessing.addAction(act_i)
                                                                                                                            
                                                                                                                            def __createViewMenu(self) :
                                                                                                                                
                                                                                                                                with open("Fichiers YAML/View.txt") as file:
                                                                                                                                    data = yaml.full_load(file)
                                                                                                                                        mainMenu = self.menuBar()
                                                                                                                                        view = mainMenu.addMenu("&View")
                                                                                                                                        for i in range(len(data)) :
                                                                                                                                            if data[i]=={'Kind': 'Separator'} :
                                                                                                                                                view.addSeparator()
                                                                                                                                                    else :
                                                                                                                                                        act_i = QAction("unknown", self)
                                                                                                                                                        if data[i]["Image"]=="None" :
                                                                                                                                                            act_i = QAction(data[i]["Title"], self)
                                                                                                                                                                else :
                                                                                                                                                                    act_i = QAction(QIcon(data[i]["Image"]), data[i]["Title"], self)
                                                                                                                                                                        act_i.setShortcut(data[i]["Shortcut"])
                                                                                                                                                                        act_i.setStatusTip(data[i]["Status"])
                                                                                                                                                                        
                                                                                                                                                                            view.addAction(act_i)
                                                                                                                                                                                
                                                                                                                                                                                
                                                                                                                                                                                def __createPointsMenu(self) :
                                                                                                                                                                                    
                                                                                                                                                                                    with open("Fichiers YAML/Points.txt") as file:
                                                                                                                                                                                        data = yaml.full_load(file)
                                                                                                                                                                                            mainMenu = self.menuBar()
                                                                                                                                                                                            points = mainMenu.addMenu("&Points")
                                                                                                                                                                                            for i in range(len(data)) :
                                                                                                                                                                                                if data[i]=={'Kind': 'Separator'} :
                                                                                                                                                                                                    points.addSeparator()
                                                                                                                                                                                                        else :
                                                                                                                                                                                                            act_i = QAction("unknown", self)
                                                                                                                                                                                                            if data[i]["Image"]=="None" :
                                                                                                                                                                                                                act_i = QAction(data[i]["Title"], self)
                                                                                                                                                                                                                    else :
                                                                                                                                                                                                                        act_i = QAction(QIcon(data[i]["Image"]), data[i]["Title"], self)
                                                                                                                                                                                                                            act_i.setShortcut(data[i]["Shortcut"])
                                                                                                                                                                                                                            act_i.setStatusTip(data[i]["Status"])
                                                                                                                                                                                                                            
                                                                                                                                                                                                                                points.addAction(act_i)
                                                                                                                                                                                                                                    
                                                                                                                                                                                                                                    def __createAreaOperationsMenu(self) :
                                                                                                                                                                                                                                        
                                                                                                                                                                                                                                        with open("Fichiers YAML/AreaOperations.txt") as file:
                                                                                                                                                                                                                                            data = yaml.full_load(file)
                                                                                                                                                                                                                                                mainMenu = self.menuBar()
                                                                                                                                                                                                                                                AreaOperations = mainMenu.addMenu("&Area Operations")
                                                                                                                                                                                                                                                for i in range(len(data)) :
                                                                                                                                                                                                                                                    if data[i]=={'Kind': 'Separator'} :
                                                                                                                                                                                                                                                        AreaOperations.addSeparator()
                                                                                                                                                                                                                                                            else :
                                                                                                                                                                                                                                                                act_i = QAction("unknown", self)
                                                                                                                                                                                                                                                                if data[i]["Image"]=="None" :
                                                                                                                                                                                                                                                                    act_i = QAction(data[i]["Title"], self)
                                                                                                                                                                                                                                                                        else :
                                                                                                                                                                                                                                                                            act_i = QAction(QIcon(data[i]["Image"]), data[i]["Title"], self)
                                                                                                                                                                                                                                                                                act_i.setShortcut(data[i]["Shortcut"])
                                                                                                                                                                                                                                                                                act_i.setStatusTip(data[i]["Status"])
                                                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                                    AreaOperations.addAction(act_i)




if __name__ == '__main__' :
    fen = Window()
    fen.show()
    app.exec_()

import sys
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
        image = Image.open('/Users/simon/Documents/2A_Ponts/TDLOG/Projet/fichiers_TDLOG/beton_def_8b/beton_def_8b_000.tif')
        label.setPixmap(QPixmap.fromImage(ImageQt.ImageQt(image)))
        self.setCentralWidget(label)

    
    def __createFileMenu(self) :
        # On définit les différents actions possible pour le menu File
        act_Open = QAction(QIcon("Icone/Open.png"), "&Open Image", self)
        act_Open.setShortcut("Ctrl+O")
        act_Open.setStatusTip("Open an image")

        act_Read = QAction("&Read Points", self)
        act_Read.setShortcut("Ctrl+R")
        act_Read.setStatusTip("Read points on image")
        
        act_Next_Slice = QAction(QIcon("Icone/right-arrow.png"), "&Next Slice", self)
        act_Next_Slice.setShortcut("X")
        act_Next_Slice.setStatusTip("Go to next Slice")

        act_Previous_Slice = QAction(QIcon("Icone/left-arrow.png"), "&Previous Slice", self)
        act_Previous_Slice.setShortcut("W")
        act_Previous_Slice.setStatusTip("Go to previous Slice")

        # On crée le menu File que l'on intègre au menu général
        mainMenu = self.menuBar()
        file = mainMenu.addMenu("&File")
        file.addAction(act_Open)
        file.addSeparator()
        file.addAction(act_Read)
        file.addAction(act_Next_Slice)
        file.addAction(act_Previous_Slice)
    
    def __createReferenceMenu(self) :
        act_Open = QAction(QIcon("Icone/Open.png"), "&Open Image", self)
        act_Open.setShortcut("Alt+O")
        act_Open.setStatusTip("Open an image")

        act_Read = QAction("&Read Points", self)
        act_Read.setShortcut("Alt+R")
        act_Read.setStatusTip("Read points on image")


        mainMenu = self.menuBar()
        reference = mainMenu.addMenu("&Reference")
        reference.addAction(act_Open)
        reference.addAction(act_Read)
    

    def __createImageProcessingMenu(self) :
        act_Histogram = QAction(QIcon("Icone/histogram.png"), "&Histogram", self)
        act_Histogram.setShortcut("H")

        mainMenu = self.menuBar()
        imageProcessing = mainMenu.addMenu("&Image Processing")
        imageProcessing.addAction(act_Histogram)
    
    def __createViewMenu(self) :
        act_SwitchImage = QAction(QIcon("Icone/slider.png"), "&Switch Image", self)
        act_SwitchImage.setShortcut("I")


        mainMenu = self.menuBar()
        view = mainMenu.addMenu("&View")
        view.addAction(act_SwitchImage)
    
    def __createPointsMenu(self) :
        act_NoCorrel = QAction(QIcon("Icone/data.png"), "&No Correl", self)
        act_NoCorrel.setShortcut("N")
        

        mainMenu = self.menuBar()
        points = mainMenu.addMenu("&Points")
        points.addAction(act_NoCorrel)
    
    def __createAreaOperationsMenu(self) :
        act_SelectArea = QAction(QIcon("Icone/radar.png"), "&Select Area", self)
        act_SelectArea.setShortcut("Alt+A")


        mainMenu = self.menuBar()
        areaOperations = mainMenu.addMenu("&Area Operations")
        areaOperations.addAction(act_SelectArea)





if __name__ == '__main__' :
    fen = Window()
    fen.show()
    app.exec_()

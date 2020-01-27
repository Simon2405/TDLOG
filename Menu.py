import sys
import yaml
import Method
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QMainWindow, QMenu, QAction, QPushButton, QFileDialog, QInputDialog
from PyQt5.Qt import QIcon
from PyQt5.QtGui import QPixmap
from PIL import Image, ImageQt

TIF = "tif"
RAW = "raw"
EMPTY_PATH = ""
EMPTY_ARGUMENT = " "
SEPARATOR = {'Kind': 'Separator'}

# Initialisation de la barre de menu
menuNames = ["&File","&Reference","&View","&Image Processing","&Points","&Area Operations"]
menuPaths = ["Fichiers YAML/File.txt","Fichiers YAML/Reference.txt","Fichiers YAML/View.txt","Fichiers YAML/ImageProcessing.txt","Fichiers YAML/Points.txt","Fichiers YAML/AreaOperations.txt"]




app = QApplication.instance()
if not app: # On ne peut avoir qu'une seule instance de QApplication ouverte à la fois
    app = QApplication(sys.argv)

class Window(QMainWindow) : # QMainWindow offre un cadre propice au développement d'une fenêtre utilisateur
    """Cette classe contient une fenêtre utilisateur et des méthodes pour l'interface graphique d'un logiciel de traitement d'images"""
    
    def __init__(self):
        QMainWindow.__init__(self)
        
        # Initialisation de la fenêtre
        self.setWindowTitle("CMV_3D") # titre
        self.resize(600,600) # taille
        self.move(400,100) # position
        
        # Attributs relatifs aux images
        self.imagePaths = [EMPTY_PATH,EMPTY_PATH] #path de l'image principale en 0, path de l'image de ref en 1
        self.imageExtensions = [EMPTY_PATH,EMPTY_PATH] #extension de l'image principale en 0, extension de l'image de ref en 1
        self.imageSlices = [500,500] #couche de l'image principale en 0, couche de l'image de ref en 1
        self.imageDims = [[0,0,0],[0,0,0]] # [x,y,z]
        self.ref = 0 #image que l'on veut afficher (0 : image principale, 1: image de ref)
        
        for i in range(len(menuNames)) :
            self.__createMenu(menuNames[i],menuPaths[i])
        
        # Image Principale et Commentaire
        self.setImage(self.ref)
        self.statusBar().showMessage("Welcome, please choose an image !")
    
    def __createMenu(self,name,path) :
        """Fonction qui crée les menus à partir des fichiers yaml, dans lesquels les informations sont stockées. Les noms de menus sont stockés dans name et les chemins vers les fichier yaml sont stockés dans path"""
        with open(path) as file:
            data = yaml.full_load(file)
            
            mainMenu = self.menuBar()
            Menu = mainMenu.addMenu(name)
            
            for i in range(len(data)) :
                
                if data[i]==SEPARATOR :
                    Menu.addSeparator()
                
                else :
                    action = QAction("unknown", self)
                    if data[i]["Image"]=="None" :
                        action = QAction(data[i]["Title"], self)
                    else :
                        action = QAction(QIcon(data[i]["Image"]), data[i]["Title"], self)
                    action.setShortcut(data[i]["Shortcut"])
                    action.setStatusTip(data[i]["Status"])
                    if (data[i]["Method"] != EMPTY_ARGUMENT) :
                        action.triggered.connect(getattr(self, data[i]["Method"]))
                    Menu.addAction(action)
    
    def setImage(self, ref) :
        """Fonction qui affiche l'image principale au niveau de la couche principale en l'encapsulant dans un QLabel"""
        try :
            label = Method.createLabel(self, ref)
            self.setCentralWidget(label)
            self.statusBar().showMessage("image : " + self.imagePaths[ref])
        except FileNotFoundError :
            self.statusBar().showMessage("File cannot be founded")
        except UnboundLocalError : #dans le cas ou imageExtensions[ref] est ni RAW, ni TIF, dans Method.createLabel, file n'est pas definit mais est appele, c'est une UnboundLocalError
            self.statusBar().showMessage("UnboundLocalError : probably no file loaded")

def openFile(self, ref):
    """charge, puis ouvre l'image (de ref si ref=True)"""
        try :
            newpath = QFileDialog.getOpenFileName(self, 'Open File', "/Users", "(*.raw *.tif)")[0] #getOpenFileName renvoie un tuple contenant le chemin et le filter
            self.imagePaths[ref] = newpath
            self.imageExtensions[ref] = newpath[-3] + newpath[-2] + newpath[-1] #l'appli est adapté pour des fichiers .raw et .tif uniquement (pour un format .jpeg, il faudrait changer la facon d'enregistrer l'extension, par exemple en utilisant QInputDialog.getText
            #format = QInputDialog.getText(self, "What is the extension of the file you just choose (raw or tif) ?", "Format :")
            #self.imageExtensions[ref] = format[0]
            self.setImage(ref)
    except IndexError : #problème intervenant si le path est empty (ce qui en soit n'est pas un problème car l'exception est géré par setImage mais on a alors un indexError lors de l'enregistrement de de imageExtensions[ref])
        self.statusBar().showMessage("you did not choose any file")
    
    def openMainFile(self):
        self.ref = 0
        self.openFile(self.ref)
    
    def openRefFile(self):
        self.ref = 1
        self.openFile(self.ref)
    
    def switchImage(self) :
        self.ref = 1-self.ref
        self.setImage(self.ref)
    
    """def chooseSlice(self) :
        try :
        slice = QInputDialog.getText(self, "Which slice ?", "Slice :")
        self.imageExtensions[ref] = int(format[0])"""



if __name__ == '__main__' :
    fen = Window()
    fen.show()
    app.exec_()

### il faut régler le problème au sein des méthodes impliquant un changement de slice. L'idéal serait que les méthodes se comportent pareil
### quelque soit le type d'image (raw ou tif), et que ce soit les paramètres extérieurs qui empechent les problèmes (du style inventés un Nz pour les fichier tif égal à 1).

### Ajouter des tests
### Commencer à rédiger le rapport/mode d'emploi
### lié les fonctions setImage et createlabel en terme d'erreur dans le cas empty path (exception raise dans createLabel et raie dans setImage
### L'image de ref et l'image principale sont indépendantes, on veut pouvoir accéder à des couches différentes

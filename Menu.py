import sys
import yaml
import Method
import os.path
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QMainWindow, QMenu, QAction, QFileDialog, QInputDialog
from PyQt5.Qt import QIcon
from PyQt5.QtGui import QPixmap
from PIL import Image, ImageQt

TIF = ".tif"
RAW = ".raw"
EMPTY_PATH = ""
EMPTY_ARGUMENT = " "
SEPARATOR = {'Kind': 'Separator'}
Nx=600
Ny=500
Nz=400
REF = 1
MAIN = 0

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
        self.imageSlice = 0
        self.imageDims = [[0,0,0,0],[0,0,0,0]] # [x,y,z,size_of_int], on utilisera ces imagedims dans le cas des .raw
        self.ref = MAIN #image que l'on veut afficher (MAIN = 0 : image principale, REF = 1 : image de ref)
        
        # Attributs concernants le zoom
        self.clic = []
        self.zoom = False
        
        # Création des menus
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
        """Fonction qui affiche l'image[ref] au niveau de la couche[ref] en l'encapsulant dans un QLabel"""
        try :
            label = Method.createLabel(self, ref)
            self.setCentralWidget(label)
            self.statusBar().showMessage("image : " + self.imagePaths[ref])
        except FileNotFoundError :
            self.statusBar().showMessage("File cannot be founded")
        except UnboundLocalError : #dans le cas ou imageExtensions[ref] est ni RAW, ni TIF, dans Method.createLabel, file n'est pas definit mais est appele, c'est une UnboundLocalError
            self.statusBar().showMessage("probably no file loaded")

def openFile(self, ref):
    """charge, puis ouvre l'image dont le chemin est celui de imagePaths[ref]"""
        try :
            newpath = QFileDialog.getOpenFileName(self, 'Open File', os.path.expanduser("~"), "(*.raw *.tif)") #getOpenFileName renvoie un tuple contenant le chemin et le filter
            self.imagePaths[ref] = newpath[0]
            self.imageExtensions[ref] = os.path.splitext(newpath[0])[1]
            
            if (self.imageExtensions[ref] == RAW) :
                #    dimensions = QInputDialog.getText(self, "What are the dimensions of your file ?", "Nx;Ny;Nz;size_of_int :")
                #    for i in range(4) :
                #       self.imageDims[ref][i] = int(dimensions[0].split(";")[i])
                self.imageDims[ref] = [Nx,Ny,Nz,8]
            if (self.imageExtensions[ref] == TIF) :
                #    dimensions = QInputDialog.getText(self, "What are the dimensions of your file ?", "Nz;size_of_int :")
                #    for i in range(2,4) :
                #       self.imageDims[ref][i] = int(dimensions[0].split(";")[i-2])
                self.imageDims[ref] = [Nx,Ny,Nz,8]
            
        self.setImage(ref)
        
        except IndexError :
            #problème intervenant si le path est empty (ce qui en soit n'est pas un problème car l'exception est géré par setImage mais on a alors un indexError lors de l'enregistrement de de imageExtensions[ref])
            #problème pouvant aussi intervenir si on ne rentre pas toutes les dimensions
            self.statusBar().showMessage("Error : Choose a file or make sur you enter the 4 dimensions required")
    except ValueError :
        #erreur survenant lorsqu'on entre les dimensions en ne respectant pas la typographie
        self.statusBar().showMessage("dims should be written like this : Nx;Ny;Nz;size_of_int")
    
    def openMainFile(self):
        self.ref = MAIN
        self.openFile(self.ref)
    
    def openRefFile(self):
        self.ref = REF
        self.openFile(self.ref)
    
    def switchImage(self) :
        self.ref = 1-self.ref
        self.setImage(self.ref)
    
    
    
    def chooseSlice(self) :
        self.imageSlice = QInputDialog.getInt(self, "Which slice do you want to go ?", "Slice : ", min=0, max=max(self.imageDims[MAIN][2], self.imageDims[REF][2]))[0]
        self.setImage(self.ref)
    
    def previousSlice(self) :
        try :
            assert(self.imageSlice > 0)
            self.imageSlice -= 1
            self.setImage(self.ref)
        except AssertionError :
            self.statusBar().showMessage("there is no previous Slice")

def nextSlice(self) :
    try :
        assert(self.imageSlice < self.imageDims[self.ref][2]-1)
        self.imageSlice += 1
            self.setImage(self.ref)
        except AssertionError :
            self.statusBar().showMessage("there is no following Slice")
                
                
                
                
                def mousePressEvent(self, event):
                    if self.zoom == True :
self.clic.append([event.x(),event.y()])
if len(self.clic) == 2 :
    print(self.clic)
    
    def zoom_image(self) :
        self.clic = []
        self.zoom = True
        i = 0
        while len(self.clic) != 2 :
            i +=1
        label = QLabel()
        coord = self.clic
        image = Method.zoom(Method.choose_slice(self.imageSlice,self.datFile),coord[0][0],coord[0][1],coord[1][0],coord[1][1])
        label.setPixmap(QPixmap.fromImage(ImageQt.ImageQt(image)))
        self.setCentralWidget(label)
        self.zoom = False



if __name__ == '__main__' :
    fen = Window()
    fen.show()
    app.exec_()

### il faut régler le problème au sein des méthodes impliquant un changement de slice. L'idéal serait que les méthodes se comportent pareil
### quelque soit le type d'image (raw ou tif), et que ce soit les paramètres extérieurs qui empechent les problèmes (du style inventés un Nz pour les fichier tif égal à 1).

### Ajouter des tests
### Commencer à rédiger le rapport/mode d'emploi (citer le site qui nous donne les Icones)
### lié les fonctions setImage et createlabel en terme d'erreur dans le cas empty path (exception raise dans createLabel et raie dans setImage
### L'image de ref et l'image principale sont indépendantes, on veut pouvoir accéder à des couches différentes
### rajouter les fichiers C et les fichiers PyQt
### attention : on vut pouvoir lire l'ensemble des tifs.

### question lorsqu'on change de couche : on change de couche pour les deux images ou pas ? veut on accéder à des couches différentes de l'image de ref et de l'image principale ?

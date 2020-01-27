##############
### IMPORT ###
##############
import sys
import yaml
import os.path
from ctypes import *

from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QMainWindow, QMenu, QAction, QFileDialog, QInputDialog
from PyQt5.Qt import QIcon
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

from PIL import Image, ImageQt

import Method
from build_Interface_C_PY_Desktop_Release import treatment

##########################
### Variables globales ###
##########################
TIF = ".tif"
RAW = ".raw"
EMPTY_PATH = "a"
EMPTY_ARGUMENT = ""
SEPARATOR = {'Kind': 'Separator'}
NO_TREATMENT = "No treatment"

REF = 1
MAIN = 0

# Initialisation de la barre de menu
menuNames = ["&File", "&Reference", "&View", "&Image Processing", "&Points","&Area Operations", "&Treatment"]
menuPaths = ["Fichiers YAML/File.txt", "Fichiers YAML/Reference.txt", "Fichiers YAML/View.txt", "Fichiers YAML/ImageProcessing.txt", "Fichiers YAML/Points.txt", "Fichiers YAML/AreaOperations.txt", "Fichiers YAML/Treatment.txt"]




app = QApplication.instance()
if not app:
    app = QApplication(sys.argv)

class Window(QMainWindow) :
    """Cette classe contient une fenêtre utilisateur et des méthodes pour l'interface graphique d'un logiciel de traitement d'images"""
    
    def __init__(self):
        QMainWindow.__init__(self)
        
        # Initialisation de la fenêtre
        self.setWindowTitle("CMV_3D")
        self.resize(600,600)
        self.move(400,100)
        
        # Attributs relatifs aux images
        self.imagePaths = [EMPTY_PATH, EMPTY_PATH] # path de l'image principale en 0, path de l'image de ref en 1
        self.imageExtensions = [EMPTY_PATH, EMPTY_PATH] # extension de l'image principale en 0, extension de l'image de ref en 1
        self.imageDims = [{"Nx" : 0, "Ny" : 0, "Nz" : 0, "dtype" : 0}, {"Nx" : 0, "Ny" : 0, "Nz" : 0, "dtype" : 0}]
        self.imageSlice = [0, 0]
        self.ref = MAIN # image que l'on veut afficher (MAIN = 0 : image principale, REF = 1 : image de ref)
        self.label = QLabel() # container pour l'image
        
        # Attributs relatifs aux zooms
        self.clic = []
        
        # Création des menus
        for i in range(len(menuNames)) :
            self.__createMenu(menuNames[i], menuPaths[i])
        
        # Image Principale et Commentaire
        self.statusBar().showMessage("Welcome, please choose an image !")
    
    
    def __createMenu(self, name, path) :
        """Fonction qui crée les menus à partir des fichiers yaml, dans lesquels les informations sont stockées. Les noms de menus sont stockés dans name et les chemins vers les fichier yaml sont stockés dans path"""
        with open(path) as file:
            data = yaml.full_load(file)
            
            mainMenu = self.menuBar()
            Menu = mainMenu.addMenu(name)
            
            for i in range(len(data)) :
                if (data[i] == SEPARATOR) :
                    Menu.addSeparator()
                
                else :
                    action = QAction("unknown", self)
                    
                    if (data[i]["Image"] == "None") :
                        action = QAction(data[i]["Title"], self)
                    else :
                        action = QAction(QIcon(data[i]["Image"]), data[i]["Title"], self)
                    
                    action.setShortcut(data[i]["Shortcut"])
                    action.setStatusTip(data[i]["Status"])
                    if (data[i]["Method"] != EMPTY_ARGUMENT) :
                        action.triggered.connect(getattr(self, data[i]["Method"]))
                    Menu.addAction(action)

####################################################
### Méthodes relatives à l'affichage d'une image ###
####################################################
def getPath(self, ref) :
    """Fonction qui permet à l'utilisateurs de choisir une image dans ses dossiers.
        On peut accèder à des fichier tif et raw."""
            try :
            # Enregistrement du Path
            path = QFileDialog.getOpenFileName(self, 'Open File', os.path.expanduser("~"), "(*.raw *.tif)")[0]
            self.imagePaths[ref] = path
            
            #Enregistrement de l'Extension (.tif ou .raw ?)
            self.imageExtensions[ref] = os.path.splitext(path)[1]
                
                except IndexError : # peut survenir dans l'accession à l'extension
                    self.statusBar().showMessage("You did not choose any file")
                    raise

def getDimsOfImage(self, ref) :
    """Fonction qui permet d'accéder au dimensions de l'image (Nx,Ny,Nz,size_of_int). On accède à ces dimensions en demandant explicitement à l'utilisateur de les indiquer."""
        try :
            assert(self.imageExtensions[ref] != EMPTY_PATH)
            
            # Tif
            if (self.imageExtensions[ref] == TIF) :
                dimensions = QInputDialog.getText(self, "What are the dimensions of your file ?", "Nz;size_of_int :")[0]
                
                image = Image.open(self.imagePaths[ref]) #Image.open est une fonction "lazy", elle ne charge pas l'image
                self.imageDims[ref]["Nx"], self.imageDims[ref]["Ny"] = image.size
                self.imageDims[ref]["Nz"], self.imageDims[ref]["dtype"] = int(dimensions.split(";")[0]), int(dimensions.split(";")[1])
                print (self.imageDims[ref])
            
            # Raw
            elif (self.imageExtensions[ref] == RAW) :
                dimensions = QInputDialog.getText(self, "What are the dimensions of your file ?", "Nx;Ny;Nz;size_of_int :")[0]
                self.imageDims[ref]["Nx"], self.imageDims[ref]["Ny"], self.imageDims[ref]["Nz"], self.imageDims[ref]["dtype"] = int(dimensions.split(";")[0]), int(dimensions.split(";")[1]), int(dimensions.split(";")[2]), int(dimensions.split(";")[3])
    
    
    except ValueError :
        self.statusBar().showMessage("Make sure you use the correct formalism (use ;)")
        raise
        except AssertionError :
            self.statusBar().showMessage("You did not choose any file")
            raise
    except IndexError :
        self.statusBar().showMessage("Make sure you enter all the 2 or 4 dimensions")
        raise

def displayImage(self, ref) :
    """Fonction qui affiche une image"""
        try :
            # Accession à l'image
            array = Method.getArray(self, ref)
            image = Method.getImage(self, ref, array)
            self.label.setPixmap(QPixmap.fromImage(ImageQt.ImageQt(image)))
            
            # Affichage
            self.resize(self.imageDims[ref]["Nx"], self.imageDims[ref]["Ny"])
            self.setCentralWidget(self.label)
            self.statusBar().showMessage("image : " + self.imagePaths[ref])
    except FileNotFoundError :
        self.statusBar().showMessage("File cannot be founded")
        except UnboundLocalError :
            self.statusBar().showMessage("probably no file loaded")

def openFile(self, ref) :
    """Ouvre un fichier """
        try :
            self.getPath(ref)
            self.getDimsOfImage(ref)
            self.displayImage(ref)
    except ValueError :
        self.statusBar().showMessage("Make sure you use the correct formalism (use ;)")
        except AssertionError :
            self.statusBar().showMessage("You did not choose any file")
    except IndexError :
        self.statusBar().showMessage("Make sure you enter all the 2 or 4 dimensions")

############################################################
### Méthodes encapsulées pour utilisation dans les menus ###
############################################################
def openMainFile(self) :
    """Ouvre une image principale"""
        self.ref = MAIN
        self.openFile(self.ref)
    
    def openRefFile(self):
        """Ouvre une image de référence"""
        self.ref = REF
        self.openFile(self.ref)
    
    def switchImage(self) :
        """Cette fonction permet de passer de l'image de référence à l'image principale et inversement."""
        try :
            self.ref = 1-self.ref
            assert(self.imagePaths[self.ref] != EMPTY_PATH)
            self.displayImage(self.ref)
        except AssertionError :
            self.statusBar().showMessage("You have only load one file")

def chooseSlice(self) :
    """Permet de choisir une couche"""
        self.imageSlice[self.ref] = QInputDialog.getInt(self,
                                                        "Which slice do you want to go ?", "Slice : ",
                                                        min=0,
                                                        max=max(self.imageDims[MAIN]["Nz"], self.imageDims[REF]["Nz"]))[0]
        self.displayImage(self.ref)
    
    def previousSlice(self) :
        """Accède à la couche d'avant"""
        try :
            assert(self.imageSlice[self.ref] > 0)
            self.imageSlice[self.ref] -= 1
            self.displayImage(self.ref)
        except AssertionError :
            self.statusBar().showMessage("there is no previous Slice")
    
    def nextSlice(self) :
        """Accède à la couche d'après"""
        try :
            assert(self.imageSlice[self.ref] < self.imageDims[self.ref]["Nz"]-1)
            self.imageSlice[self.ref] += 1
            self.displayImage(self.ref)
        except AssertionError :
            self.statusBar().showMessage("there is no following Slice")

####################################
### Gestion de la souris et zoom ###
####################################
def mousePressEvent(self, event):
    self.clic.append((event.x(),event.y()))
    
    if (len(self.clic) == 2) :
        # Identification de la zone de zoom
        top_left_x, top_left_y = self.clic[0]
        bottom_right_x, bottom_right_y = self.clic[1]
        
        # Réduction de l'image
        array = Method.getArray(self, self.ref)
            image = Method.getImage(self, self.ref, array)
            image = image.crop((top_left_x, top_left_y, bottom_right_x, bottom_right_y))
            image = image.resize((self.imageDims[self.ref]["Nx"], self.imageDims[self.ref]["Ny"]), resample = Image.NEAREST)
            
            # Affichage
            self.label.setPixmap(QPixmap.fromImage(ImageQt.ImageQt(image)))
            self.setCentralWidget(self.label)
            self.clic = []

###########################
### Traitement d'images ###
###########################
def clear(self) :
    """Clear l'image, travaille à partir de l'ImageQt."""
        try :
            # On récupère l'image
            array = Method.getArray(self, self.ref)
            image = Method.getImage(self, self.ref, array)
            image = ImageQt.ImageQt(image)
            
            # Traitement
            Bits = image.bits()
            treatment.clear((Bits.__int__()), self.imageDims[self.ref]["Nx"], self.imageDims[self.ref]["Ny"])
            
            # Affichage
            self.label.setPixmap(QPixmap.fromImage(image))
            self.resize(self.imageDims[self.ref]["Nx"], self.imageDims[self.ref]["Ny"])
            self.setCentralWidget(self.label)
            self.statusBar().showMessage("image blurred : " + self.imagePaths[self.ref])
    
    except FileNotFoundError :
        self.statusBar().showMessage("File cannot be founded")
        except UnboundLocalError :
            self.statusBar().showMessage("probably no file loaded")



if __name__ == '__main__' :
    fen = Window()
    fen.show()
    app.exec_()

import sys
import yaml
import Method
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMainWindow, QMenu, QAction, QPushButton
from PyQt5.Qt import QIcon

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
        Name = ["&File","&Reference","&View","&Image Processing","&Points","&Area Operations"]
        Path = ["Fichiers YAML/File.txt","Fichiers YAML/Reference.txt","Fichiers YAML/View.txt","Fichiers YAML/ImageProcessing.txt","Fichiers YAML/Points.txt","Fichiers YAML/AreaOperations.txt"]
        
        for i in range(len(Name)) :
            self.__createMenu(Name[i],Path[i])
        
        self.statusBar().showMessage("Welcome !")
        
        # Chargement d'une image
        label = QLabel()
        path = "C:/Users/simon/OneDrive/Documents/Projet TDLog/fichiers_TDLOG/beton_def_8b.raw"
        image = Method.choose_slice(200,path)
        #image = Method.zoom(image,30,30,200,200)
        label.setPixmap(QPixmap.fromImage(ImageQt.ImageQt(image)))
    
    self.setCentralWidget(label)

    def __createMenu(self,name,path) :
        
        with open(path) as file:
            data = yaml.full_load(file)
        mainMenu = self.menuBar()
        Menu = mainMenu.addMenu(name)
for i in range(len(data)) :
    if data[i]=={'Kind': 'Separator'} :
        Menu.addSeparator()
            else :
                act_i = QAction("unknown", self)
                if data[i]["Image"]=="None" :
                    act_i = QAction(data[i]["Title"], self)
                else :
                    act_i = QAction(QIcon(data[i]["Image"]), data[i]["Title"], self)
                act_i.setShortcut(data[i]["Shortcut"])
                act_i.setStatusTip(data[i]["Status"])
    
            Menu.addAction(act_i)




if __name__ == '__main__' :
    fen = Window()
    fen.show()
    app.exec_()

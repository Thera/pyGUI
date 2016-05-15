import sys
from PyQt4 import QtGui, QtCore
import cv2

class Window(QtGui.QMainWindow):

    def __init__(self):

        '''create the menuBar and the statusBar'''

        super(Window, self).__init__()

        self.setGeometry(50, 50, 500, 300)
        self.setWindowTitle("PyQT tuts!")
        self.setWindowIcon(QtGui.QIcon('pythonlogo.png'))
        #create the window

        '''the menu inside'''
        extractAction = QtGui.QAction("&GET TO THE CHOPPAH!!!", self)
        extractAction.setShortcut("Ctrl+Q")
        extractAction.setStatusTip('Leave The App')
        extractAction.triggered.connect(self.close_application)
        #quit

        openEditor = QtGui.QAction("&Editor", self)
        openEditor.setShortcut("Ctrl+E")
        openEditor.setStatusTip('Open Editor')
        openEditor.triggered.connect(self.editor)
        #open editor

        openFile = QtGui.QAction("&Open File", self)
        openFile.setShortcut("Ctrl+O")
        openFile.setStatusTip('Open File')
        openFile.triggered.connect(self.file_open)
        #open file
        saveFile = QtGui.QAction("&Save File", self)
        saveFile.setShortcut("Ctrl+S")
        saveFile.setStatusTip('Save File')
        saveFile.triggered.connect(self.file_save)
        #save file
        '''end the menu inside'''


        self.statusBar()
        #create the statusBar

        mainMenu = self.menuBar()
        #creat the mainMenu
        fileMenu = mainMenu.addMenu('&File')
        fileMenu.addAction(extractAction)
        fileMenu.addAction(openFile)
        fileMenu.addAction(saveFile)
        #add the first menu
        editorMenu = mainMenu.addMenu("&Editor")
        editorMenu.addAction(openEditor)
        #add the second menu

        self.home()



    def home(self):
        btn = QtGui.QPushButton("Quit", self)
        btn.clicked.connect(self.close_application)
        btn.resize(btn.minimumSizeHint())
        btn.move(500,500)
        #quit button

        btn = QtGui.QPushButton("Open File", self)
        btn.clicked.connect(self.file_open)
        btn.resize(btn.minimumSizeHint())
        btn.move(650,500)
        #open_file button

        btn = QtGui.QPushButton("pretreatment", self)
        btn.clicked.connect(self.file_open)
        btn.resize(btn.minimumSizeHint())
        btn.move(800,100)
        #pretreatment button

        btn = QtGui.QPushButton("iMFilter", self)
        btn.clicked.connect(self.file_open)
        btn.resize(btn.minimumSizeHint())
        btn.move(800,170)
        #iMFilter button

        btn = QtGui.QPushButton("otsu", self)
        btn.clicked.connect(self.file_open)
        btn.resize(btn.minimumSizeHint())
        btn.move(800,240)
        #otsu button

        btn = QtGui.QPushButton("Change", self)
        btn.clicked.connect(self.file_open)
        btn.resize(btn.minimumSizeHint())
        btn.move(800,310)
        #Change button

        btn = QtGui.QPushButton("Result", self)
        btn.clicked.connect(self.file_open)
        btn.resize(btn.minimumSizeHint())
        btn.move(800,380)
        #result button


        #self.imageLabel = QtGui.QLabel()
        #for show the image
        #self.imageLabel.setScaledContents(True)
        #resize the image 
        #self.setCentralWidget(self.imageLabel)
        #place the center
        #self.image = QImage()

        #self.createAction() #create the action

        extractAction = QtGui.QAction(QtGui.QIcon('apple.png'), 'Flee the Scene', self)
        extractAction.triggered.connect(self.close_application)
        self.toolBar = self.addToolBar("Extraction")
        self.toolBar.addAction(extractAction)
        #the image in the statusBar

        fontChoice = QtGui.QAction('Font', self)
        fontChoice.triggered.connect(self.font_choice)
        #self.toolBar = self.addToolBar("Font")
        self.toolBar.addAction(fontChoice)
        #choose the font style

        checkBox = QtGui.QCheckBox('Enlarge', self)
        checkBox.move(300, 10)
        checkBox.stateChanged.connect(self.enlarge_window)
        #enlarge the window when choose the checkbox

        '''the GUI style'''
        #print(self.style().objectName())
        self.styleChoice = QtGui.QLabel("Windows Vista", self)

        comboBox = QtGui.QComboBox(self)
        comboBox.addItem("motif")
        comboBox.addItem("Windows")
        comboBox.addItem("cde")
        comboBox.addItem("Plastique")
        comboBox.addItem("Cleanlooks")
        comboBox.addItem("windowsvista")

        comboBox.move(150, 500)
        self.styleChoice.move(50,500)
        comboBox.activated[str].connect(self.style_choice)
        '''end the GUI style'''

        self.show()




    def file_open(self):
        name = QtGui.QFileDialog.getOpenFileName(self, 'Open File')
        file = open(name,'r')

        self.editor()
        with file:
            text = file.read()
            self.textEdit.setText(text)

    def file_save(self):
        name = QtGui.QFileDialog.getSaveFileName(self, 'Save File')
        file = open(name,'w')
        text = self.textEdit.toPlainText()
        file.write(text)
        file.close()

    def color_picker(self):
        color = QtGui.QColorDialog.getColor()
        self.styleChoice.setStyleSheet("QWidget { background-color: %s}" % color.name())


    def editor(self):
        self.textEdit = QtGui.QTextEdit()
        self.setCentralWidget(self.textEdit)
    

    def font_choice(self):
        font, valid = QtGui.QFontDialog.getFont()
        if valid:
            self.styleChoice.setFont(font)


    def style_choice(self, text):
        self.styleChoice.setText(text)
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create(text))
        
        

    def enlarge_window(self, state):
        if state == QtCore.Qt.Checked:
            self.setGeometry(50,50, 1000, 600)
        else:
            self.setGeometry(50, 50, 500, 300)
        


    def close_application(self):
        choice = QtGui.QMessageBox.question(self, 'Extract!',
                                            "Get into the chopper?",
                                            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if choice == QtGui.QMessageBox.Yes:
            print("Extracting Naaaaaaoooww!!!!")
            sys.exit()
        else:
            pass
        
        

    
def run():
    app = QtGui.QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())


run()

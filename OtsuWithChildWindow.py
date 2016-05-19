# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui, QtCore
import cv2
from PIL import Image, ImageQt
import ImageQt
import ImageEnhance
import numpy as np
from pre_widget import pre 

global raw,result,img_raw,img_gray

class Window(QtGui.QMainWindow):

    def __init__(self):

        '''create the menuBar and the statusBar'''

        super(Window, self).__init__()
        global raw,result,img_raw,img_gray

        self.setGeometry(50, 50, 500, 300)
        self.setWindowTitle("PyQT tuts!")
        self.setWindowIcon(QtGui.QIcon('pythonlogo.png'))
        #create the window
        self.setStyleSheet("background:#5D6D7E;")

        '''the menu inside'''
        extractAction = QtGui.QAction("&GET TO THE CHOPPAH!!!", self)
        extractAction.setShortcut("Ctrl+Q")
        extractAction.setStatusTip('Leave The App')
        extractAction.triggered.connect(self.close_application)
        #quit

        openFile = QtGui.QAction("&Open File", self)
        openFile.setShortcut("Ctrl+O")
        openFile.setStatusTip('Open File')
        openFile.triggered.connect(self.file_open)
        #open file

        '''end the menu inside'''


        stBar = self.statusBar()
        #create the statusBar

        mainMenu = self.menuBar()
        #creat the mainMenu
        fileMenu = mainMenu.addMenu('&File')
        fileMenu.addAction(extractAction)
        fileMenu.addAction(openFile)
        #add the first menu


        self.label1 = QtGui.QLabel(self)
        self.label1.resize(480,370)
        self.label1.move(50,70)
        self.label1.setStyleSheet("QLabel{border: 3px solid gray;border-radius: 40px;background: white;}")

        self.label2 = QtGui.QLabel(self)
        self.label2.resize(480,370)
        self.label2.move(550,70)
        self.label2.setStyleSheet("QLabel{border: 3px solid gray;border-radius: 40px;background: white;}")

        #add the label

        self.home()



    def home(self):
        btn_1 = QtGui.QPushButton("Quit", self)
        btn_1.clicked.connect(self.close_application)
        btn_1.resize(140, 70)
        btn_1.move(600,470)
        #quit button
        btn_1.setStyleSheet("QPushButton{background-color:#D35400;border-radius:5px;color:#ffffff;font-size:20px;}"
                                 "QPushButton:hover{background-color:#333333;}")

        btn_2 = QtGui.QPushButton("Open File", self)
        btn_2.clicked.connect(self.file_open)
        btn_2.resize(140, 70)
        btn_2.move(850,470)
        #open_file button
        btn_2.setStyleSheet("QPushButton{background-color:#16A085;border:none;border-radius:5px;color:#ffffff;font-size:20px;}"
                                "QPushButton:hover{background-color:#333333;}")


        btn = QtGui.QPushButton("pretreatment", self)
        btn.clicked.connect(self.child)
        btn.resize(200,115)
        btn.move(1100,40)
        #pretreatment button
        btn.setStyleSheet("QPushButton{color: rgb(255, 255, 255);background-color: #34495E;border:none;padding: 3px;font-family: 'Verdana';font-size: 15px;text-align: center;}"
                          "QPushButton:hover, QPushButton:pressed, QPushButton:checked{background-color: #1ABC9C;text-align: right;padding-right: 20px;font-weight:100}"
                          "QPushButton:hover{background-image: url(next.png);background-repeat:no-repeat;background-position: center left;}"
                          "QPushButton:pressed, QPushButton:checked{background-image: url(next.png);background-repeat:no-repeat;background-position: center left;}")


        btn = QtGui.QPushButton("Median Filter", self)
        btn.clicked.connect(self.iMFilter)
        btn.resize(200,115)
        btn.move(1100,145)
        #iMFilter button
        btn.setStyleSheet("QPushButton{color: rgb(255, 255, 255);background-color: #34495E;border:none;padding: 3px;font-family: 'Verdana';font-size: 15px;text-align: center;}"
                          "QPushButton:hover, QPushButton:pressed , QPushButton:checked{background-color: #1ABC9C;text-align: right;padding-right: 20px;font-weight:100}"
                          "QPushButton:hover{background-image: url(next.png);background-repeat:no-repeat;background-position: center left;}"
                          "QPushButton:pressed, QPushButton:checked{background-image: url(next.png);background-repeat:no-repeat;background-position: center left;}")


        btn = QtGui.QPushButton("Otsu Filter", self)
        btn.clicked.connect(self.otsu)
        btn.resize(200,115)
        btn.move(1100,250)
        #otsu button
        btn.setStyleSheet("QPushButton{color: rgb(255, 255, 255);background-color: #34495E;border:none;padding: 3px;font-family: 'Verdana';font-size: 15px;text-align: center;}"
                          "QPushButton:hover, QPushButton:pressed , QPushButton:checked{background-color: #1ABC9C;text-align: right;padding-right: 20px;font-weight:100}"
                          "QPushButton:hover{background-image: url(next.png);background-repeat:no-repeat;background-position: center left;}"
                          "QPushButton:pressed, QPushButton:checked{background-image: url(next.png);background-repeat:no-repeat;background-position: center left;}")


        btn = QtGui.QPushButton("Corrosion", self)
        btn.clicked.connect(self.Change)
        btn.resize(200,115)
        btn.move(1100,355)
        #Change button
        btn.setStyleSheet("QPushButton{color: rgb(255, 255, 255);background-color: #34495E;border:none;padding: 3px;font-family: 'Verdana';font-size: 15px;text-align: center;}"
                          "QPushButton:hover, QPushButton:pressed , QPushButton:checked{background-color: #1ABC9C;text-align: right;padding-right: 20px;font-weight:100}"
                          "QPushButton:hover{background-image: url(next.png);background-repeat:no-repeat;background-position: center left;}"
                          "QPushButton:pressed, QPushButton:checked{background-image: url(next.png);background-repeat:no-repeat;background-position: center left;}")


        btn = QtGui.QPushButton("Show Result", self)
        btn.clicked.connect(self.result_show)
        btn.resize(200,110)
        btn.move(1100,460)
        #result button
        btn.setStyleSheet("QPushButton{color: rgb(255, 255, 255);background-color: #34495E;border:none;padding: 3px;font-family: 'Verdana';font-size: 15px;text-align: center;}"
                          "QPushButton:hover, QPushButton:pressed , QPushButton:checked{background-color: #1ABC9C;text-align: right;padding-right: 20px;font-weight:100}"
                          "QPushButton:hover{background-image: url(play.png);background-repeat:no-repeat;background-position: center left;}"
                          "QPushButton:pressed, QPushButton:checked{background-image: url(play.png);background-repeat:no-repeat;background-position: center left;}")

        extractAction = QtGui.QAction(QtGui.QIcon('apple.png'), 'Flee the Scene', self)
        extractAction.triggered.connect(self.close_application)
        self.toolBar = self.addToolBar("Extraction")
        self.toolBar.addAction(extractAction)
        #the image in the statusBar

        fontChoice = QtGui.QAction('Font', self)
        fontChoice.triggered.connect(self.font_choice)
        #self.toolBar = self.addToolBar("Font")
        self.toolBar.addAction(fontChoice)
        self.toolBar.setStyleSheet("background:transparent;")
        #choose the font style

        checkBox = QtGui.QCheckBox('Enlarge', self)
        checkBox.move(300, 7)
        checkBox.stateChanged.connect(self.enlarge_window)
        checkBox.setStyleSheet("QCheckBox{background:transparent;spacing: 5px;font-size: 15px;}"
                               "QCheckBox::indicator { width: 26px;height: 50px;}"
                               "QCheckBox::indicator::unchecked {image: url(check_before.png);}"
                               "QCheckBox::indicator::checked { image: url(check_after.png);}")
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
        #add the style

        self.show()

    def child(self):
        print u'open the preChild'
        self.w2 = pre()
        self.connect(self.w2, QtCore.SIGNAL("myclicked()"), self.recv)
        self.w2.show()
       
         
    @QtCore.pyqtSlot(str) 
    def recv(self,s):
        print u'get the preChild value'
        print s
 





    def pil2pixmap(self,im):
        if im.mode == "RGB":
            pass
        #elif im.mode =="L":
            #im = im.convert("RGBA")
        data = im.convert("RGBA").tostring("raw","RGBA")
        qim = QtGui.QImage(data, im.size[0], im.size[1], QtGui.QImage.Format_ARGB32)
        pixmap = QtGui.QPixmap.fromImage(qim)
        return pixmap



    def resize(self, w, h, w_box, h_box, pil_image):
        '''
        resize a pil_image object so it will fit into
        a box of size w_box times h_box, but retain aspect ratio
        '''
        f1 = 1.0*w_box/w # 1.0 forces float division in Python2
        f2 = 1.0*h_box/h
        factor = min([f1, f2])
        #print(f1, f2, factor) # test
        # use best down-sizing filter
        width = int(w*factor)
        height = int(h*factor)
        return pil_image.resize((width + 3, height + 3), Image.ANTIALIAS)
    

    ''' open fuction '''    

    def rgb2gray(self):
        global img_gray, img_raw
 
        img_gray = cv2.cvtColor(img_raw, cv2.COLOR_BGR2GRAY)
        #image: RGB2Gray

        gray_show = Image.fromarray(img_gray)
        
        w,h = gray_show.size
        ir = self.resize(w, h, 480, 360, gray_show)
        
        #image = gray_show

        #frame = img_gray

       
        #height, width = frame.shape[:2]
        #img = QtGui.QImage(frame, width, height, QtGui.QImage.Format_RGB888)
        #img = QtGui.QPixmap.fromImage(img)
        #self.label2.setPixmap(img)

        self.label2.setPixmap(self.pil2pixmap(ir))


        #gray_show = Image.fromarray(img_gray)
        #image = cv2.cvtColor(gray_show, cv2.COLOR_BGR2RGB)
        #image = QtGui.QImage(image.data, img_gray.shape[1], image.shape[0], QtGui.QImage.Format_RGB888)
        #print image
        #ipixmap = QtGui.QPixmap.fromImage(gray_show)
        #scaled_pixmap = ipixmap.scaled(self.label2.size())
        #self.label2.setPixmap(scaled_ipixmap) 


    def iMFilter(self):
        global img_gray
        #result = self.salt(img_gray, 500)
        #img_otsu = cv2.medianBlur(result, 7)
        img_otsu = cv2.medianBlur(img_gray, 7)
        img_gray = img_otsu

        img_otsu = Image.fromarray(img_otsu)
        
        w,h = img_otsu.size
        ir = self.resize(w, h, 480, 360, img_otsu)
        self.label2.setPixmap(self.pil2pixmap(ir))


    def otsu(self):
        global img_gray
        ret2,img_otsu = cv2.threshold(img_gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        ret2,img_otsu = cv2.threshold(img_gray,ret2*14/15,255,cv2.THRESH_BINARY)
        
        img_gray = img_otsu
        img_otsu = Image.fromarray(img_otsu)
        
        w,h = img_otsu.size
        ir = self.resize(w, h, 480, 360, img_otsu)
        self.label2.setPixmap(self.pil2pixmap(ir))
         
                
    def Change(self):
        global img_gray
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(3, 3))
        img_otsu = cv2.dilate(img_gray,kernel) 
        img_gray = img_otsu
        img_otsu = Image.fromarray(img_otsu)

        w,h = img_otsu.size
        ir = self.resize(w, h, 480, 360, img_otsu)      
        self.label2.setPixmap(self.pil2pixmap(ir))

    def result_show(self):
        global img_gray,img_raw
        contours, hierarchy = cv2.findContours(img_gray,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)  
        cv2.drawContours(img_raw,contours,-1,(0,0,255),3)  
        #cv2.imshow('re',img_raw)
        #cv2.waitKey(0) 
        img_show = Image.fromarray(img_raw)

        w,h = img_show.size
        ir = self.resize(w, h, 480, 360, img_show)      
        self.label2.setPixmap(self.pil2pixmap(ir))
        


    '''end opencv function'''

    """function"""
    #img_raw = cv2.imread(cvfilename)
    def salt(img, n):    
        for k in range(n):    
            i = int(np.random.random() * img.shape[1])    
            j = int(np.random.random() * img.shape[0])    
            if img.ndim == 2:     
                img[j,i] = 255    
            elif img.ndim == 3:     
                img[j,i,0]= 255    
                img[j,i,1]= 255    
                img[j,i,2]= 255    
        return img
    #when the pix is black or white,it will be replaced by the neighborhood value 
    #img = cv2.imread("lena.jpeg", 0)  
    #result = salt(img, 500)  
    #median = cv2.medianBlur(result, 5)

    """end function"""


    def file_open(self):
        global img_raw 

        filename = QtGui.QFileDialog.getOpenFileName(self,
                              self.tr("Open Image"), ".",
                              self.tr("Image Files (*.jpg;*.bmp;*.png);;All Files (*)"))
        #open the file 

        if not filename.isEmpty():
            cvfilename = filename.toLocal8Bit().data()
            #convert Qstrig to char*            
            img_raw = cv2.imread(cvfilename)
            #read image with opencv 

            pre_show = Image.fromarray(img_raw)
        
            w,h = pre_show.size
            ir = self.resize(w, h, 480, 360, pre_show)
            self.label1.setPixmap(self.pil2pixmap(ir))

            #image = QtGui.QImage(cvfilename)  
            #convert numpy array to QImage         
            #ipixmap = QtGui.QPixmap.fromImage(image)
            #scaled_pixmap = ipixmap.scaled(self.label1.size())
            #set the image scale
            #self.label1.setPixmap(scaled_pixmap) 
            #show the image
   

    def font_choice(self):
        font, valid = QtGui.QFontDialog.getFont()
        if valid:
            self.styleChoice.setFont(font)


    def style_choice(self, text):
        self.styleChoice.setText(text)
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create(text))
        
        

    def enlarge_window(self, state):
        if state == QtCore.Qt.Checked:
            self.setGeometry(50, 50, 1300, 570)
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
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui, QtCore, Qt
import cv2
from PIL import Image, ImageQt
import ImageQt
import ImageEnhance
import numpy as np



global raw,result,img_raw,img_gray
global img_pre,t,m,n,p

class Window(QtGui.QMainWindow):

    def __init__(self):
        global raw,result,img_raw,img_gray,img_pre, t, m, n, p

        '''create the menuBar and the statusBar'''

        super(Window, self).__init__()

        self.setGeometry(50, 50, 500, 300)
        self.setWindowTitle("PyQT tuts!")
        self.setWindowIcon(QtGui.QIcon('pythonlogo.png'))
        #create the window
        self.setStyleSheet("background:#5D6D7E;")
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)


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
        self.label1.move(50,43)
        self.label1.setStyleSheet("QLabel{border: 3px solid gray;border-radius: 40px;background: white;}")

        self.label2 = QtGui.QLabel(self)
        self.label2.resize(480,370)
        self.label2.move(50,420)
        self.label2.setStyleSheet("QLabel{border: 3px solid gray;border-radius: 40px;background: white;}")


        self.label_pic = QtGui.QLabel(self)
        self.label_pic.resize(480,360)
        self.label_pic.move(800,60)
        self.label_pic.setStyleSheet("QLabel{background:3px solid gray;border:none;background: white;;}")

        #self.label_pic.setPixmap(self.pil2pixmap(img_gray))

        label_co = QtGui.QLabel('color',self)
        label_co.move(850,500)

        label_br = QtGui.QLabel('brightness',self)
        label_br.move(850,530)

        label_con = QtGui.QLabel('contrast',self)
        label_con.move(850,560)

        label_sh = QtGui.QLabel('sharpness',self)
        label_sh.move(850,590)
        #add label


        lcd_color = QtGui.QLCDNumber(self)
        lcd_color.move(1100,500)

        lcd_brightness = QtGui.QLCDNumber(self)
        lcd_brightness.move(1100,530)

        lcd_contrast = QtGui.QLCDNumber(self)
        lcd_contrast.move(1100,560)

        lcd_sharpness = QtGui.QLCDNumber(self)
        lcd_sharpness.move(1100,590)

        # add the lcd


        self.slider_color = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self.slider_color.setFocusPolicy(QtCore.Qt.NoFocus)
        self.slider_color.resize(150,30)
        self.slider_color.move(920,500)
        self.slider_color.setRange(0,8)

        self.slider_brightness = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self.slider_brightness.resize(150,30)
        self.slider_brightness.move(920,530)
        self.slider_brightness.setRange(0,8)

        self.slider_contrast = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self.slider_contrast.resize(150,30)
        self.slider_contrast.move(920,560)
        self.slider_contrast.setRange(4,12)

        self.slider_sharpness = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self.slider_sharpness.resize(150,30)
        self.slider_sharpness.move(920,590)
        self.slider_sharpness.setRange(0,8)
        #add the slider


        self.connect(self.slider_color, QtCore.SIGNAL('valueChanged(int)'), self.changeColorValue)
        self.connect(self.slider_color, QtCore.SIGNAL('valueChanged(int)'), lcd_color, QtCore.SLOT('display(int)'))

        self.connect(self.slider_brightness, QtCore.SIGNAL('valueChanged(int)'), self.changeBriValue)
        self.connect(self.slider_brightness, QtCore.SIGNAL('valueChanged(int)'), lcd_brightness, QtCore.SLOT('display(int)'))
        
        self.connect(self.slider_contrast, QtCore.SIGNAL('valueChanged(int)'), self.changeConValue)
        self.connect(self.slider_contrast, QtCore.SIGNAL('valueChanged(int)'), lcd_contrast, QtCore.SLOT('display(int)'))

        self.connect(self.slider_sharpness, QtCore.SIGNAL('valueChanged(int)'), self.changeSharValue)
        self.connect(self.slider_sharpness, QtCore.SIGNAL('valueChanged(int)'), lcd_sharpness, QtCore.SLOT('display(int)'))     

        self.home()


    def home(self):

        btn_1 = QtGui.QPushButton("Quit", self)
        btn_1.clicked.connect(self.close_application)
        btn_1.resize(200, 115)
        btn_1.move(550, 570)
        #quit button
        btn_1.setStyleSheet("QPushButton{background-color:#D35400;border:none;color:#ffffff;font-size:20px;}"
                                 "QPushButton:hover{background-color:#333333;}")

        btn_2 = QtGui.QPushButton("Open File", self)
        btn_2.clicked.connect(self.file_open)
        btn_2.resize(200, 115)
        btn_2.move(550, 675)
        #open_file button
        btn_2.setStyleSheet("QPushButton{background-color:#16A085;border:none;color:#ffffff;font-size:20px;}"
                                "QPushButton:hover{background-color:#333333;}")


        btn = QtGui.QPushButton("pretreatment", self)
        btn.clicked.connect(self.rgb2gray)
        btn.resize(200,115)
        btn.move(550,40)
        #pretreatment button
        btn.setStyleSheet("QPushButton{color: rgb(255, 255, 255);background-color: #34495E;border:none;padding: 3px;font-family: 'Verdana';font-size: 15px;text-align: center;}"
                          "QPushButton:hover, QPushButton:pressed, QPushButton:checked{background-color: #1ABC9C;text-align: right;padding-right: 20px;font-weight:100}"
                          "QPushButton:hover{background-image: url(next.png);background-repeat:no-repeat;background-position: center left;}"
                          "QPushButton:pressed, QPushButton:checked{background-image: url(next.png);background-repeat:no-repeat;background-position: center left;}")


        btn = QtGui.QPushButton("Median Filter", self)
        btn.clicked.connect(self.iMFilter)
        btn.resize(200,115)
        btn.move(550,145)
        #iMFilter button
        btn.setStyleSheet("QPushButton{color: rgb(255, 255, 255);background-color: #34495E;border:none;padding: 3px;font-family: 'Verdana';font-size: 15px;text-align: center;}"
                          "QPushButton:hover, QPushButton:pressed , QPushButton:checked{background-color: #1ABC9C;text-align: right;padding-right: 20px;font-weight:100}"
                          "QPushButton:hover{background-image: url(next.png);background-repeat:no-repeat;background-position: center left;}"
                          "QPushButton:pressed, QPushButton:checked{background-image: url(next.png);background-repeat:no-repeat;background-position: center left;}")


        btn = QtGui.QPushButton("Otsu Filter", self)
        btn.clicked.connect(self.otsu)
        btn.resize(200,115)
        btn.move(550,250)
        #otsu button
        btn.setStyleSheet("QPushButton{color: rgb(255, 255, 255);background-color: #34495E;border:none;padding: 3px;font-family: 'Verdana';font-size: 15px;text-align: center;}"
                          "QPushButton:hover, QPushButton:pressed , QPushButton:checked{background-color: #1ABC9C;text-align: right;padding-right: 20px;font-weight:100}"
                          "QPushButton:hover{background-image: url(next.png);background-repeat:no-repeat;background-position: center left;}"
                          "QPushButton:pressed, QPushButton:checked{background-image: url(next.png);background-repeat:no-repeat;background-position: center left;}")


        btn = QtGui.QPushButton("Corrosion", self)
        btn.clicked.connect(self.Change)
        btn.resize(200,115)
        btn.move(550,355)
        #Change button
        btn.setStyleSheet("QPushButton{color: rgb(255, 255, 255);background-color: #34495E;border:none;padding: 3px;font-family: 'Verdana';font-size: 15px;text-align: center;}"
                          "QPushButton:hover, QPushButton:pressed , QPushButton:checked{background-color: #1ABC9C;text-align: right;padding-right: 20px;font-weight:100}"
                          "QPushButton:hover{background-image: url(next.png);background-repeat:no-repeat;background-position: center left;}"
                          "QPushButton:pressed, QPushButton:checked{background-image: url(next.png);background-repeat:no-repeat;background-position: center left;}")


        btn = QtGui.QPushButton("Show Result", self)
        btn.clicked.connect(self.result_show)
        btn.resize(200,110)
        btn.move(550,460)
        #result button
        btn.setStyleSheet("QPushButton{color: rgb(255, 255, 255);background-color: #34495E;border:none;padding: 3px;font-family: 'Verdana';font-size: 15px;text-align: center;}"
                          "QPushButton:hover, QPushButton:pressed , QPushButton:checked{background-color: #1ABC9C;text-align: right;padding-right: 20px;font-weight:100}"
                          "QPushButton:hover{background-image: url(play.png);background-repeat:no-repeat;background-position: center left;}"
                          "QPushButton:pressed, QPushButton:checked{background-image: url(play.png);background-repeat:no-repeat;background-position: center left;}")


        button_getImg = QtGui.QPushButton('save',self)
        #button_getImg.clicked.connect(self.saveImage())
        button_getImg.move(800,670)

        button_comfirm = QtGui.QPushButton('information',self)
        button_comfirm.clicked.connect(self.infosend)
        button_comfirm.move(1060,670)



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

        comboBox.move(1000, 730)
        self.styleChoice.move(900,730)
        comboBox.activated[str].connect(self.style_choice)
        '''end the GUI style'''
        #add the style

        self.show()

    #def ImgShow(self):
        #global img_gray
        #img_gray = img_gray.convert('RGB')
        #img_gray = numpy.array(img_gray)
        #img = np.asarray(img_gray)
        #print img   
        #pil to opencv



    def infosend(self):
        global t,m,n,p
        print t
        print m
        print n
        print p

        
    def changeColorValue(self):
        global t, img_pre
        pos = self.slider_color.value()
        print pos
        t = pos
        imgenhancer_Color = ImageEnhance.Color(img_pre)
    
        factor = pos/4.0
        img_enhance_color = imgenhancer_Color.enhance(factor)
        #img_enhance_color.show("Color %f" %factor)

        #img = Image.fromarray(img_enhance_color)
        #self.label.setPixmap(self.pil2pixmap(img))
        img_pre = img_enhance_color
        self.label_pic.setPixmap(self.pil2pixmap(img_pre))

        
    def changeBriValue(self):
        global m, img_pre
        pos = self.slider_brightness.value()
        print pos
        m = pos
        imgenhancer_Brightness = ImageEnhance.Brightness(img_pre)

        factor = pos/4.0
        img_enhance_Brightness = imgenhancer_Brightness.enhance(factor)
        #img_enhance_Brightness.show("Brightness %f" %factor)
        

        img_pre = img_enhance_Brightness
        self.label_pic.setPixmap(self.pil2pixmap(img_pre))


    def changeConValue(self):
        global n, img_pre
        pos = self.slider_contrast.value()
        print pos
        n = pos
        imgenhancer_Contrast = ImageEnhance.Contrast(img_pre)
        
        factor = pos/4.0
        img_enhance_Contrast = imgenhancer_Contrast.enhance(factor)
        #img_enhance_Contrast.show("Contrast %f" %factor)
        

        img_pre = img_enhance_Contrast
        self.label_pic.setPixmap(self.pil2pixmap(img_pre))        

                    
 
    def changeSharValue(self):
        global p, img_pre
        pos = self.slider_sharpness.value()
        print pos
        p = pos
        imgenhancer_Sharpness = ImageEnhance.Sharpness(img)

        factor = pos/4.0
        img_enhance_Sharpness = imgenhancer_Sharpness.enhance(factor)

        img_enhance_Sharpness.save("PreProgressing_%.2f.jpg" %factor) 

        img_pre = img_enhance_Sharpness
        self.label_pic.setPixmap(self.pil2pixmap(img_pre))        


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
        global img_gray, img_raw, img_pre


        #img_gray:pil

        img_gray = cv2.cvtColor(img_raw, cv2.COLOR_BGR2GRAY)
        #image: RGB2Gray        
        pre_show = Image.fromarray(img_gray)
        #cv convert to pil
        img_pre = pre_show

        #gray_show = Image.fromarray(img_gray)


        w,h = pre_show.size
        ir = self.resize(w, h, 480, 360, pre_show)
        
        #image = gray_show

        #frame = img_gray

       
        #height, width = frame.shape[:2]
        #img = QtGui.QImage(frame, width, height, QtGui.QImage.Format_RGB888)
        #img = QtGui.QPixmap.fromImage(img)
        #self.label2.setPixmap(img)

        #self.label2.setPixmap(self.pil2pixmap(ir))

        self.label_pic.setPixmap(self.pil2pixmap(ir))



        #gray_show = Image.fromarray(img_gray)
        #image = cv2.cvtColor(gray_show, cv2.COLOR_BGR2RGB)
        #image = QtGui.QImage(image.data, img_gray.shape[1], image.shape[0], QtGui.QImage.Format_RGB888)
        #print image
        #ipixmap = QtGui.QPixmap.fromImage(gray_show)
        #scaled_pixmap = ipixmap.scaled(self.label2.size())
        #self.label2.setPixmap(scaled_ipixmap) 


    def iMFilter(self):
        global img_gray,img_raw
        img_gray = cv2.cvtColor(img_raw, cv2.COLOR_BGR2GRAY)
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
            self.setGeometry(20, 0, 1300, 790)
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
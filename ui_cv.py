#-*-coding:utf-8-*-

from Tkinter import *
from PIL import ImageTk,Image
import FileDialog as FD
import cv2

global raw,result,img_raw,img_gray
root = Tk()

def resize(w, h, w_box, h_box, pil_image):
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

def open_img():
    global img_raw
    fd = FD.LoadFileDialog(root) # 创建打开文件对话框
    filename = fd.go() # 显示打开文件对话框，并获取选择的文件名称
    #print filename
    img_raw = cv2.imread(filename)
    ir = Image.open(filename)
    w, h = ir.size
    ir = resize(w, h, 480, 360, ir)
    image = ImageTk.PhotoImage(ir)
    raw.delete('pic')
    raw.create_image(0, 0, image = image, anchor = NW, tags = 'pic')
    root.mainloop()

def rgb2gray():
    global img_gray
    img_gray = cv2.cvtColor(img_raw, cv2.COLOR_BGR2GRAY)
    gray_show = Image.fromarray(img_gray)
    w,h = gray_show.size
    ir = resize(w, h, 480, 360, gray_show)
    image = ImageTk.PhotoImage(ir)
    result.delete('pic')
    result.create_image(0, 0, image = image, anchor = NW, tags = 'pic')
    root.mainloop()
    
def ostu():
    global img_gray
    ret2,img_ostu = cv2.threshold(img_gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    ret2,img_ostu = cv2.threshold(img_gray,ret2*14/15,255,cv2.THRESH_BINARY)
    
    img_gray = img_ostu
    img_ostu = Image.fromarray(img_ostu)
    w,h = img_ostu.size
    ir = resize(w, h, 480, 360, img_ostu)
    image = ImageTk.PhotoImage(ir)
    result.delete('pic')
    result.create_image(0, 0, image = image, anchor = NW, tags = 'pic')
    root.mainloop()

def zhongzhi():
    global img_gray
    img_ostu =  cv2.medianBlur(img_gray, 7)
    img_gray = img_ostu
    img_ostu = Image.fromarray(img_ostu)
    w,h = img_ostu.size
    ir = resize(w, h, 480, 360, img_ostu)
    image = ImageTk.PhotoImage(ir)
    result.delete('pic')
    result.create_image(0, 0, image = image, anchor = NW, tags = 'pic')
    root.mainloop()
    
def result_show():

    global img_gray,img_raw
    contours, hierarchy = cv2.findContours(img_gray,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)  
    cv2.drawContours(img_raw,contours,-1,(0,0,255),3)  
    #cv2.imshow('re',img_raw)
    #cv2.waitKey(0) 
    img_show = Image.fromarray(img_raw)
    w,h = img_show.size
    ir = resize(w, h, 480, 360, img_show)
    image = ImageTk.PhotoImage(ir)
    result.delete('pic')
    result.create_image(0, 0, image = image, anchor = NW, tags = 'pic')
    root.mainloop()
    
def fushi():
    global img_gray
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(3, 3))
    img_ostu = cv2.dilate(img_gray,kernel) 
    img_gray = img_ostu
    img_ostu = Image.fromarray(img_ostu)
    w,h = img_ostu.size
    ir = resize(w, h, 480, 360, img_ostu)
    image = ImageTk.PhotoImage(ir)
    result.delete('pic')
    result.create_image(0, 0, image = image, anchor = NW, tags = 'pic')
    root.mainloop()
    
def ui():
    '''欢迎界面'''
    root.title('图像处理')
    root.geometry('1000x480')
    root.resizable(0,0)

    global result,raw
    raw = Canvas(root,width = 480, height = 360, bg = 'black')
    raw.place(x = 10, y = 10)
    print raw

    result = Canvas(root,width = 480, height = 360, bg = 'black')
    result.place(x = 510, y = 10)

    btn_openImg = Button(root, text = '打开图片', command = open_img)
    btn_openImg.place(x = 10, y = 380)
    
    btn_gray = Button(root, text = '预处理', command = rgb2gray)
    btn_gray.place(x = 200, y = 380)
    
    btn_zz = Button(root, text = '中值滤波', command = zhongzhi)
    btn_zz.place(x = 300, y = 380)
    
    btn_ostu = Button(root, text = 'ostu滤波', command = ostu)
    btn_ostu.place(x = 400, y = 380)
    
    btn_fs = Button(root, text = '腐蚀处理', command = fushi)
    btn_fs.place(x = 500, y = 380)
    
    btn_res = Button(root, text = '处理结果', command = result_show)
    btn_res.place(x = 600, y = 380)

    root.mainloop()
    
    

if __name__ == "__main__":
   
    ui()

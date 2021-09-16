from PyQt5 import QtWidgets, uic
import sys
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon
import cv2
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QImage
import cv2
# import imutils

import sys
from PyQt5.QtWidgets import  QWidget, QLabel, QApplication
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap

#--------------------
import numpy as np
import os
# from PIL import Image
import winsound
frequency = 2500  # Set Frequency To 2500 Hertz
duration = 500  # Set Duration To 1000 ms == 1 second
winsound.Beep(frequency, duration)

#--------face
# Load the cascade
# face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_eye.xml
# eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
# mouth_cascade = cv2.CascadeClassifier('haarcascade_mcs_mouth.xml')
mouth_cascade = cv2.CascadeClassifier('haarcascade_smile.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye_tree_eyeglasses.xml')
ear_left = cv2.CascadeClassifier('haarcascade_mcs_leftear.xml')
ear_right = cv2.CascadeClassifier('haarcascade_mcs_rightear.xml')
global ifFace
global ifEyes
global ifEar
global eyeCount
global font

ifFace=False
ifEyes=False
ifEar=False
eyeCount=0
font = cv2.FONT_HERSHEY_COMPLEX

global camera
global exitflag
exitflag=False
global isCamrun
isCamrun=False
global exitflagCam
exitflagCam=False



class Ui(QtWidgets.QMainWindow):
  
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('DriverDrowsiness.ui', self)
        self.CameraButton.clicked.connect(self.startCam)
        self.label1.setText(" ")
        self.label2.setText(" ")
        self.show()
        
    
    def predict(self,image_np):  
        global ifFace
        global ifEyes
        global ifEar
        global eyeCount
        # global font   
        gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
        # faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        faces = face_cascade.detectMultiScale(gray)
        
        ear_L=ear_left.detectMultiScale(gray)
        ear_R=ear_right.detectMultiScale(gray)
        self.label1.setText(' ')  
        for (x,y,w,h) in ear_R:
            # cv2.putText(img,'Right_ear',(x+w,y+h),font,1,(250,250,250),2,cv2.LINE_AA)
            cv2.rectangle(image_np,(x,y),(x+w,y+h),(0,255,0),2)
            # cv2.putText(image_np,'Driver Not Focusing',(50,50),font,1,(0,0,250),2,cv2.LINE_AA)
            self.label1.setText('Driver Not Focusing')  
            winsound.Beep(frequency, duration)
            print('Driver Not Focusing...')
            ifEar=True
        for (x,y,w,h) in ear_L:
            # cv2.putText(img,'Left_ear',(x+w,y+h),font,1,(250,250,250),2,cv2.LINE_AA)
            cv2.rectangle(image_np,(x,y),(x+w,y+h),(0,255,0),2)
            # cv2.putText(image_np,'Driver Not Focusing',(50,50),font,1,(0,0,250),2,cv2.LINE_AA)
            self.label1.setText('Driver Not Focusing')  
            winsound.Beep(frequency, duration)
            # print('Driver Not Focusing...')
            ifEar=True

        if ifEar == False:

            for (xf,yf,wf,hf) in faces:
                
                cv2.putText(image_np,'Face',(xf+wf,yf+hf),font,1,(250,250,250),2,cv2.LINE_AA)
                cv2.rectangle(image_np,(xf,yf),(xf+wf,yf+hf),(255,0,0),2)
                roi_gray = gray[yf:yf+hf, xf:xf+wf]
                roi_color = image_np[yf:yf+hf, xf:xf+wf]
                ifFace=True
                eyes = eye_cascade.detectMultiScale(roi_gray)


                for (ex,ey,ew,eh) in eyes:
                    # cv2.putText(img,'eyes',(ex+ew,ey+eh),font,1,(250,250,250),2,cv2.LINE_AA)
                    cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
                    ifEyes=True
                
                if ifEyes == False:
                    eyeCount=eyeCount+1
                    if eyeCount > 2:
                        winsound.Beep(frequency, duration)
                        print('Driver sleeping..')
                        self.label1.setText('Driver is sleeping')  
                        # cv2.putText(image_np,'Driver is sleeping',(50,50),font,1,(0,0,250),2,cv2.LINE_AA)
                else:
                    eyeCount=0

            ifEyes=False
        ifEar=False
        
        image_np=cv2.resize(image_np, (720, 480))
        self.image = image_np
        self.setPhoto(self.image)   
        # cv2.imshow('img',image_np)   

        # self.label1.setText('label1')  

        # self.label2.setText(" label2")

       
  
    def setPhoto(self,image):
        self.tmp = image
        # image = imutils.resize(image,width=640)
        frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = QImage(frame, frame.shape[1],frame.shape[0],frame.strides[0],QImage.Format_RGB888)
        self.ImageToShow.setPixmap(QtGui.QPixmap.fromImage(image))
        

    def startCam(self):
        global isCamrun
        global camera
        global exitflagCam
        
        if isCamrun:
            exitflagCam=True
            camera.release
            self.CameraButton.setText('Cam')
            isCamrun=False
            exitflagCam=True
            print('Stopping Camera.....')
        else:
            print('Starting Camera.....')
            isCamrun=True
            exitflagCam=False
            self.CameraButton.setText('Stop')
            camera = cv2.VideoCapture(0)
            self.label1.setText(" ")
            self.label2.setText(" ")

            # cv2.waitKey(1000)

            # image_np = cv2.imread(filename)
            # self.predict(image_np)
            while exitflagCam==False:
                # if exitflag:
                #     break
                try:
                    ret, image_np = camera.read()    
                    image_np = cv2.flip(image_np, 1)
                    self.predict(image_np)
                    self.update()
                    cv2.waitKey(1)
                except:
                    print('frame cant read from camera')
                    pass
                    

app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
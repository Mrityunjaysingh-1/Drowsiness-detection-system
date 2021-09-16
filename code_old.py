# import numpy as np
import cv2

# multiple cascades: https://github.com/Itseez/opencv/tree/master/data/haarcascades

#https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_eye.xml
# eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
# mouth_cascade = cv2.CascadeClassifier('haarcascade_mcs_mouth.xml')
mouth_cascade = cv2.CascadeClassifier('haarcascade_smile.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye_tree_eyeglasses.xml')
ear_left = cv2.CascadeClassifier('haarcascade_mcs_leftear.xml')
ear_right = cv2.CascadeClassifier('haarcascade_mcs_rightear.xml')

cap = cv2.VideoCapture(0)
ifFace=False
ifEyes=False
ifEar=False
eyeCount=0
font = cv2.FONT_HERSHEY_COMPLEX
# import winsound
# frequency = 2500  # Set Frequency To 2500 Hertz
# duration = 250  # Set Duration To 1000 ms == 1 second
# winsound.Beep(frequency, duration)
while 1:
    ret, img = cap.read()
    img = cv2.flip(img, 1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    faces = face_cascade.detectMultiScale(gray)
    
    ear_L=ear_left.detectMultiScale(gray)
    ear_R=ear_right.detectMultiScale(gray)
    for (x,y,w,h) in ear_R:
        # cv2.putText(img,'Right_ear',(x+w,y+h),font,1,(250,250,250),2,cv2.LINE_AA)
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
        cv2.putText(img,'Driver Not Focusing',(50,50),font,1,(0,0,250),2,cv2.LINE_AA)
        print('Driver Not Focusing...')
        ifEar=True
    for (x,y,w,h) in ear_L:
        # cv2.putText(img,'Left_ear',(x+w,y+h),font,1,(250,250,250),2,cv2.LINE_AA)
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
        cv2.putText(img,'Driver Not Focusing',(50,50),font,1,(0,0,250),2,cv2.LINE_AA)
        # print('Driver Not Focusing...')
        ifEar=True

    if ifEar == False:

        for (xf,yf,wf,hf) in faces:
            
            cv2.putText(img,'Face',(xf+wf,yf+hf),font,1,(250,250,250),2,cv2.LINE_AA)
            cv2.rectangle(img,(xf,yf),(xf+wf,yf+hf),(255,0,0),2)
            roi_gray = gray[yf:yf+hf, xf:xf+wf]
            roi_color = img[yf:yf+hf, xf:xf+wf]
            ifFace=True
            eyes = eye_cascade.detectMultiScale(roi_gray)


            for (ex,ey,ew,eh) in eyes:
                # cv2.putText(img,'eyes',(ex+ew,ey+eh),font,1,(250,250,250),2,cv2.LINE_AA)
                cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
                ifEyes=True
            
            if ifEyes == False:
                eyeCount=eyeCount+1
                if eyeCount > 3:
                    print('Driver sleeping..')
                    cv2.putText(img,'Driver is sleeping',(50,50),font,1,(0,0,250),2,cv2.LINE_AA)
            else:
                eyeCount=0

        ifEyes=False
    ifEar=False
     
        
    cv2.imshow('img',img)
    if cv2.waitKey(10) & 0xff == ord('q'):
          break
   

cap.release()
cv2.destroyAllWindows()

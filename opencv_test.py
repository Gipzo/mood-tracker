# coding: utf-8

import cv2
    


faceCascade = cv2.CascadeClassifier("data/haarcascade_frontalface_alt.xml")
    
cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)

if vc.isOpened():
    rval, frame = vc.read()
    
    while rval:
        rval, frame = vc.read()
        gray_frame = cv2.cvtColor(frame,cv2.cv.CV_BGR2GRAY)
        gray_frame = cv2.resize(gray_frame, (0,0), fx=0.25, fy=0.25)
        faces = faceCascade.detectMultiScale(
            gray_frame,
            scaleFactor=1.1,
            minNeighbors=3,
            minSize=(30, 30),
            flags = cv2.cv.CV_HAAR_SCALE_IMAGE
        )
        
        if len(faces)>0:
            (x, y, w, h) = faces[0]
            face_image = gray_frame[y:y+h,x:x+w]
            face_image = cv2.resize(face_image, (100, 100), 0, 0);
            cv2.imshow("preview", face_image)

    cv2.destroyWindow("preview")
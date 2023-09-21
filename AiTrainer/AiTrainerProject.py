import cv2
import numpy as np
import time
import PoseModule as pm

cap = cv2.VideoCapture(0)
detector = pm.PoseDetector()

##########################
wCam, hCam = 800, 450
cap.set(3, wCam)
cap.set(4, hCam)
##########################

while True:
    success, img = cap.read()
    img = detector.findPose(img)
    lmList = detector.findPosition(img, draw=False)
    # print(lmList)
    if len(lmList) != 0:
        detector.findAngle(img, 12, 14, 16)

    cv2.imshow('Image', img)
    cv2.waitKey(1)

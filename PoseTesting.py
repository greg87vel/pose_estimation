import cv2
import time
from PoseModule import PoseDetector


cap = cv2.VideoCapture(0)

##########################
wCam, hCam = 800, 600
cap.set(3, wCam)
cap.set(4, hCam)
##########################

pTime = 0
detector = PoseDetector()
while True:
    success, img = cap.read()
    img = detector.findPose(img)
    lmList = detector.findPosition(img)
    if len(lmList) != 0:
        print(lmList)
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_ITALIC, 1, (255, 0, 0), 3)

    cv2.imshow('Image', img)
    cv2.waitKey(1)
import cv2
import numpy as np
import time
import PoseModule as pm

cap = cv2.VideoCapture(0)
detector = pm.PoseDetector()
count = 0
dir = 0
dirw = ''

##########################
wCam, hCam = 800, 450
cap.set(3, wCam)
cap.set(4, hCam)
##########################

pTime = 0

while True:
    success, img = cap.read()
    img = detector.findPose(img, draw=False)
    lmList = detector.findPosition(img, draw=False)
    # print(lmList)
    if len(lmList) != 0:
        # # Right arm
        # detector.findAngle(img, 12, 14, 16)
        # Left arm
        angle = detector.findAngle(img, 11, 13, 15)
        per = np.interp(angle, (40, 155), (0, 100))
        bar = np.interp(angle, (40, 155), (400, 100))
        # print(int(angle),'   ', int(per))

        # check for the dumbbell curls
        if per == 100:
            if dir == 0:
                count += .5
                dir = 1
                dirw = 'up'
        if per == 0:
            if dir == 1:
                count += .5
                dir = 0
                dirw = 'down'
        # print(count)

        # Bar
        cv2.rectangle(img, (700, 100), (775, 400), (0, 150, 255), 2)
        if per == 0:
            cv2.rectangle(img, (700, 400), (775, 500-int(bar)), (0, 0, 255), cv2.FILLED)
        else:
            cv2.rectangle(img, (700, 400), (775, 500-int(bar)), (0, 255, 255), cv2.FILLED)
        if per == 0:
            cv2.putText(img, f'{int(100-per)}%', (700, 75), cv2.FONT_ITALIC, 1, (0, 0, 255), 2)
        else:
            cv2.putText(img, f'{int(100-per)}%', (700, 75), cv2.FONT_ITALIC, 1, (0, 255, 255), 2)

        # Count
        cv2.rectangle(img, (0, 370), (180, 480), (0, 150, 255), cv2.FILLED)
        cv2.putText(img, f'{count}', (10, 450), cv2.FONT_ITALIC, 2, (0, 255, 255), 3)
        cv2.putText(img, dirw, (10, 100), cv2.FONT_ITALIC, 2, (0, 255, 255), 2)

    # cTime = time.time()
    # fps = 1 / (cTime - pTime)
    # pTime = cTime

    cv2.imshow('Image', img)
    cv2.waitKey(1)

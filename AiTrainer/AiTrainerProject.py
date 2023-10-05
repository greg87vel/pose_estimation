import cv2
import numpy as np
import PoseModule as pm

cap = cv2.VideoCapture(0)
detector = pm.PoseDetector()
count = 0
dir = 0
dirw = ''

##########################
cam_w = int(cap.get(3))
cam_h = int(cap.get(4))
print(cam_w, cam_h)
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
        polsosx_x = (int(lmList[15][1]))
        polsosx_y = (int(lmList[15][2]))
        angle = detector.findAngle(img, 11, 13, 15)
        per = np.interp(angle, (40, 155), (0, 100))
        bar = np.interp(angle, (40, 155), (cam_h - 100, 100))
        # print(int(angle),'   ', int(per))

        # check for the dumbbell curls
        if per == 100:
            if dir == 0:
                count += .5
                dir = 1
                dirw = 'sali'
        if per == 0:
            if dir == 1:
                count += .5
                dir = 0
                dirw = 'scendi'
        # print(count)

        # Bar
        cv2.rectangle(img, (cam_w - 100, cam_h - 100), (cam_w - 25, 100), (0, 150, 255), 2)
        if per == 0:
            cv2.rectangle(img, (cam_w - 100, cam_h - 100), (cam_w - 25, cam_h - int(bar)), (0, 0, 255), cv2.FILLED)
        else:
            cv2.rectangle(img, (cam_w - 100, cam_h - 100), (cam_w - 25, cam_h - int(bar)), (0, 255, 255), cv2.FILLED)
        if per == 0:
            cv2.putText(img, f'{int(100 - per)}%', (cam_w - 100, 75), cv2.FONT_ITALIC, 1, (0, 0, 255), 2)
        else:
            cv2.putText(img, f'{int(100 - per)}%', (cam_w - 100, 75), cv2.FONT_ITALIC, 1, (0, 255, 255), 2)

        # Count
        cv2.rectangle(img, (0, cam_h - 100), (180, cam_h), (0, 150, 255), cv2.FILLED)
        cv2.putText(img, f'{count}', (10, cam_h - 30), cv2.FONT_ITALIC, 2, (0, 255, 255), 3)

        # Direction
        cv2.putText(img, dirw, (polsosx_x + 20, polsosx_y), cv2.FONT_ITALIC, 2, (255, 0, 255), 3)
        if dir == 0:
            punto_1 = (polsosx_x - 8, polsosx_y)
            punto_2 = (polsosx_x, polsosx_y + 30)
            punto_3 = (polsosx_x + 8, polsosx_y)
            fig_polso = np.array([punto_1, punto_2, punto_3], np.int32)
            fig_polso = fig_polso.reshape((-1, 1, 2))
            print(fig_polso)
            cv2.polylines(img, [fig_polso], isClosed=True, color=(0, 255, 0), thickness=3)
        if dir == 1:
            punto_1 = (polsosx_x - 8, polsosx_y)
            punto_2 = (polsosx_x, polsosx_y - 30)
            punto_3 = (polsosx_x + 8, polsosx_y)
            fig_polso = np.array([punto_1, punto_2, punto_3], np.int32)
            fig_polso = fig_polso.reshape((-1, 1, 2))
            print(fig_polso)
            cv2.polylines(img, [fig_polso], isClosed=True, color=(0, 255, 0), thickness=3)

    cv2.imshow('Image', img)
    cv2.waitKey(1)

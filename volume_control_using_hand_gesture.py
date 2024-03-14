import cv2
import time
import numpy as np
import Tracking as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

wCam, hCam = 500,500

cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4, hCam)
pTime = 0

detector = htm.handDetector(detectionCon=0.7)

#**********************************************************
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]
volBar = 400
volper = 0
#**********************************************************

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmlist = detector.findPositin(img,draw=False)
    if len(lmlist) != 0:
        x1,y1 = lmlist[4][1] , lmlist[4][2]
        x2,y2 = lmlist[8][1] , lmlist[8][2]
        cx,cy = (x1+x2)//2,(y1+y2)//2
        cv2.circle(img, (x1,y1), 8, (255,0,255),cv2.FILLED)
        cv2.circle(img, (x2,y2), 8, (255,0,255),cv2.FILLED)
        cv2.circle(img, (cx,cy), 12, (255,0,255),cv2.FILLED)
        cv2.line(img, (x1,y1),(x2,y2),(255,0,255),3)

        length = math.hypot(x2-x1,y2-y1)

        # volume range  = 40-190
        vol = np.interp(length,[40,190],[minVol,maxVol])
        volBar = np.interp(length,[40,190],[400,150])
        volper = np.interp(length,[40,190],[0,100])

        volume.SetMasterVolumeLevel(vol, None)

        if length < 40:
            cv2.circle(img, (cx,cy), 12, (0,255,0),cv2.FILLED)
        elif length > 190:
            cv2.circle(img, (cx,cy), 12, (0,0,255),cv2.FILLED)

    cv2.rectangle(img,(50,150),(85,400),(0,255,0),3)
    cv2.rectangle(img,(50,int(volBar)),(85,400),(0,255,0),cv2.FILLED)
    cv2.putText(img,f"{int(volper)} %",(48,450), cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),3)


    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img,f'FPS:{int(fps)}',(48,48),cv2.FONT_HERSHEY_COMPLEX,
                1,(255,0,0),3)

    cv2.imshow("Img", img)
    cv2. waitKey(1)
    


import autopy
import cv2
import numpy as np
import mediapipe as mp
import math
import time
import pyautogui
mphands = mp.solutions.hands
hands = mphands.Hands()
mpdraw = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
tipids=[4,8,12,16,20]
wscr,hscr=autopy.screen.size()
tpad=300
smooth=7
plocx,plocy=0,0
clocx,clocy=0,0
ptime=0
ctime=0
while True:
    ret, frame = cap.read()
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    flipped_frame = cv2.flip(frame, 1)
    flipped_frame_rgb = cv2.flip(frame_rgb, 1)
    result = hands.process(flipped_frame_rgb)
    h,w,_=flipped_frame.shape
    if result.multi_hand_landmarks:
        for handlms in result.multi_hand_landmarks:
            mpdraw.draw_landmarks(flipped_frame, handlms, mphands.HAND_CONNECTIONS)
        x1,y1=int(handlms.landmark[8].x*w),int(handlms.landmark[8].y*h)
        x2,y2=int(handlms.landmark[12].x*w),int(handlms.landmark[12].y*h)
        finger=[]
        if handlms.landmark[4].x<handlms.landmark[2].x:
            finger.append(1)
        else:
            finger.append(0)
        for id in range(1,5):

            if handlms.landmark[tipids[id]].y<handlms.landmark[tipids[id]-2].y:
                finger.append(1)
            else:
                finger.append(0)
        cv2.rectangle(flipped_frame,(tpad,tpad),(1280-tpad,720-tpad),(0,255,0),5)
        ctime=time.time()

        if finger[1]==1 and finger[2]==0:
            print("moving mode")
            x3=np.interp(x1,(tpad,1280-tpad),(0,wscr))
            y3=np.interp(y1,(tpad,720-tpad),(0,hscr))
            clocx=plocx+(x3-plocx)/smooth
            clocy=plocy+(y3-plocy)/smooth
            autopy.mouse.move(clocx,clocy)
            plocx,plocy=clocx,clocy
            cv2.circle(flipped_frame,(x1,y1),10,(0,0,0),cv2.FILLED)
        if finger[4]==1 and finger[3]==0:
            print("wanna scroll down ")
            pyautogui.scroll(-120)
        if finger[4]==1 and finger[3]==1:
            print("wanna scroll up ")
            pyautogui.scroll(120)
        if finger[1]==1 and finger[2]==1:

            print("clicking mode")
            length = math.hypot(x2 - x1, y2 - y1)
            cv2.line(flipped_frame,(x1,y1),(x2,y2),(255,0,255),2)
            cv2.circle(flipped_frame,(int((x1+x2)/2),int((y1+y2)/2)),1,(0,0,255),5,cv2.FILLED)
            print(length)
            if length < 30 and ctime-ptime>0.3:
                cv2.circle(flipped_frame,(x2,y2),5,(0,255,0),5)
                autopy.mouse.click()
                ptime=ctime
    if not ret:
        break
    cv2.imshow("frame", flipped_frame)
    if cv2.waitKey(1) & 0xFF == ord(' '):
        break
cap.release()
cv2.destroyAllWindows()
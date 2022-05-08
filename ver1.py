import cv2
import math
import numpy.linalg as la
import cv2.aruco as aruco
import numpy as np
def findArucoMarkers(img, markerSize=6,TotalMarkers=250,draw=True):
    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    key =getattr(aruco,f'DICT_{markerSize}X{markerSize}_{TotalMarkers}')
    arucoDict=aruco.Dictionary_get(key)
    arucoParam= aruco.DetectorParameters_create()
    bbox,ids,rejected=aruco.detectMarkers(img,arucoDict,parameters=arucoParam)
    aruco.drawDetectedMarkers(img, bbox)
cap=cv2.VideoCapture(1)
while True:
    worked,img=cap.read()
    findArucoMarkers(img)
    cv2.imshow("image", img)
    cv2.waitKey(1)
import cv2
import numpy
import os
 #on Windows System
paths=[]
path=[]
poth=[]
peth=[]
cap=cv2.VideoCapture(0)
def selectedpoints( event, x, y, flags, param):

    if event == cv2.EVENT_LBUTTONDOWN and len(path) == 0:
        path.append([x, y])
        peth.append([x, y])

    elif event == cv2.EVENT_LBUTTONDOWN and len(path) == 1:
        path.append([[x, y]])
        peth.append([x, y])

    elif event == cv2.EVENT_LBUTTONDOWN and len(path) > 1:
        path[1].append([x, y])
        peth.append([x, y])

    elif event == cv2.EVENT_RBUTTONDOWN:
        path.append([x, y])
        paths.append(path)
cap = cv2.VideoCapture(1)
c=0
while True:
        worked, img = cap.read()
        [cv2.drawMarker(img,i,(0,0,255))for i in peth]
        [cv2.line(img,peth[k-1],i,(0,255,0))for k,i in enumerate(peth)]
        cv2.imshow("image", img)
        cv2.setMouseCallback("image", selectedpoints)
        k = cv2.waitKey(33)
        if len(path) == 3:  # Esc key to stop
            poth=path.copy()
            poth[1]=path[1].copy()
            #print("poth:",poth,"path",path)
            poth.reverse()
            #print("poth:",poth,"path",path)
            poth.pop(0)
            #print("poth:",poth,"path",path)
            poth[0].reverse()
            #print("poth:",poth,"path",path)
            paths.append(poth)
            k=str(input("place and matrix point"))
            print(k,":")
            print(paths)
            paths = []
            path = []
            poth = []
            peth = []

cv2.destroyAllWindows()

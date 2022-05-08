import cv2
import math
import numpy.linalg as la
import cv2.aruco as aruco
import numpy as np
import test
import copy
import bot
import os
p=0
q=0
bot1_paths=[[["bot1"],[[[134, 131], [[555, 165], [556, 208]], [556, 242]], [[[556, 208], [555, 165]], [134, 131]]]],[["bot1"],[[[153, 132], [[546, 168], [545, 133]], [552, 104]], [[[545, 133], [546, 168]], [153, 132]]]]]
bot2_paths=[[["bot2"],[[[127, 325], [[538, 327], [542, 353]], [539, 384]], [[[542, 353], [538, 327]], [127, 325]]]],[["bot2"],[[[125, 320], [[544, 322], [551, 276]], [555, 244]], [[[551, 276], [544, 322]], [125, 320]]]]]
point=[0,0]
bot1=bot.bot()
bot2=bot.bot()
bot1.number=0
bot1.id=9
bot2.number=1
bot2.id=4
def anticollision():
    distance=bot.Distance(bot1.center,bot2.center)
    if distance<26:
        return False
    else:
        return True
def director():
    global p,q
    #bot1.destination=bot1_paths[p][0][0]
    #bot2.destination=bot2_paths[q][0][0]
    a=copy.deepcopy(bot1_paths[0][1])
    b=copy.deepcopy(bot2_paths[0][1])
    bot1.manager(a)
    bot2.manager(b)

def vector(a,b):
    distance=[a[0]-b[0],a[1]-b[1]]
    nor=math.sqrt(distance[0]**2+distance[1]**2)
    direction=[distance[0]/nor,distance[1]/nor]
    return direction
def angle(v1,v2):
    vector1=vector(v1[0],v1[1])
    vector2=vector(v2[0],v2[1])
    cos=np.dot(vector1,vector2)
    sin=la.norm(np.cross(vector1,vector2))
    return np.arctan2(sin,cos)
def midpoint(x,y):
    a=(x[0]+y[0])/2
    b=(y[1]+x[1])/2
    return [int(a),int(b)]
def show(botobj,img):
    [cv2.drawMarker(img,i,(0,0,255))for i in botobj.midpoints]
    cv2.line(img,botobj.center,botobj.future_point,(0,255,0))
    cv2.line(img,botobj.center,botobj.midpoints[0],(0,255,0))
    cv2.putText(img,botobj.destination,botobj.center,cv2.FONT_HERSHEY_PLAIN,1,(0,0,255))

def findArucoMarkers(img, markerSize=6,TotalMarkers=250,draw=True):
    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    key =getattr(aruco,f'DICT_{markerSize}X{markerSize}_{TotalMarkers}')
    arucoDict=aruco.Dictionary_get(key)
    arucoParam= aruco.DetectorParameters_create()
    bbos,ids,rejected=aruco.detectMarkers(img,arucoDict,parameters=arucoParam)
    # to make  a list of box coordinates and its keys example : box = [[[x,y],[x,y],[x,y],[x,y]],[id]]
    director()
    try:
        bot1.handle(bbos, ids)
        show(bot1, img)
    except:
        print("bot1 not responding")
    try:
        if len(bot2.center)==0:
            bot2.handle(bbos,ids)
        elif anticollision() :
            bot2.handle(bbos,ids)
        show(bot2, img)
    except:
        print("bot2 not recognizing")
cap=cv2.VideoCapture(1)
while True:
    worked,img=cap.read()
    findArucoMarkers(img)
    cv2.imshow("image", img)
    cv2.waitKey(1)

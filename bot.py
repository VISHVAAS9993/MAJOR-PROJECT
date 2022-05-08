import test
import copy
import cv2
import math
import numpy.linalg as la
import cv2.aruco as aruco
import numpy as np
paths=[]
pat=[]
def Distance(center,point):
    return  int(((((center[0] - point[0]) ** 2) + ((center[1] - point[1]) ** 2)) ** 0.5))
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
class bot():
    number=0
    work="idle"
    goal=22
    id=0
    rect=[]
    path=[]
    temp=False
    destination=''
    present_point=[]
    future_point=[]
    state="picked_up"
    midpoints=[]
    angles=[]
    center=[]
    d=0
    #turntime=0
    #blocktime=0
    def manager(self,ps):
        if self.work=="idle" and self.state=="picked_up":
            self.path=ps[0].copy()
            self.future_point = self.path[0]
            self.work="advancing"
        elif self.state=="droped" and self.work=="advancing":
            self.path=ps[1].copy()
            self.future_point=self.path[0][0]
            print(self.path)
            self.work="returning"
        if len(self.path)==0:
            self.temp=True


    def turnandbow(self,point):
        pointangles=[angle([self.center,point], [self.center, i]) for i in self.midpoints]
        if pointangles[0]<=0.2:
            test.drop(self.number)
            if self.state=="droped":
                self.state="picked_up"
            elif self.state=="picked_up":
                self.state="droped"
        else:
            if pointangles[1]>=pointangles[3]:
                test.left(self.number)
            elif pointangles[3]>pointangles[1]:
                test.right(self.number)
    def selectedpoints(self,event, x, y, flags, param):
        global paths, pat
        pat.append([x, y])
        if event == cv2.EVENT_LBUTTONDOWN and len(paths) == 0:
            paths.append([x, y])
        elif event == cv2.EVENT_LBUTTONDOWN and len(paths) == 1:
            paths.append([[x, y]])
        elif event == cv2.EVENT_LBUTTONDOWN and len(paths) > 1:
            paths[1].append([x, y])
        elif event == cv2.EVENT_RBUTTONDOWN:
            paths.append([x, y])
            self.path = paths
            self.temp = self.path
            print(self.path)
            print(self.temp)
    def driver(self,point):
        distance = Distance(self.center,point)
        forwardangle = self.angles[0]
        leftangle = self.angles[3]
        rightangle = self.angles[1]
        backangle = self.angles[2]
        if forwardangle <0.4:
            rs=1000
            ls=1000
            test.forward(self.number)
        else:
            if leftangle > rightangle:
                test.right(self.number)
            elif rightangle >= leftangle:
                test.left(self.number)
    def find(self,bbos,ids):
        id=[int(i) for i in ids[0]]
        idex =id.index(self.id)
        self.rect= [[int(i[0]), int(i[1])] for i in (bbos[idex][0])]
        self.midpoints=[midpoint(self.rect[0],self.rect[1]),midpoint(self.rect[1],self.rect[2]),midpoint(self.rect[2],self.rect[3]),midpoint(self.rect[3],self.rect[0])]
        self.center = (midpoint(self.rect[0], self.rect[2]))
        self.angles = [angle([self.center, self.future_point], [self.center, i]) for i in self.midpoints]
    def pathmaker(self):
        global paths
        if len(self.path)==3:
            point = self.path[0]
            self.d = Distance(self.center, point)
            if self.d < self.goal:
                # self.completed_path.insert(0,[point])
                self.path.remove(point)
                self.future_point = self.path[0][0]
                self.state = "picked_up"
            else:
                self.driver(point)

        elif len(self.path)==2:
            if len(self.path[0])>0:
                point=self.path[0][0]
                self.d=Distance(self.center,point)
                if self.d < self.goal:
                    #self.completed_path.insert(0,[point])
                    self.path[0].remove(point)
                    self.present_point=point
                    if len(self.path[0])>0:
                        self.future_point=self.path[0][0]
                    else:
                        self.future_point=self.path[1]
                        self.path.pop(0)
                else:
                    self.driver(point)
            else:
                self.path.pop(0)
        elif len(self.path) == 1:

            point = self.path[0]
            if self.state == "droped" :
                point = self.path[0]
                self.d = Distance(self.center, point)
                if self.d < self.goal:
                   self.path.remove(point)
                   self.work = "idle"
                   self.temp = True
                else:
                    self.driver(point)
                #if self.work=="returning":
                    #self.work="idle"
                    #self.temp=True
            else:
                self.turnandbow(point)
    def handle(self,bbos,ids):
        self.find(bbos,[ids])
        self.pathmaker()

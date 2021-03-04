
import sys
import time
import csv
import numpy as np
from numba import njit
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.colors import LinearSegmentedColormap


#--------globaleVariableneinlesen--------

#----Werkstueck--------
blockLength = 1000 #(mm/10)
blockWidth = 1500 #(mm/10)
blockHeight = 2500 #(mm/10)
block = [blockLength,blockWidth,blockHeight]
#-----Werkstueck fertig-------

#----Werkzeug-------
drillHeight = 200 #(mm/10)
drillRad = 60 #(mm/10)
drill = [drillHeight,drillRad]
#----Werkzeug fertig----

#-----Punkte Einlesen------
points = np.empty((0,3))

with open('punkte.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in spamreader:
        pointX = int(float(row[0])*10)+500
        pointY = int(float(row[1])*10)+750
        pointZ = int(float(row[2])*10)+250
        points = np.r_[points, [[pointX,pointY,pointZ]]]

print(len(points))
for i in range(0,len(points)):
    print(points[i])  
#------Ende der Punkt Eingabe-----------


def f(x,y, feld):
    return feld[x,y]


def createBlock():
    #Hoehenfeldkreieren
    hFeld = np.zeros([block[0],block[1]])
    #Hoehenfeldfuellen
    for x in range(block[0]):
        for y in range(block[1]):
            hFeld[x][y]=block[2]

    return hFeld


def calcNormVec(point1,point2):
    vec = np.zeros(3)
    vec[0] = point2[0]-point1[0]
    vec[1] = point2[1]-point1[1]
    vec[2] = point2[2]-point1[2]
    length = np.sqrt( (vec[0]**(2)) + (vec[1]**(2)) + (vec[2]**(2)) )
    normVec = np.zeros(3)
    normVec[0] = vec[0]/length
    normVec[1] = vec[1]/length
    normVec[2] = vec[2]/length 
    normLength = np.sqrt( (normVec[0]**(2)) + (normVec[1]**(2)) + (normVec[2]**(2)) )
    return normVec

def calcVecLen(point1,point2):
    vec = np.zeros(3)
    vec[0] = point2[0]-point1[0]
    vec[1] = point2[1]-point1[1]
    vec[2] = point2[2]-point1[2]
    length = np.sqrt( (vec[0]**(2)) + (vec[1]**(2)) + (vec[2]**(2)) )
    return length

@njit
def millPoint(currentPos, hFeld, drill, block):  
    for x in range(drill[1]):
        for y in range(drill[1]):
            posX = currentPos[0] - (drill[1]/2) + x
            posY = currentPos[1] - (drill[1]/2) + y
            if(posX<0 or posX>block[0]):
                continue
            if(posY<0 or posY>block[1]):
                continue
            #abstand berechnen
            disX = posX-currentPos[0]
            disY = posY-currentPos[1]
            dis = np.sqrt((disX**(2))+ (disY**(2)))
            if(dis < (drill[1]/2)):
                nextHeight = currentPos[2]-drill[1]
                newHeight = min(nextHeight,hFeld[int(posX)][int(posY)])
                newHeight = max(0,newHeight)                
                hFeld[int(posX)][int(posY)] = newHeight


def mill(hFeld, drill, block, points):
    #der fraesprozess an sich
    for i in range(len(points)):
        if(i==0):
            continue
        normVec = calcNormVec(points[i-1],points[i])
        length = calcVecLen(points[i-1],points[i])
        currentPos = np.zeros(3)
        currentPos = points[i-1]

        for y in range(int(length)+1):
            # solange wir noch nicht am Punkt2 sind soll folgendes ausgefuehrt werden
            millPoint(currentPos, hFeld, drill, block)
            currentPos = currentPos + normVec
            #print(currentPos)            

def main():
    #Werkstueck erstellen
    t0 = time.time()
    feld = createBlock()
    t1 = time.time()-t0
    print(t1)

    
    t0 = time.time()
    # der Fraesen an sich
    mill(feld, drill, block, points)
    t1 = time.time()-t0
    print(t1)

    X = np.arange(0,block[0],1)
    Y = np.arange(0,block[1],1)
    X,Y = np.meshgrid(X,Y)
    Z = f(X,Y, feld)

    #Transperent colors
    # get colormap
    ncolors = 256
    color_array = plt.get_cmap('inferno')(range(ncolors))

    # change alpha values
    color_array[:,-1] = np.linspace(0.5,1,ncolors)

    # create a colormap object
    cmap = LinearSegmentedColormap.from_list(name='rainbow_alpha',colors=color_array)

    # register this new colormap with matplotlib

    plt.register_cmap(cmap=cmap)
    
    
    fig = plt.figure()
    ay = fig.add_subplot(111, projection='3d')
    surf = ay.plot_surface(X=X,Y=Y,Z=Z, cmap='rainbow_alpha')
    for i in range(len(points)) :
        if(i != 0):
            ay.plot(np.array([points[i-1][0],points[i][0]])
                ,np.array([points[i-1][1],points[i][1]]),
                np.array([points[i-1][2],points[i][2]]))

    plt.show()


if __name__ == "__main__":
    main()

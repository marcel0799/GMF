
import sys
import numpy as np
import matplotlib.pyplot as plt
import time
from numba import njit
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.colors import LinearSegmentedColormap

#-----Test einstellungen#
testSettings = False
if (len(sys.argv)>1):
    testSettings = True

#--------globaleVariableneinlesen--------
if (not testSettings):
    try:
        #----Werkstueck--------
        blockLength, blockWidth, blockHeight = input("Werkstueck Laenge, Breite, Hoehe angeben [in mm] : ").split()
        blockLength = float(blockLength)
        blockWidth = float(blockWidth)
        blockHeight = float(blockHeight)
        
        if(blockLength < 0 or blockWidth < 0 or blockHeight<0):
            print("eingaben duerfen nicht negativ sein")
            exit(0)
        if(blockHeight>1100):
            print("Block wuerde die Maschine beschaedigen, da diese auf Hoehe 110 schneiden soll und der Block groeser ist")
            exit(0)
            
        block = [blockLength,blockWidth,blockHeight]
        #-----Werkstueck fertig-------
        
        #----Werkzeug-------
        drillHeight, drillRad = input("Werkzeug Hoehe Radius [in mm] : ").split()
        drillHeight = float(drillHeight)
        drillRad = float(drillRad)

        if(drillHeight<=0 or drillRad<=0):
            print("Werkzeug Mase duerfen nicht kleiner oder gleich null sein")
            exit(0)
        if(drillHeight > blockHeight):
            print("Werkzeug ist zu gros, es wuerde durch die Grundplatte schneiden")
            exit(0)

        drill = [drillHeight,drillRad]
        #----Werkzeug fertig----
        
    except ValueError:
        print("Value exception")
        exit(1)
    except:
        print("generell Exception")
else:
    block = [1000,1000,1000.]
    drill = [50.,10.]

#-----Punkte Einlesen------
if(not testSettings):
    points = np.empty((0,3))
    try:
        while(True):
            pointX, pointY, pointZ = input(str(len(points)+1) + ".Punkt [x y z]: ").split()
            pointX = int(pointX)
            pointY = int(pointY)
            pointZ = int(pointZ)
            #if(pointX<0 or pointY<0 or pointY<0):
            #    print("Der gewaehlte Punkt darf nicht negativ sein")
            #    exit(0)
            #if(pointX>blockLength or pointY>blockWidth or pointY>blockHeight):
            #    print("Der gewaehlte Punkt ist groesser als das Werkstueck")
            #   exit(0)
            points = np.r_[points, [[pointX,pointY,pointZ]]]
            print(points)
    except ValueError:
        print("Ende der Eingabe, es wurden " + str(len(points)) + " eingegeben")
        #ende der eingabe
    except:
        print("es ist ein fehler aufgetreten")
        exit(0)
        
    if(len(points) <= 0):
        print("Sie haben keine Punkte eingegeben")
        exit(0)
        
else:
     #points = np.array([[100.,100.,900.],[200.,200.,800.],[300.,400.,600],[400.,300.,700.],[800.,800.,900.],[600.,900.,1000]])
        points = np.array([[0.,0.,900],[200,200,800]])
#------Ende der Punkt Eingabe-----------

@njit
def distance(p1,p2):
    return np.linalg.norm(p2-p1)

    
#Gibt den Punkt auf der Strecke von p1 nach p2 zurück, welcher in x,y Dimension am wenigsten Abstand zu a hat.
#In der Ausgabe hat der Punkt jedoch eine Z-Koordinate
@njit
def nearestPointNoZ(p1,p2,a):
    #das gleiche wie nearest Point, nur in x&y Dimension
    p1p2 = p2-p1
    #Line:
    #x = (p2-p1) * t + p1
    
    nPoint = nearestPoint2D(p1[:2],p2[:2], a[:2])
    t = 0
    nP= np.zeros(3)
    nP[0] = nPoint[0]
    nP[1] = nPoint[1]
    #get Z für nearestPoint
    if(p1p2[0] != 0):
        t = (nP[0]-p1[0])/p1p2[0]
    if(p1p2[1] != 0):
        t = (nP[1]-p1[1])/p1p2[1]
    z = p1p2[2]*max(0,min(1,t)) + p1[2]
    nP[2] = z
    return nP

@njit
def nearestPoint2D(p1,p2,a):
    p1p2 = p2-p1
    d = np.dot(p1p2,a)
    f = np.dot(p1p2,p1)
    g = np.dot(p1p2,p1p2)
    t = (d-f)/g
    return ((p2-p1)* max(0,min(1,t)) + p1)

# Gibt den nächsten Punkt zu a auf der Strecke P1-P2
@njit
def nearestPoint(p1,p2,a):

    p1p2 = p2-p1
    #Line:
    #x = (p2-p1)* t + p1
    #Plane:
    #0 = (p2-p1) 'dot' (x-a)
    #(p2-p1)'dot'(a) = (p2-p1)'dot'(x)
    #Line 'X' Plane
    #(p2-p1)'dot'(a) = (p2-p1)'dot'((p2-p1)* t + p1)
    #(p2-p1)'dot'(a) = (p2-p1)'dot'((p2-p1)* t) + (p2-p1)'dot'(p1)
    #(p2-p1)'dot'(a) - (p2-p1)'dot'(p1) = (p2-p1)'dot'((p2-p1)* t)
    #(p2-p1)'dot'(a) - (p2-p1)'dot'(p1) = (p2[0]-p1[0])^2 * t + (p2[1]-p1[1])^2 * t + (p2[2]-p1[2])^2 *t
    #(p2-p1)'dot'(a) - (p2-p1)'dot'(p1) =((p2[0]-p1[0])^2+(p2[1]-p1[1])^2+(p2[2]-p1[2])^2) * t
    #t =((p2-p1)'dot'(a) - (p2-p1)'dot'(p1)) /((p2[0]-p1[0])^2+(p2[1]-p1[1])^2+(p2[2]-p1[2])^2)
    #           d                   f                               g
    
    #t =(np.dot(p2-p1,a) - np.dot(p2-p1,p1)) /((p2[0]-p1[0])^2+(p2[1]-p1[1])^2+(p2[2]-p1[2])^2)
    d = np.dot(p1p2,a)
    f = np.dot(p1p2,p1)
    g = np.dot(p1p2,p1p2)
    t = (d-f)/g
    return ((p2-p1)* max(0,min(1,t)) + p1)

def createBlock():
    #Hoehenfeldkreieren
    hFeld = np.zeros([block[0],block[1]])


    #Hoehenfeldfuellen
    for x in range(block[0]):
        for y in range(block[1]):
            hFeld[x][y]=block[2]

    return hFeld


def mill(hFeld):
    #der fraesprozess an sich

    for x in range(block[0]):
        for y in range(block[1]):
            #korriegierte x und y werte
            
            a = np.array([x,y,hFeld[x][y]])
            
            #Fuer alle aus den Punkten enstehenden Geraden wird gefrast
            for i in range(len(points)) :
                if(i != 0):
                
                    n = points[i]-points[i-1]
                    
                    cutPoint = nearestPointNoZ(points[i-1],points[i],a)
                    
                    #abstand des aktuellen punktes zur gefraesten gerade
                    
                    dis = distance(a[:2],cutPoint[:2])
                    
                    if(dis < drill[1]):
                        #die neue hoehe ist die Höhe auf dem Das Werkzeug bewegt wird, oder die aktuelle Höhe vom Werkstück
                        hFeld[x][y] = min([cutPoint[2],hFeld[x][y]])

def f(x,y, feld):
    return feld[x,y]

def main():
    #Werkstueck erstellen
    feld = createBlock()

    #darstellen des unbehandelten Werkstuecks
    t0 = time.time()

    # der Fraesen an sich
    mill(feld)
    t1 = time.time()-t0
    print(t1)
    X = np.arange(0,int(block[0]),1)
    Y = np.arange(0,int(block[1]),1)
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


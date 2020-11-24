import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.colors import LinearSegmentedColormap
#--------globaleVariableneinlesen--------
bufferSize = 2

#----Werkstueck--------
blockLength = int(input("Werkstueck Laenge [in cm] : "))
blockWidth = int(input("Werkstueck Breite [in cm] :  "))
blockHeight = int(input("Werkstueck Hoehe [in cm] :  "))

if(blockLength < 0 or blockWidth < 0 or blockHeight<0):
    print("eingaben duerfen nicht negativ sein")
    exit(0)
if(blockHeight>110):
    print("Block wuerde die Maschine beschaedigen, da diese auf Hoehe 110 schneiden soll und der Block groeser ist")
    exit(0)

block = [blockLength,blockWidth,blockHeight]
#-----block fertig-----

#----Werkzeug-------
drillHeight = float(input("Werkzeug Hoehe [in cm] :  "))
drillRad = float(input("Werkzeug Radius [in cm] :  "))

if(drillHeight<=0 or drillRad<=0):
    print("Werkzeug Mase duerfen nicht kleiner oder gleich null sein")
    exit(0)
if(drillHeight > blockHeight):
    print("Werkzeug ist zu gros, es wuerde durch die Grundplatte schneiden")
    exit(0)

drill = [drillHeight,drillRad]
#----Werkzeug fertig----


points = np.array([[20,20,90],[80,20,90],[70,60,80],[90,40,70],[20,20,90]])

def distance(p1,p2):
    return np.linalg.norm(p2-p1)

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
    

def distanc(x,y,x1,y1,x2,y2):

    m = (y2-y1)/(x2-x1)
    d = m*x + (y1-m*x1)-y
    return d

def createBlock():
    #Hoehenfeldkreieren
    hFeld = np.zeros([block[0]+bufferSize*2,block[1]+bufferSize*2])


    #Hoehenfeldfuellen
    for x in range(block[0]):
        for y in range(block[1]):
            hFeld[x+bufferSize][y+bufferSize]=block[2]

    return hFeld

def mill(hFeld):
    #der fraesprozess an sich

    for x in range(block[0]):
        for y in range(block[1]):
            #korriegierte x und y werte
            xTemp = x + bufferSize
            yTemp = y + bufferSize
            
            a = np.array([xTemp,yTemp,hFeld[xTemp][yTemp]])
            
            #Fuer alle aus den Punkten enstehenden Geraden wird gefrast
            for i in range(len(points)) : 
                if(i != 0):
                
                    n = points[i]-points[i-1]
                    #for i in range(len(n)):
                    #    n[i] *= 1/(np.linalg.norm(n))
                        
                        
                    ##Nachster Punkt auf Gerade von beliebigem Punkt a durch Schnittpunkt mit Ebene
                    #Ebene durch a mit normalen n ist :
                    # n[0]*x + n[1]*x2 + n[2]*x3 = d
                    #gerade = n * t + points[i-1]
                    
                    #n[0]*(n[0] * t + points[i-1][0]) +
                    #n[1]*(n[1] * t + points[i-1][1]) + 
                    #n[2]*(n[2] * t + points[i-1][2]) = d
                    #(n dot n)  * t + n dot points[i-1] = d
                    # (np.dot(n,a)- np.dot(n,points[i-1]))/ np.dot(n,n) = t
                    
                    
                    #Punkt auf der Geraden, welcher am nachsten am punkt a liegt.
                    #ta = (np.dot(n,a)-np.dot(n,points[i-1]))/ np.dot(n,n)
                    #ta = (n[0]*a[0]+n[1]*a[1]- n[0]*points[i-1][0]-n[1]*points[i-1][1])/(n[0]^2 + n[1]^2)
                    
                    #cutPoint = n * ta + points[i-1]
                    cutPoint = nearestPoint(points[i-1],points[i],a)
                    
                    #abstand des aktuellen punktes zur gefraesten gerade
                    
                    dis = distance(a[:2],cutPoint[:2])
                    
                    #dis = distanc(xTemp,yTemp,points[i-1][0],points[i-1][1],points[i][0],points[i][1])
                    #ist der punkt so nah an der gerade das er im radius des werkzeugsliegt, wird di hoehe verringert
                    if(dis < drill[1]):
                        #die neue hoehe ist die alte hoehe minus die groese des Werkzeugs
                        hFeld[xTemp][yTemp] = min([cutPoint[2],hFeld[xTemp][yTemp]])

def f(x,y, feld):
    return feld[x,y]

def main():
    #Werkstueck erstellen
    feld = createBlock()

    #darstellen des unbehandelten Werkstuecks


    # der Fraesen an sich
    mill(feld)

    X = np.arange(0,block[0],1)
    Y = np.arange(0,block[1],1)
    X,Y = np.meshgrid(X,Y)
    Z = f(X,Y, feld)

    #Transperent colors
    # get colormap
    ncolors = 256
    color_array = plt.get_cmap('cool')(range(ncolors))

    # change alpha values
    color_array[:,-1] = np.linspace(0.0,1.0,ncolors)

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

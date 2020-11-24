import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
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


points = np.array([[20,20, 90],[80,20,90]])



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
            
            a = np.array([xTemp,yTemp,block[2]])
            
            
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
                    ta = (np.dot(n,a)-np.dot(n,points[i-1]))/ np.dot(n,n)
                    #ta = (n[0]*a[0]+n[1]*a[1]- n[0]*points[i-1][0]-n[1]*points[i-1][1])/(n[0]^2 + n[1]^2)
                    
                    cutPoint = n * ta + points[i-1]
                    
                    #abstand des aktuellen punktes zur gefraesten gerade
                    #dis = np.sqrt(a[0]*cutPoint[0]+a[1]*cutPoint[1])
                    
                    dis = distanc(xTemp,yTemp,points[i-1][0],points[i-1][1],points[i][0],points[i][1])
                    #ist der punkt so nah an der gerade das er im radius des werkzeugsliegt, wird di hoehe verringert
                    if(dis < drill[1] and dis > (-drill[1]) ):
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


    fig = plt.figure()
    ay = fig.add_subplot(111, projection='3d')
    surf = ay.plot_surface(X=X,Y=Y,Z=Z, cmap=cm.Greens)

    plt.show()


if __name__ == "__main__":
    main()

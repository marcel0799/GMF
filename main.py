import numpy as np
import matplotlib.pyplot as plt

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



def distanc(x,y):
    #bestimmt den Abstan eines Punktes zur Gerade auf der Gefraest wird
    # y = (2/15)*x -6 ist die Gerade auf der gefraest wird (siehe Dokumentation)
    dTemp = (float(float(x)*2)/15)-6
    # distanz = (2/15)*x -6 -y (siehe MafI2)
    d=dTemp - y
    # distanz zurueckgeben
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
            #abstand des aktuellen punktes zur gefraesten gerade
            d = distanc(xTemp,yTemp)
            #ist der punkt so nah an der gerade das er im radius des werkzeugsliegt, wird di hoehe verringert
            if(d < drill[1] and d > (-drill[1]) ):
                #die neue hoehe ist die alte hoehe minus die groese des Werkzeugs
                hFeld[xTemp][yTemp] = float(block[2]) - drill[0]
    

def main():
    #Werkstueck erstellen
    feld = createBlock()
    
    #darstellen des unbehandelten Werkstuecks
    rotated = np.rot90(feld, 1)
    plt.imshow(rotated)
    plt.show()
    
    # der Fraesen an sich
    mill(feld)
    
    #darstellen das fertigen Werstuecks
    rotated = np.rot90(feld, 1)
    plt.imshow(rotated)
    plt.show()
    

if __name__ == "__main__":
    main()
import sys
import numpy as np

block = [100,100,100]
drill = [5,10]
points = np.array([[0,0,0],[5,10,0], [20,15,10], [30,25,20]])
maxSpeed = 300.0 # [mm/s]
maxAccelerationX = 8000.0 # [mm/s^2]
maxAccelerationY = 8000.0 # [mm/s^2]
maxAccelerationZ = 5000.0 # [mm/s^2]

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

def main():
    lastSpeedX = 0.0
    lastSpeedY = 0.0
    lastSpeedZ = 0.0
    time = 0.0
    
    for i in range(len(points)):
        oneTime = 0.0
        if(i==0):
            continue
        normVec = calcNormVec(points[i-1],points[i])
        normVec[0] = np.abs(normVec[0])
        normVec[1] = np.abs(normVec[1])
        normVec[2] = np.abs(normVec[2])
        length = calcVecLen(points[i-1],points[i])
        
        for y in range(int((length+1)/2)):
            # fuer jeden iterativen Fraess Schritt, welcher jeweils 1mm laenge hat, wird hier die maximal erlaubte geschwindkeit berechnet
            
            curSpeedX = maxSpeed
            curSpeedY = maxSpeed
            curSpeedZ = maxSpeed
            print("Der " + str(y) + " Schritt")
            if(normVec[0] != 0.0):
                XnegP = (lastSpeedX / normVec[0])
                XnegQ = (maxAccelerationX / normVec[0])
                curSpeedX = ( (XnegP/2) + np.sqrt( ((XnegP/2)**(2)) + XnegQ ) )
                print("Maximale Geschw. das die Besch. der X-Achse nicht ueberschritten wird :" + str(curSpeedX))

            if(normVec[1] != 0.0):
                YnegP = (lastSpeedY / normVec[1])
                YnegQ = (maxAccelerationY / normVec[1])
                curSpeedY = ( (YnegP/2) + np.sqrt( ((YnegP/2)**(2)) + YnegQ ) )
                print("Maximale Geschw. das die Besch. der Y-Achse nicht ueberschritten wird " + str(curSpeedY))

            if(normVec[2] != 0.0):
                ZnegP = (lastSpeedZ / normVec[2])
                ZnegQ = (maxAccelerationZ / normVec[2])
                curSpeedZ = ( (ZnegP/2) + np.sqrt( ((ZnegP/2)**(2)) + ZnegQ ) )
                print("Maximale Geschw. das die Besch. der Z-Achse nicht ueberschritten wird " + str(curSpeedZ))

            realSpeed = min(curSpeedX,curSpeedY,curSpeedZ,maxSpeed)

            lastSpeedX = normVec[0] / (1/realSpeed)
            lastSpeedY = normVec[1] / (1/realSpeed)
            lastSpeedZ = normVec[2] / (1/realSpeed)

            print("gewaehlte Gesch: " + str(realSpeed))

            oneTime = oneTime + (1/realSpeed)

            print("-------------------------------------")
        oneTime = oneTime*2
        time = time + oneTime
        print("die benötigte Zeit für diese Gerade = " + str(oneTime) + " sekunden, die Gerade war " + str(length) + "mm lang" )

    print("Insgesamt dauert das Fraessen: " + str(time) + " sekunden")

if __name__ == "__main__":
    main()

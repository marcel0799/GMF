import csv
import numpy as np

points = np.empty((0,3))

with open('punkte_klein.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in spamreader:
        pointX = int(float(row[0])*10)+50
        pointY = int(float(row[1])*10)+75
        pointZ = int(float(row[2])*10)+25
        points = np.r_[points, [[pointX,pointY,pointZ]]]

print(len(points))
for i in range(0,len(points)):
    print(points[i])


    
        


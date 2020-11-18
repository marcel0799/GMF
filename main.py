import numpy as np
import matplotlib.pyplot as plt

# --------globale Variablen einlesen --------
bufferSize = 2

# ---- Werkstueck --------
blockLength = int(input("Werkstueck Laenge: "))
blockWidth = int(input("Werkstueck Breite: "))
blockHeight = int(input("Werkstueck Hoehe: "))
if(blockLength<0 or blockWidth<0 or blockHeight<0):
	print("eingaben duerfen nicht negativ sein")
	exit(0)

## ---- Werkzeug -------
#drillHeight = int(input("Werkzeug Hoehe: "))
#drillRad = int(input("Werkzeug Radius: "))

def main ():
	block = [blockLength,blockWidth,blockHeight]

	# Hoehenfeld kreieren
	feld = np.zeros([block[0] + bufferSize*2, block[1] + bufferSize*2])
	

	# Hoehenfeld fuellen
	for x in range(block[0]):
		for y in range(block[1]):
			feld[x+bufferSize][y+bufferSize] = block[2] 


	print(feld)

	plt.imshow(feld)
	plt.show()








if __name__ == "__main__":
    main()
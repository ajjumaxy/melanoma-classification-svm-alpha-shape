import numpy as np
import cv2, math, glob, os, csv, re
import pandas as pd
import alphashape as a
import matplotlib.pyplot as plt
from draw_hull import draw

def channels_red(img):
    rows, cols, channels = img.shape
    
    red = np.zeros(rows*cols, dtype = np.float32).reshape((rows, cols))
    for i in range(rows):
        for j in range(cols):
            red[i, j] = img[i, j, 2] 
    red = np.uint8(red)            
    return red

def gama(img, c, gama):
    rows, cols = img.shape
    
    result = np.zeros((rows*cols), dtype = np.float32).reshape((rows, cols))

    for i in range(rows):
        for j in range(cols):
            result[i, j] = c * (img[i, j]**gama)

    result = np.uint8(result)
    return result

def median_filter(img):

	windowsize = 9
	edge = windowsize//2

	neighbors = []

	rows, cols = img.shape

	new = np.zeros(rows*cols, dtype = np.float32).reshape((rows,cols))	

	for i in range(edge, rows-edge):
		for j in range(edge, cols-edge):
			
			for x in range(windowsize):
				for y in range(windowsize):
					neighbors.append(img[i-edge+x,j-edge+y])

			neighbors.sort()

			newpixel = neighbors[len(neighbors)//2]

			new[i,j] = newpixel

			neighbors = []

	new = np.uint8(new)

	return new

def getCoord(img, filename):
	with open(os.path.join(filename), 'w') as csvfile:
		csvfile.write("LINHA,COLUNA\n");
		rows, cols = img.shape
		for i in range(rows):
			for j in range(cols):
				if img[i, j] != 0:
					csvfile.write(str(i) + "," + str(j) + "\n")



if __name__ == "__main__":
	pathSeg = "Dermatoscopia/Preprocessado"
	path = "Resultado/"
	pathBordas = "Borda"
	pathCoord = "Coordenadas/"
	pathAlpha = "AlphaShape/"

	# # EXTRAIR BORDAS DAS REGIÕES DE INTERESSE

	# for img in glob.glob(pathSeg+'/*.bmp'):
	#     #ler imagens nas respectivas variaveis usando RGB
	# 	img2 = cv2.imread(img, 0)

	# 	#modifica o conjunto formato das imagens de uint_8 para int_32 para não da sobrecarga nas operações
	# 	#f_img = np.float32(img2)

	# 	#listas recebem retorno das operações
	# 	#img_gama = gama(f_img, 5.867, 0.785)
	# 	filtro_mediana = median_filter(img2)
	# 	canny = cv2.Canny(filtro_mediana, 245, 250)
	# 	name = os.path.basename(str(img))
	# 	new_filename = '{path}{name}' .format(path=pathBordas, name=name)
	# 	cv2.imwrite(new_filename, canny)
	# ###############################################

	# # EXTRAIR COORDENADAS DE PONTOS DE BORDA
	# for img in glob.glob(pathBordas+'/*.bmp'):
	# 	img2 = cv2.imread(img, 0)
	# 	name = os.path.basename(str(img))
	# 	new_filename = '{path}{name}'.format(path=pathCoord, name=name.split('.')[0]+".csv")
	# 	getCoord(img2, new_filename)

	# ###################################################

	#Extrair caracteristicas do AlphaShape

	features = []
	for f_csv in glob.glob(pathCoord+'*.csv'):
		name = os.path.basename(str(f_csv))
		filename = '{path}{name}'.format(path=pathCoord, name=name.split('.')[0]+".csv")
		file = open(filename, 'r')
		reader = csv.reader(file, delimiter=',')
		data = list(reader)
		pts = [(float(x[0]), float(x[1])) for x in data[1:]]
		#params = [0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
		params = [0.05]
		lines = a.getAlfaShapes(pts, alfas=params)

		features.append(lines)
		#print(lines)

		# for i, line in enumerate(lines):
		# 	plt.figure()
		# 	draw(line, pts, plt, splined=False)
		# for i, line in enumerate(lines):
		# 	plt.figure()
		# 	draw(line, pts, plt, splined=True)

		# plt.show()
		#break

	#print(features)
	df = pd.DataFrame(features)
	df.fillna(0, inplace=True)
	print(df.head(5))

	df.to_csv("features_alpha.csv")
# -*- coding: utf-8 -*-
import math
import fnmatch
import os
from PIL import Image # instalar desde repositorios
import numpy # instalar desde repositorios
import mahotas # ver wiki para instalar

#
# La actual versión del algoritmo pyFIA para cada imagen/núcleo en una determinada ruta:
# 1. Lee la matriz de píxeles del canal verde de una imagen en color o el único canal si está en escala de grises.
# 2. Estima el umbral por el método de Otsu usando las librerías de mahotas.
# 3. Estima la media del fondo (pixels cuyo valor es superior al umbral).
# 4. A los píxeles cuya intensidad está por debajo del umbral se les calcula la densidad óptica.
# 5. La densidad óptica integrada es la suma de densidades ópticas para cada núcleo.
# La media de foto y la densidad óptica de cada píxel están redondeadas al segundo decimal según Rasch 2006.
#

def algoritmo(ruta, foto):

	def calcular_iod(pixmap):

		count_pix = 0
		
		iod = 0 # densidad óptica integrada de cada núcleo
		pixels_fondo = 0 # número de píxels del fondo
		suma_fondo = 0 # suma de valores de los píxeles del fondo
		media_fondo = 0 # valor medio de los píxeles del fondo

#		for pixels in pixmap:
#			if pixels < umbral: 
#			if pixels > umbral: 
#				pixels_fondo += 1
#				suma_fondo += int(pixels)

#		media_fondo = 1.0 * suma_fondo/pixels_fondo # calcula la media del fondo de la imagen

		for pixels in pixmap:

			if int(pixels) <= umbral and int(pixels) <= 250 : # pixels inferiores al umbral y distintos de 0
#			if int(pixels) <= umbral and int(pixels) != 0: # pixels inferiores al umbral y distintos de 0
#				logaritmo = -math.log10(int(round(media_fondo,2)/int(pixels))  # calcula densidad óptica individual de cada píxel
#				logaritmo = -math.log10(int(pixels)/round(media_fondo,2))  # calcula densidad óptica individual de cada píxel
#				iod += round(logaritmo,2) # calcula densidad óptica integrada del núcleo
				count_pix += 1
		print count_pix
				
		return count_pix, umbral


	direccion = ruta +"/" + foto # Ruta completa a la imagen

	if fnmatch.fnmatch(foto, '*.jpg'):
#		pixmap = scipy.misc.pilutil.imread(str(direccion)) # abrir imagen con scipy
		imagen = Image.open(str(direccion)) # abrir imagen tif
#		print imagen
		if imagen.mode == "L":
			pixmap = list(imagen.getdata())  # realizar una lista con los valores del canal verde
		elif imagen.mode == "RGB" or "RGBA":
			pixmap = list(imagen.getdata(2))  # realizar una lista con los valores del canal
#			print pixmap
		dna = numpy.array(pixmap, dtype='uintc') # de lista a array numpy
		umbral = mahotas.thresholding.otsu(dna) # umbral por el metodo de otsu
		(count_pix, umbral) = calcular_iod(pixmap) #aplicamos el algoritmo
	elif fnmatch.fnmatch(foto, '*.txt'):
		imagen = open(str(direccion), 'r') # abrir fichero de texto
		leer = imagen.read() # leer
		pixmap = leer.split() # lista con los valores del fichero
		dna = numpy.array(pixmap, dtype='uintc') # de lista a array numpy
#		umbral = mahotas.thresholding.otsu(dna) # umbral por el metodo de otsu
		umbral = 230 
		(count_pix, umbral) = calcular_iod(pixmap) # aplicamos el algoritmo
	
	return count_pix, umbral

def abre_salida(ruta):
	f_salida = ruta + "/output"
	salida = open(f_salida ,"w")
	salida.write("%s \t %s \t %s" % ("imagen", "pixels" , "umbral" "\n"))
	salida.write("-" * 40)
	return salida

def aplicar_algoritmo(ruta):
	# Recorro todo el árbol de directorios a partir de la ruta
	for root, dirs, files in os.walk(ruta):
		print '\n@@@@@@@@@@@@@@@@'
		print 'Analizando el path: ' + root # Ruta en la que estamos
		#print files # Ficheros que contiene
		
		# Ordenamos la lista de ficheros,
		# para recorrerla por orden alfabético
		files.sort()
		
		primer_fichero = True;

		for current_file in files:
			
			if fnmatch.fnmatch(current_file, '*.txt') \
			or fnmatch.fnmatch(current_file, '*.jpg') :
				
				# Si es el primer fichero, creo el fichero de salida
				# Así no crea ficheros en los directorios sin ficheros analizables
				if primer_fichero is True:
					salida = abre_salida(root);
					primer_fichero = False					
				
				print "Analizando " + current_file
				(count_pix, umbral) = algoritmo(root, current_file)
				
#				iod_str = str(iod).replace(".", ",")
#				media_fondo_str = str(media_fondo).replace(".", ",")
				salida.write("\n%s \t %s \t %s" % (current_file,  str(count_pix), umbral))
		
		if primer_fichero is False:
			salida.close()

print "\nThis is the Funny Program for Feulgen Image Analysis Densitometry"
url = str(raw_input("\n>>>Introduzca ruta de las imagenes:"))
aplicar_algoritmo(url)

print "\n FINISH \n"

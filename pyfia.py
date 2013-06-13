#! /usr/bin/python
# -*- coding: utf-8 -*-
import math
import fnmatch
import os
from PIL import Image # install from repositories
import numpy # install from repositories
import mahotas # see pyFIA's wiki for installing

#
# This is a version of pyFIA for area quantification, instead densitometry, for each object in a determinated path:
# 1. Reads the matrix of pixels from green canal (it can be modified to red or blue) or the only channel if it is grayscale.
# 2. Estimates the threshold between the object and the background by Otsu's method using the mahotas library.
# 3. Estimates the average from background (pixels with a value greater the threshold).
# 4. Optical Density (OD) is calculated for pixels with a value lower the threshold.
# 5. Integrated OD (IOD) is the sum of OD for each object-
# All OD are rounded to the second decimal as Rasch 2006.
#

def algoritmo(ruta, foto):

	def calcular_iod(pixmap):
		
		iod = 0 # densidad óptica integrada de cada núcleo
		pixels_fondo = 0 # número de píxels del fondo
		suma_fondo = 0 # suma de valores de los píxeles del fondo
		media_fondo = 0 # valor medio de los píxeles del fondo

		for pixels in pixmap:
			if pixels > umbral: 
				pixels_fondo += 1
				suma_fondo += int(pixels)

		media_fondo = 1.0 * suma_fondo/pixels_fondo # calcula la media del fondo de la imagen

		for pixels in pixmap:

			if int(pixels) <= umbral and int(pixels) != 0: # pixels inferiores al umbral y distintos de 0
				logaritmo = -math.log10(int(pixels)/round(media_fondo,2))  # calcula densidad óptica individual de cada píxel
				iod += round(logaritmo,2) # calcula densidad óptica integrada del núcleo
				
		return iod, umbral

	direccion = ruta +"/" + foto # Ruta completa a la imagen

	if fnmatch.fnmatch(foto, '*.tif'):
#		pixmap = scipy.misc.pilutil.imread(str(direccion)) # abrir imagen con scipy
		imagen = Image.open(str(direccion)) # abrir imagen tif
		if imagen.mode == "L":
			pixmap = list(imagen.getdata())  # realizar una lista con los valores del canal verde
		elif imagen.mode == "RGB" or "RGBA":
			pixmap = list(imagen.getdata(1))  # realizar una lista con los valores del canal
		dna = numpy.array(pixmap, dtype='uintc') # de lista a array numpy
		umbral = mahotas.thresholding.otsu(dna) # umbral por el metodo de otsu
		(iod, umbral) = calcular_iod(pixmap) #aplicamos el algoritmo
	elif fnmatch.fnmatch(foto, '*.txt'):
		imagen = open(str(direccion), 'r') # abrir fichero de texto
		leer = imagen.read() # leer
		pixmap = leer.split() # lista con los valores del fichero
		dna = numpy.array(pixmap, dtype='uintc') # de lista a array numpy
		umbral = mahotas.thresholding.otsu(dna) # umbral por el metodo de otsu
		(iod, umbral) = calcular_iod(pixmap) # aplicamos el algoritmo
	
	return iod, umbral

def abre_salida(ruta):
	f_salida = ruta + "/output"
	salida = open(f_salida ,"w")
	salida.write("%s \t %s \t  %s" % ("imagen", "IOD", "umbral" "\n"))
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
			or fnmatch.fnmatch(current_file, '*.tif') :
				
				# Si es el primer fichero, creo el fichero de salida
				# Así no crea ficheros en los directorios sin ficheros analizables
				if primer_fichero is True:
					salida = abre_salida(root);
					primer_fichero = False					
				
				print "Analizando " + current_file
				(iod, umbral) = algoritmo(root, current_file)
				
				iod_str = str(iod).replace(".", ",")
#				media_fondo_str = str(media_fondo).replace(".", ",")
				salida.write("\n%s \t %s \t %s" % (current_file, iod_str, umbral))
		
		if primer_fichero is False:
			salida.close()

print "\nThis is the Funny Program for Feulgen Image Analysis Densitometry"
url = str(raw_input("\n>>>Introduzca ruta de las imagenes:"))
aplicar_algoritmo(url)

print "\n FINISH \n"

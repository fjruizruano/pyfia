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
		
		iod = 0 # IOD of each object
		pixels_fondo = 0 # number of background pixels
		suma_fondo = 0 # sum of the values of background pixels
		media_fondo = 0 # average value of the background pixels

		for pixels in pixmap:
			if pixels > umbral: 
				pixels_fondo += 1
				suma_fondo += int(pixels)

		media_fondo = 1.0 * suma_fondo/pixels_fondo # calculate the background average of the image

		for pixels in pixmap:

			if int(pixels) <= umbral and int(pixels) != 0: # pixels lower the threshold and different to 0
				logaritmo = -math.log10(int(pixels)/round(media_fondo,2))  # calculate the OD of each pixel
				iod += round(logaritmo,2) # calculates IOD of the object
				
		return iod, umbral

	direccion = ruta +"/" + foto # Full path to the image

	if fnmatch.fnmatch(foto, '*.tif'):
		imagen = Image.open(str(direccion)) # open TIFF images
		if imagen.mode == "L":
			pixmap = list(imagen.getdata()) # make a list with the values of one channel
		elif imagen.mode == "RGB" or "RGBA":
			pixmap = list(imagen.getdata(1)) # make a list with the values of indicated channel
			# you can change de value: 0 = red, 1 = green, 2 = red
		dna = numpy.array(pixmap, dtype='uintc') # from lista to numpy array
		umbral = mahotas.thresholding.otsu(dna)  # threshold by Otsu's method
		(iod, umbral) = calcular_iod(pixmap) # apply the algorithm
	elif fnmatch.fnmatch(foto, '*.txt'):
		imagen = open(str(direccion), 'r') # open text file
		leer = imagen.read() # read
		pixmap = leer.split() # list with the values of the file
		dna = numpy.array(pixmap, dtype='uintc') # from lista to numpy array
		umbral = mahotas.thresholding.otsu(dna) # threshold by Otsu's method
		(iod, umbral) = calcular_iod(pixmap)  # apply the algorithm
	
	return iod, umbral

def abre_salida(ruta):
	f_salida = ruta + "/output"
	salida = open(f_salida ,"w")
	salida.write("%s \t %s \t  %s" % ("imagen", "IOD", "umbral" "\n"))
	salida.write("-" * 40)
	return salida

def aplicar_algoritmo(ruta):
	# Walks all the tree of folders since the path
	for root, dirs, files in os.walk(ruta):
		print '\n@@@@@@@@@@@@@@@@'
		print 'Analyzing the path: ' + root # Path where it is
		
		# Sort alphabetically the list of files 		
		files.sort()
		
		primer_fichero = True;

		for current_file in files:
			
			if fnmatch.fnmatch(current_file, '*.txt') \
			or fnmatch.fnmatch(current_file, '*.tif') :
				
				# If it is the first file, it create the output file
				# Thus, it does not create file in the folders without
				if primer_fichero is True:
					salida = abre_salida(root);
					primer_fichero = False					
				
				print "Analyzing " + current_file
				(iod, umbral) = algoritmo(root, current_file)
				
				iod_str = str(iod).replace(".", ",")
				salida.write("\n%s \t %s \t %s" % (current_file, iod_str, umbral))
		
		if primer_fichero is False:
			salida.close()

print "\nThis is pyFIA, the Funny Program for Feulgen Image Analysis Densitometry"
url = str(raw_input("\n>>>Type the path of the images: "))
aplicar_algoritmo(url)

print "\n FINISH \n"

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
# 3. Counts the pixels with a value lower the threshold.
#

def algoritmo(ruta, foto):

	def calcular_iod(pixmap):

		count_pix = 0
		
		for pixels in pixmap:
			if int(pixels) <= umbral and int(pixels) != 0: # pixels lower the threshold and different of 0
				count_pix += 1 # count 1 for each pixel
		return count_pix, umbral


	direccion = ruta +"/" + foto # Full path of the image

	if fnmatch.fnmatch(foto, '*.jpg'):
		imagen = Image.open(str(direccion)) # open JPG image
		if imagen.mode == "L":
			pixmap = list(imagen.getdata()) # make a list with the values of one channel
		elif imagen.mode == "RGB" or "RGBA":
			pixmap = list(imagen.getdata(1)) # make a list with the values of indicated channel
			# you can change de value: 0 = red, 1 = green, 2 = red
		dna = numpy.array(pixmap, dtype='uintc') # from lista to numpy array
		umbral = mahotas.thresholding.otsu(dna) # threshold by Otsu's method
		(count_pix, umbral) = calcular_iod(pixmap) # applies the algorithm
	elif fnmatch.fnmatch(foto, '*.txt'):
		imagen = open(str(direccion), 'r') # opens text file
		leer = imagen.read() # reads
		pixmap = leer.split() # list with the values of the file
		dna = numpy.array(pixmap, dtype='uintc') # from lista to numpy array
		umbral = mahotas.thresholding.otsu(dna) # threshold by Otsu's method
#		umbral = 230 
		(count_pix, umbral) = calcular_iod(pixmap) # apply the algorithm
	
	return count_pix, umbral

def abre_salida(ruta):
	f_salida = ruta + "/output"
	salida = open(f_salida ,"w")
	salida.write("%s \t %s \t %s" % ("imagen", "pixels" , "umbral" "\n"))
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
			or fnmatch.fnmatch(current_file, '*.jpg') :
				
				# If it is the first file, it create the output file
				# Thus, it does not create file in the folders without
				if primer_fichero is True:
					salida = abre_salida(root);
					primer_fichero = False					
				
				print "Analyzing " + current_file
				(count_pix, umbral) = algoritmo(root, current_file)
				
				salida.write("\n%s \t %s \t %s" % (current_file,  str(count_pix), umbral))
		
		if primer_fichero is False:
			salida.close()

print "\nThis is the Funny Program based in pyFIA for area measurement by Image Analysis"
url = str(raw_input("\n>>>Type the path of the images: "))
aplicar_algoritmo(url)

print "\n FINISH \n"

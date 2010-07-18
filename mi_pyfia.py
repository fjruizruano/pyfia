# -*- coding: utf-8 -*-
import math
import fnmatch
import os
from PIL import Image

#
# La actual versión del algoritmo pyFIA para cada imagen/núcleo en una determinada ruta:
# 1. Lee la matriz de píxeles del canal verde de una imagen en color o el único canal si está en escala de grises.
# 2. Estima la media del fondo para definir un umbral.
# 3. A los píxeles cuya intensidad está por debajo del umbral se les calcula la densidad óptica.
# 4. La densidad óptica integrada es la suma de densidades ópticas para cada núcleo.
#

def algoritmo(ruta, foto):

	def calcular_iod(pixmap, lower_limit, upper_limit, gap_limit):
		
		iod = 0 # densidad óptica integrada de cada núcleo
		pixels_fondo = 0 # número de píxels del fondo
		suma_fondo = 0 # suma de valores de los píxeles del fondo
		media_fondo = 0 # valor medio de los píxeles del fondo
		umbral = 0 # valor de píxel por debajo del cual se considera núcleo
		
		for pixels in pixmap:
			if lower_limit < int(pixels) < upper_limit: 
				pixels_fondo += 1
				suma_fondo += int(pixels)

		media_fondo = 1.0 * suma_fondo/pixels_fondo # calcula la media del fondo de la imagen
		umbral = -math.log10((media_fondo-gap_limit)/media_fondo) # define el umbral entre núcleo y fondo

		for pixels in pixmap:
			if int(pixels) != 0:  
				logaritmo = -math.log10(int(pixels)/media_fondo)  # calcula densidad óptica individual de cada píxel
			else:
				logaritmo = 0 # para que no dé error si el valor de píxel es 0

			if logaritmo > umbral:
				iod += logaritmo # calcula densidad óptica integrada del núcleo
				
		return iod, media_fondo

	direccion = ruta +"/" + foto # Ruta completa a la imagen

	if fnmatch.fnmatch(foto, '*.tif'):
		imagen = Image.open(str(direccion))
		pixmap = list(imagen.getdata(1))
		(iod, media_fondo) = calcular_iod(pixmap, 180, 210, 10)
	elif fnmatch.fnmatch(foto, '*.txt') :
		imagen = open(str(direccion), 'r')
		leer = imagen.read()
		pixmap = leer.split()
		(iod, media_fondo) = calcular_iod(pixmap, 30000, 50000, 640)
	
	return iod, media_fondo

def abre_salida(ruta):
	f_salida = ruta + "/output"
	salida = open(f_salida ,"w")
	salida.write("%s \t %s \t \t %s" % ("imagen", "IOD", "fondo" "\n"))
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
				(iod, media_fondo) = algoritmo(root, current_file)
				
				iod_str = str(iod).replace(".", ",")
				media_fondo_str = str(media_fondo).replace(".", ",")
				salida.write("\n%s \t %s \t %s" % (current_file, iod_str, media_fondo_str))
		
		if primer_fichero is False:
			salida.close()


print "\nThis is the Funny Program for Feulgen Image Analysis Densitometry"
url = str(raw_input("\n>>>Introduzca ruta de las imagenes:"))
aplicar_algoritmo(url)

print "\n FINISH \n"

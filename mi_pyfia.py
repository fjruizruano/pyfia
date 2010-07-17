# -*- coding: utf-8 -*-
from commands import *
import commands
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

print "\nThis is the Funny Program for Feulgen Image Analysis Densitometry"

##Definimos el algoritmo que se aplica a cada imagen

def algoritmo(ruta, foto, extension, fichero_salida):

	#nota para facilitar: imagen en la funcion algoritmo es foto

	iod = 0

	sumapixels = 0

	sumafondo = 0

	fondo = 0
	
	umbral = 0

	direccion = ruta +"/" + foto


	if extension != ".txt":

		imagen = Image.open(str(direccion))

		pixmap = list(imagen.getdata(0))

		for pixels in pixmap:

#			print pixels

			if 180 < pixels < 210: # umbral puesto "a ojo" para calcular media del fondo

				sumapixels += 1

				sumafondo += pixels

		fondo = 1.0 * sumafondo/sumapixels # calcula la media del fondo de la imagen

		umbral = -math.log10((fondo-10)/fondo) # define el umbral entre núcleo y fondo

		for pixels in pixmap:

			if pixels != 0:  

				logaritmo = -math.log10(pixels/fondo)  # calcula densidad óptica de los píxels
    
			else:

				logaritmo = 0 # para que no dé error si el valor de píxel es 0


			if logaritmo > umbral:

				iod += logaritmo # calcula densidad óptica integrada del núcleo


	elif extension == ".txt":

		imagen = open(str(direccion), 'r')

		leer = imagen.read()

		pixmap = leer.split()

		for pixels in pixmap:

#			if 52000 < int(pixels) < 55000: # umbral puesto "a ojo" para calcular media del fondo

			if 30000 < int(pixels) < 50000:

				sumapixels += 1

				sumafondo += int(pixels)

		fondo = 1.0 * sumafondo/sumapixels # calcula la media del fondo de la imagen

		umbral = -math.log10((fondo-640)/fondo) # define el umbral entre núcleo y fondo

		for pixels in pixmap:

			if int(pixels) != 0:  

				logaritmo = -math.log10(int(pixels)/fondo) # calcula densidad óptica de los píxels
    
			else:

				logaritmo = 3 # para que no dé error si el valor de píxel es 0

			if logaritmo > umbral:

				iod += logaritmo # calcula densidad óptica integrada del núcleo

	iod = str(iod)
	fondo = str(fondo)

	posicion = iod.find(".")	#encuentra en una cadena el caracter .
	posicion1 = fondo.find(".")

	lista_temp = list(iod)		#pasamos iod de cadena a lista
	lista_temp1 = list(fondo)

	lista_temp[posicion] = ","	#cambiamos el caracter . por , en la lista
	lista_temp1[posicion1] = ","

	iod = "".join(lista_temp)	#pasamos iod de lista a cadena
	fondo = "".join(lista_temp1)

	fichero_salida.write("\n%s \t %s \t %s" % (foto, iod, fondo))

def abre_salida(ruta):
	f_salida = ruta + "/output"
	salida = open(f_salida ,"w")
	salida.write("%s \t %s \t \t %s" % ("imagen", "IOD", "fondo" "\n"))
	salida.write("-" * 40)
	return salida

for root, dirs, files in os.walk('/home/ruano/feulgen'):
	print '\n@@@@@@@@@@@@@@@@'
	print root # Ruta en la que estamos
	print files # Ficheros que contiene
	
	# Creo el fichero de salida
	primer_txt = True;

	for current_file in files:
		
		if fnmatch.fnmatch(current_file, '*.txt'):
			print current_file + " is an txt "
			if primer_txt is True:
				salida = abre_salida(root);
				primer_txt = False
			algoritmo(root, current_file, '.txt', salida)
	
	if primer_txt is False:
		salida.close()

print "\n FINISH \n"

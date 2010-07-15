# -*- coding: utf-8 -*-
from commands import *
import commands
import math
import fnmatch
import os
from PIL import Image

#
# DEFINICIÓN DEL ALGORITMO
#
# POR JESUCRISTO, COMÉNTALO
#

# Hay que tener en cuenta que el umbral en este caso esta puesto
# de forma arbitraria en un valor de 0.7 (0.16)
#
print "\nThis is the Funny Program for Feulgen\'s Reaction Image Analysis"
#fondo = float(raw_input("\nIndique media fondo: "))

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

			if 1 < pixels < 255:

				sumapixels += 1

				sumafondo += pixels

		fondo = 1.0 * sumafondo/sumapixels

		umbral = -math.log10((fondo-10)/fondo)

		for pixels in pixmap:

			if pixels != 0:  

				logaritmo = -math.log10(pixels/fondo)
    
			else:

				logaritmo = 0


			if logaritmo > umbral:

				iod += logaritmo


	elif extension == ".txt":

		imagen = open(str(direccion), 'r')

		leer = imagen.read()

		pixmap = leer.split()

		for pixels in pixmap:


#			if 52000 < int(pixels) < 55000:

#			if 42000 < int(pixels) < 45000:

#			if 38500 < int(pixels) < 41000:

#			if 45500 < int(pixels) < 48000:

#			if 46500 < int(pixels) < 49000:

#			if 44500 < int(pixels) < 47000:

			if 37500 < int(pixels) < 40000:


			#	print int(pixels)

				sumapixels += 1

				sumafondo += int(pixels)

#			print sumafondo

		fondo = 1.0 * sumafondo/sumapixels

#		print fondo

		umbral = -math.log10((fondo-640)/fondo)

		for pixels in pixmap:

			if int(pixels) != 0:  

				logaritmo = -math.log10(int(pixels)/fondo)
    
			else:

				logaritmo = 3

			if logaritmo > umbral:

				iod += logaritmo

#	print iod

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

for root, dirs, files in os.walk('/home/jlpino/00facul/pyfia/pyfia/'):
	print '@@@@@@@@@@@@@@@@'
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


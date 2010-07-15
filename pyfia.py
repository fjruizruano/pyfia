from commands import *
import commands

#####################################################
######creamos archivo con listado de imagenes########
#####################################################

def run_command(cmd):
    getstatusoutput(cmd)

# url = str(raw_input("\n>>>Introduzca ruta de las imagenes:"))

url = "/home/ruano/feulgen"

print "\nNota: Los nombres de las imagenes deben estar"
print "compuestas de una sola palabra, sin espacios"

home = str(commands.getoutput("echo $HOME"))

url_temp_folders = str(home + "/.temp_folders")    #poner oculto

url_temp_files = str(home + "/.temp_files")        #poner oculto

comando1 = str("ls " + url + " > " + home + "/.temp_folders")    #oculto contiene lista de folders

run_command(comando1)

################################################################
######creamos lista que contiene direcciones de carpetas########
################################################################

lista_folders = []

file_read_folders = open(url_temp_folders)

for linea in file_read_folders:
        
    lista_folders.append(linea)


###Con este bucle eliminamos el caracter de retorno de carro \n 

i = 0

for folder in lista_folders:

    ruta = folder[0:-1]
    lista_folders[i] = str(ruta)
    i += 1


################################################################
######definimos las extensiones con que vamos a trabajar #######
################################################################

#extension = ".jpg"

extension = ".txt"

#extension = str(raw_input("\n\t>>>Introduzca extension de archivos (nada = jpg): "))

#if len(extension) == 0:

#	extension = "jpg"

#extension = "." + extension


#####################################################
######Aplicamos el algoritmo_paco a cada una ########
#####################################################

# -*- coding: utf-8 -*-
#
# Hay que tener en cuenta que el umbral en este caso esta puesto
# de forma arbitraria en un valor de 0.7 (0.16)
#


print "\nThis is the Funny Program for Feulgen\'s Reaction Image Analysis"

import math

from PIL import Image

#fondo = float(raw_input("\nIndique media fondo: "))

##Definimos el algoritmo que se aplica a cada imagen

def algoritmo(foto):

	#nota para facilitar: imagen en la funcion algoritmo es foto

	iod = 0

	sumapixels = 0

	sumafondo = 0

	fondo = 0
	
	umbral = 0

	direccion = str(url2 +"/" + foto)


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

	salida.write("\n%s \t %s \t %s" % (foto, iod, fondo))




#############################################################
######Creamos la lista de archivos y aplicamos algoritmo#####
#############################################################

for folder in lista_folders:

	url2 = url + "/" + folder

	comando2 = str("ls " + url2 + " | grep '" + extension + "'" + " > " + home + "/.temp_files")	#oculto contiene lista de files

	run_command(comando2)

	lista_files = []

	file_read_files = open(url_temp_files)

#creamos la lista_files que contiene direcciones de imagenes

	for linea in file_read_files:
		
		linea = str(linea[0:-1])	#eliminamos el caracter de retorno de carro \n	
		   
		lista_files.append(linea)	


	print "\n>>", len(lista_files), "ficheros en el directorio " + folder

	###Comprobacion de carpeta. Si esta vacia se sale del programa

	if len(lista_files) == 0:

		print "\nAtencion: El directorio no contiene ficheros"
		break

###Creamos archivo que contiene los calculos 

	salida = open(url2 + "/output","w") #crea archivo en la carpeta indicada
	salida.write("%s \t %s \t \t %s" % ("imagen", "IOD", "fondo" "\n"))
	salida.write("-" * 40)

	for imagen in lista_files:

		algoritmo(str(imagen))

		print imagen		#puede ser util para conocer el progreso

	salida.close()

#####################################################
######Borramos archivos temporales y ceramos ########
#####################################################

file_read_folders.close()
file_read_files.close()

comando_borrar_folders = "rm " + url_temp_folders
comando_borrar_files = "rm " + url_temp_files  

run_command(comando_borrar_folders)
run_command(comando_borrar_files)

print "\nSe han creado", len(lista_folders), "archivos\n"


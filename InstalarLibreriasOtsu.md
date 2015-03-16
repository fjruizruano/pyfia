# Cómo Instalar #

En primer lugar es necesario instalar algunas librerías y herramientas que se encuentran en los repositorios de Debian y Ubuntu. En un terminal escribimos:

sudo aptitude install python-numpy ipython python-matplotlib python-scipy python-dev python-setuptools python-all python-all-dev

Para instalar 'pymorph' y 'mahotas' podemos descargarlos desde su página oficial o empleando 'pip' (más sencillo):

Instalamos pip mediante:

sudo aptitude install python-pip

E instalamos los paquetes con 'pip' mediante:

sudo pip install pymorph

sudo pip install mahotas


# Script de comprobación #

import mahotas

import scipy

dna = scipy.misc.pilutil.imread('./78g.tif')

T = mahotas.thresholding.otsu(dna)

print T
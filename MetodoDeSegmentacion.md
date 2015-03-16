La segmentación consiste en aislar objetos del fondo de una imagen, regiones distintas que son homogéneas en alguna propiedad como puede ser la intensidad de píxel.

El método más extendido de segmentación está basado en conceptos topográficos. Consiste en representar la imagen con tres dimensiones, donde la "base" viene dada por la posición de cada píxel en la imagen, mientras que la altura es la intensidad de píxel. Esto es denominado en inglés "watershed" (formación de cuencas hidrográficas). La búsqueda de regiones se hace simulando que esa "orografía" es inundada y determinando en qué regiones se forman "lagos", que van a corresponder a cada objeto. Así de delimitan unas líneas que corresponde a cada una de estas cuencas.

Ver Wikipedia http://en.wikipedia.org/wiki/Watershed_%28algorithm%29

Ver animaciones http://cmm.ensmp.fr/~beucher/wtshed.html

Ver Scipy http://www.scipy.org/Cookbook/Watershed

Basado en http://pythonvision.org/basic-tutorial.

# Pasos para la segmentación #

1. Abrir imagen.

2. Aplicar un filtro gaussiano para no tener bordes con imperfecciones.

3. Buscar zonas con valores de píxel mínimos respecto a su entorno. Estas serán las semillas.

4. Determinar valor umbral por el método de Otsu.

5. Definimos una distancia para discriminar distintos objetos solapados.

6. Convertir imagen en un relieve.

7. Dividir en regiones.

8. Eliminar regiones con objetos cortados por los bordes.


# Ejemplo de script #

#

# Script no comprobado

# Problemas para que se vean los corchetes, copiar en modo editar

#


import mahotas

import pymorph

import scipy

from scipy import ndimage

import numpy as np

import pylab


dna = scipy.misc.pilutil.imread('dna.jpeg') # abrir imagen

dnaf = ndimage.gaussian\_filter(dna, 8) # filtro gaussiano

rmin = pymorph.regmin(dnaf) # buscar mínimos regionales

seeds,nr\_nuclei = ndimage.label(rmin) # marcar semillas

T = mahotas.thresholding.otsu(dnaf) # buscar valor umbral

dist = ndimage.distance\_transform\_edt(dnaf > T)

dist = dist.min() - dist

dist -= dist.max()

dist = dist/float(dist.ptp()) **255**

dist = dist.astype(np.uint8) # distancia para discriminar objetos solapados

nuclei = pymorph.cwatershed(dist, seeds) # convertir imagen en relieve

whole = mahotas.segmentation.gvoronoi(nuclei) # dividir según las distintas cuencas encontradas

# para eliminar objetos cortados por los bordes

borders = np.zeros(nuclei.shape, np.bool)

borders[0,:]= 1

borders[-1,:] = 1

borders[:, 0] = 1

borders[:,-1] = 1

at\_border = np.unique(nuclei[borders](borders.md))

for obj in at\_border:

> whole[== obj](whole.md) = 0

# ver resultado

pylab.imshow(whole)

pylab.show()
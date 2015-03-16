| **Fecha** | **Versión** | **Resumen** |
|:----------|:-------------|:------------|
| 20/09/2010 | 0.1 | Funcionalidades básicas |
|  | 0.2 | Segmentación automática |

# pyfia 0.1 #
  * Interfaz web que permite subir varias imágenes (o matrices de píxeles en txt), que deben tener una única célula.

  * El procesamiento (en el lado del servidor):
    1. Se lee la imagen
    1. Se estima el umbral por el método de Otsu.
    1. Se estima la media del fondo (píxeles mayores que el umbral).
    1. Se calcula la suma de la densidad óptica de los píxeles por debajo del umbral.


# pyfia 0.2 #
  * Segmentación automática
  * Interfaz para seleccionar las células deseadas.


# Futuras funcionalidades #

  * Soporte real para imágenes TIFF a 16 bits (opencv las abre, pero las carga como 8 bits).
  * Realización y análisis de histogramas.
  * Cuentas de usuario, almacenamiento en BD y estadísticas.
  * Grupos de trabajo para compartir resultados.
  * Obtener información EXIF de las imágenes.

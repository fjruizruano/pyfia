pyFIA have been development and testing in GNU/Linux Debian and Ubuntu distributions. This instructions are adjusted for it.

# Installation #

Firstly we have to install some libreries and tools found in repositories. In a terminal type:

**$ sudo aptitude install python-numpy ipython python-matplotlib python-scipy python-dev python-setuptools python-all python-all-dev**

For 'pymorph' and 'mahotas' installation we can download it from its project's web or using 'pip' (simpler). We install pip typing:

**$ sudo aptitude install python-pip**

And install this packages with 'pip':

**$ sudo pip install pymorph**

**$ sudo pip install mahotas**

Then we can check the installation write in python:

**>>> import mahotas**

**>>> import scipy**

**>>> dna = scipy.misc.pilutil.imread('./file.tif')**

**>>> T = mahotas.thresholding.otsu(dna)**

**>>> print T**

# Running #

Files from each sample have to show .txt, .tif, .jpg extension to be recognized pyFIA.

Download pyfia.py or pyfia\_area.py script from Downloads pages or typing:

**$ svn checkout http://pyfia.googlecode.com/svn/ pyfia-read-only**

Eject pyFIA with:

**$ python pyfia.py**

**$ python pyfia\_area.py**

pyFIA will wonder us the path where file are, if they are in the same folder that the script you have to type **"."**. It walks all folders and analyzes files for each folder and the results are saved in a text file called "output".

Results can be opened with Gnumeric or other spreadsheet.
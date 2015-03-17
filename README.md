

#How to install and run pyFIA.

pyFIA has been developed and tested in GNU/Linux Debian and Ubuntu distributions. These instructions explain how to use it in these environments.

##Installation##

Firstly, we have to install some libreries and tools that can be found in repositories. In a terminal, type:

```bash
sudo aptitude install python-numpy ipython python-matplotlib python-scipy python-dev python-setuptools python-all python-all-dev
```
For 'pymorph' and 'mahotas' can be installed using 'pip'. To install pip:

```sudo aptitude install python-pip```

And install this packages with 'pip':

```sudo pip install pymorph```

```sudo pip install mahotas```

Then we can check the installation by typing the following commands in Python's interactive shell:

```
import mahotas
import scipy
dna = scipy.misc.pilutil.imread('./file.tif')
T = mahotas.thresholding.otsu(dna)
print T
```

##Running##

Sample files must have .txt, .tif or .jpg extension to be found by pyFIA.

You can download the source code from the repository using::

```git clone https://github.com/fjruizruano/pyfia.git```

You can execute pyFIA with:

```python pyfia.py```

```python pyfia_area.py```

You must provide the path of the files to pyFIA. If they are in the same folder that the script, you can just type ".". The script will also analyse the subfolders and store the result in a text file called "output".

The resulting files can open with Gnumeric or other spreadsheet software.

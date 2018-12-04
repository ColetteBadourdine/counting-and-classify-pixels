#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from osgeo import gdal
from math import sqrt
import numpy as np
from pprint import pprint

A = [659010, 5256483]
# B=[679728, 5663085]
B = [679728, 5263085]
nb_cercle = 10


# fonction attribution des points pour que le point A ait toujours la plus petite valeur de x
# on est pas sure que cela soit completement necessaire pour la fonction distrib_forme
def pluspetitx(A, B):
    if A[0] >= B[0]:
        A, B = B, A
    return(A, B)


def distance(A, B):
    l = sqrt((A[0] - B[0])**2 + (A[1] - B[1])**2)
    return l


def distrib_forme(A, B, nb_cercle=10):
    """fonction pour placer les centres des cercles"""
    liste_centre = []
    for i in np.linspace(0, nb_cercle, nb_cercle, endpoint=False):
        x = A[0] + (i / (nb_cercle-1)) * (B[0] - A[0])
        y = A[1] + i / (nb_cercle-1) * (B[1] - A[1])
        liste_centre.append([x, y])
    return liste_centre


l = distance(A, B)
print 'longueur AB = %.1f' % l

R = (l / (nb_cercle-1)) / 2
print 'rayon = %.1f' % R

# on ouvre l'image
fichier = 'angers_2010_red4.tif'
ds = gdal.Open(fichier, gdal.GA_ReadOnly)
if ds is None:
    print("impossible d'ouvrir : %s" % file)
    sys.exit(1)

image = ds.ReadAsArray()

# On recupere les coordonnees des pixels
geotransform = ds.GetGeoTransform()
originX = geotransform[0]
originY = geotransform[3]
pixelWidth = geotransform[1]
pixelHeight = geotransform[5]
centres = distrib_forme(A, B, nb_cercle=nb_cercle)

print "originX = %f, originY = %f" % (originX, originY)
print "pixelWidth = %f, pixelHeight = %f" % (pixelWidth, pixelHeight)

point_cercle = {k: {} for k in range(nb_cercle)}
print point_cercle
mindist = 1e8
for k in range(nb_cercle):
    print k, centres[k]
    for i in range(ds.RasterXSize):
        x = originX + i * pixelWidth
        for j in range(ds.RasterYSize):
            y = originY + j * pixelHeight
            d = distance((x, y), centres[k])
            mindist = min(d, mindist)
            if d < R:
                cercle_k = point_cercle[k]
                c = image[j, i]
                if c in cercle_k.keys():
                    cercle_k[c] += 1
                else:
                    cercle_k[c] = 0
print("")
for k, v in point_cercle.iteritems():
    print("Nombre de pixel dans le cercle %d : %d" % (k, sum(v.values())))
    print("Répartition des pixels par classe : ")
    pprint(v)
    print("")

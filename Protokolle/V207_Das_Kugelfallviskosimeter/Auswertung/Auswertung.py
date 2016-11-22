import numpy as np
from scipy.stats import sem
from uncertainties import ufloat
import uncertainties.unumpy as unp
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

daten = np.genfromtxt("Daten.txt", unpack = True)

RadiusGr  = np.array([0.01561/2, 0.01560/2, 0.01560/2])
RadiusKl  = np.array([0.01543/2, 0.01544/2, 0.01543/2])
GewichtGr = np.array([0.00496, 0.00496, 0.00496])
GewichtKl = np.array([0.00445, 0.00445, 0.00445])

s = 1 / np.sqrt(3)

Rgr = ufloat(np.mean(RadiusGr), np.std(RadiusGr, ddof = 1) * s)
Rkl = ufloat(np.mean(RadiusKl), np.std(RadiusKl, ddof = 1) * s)
Ggr = ufloat(np.mean(GewichtGr), np.std(GewichtGr, ddof = 1) * s)
Gkl = ufloat(np.mean(GewichtKl), np.std(GewichtKl, ddof = 1) * s)

#Auslesen und Mitteln der Daten

FallzeitKugel2 = ufloat(np.mean(daten[0]), np.std(daten[0], ddof = 1) * s)
FallzeitKugel1 = ufloat(np.mean(daten[1]), np.std(daten[1], ddof = 1) * s)
Temperaturen = daten[2]
Messungen = np.array([daten[3], daten[4]])
Messungen = np.transpose(Messungen)

Mittelwerte = np.array([ np.mean(row) for row in Messungen ])
Fehler = np.array([s * np.std(row) for row in Messungen])
kombiniert = np.array([ufloat(n, Fehler[i]) for i,n in enumerate(Mittelwerte)])

#Ermittlung der Kugeldichte und benötigte Daten

DichteKl = Gkl / (4/3 * np.pi * Rkl**3)
DichteKl /= 1000                         # Anpassung in g/cm^3
DichteGr = Ggr / (4/3 * np.pi * Rgr**3)
DichteGr /= 1000                         # Anpassung in g/cm^3
DichteW = 1.000
Kkl = 0.07640/1000 # Umrechnung in Pa * cm^3 / g
Strecke = 0.1

#Ermittlung von K

Kgr = (Kkl * (DichteKl - DichteW) * FallzeitKugel2) / ( (DichteGr - DichteW) * FallzeitKugel1)

print(Kkl * (DichteKl - DichteW) * FallzeitKugel2)

print(Kgr * 1000)

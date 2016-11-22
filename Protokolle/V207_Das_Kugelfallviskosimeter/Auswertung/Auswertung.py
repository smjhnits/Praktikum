import numpy as np
from scipy.stats import sem
from uncertainties import ufloat
import uncertainties.unumpy as unp
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

RadiusGr  = np.array([0.01561, 0.01560, 0.01560])
RadiusKl  = np.array([0.01543, 0.01544, 0.01543])
GewichtGr = np.array([0.00496, 0.00496, 0.00496])
GewichtKl = np.array([0.00445, 0.00445, 0.00445])

Strecke = 0.1

daten = np.genfromtxt("Daten.txt", unpack = True)
s = 1 / np.sqrt(3)

FallzeitKugel2 = ufloat(np.mean(daten[0]), np.std(daten[0], ddof = 1) * s)
FallzeitKugel1 = ufloat(np.mean(daten[1]), np.std(daten[1], ddof = 1) * s)

Temperaturen = daten[2]

Messungen = np.array(daten[3], daten[4])
Mesungen = Messungen.T

print(Messungen)

Rgr = ufloat(np.mean(RadiusGr), np.std(RadiusGr, ddof = 1) * s)
Rkl = ufloat(np.mean(RadiusKl), np.std(RadiusKl, ddof = 1) * s)
Ggr = ufloat(np.mean(GewichtGr), np.std(GewichtGr, ddof = 1) * s)
Gkl = ufloat(np.mean(GewichtKl), np.std(GewichtKl, ddof = 1) * s)

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

print("Radius große Kugel: ", Rgr)
print("Gewicht große Kugel: ", Ggr)
print("Radius kleine Kugel: ", Rkl)
print("Gewicht kleine Kugel: ", Gkl)
print('\n')

#Auslesen und Mitteln der Daten

FallzeitKugel2 = ufloat(np.mean(daten[0]), np.std(daten[0], ddof = 1) * s)
FallzeitKugel1 = ufloat(np.mean(daten[1]), np.std(daten[1], ddof = 1) * s)
Temperaturen = daten[2]
Temperaturen += 273.15
Messungen = np.array([daten[3], daten[4]])
Messungen = np.transpose(Messungen)

print("Fallzeit kleine Kugel: ", FallzeitKugel2)
print("Fallzeit große Kugel: ", FallzeitKugel1)
print("Temperaturen: ", Temperaturen)
print('\n')

Mittelwerte = np.array([ np.mean(row) for row in Messungen ])
Fehler = np.array([s * np.std(row) for row in Messungen])
kombiniert = np.array([ufloat(n, Fehler[i]) for i,n in enumerate(Mittelwerte)])

print("Messung der Fallzeiten: ", kombiniert)
print('\n')

#Ermittlung der Kugeldichte und benötigte Daten

DichteKl = Gkl / (4/3 * np.pi * Rkl**3)
DichteKl /= 1000                         # Anpassung in g/cm^3
DichteGr = Ggr / (4/3 * np.pi * Rgr**3)
DichteGr /= 1000                         # Anpassung in g/cm^3
DichteW = 0.998
DichteW_array = np.array([0.9957, 0.994, 0.9922, 0.9902, 0.9880, 0.9980, 0.9857, 0.9832, 0.9806, 0.9778])
Kkl = 0.07640/1000                       # Umrechnung in Pa * cm^3 / g
Strecke = 0.1

print("Dichte der kleinen Kugel: ", DichteKl)
print("Dichte der großen Kugel: ", DichteGr)
print("Dichte Wasser: ", DichteW)
print('\n')

#Ermittlung von K

Viskositätkl20 = (Kkl * (DichteKl - DichteW) * FallzeitKugel2)
Kgr = Viskositätkl20 / ( (DichteGr - DichteW) * FallzeitKugel1)
print("Viskosität kleiner Kugel: ", Viskositätkl20)
print("Apparaturkonstante kleine Kugel: ", Kkl)
print("Apparaturkonstante große Kugel: ", Kgr)
print('\n')

#Umrechnung in milliPascal *cm^3 / g

Kgr1 = Kgr*1000

#Ermittlung der ViskositäTemperaturen

Viskos = np.array([ Kgr * (DichteGr - DichteW_array[i]) * n for i,n in enumerate(kombiniert) ])
print("Viskositäten: ", Viskos)

#Plot anfertigen

yAchse = unp.log(Viskos)
xAchse = 1 / kombiniert

plt.plot(1/Temperaturen, unp.nominal_values(Viskos), "b-",)
plt.title("Viskos gegen T")
plt.yscale('log')
#plt.xlim(300, 350)
#plt.ylim(0.5e-5, 1.5e-5)
plt.show()

#Geschwindigkeiten

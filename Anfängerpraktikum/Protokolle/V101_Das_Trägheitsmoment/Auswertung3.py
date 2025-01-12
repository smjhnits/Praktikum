import numpy as np
from scipy.stats import sem
from uncertainties import ufloat
import uncertainties.unumpy as unp

Zeiten = np.genfromtxt("Restdaten.txt", unpack = True)

#print(Zeiten[2:])

Zeiten /= 5

#print(Zeiten[2:])

daten = np.genfromtxt("WRGdyn.txt", unpack = True)

Mittelwerte = np.array([np.mean(row) for row in Zeiten])
Fehler = np.array([np.std(row, ddof = 1) for row in Zeiten])
s = 1/np.sqrt(len(Zeiten[0]))
Fehler = s*Fehler

T = np.array([ufloat(x, Fehler[index]) for index, x in np.ndenumerate(Mittelwerte)])

Wrg = ufloat(daten[0], daten[1])
Id = ufloat(daten[2], daten[3])

#Trägheitsmoment der Kugel

MasseK = 0.8124
RadiusK = 0.13766 / 2

Ik_theoretisch = 2/5 * MasseK * RadiusK**2

Ik_praktisch = T[0]**2 * Wrg /(4* (np.pi**2)) - Id

#print("IK: ")
#print(T[0])
print(Ik_theoretisch, Ik_praktisch)
print(Ik_praktisch/Ik_theoretisch)

#trägheitsmoment des Zylinders

MasseZ = 1.0058
RadiusZ = 0.08024/2
HöheZ = 0.13990

Iz_theoretisch = 1/2 * MasseZ * RadiusZ**2

Iz_praktisch = T[1]**2 * Wrg / (4* (np.pi**2)) - Id

#print("IZ: ")
#print(T[1])
print(Iz_theoretisch, Iz_praktisch)
print(Iz_praktisch/Iz_theoretisch)

#Trägheitsmoment Position 1

Ip1 = T[2]**2 * Wrg / (4 * (np.pi**2)) - Id

#Trägheitsmoment Position 2

Ip2 = T[3]**2 * Wrg / (4 * (np.pi**2)) - Id

#print(T[2], T[3])
print(Ip1, Ip2)

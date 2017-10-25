import numpy as np
from scipy.stats import sem
from uncertainties import ufloat
import uncertainties.unumpy as unp

daten = np.genfromtxt("Daten797.txt", unpack = False)
daten = daten.T

daten[0:3] /= 5

Mittelwerte = np.array([np.mean(row) for row in daten])

Abweichungen = np.array([np.std(row, ddof = 1) for row in daten])

s = 1/np.sqrt(len(daten[0]))

Abweichungen = s*Abweichungen

u = np.array([ufloat(x, Abweichungen[index]) for index, x in np.ndenumerate(Mittelwerte)])

K = (u[3]**2 - u[2]**2)/(u[3]**2 + u[2]**2)

T = (u[3]*u[2])/(u[3] - u[2])

Werte = np.append([Mittelwerte], [[K.n], [T.n]])
Fehler = np.append([Abweichungen], [[K.s], [T.n]])

np.savetxt("Werte797.txt", np.column_stack([Werte, Fehler]), header = "Werte und Fehler, Reihenfolge: T links, T rechts, T gegen, T gleich, T Schwebung, T 5 Schwebungen, K, T Schwebung berechnet")

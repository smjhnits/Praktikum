import numpy as np
from scipy.stats import sem
from uncertainties import ufloat
import uncertainties.unumpy as unp

daten = np.genfromtxt("Daten946.txt", unpack = False)
daten = daten.T

daten[0] = daten[0]/5
daten[1] = daten[1]/5
daten[2] = daten[2]/5
daten[3] = daten[3]/5

Mittelwerte = np.array([np.mean(row) for row in daten])

Abweichungen = np.array([np.std(row, ddof = 1) for row in daten])

s = 1/np.sqrt(len(daten[0]))

Abweichungen = s*Abweichungen

u = np.array([ufloat(x, Abweichungen[index]) for index, x in np.ndenumerate(Mittelwerte)])

K = (u[3]**2 - u[2]**2)/(u[3]**2 + u[2]**2)

T = (u[3]*u[2])/(u[3] - u[2])

Werte = [Mittelwerte[0], Mittelwerte[1], Mittelwerte[2], Mittelwerte[3],
            Mittelwerte[4], Mittelwerte[5], K.n, T.n]
Fehler = [Abweichungen[0], Abweichungen[1], Abweichungen[2], Abweichungen[3],
            Abweichungen[4], Abweichungen[5], K.s, T.n]

np.savetxt("Werte946.txt", np.column_stack([Werte, Fehler]), header = "Werte und Fehler, Reihenfolge: T links, T rechts, T gegen, T gleich, T Schwebung, T 5 Schwebungen, K, T Schwebung berechnet")

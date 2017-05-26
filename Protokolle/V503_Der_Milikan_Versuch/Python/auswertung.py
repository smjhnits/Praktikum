import numpy as np
import math
from scipy.stats import sem
from uncertainties import ufloat
import uncertainties.unumpy as unp
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import scipy.constants as const
from uncertainties.unumpy import (nominal_values as noms, std_devs as stds)
from pint import UnitRegistry

u = UnitRegistry()
Q_ = u.Quantity
g = Q_(const.g, 'meter / (second**2)')
e_0 = Q_(const.e, 'coulomb')
dichte_oel = Q_(886, 'kilogram / meter**3')
d_Kondensator = Q_(ufloat(7.6250, 0.0051), 'millimeter')
print(const.e)
## Fitfunktionen

def poly(x, a, b, c):
    return a * x**2 + b * x + c

def linear(x, a, b):
    return a * x + b

## Messwerte

widerstand_gemessen = np.array([1.96, 1.92, 1.87, 1.81, 1.78, 1.71, 1.75, 1.75, 1.75, 1.75, 1.74, 1.74, 1.73, 1.73, 1.73, 1.72, 1.73, 1.72, 1.72, 1.72, 1.71, 1.71, 1.71, 1.71, 1.71, 1.7, 1.7, 1.71, 1.7, 1.7])


t_0 = np.array([17.78, 29.26, 35.03, 15.76, 34, 23.2, 15.41, 6.83, 11.4, 6.61, 9.93, 18, 19.26, 13.78, 9.4, 20.3, 11.56, 6.84, 13.58, 15.49, 8.49, 9.55, 8.13, 15.55, 9.03, 12.13, 16.18, 12.67, 6.95, 14.95])

U_gleichgewicht = Q_(np.array([269, 96, 11, 58, 35, 147, 77, 187, 200, 112, 118, 53, 61, 41, 134, 92, 122, 113, 50, 40, 76, 76, 175, 140, 192, 140, 113, 118, 155, 90]), 'volt')

temp = np.linspace(10, 39, 30)
Widerstand = np.array([3.239, 3.118, 3.004, 2.897, 2.795, 2.7, 2.61, 2.526, 2.446, 2.371, 2.3, 2.233, 2.169, 2.11, 2.053, 2, 1.95, 1.902, 1.857, 1.815, 1.774, 1.736, 1.7, 1.666, 1.634, 1.603, 1.574, 1.547, 1.521, 1.496])

## Temperatur

params_temp, covariance_temp = curve_fit(poly, Widerstand, temp)

temp_gemessen = poly(widerstand_gemessen, *params_temp)
x_temp = np.linspace(1.65, 2, 1000)
plt.clf()
plt.plot(widerstand_gemessen, temp_gemessen, 'rx', label = r'Temperatur')
plt.plot(x_temp, poly(x_temp, *params_temp), 'b-', label = r'Fit')
plt.xlabel(r'Widerstand in M$\Omega$')
plt.ylabel('Temperatur in C')
plt.xlim(1.67, 1.97)
plt.legend(loc='best')
plt.tight_layout()
plt.savefig('Temp.pdf')


## Viskosität von Luft

pkt = np.array([[16, 30], [1.805, 1.882]]) # Punkte von der Geraden Abb. 3

params_visko, covaraince_visko = curve_fit(linear, pkt[0], pkt[1])

visko_gemessen = Q_(linear(temp_gemessen, *params_visko) * 10**(-5), 'newton * second * meters**(-2)')

## Geschwindigkeit ohne E-Feld

v_0 = Q_(0.5/ t_0, 'millimeter / second') ## mm pro s

## Radius der Öltröpfchen ## dichte Luft vernachlässigen

r_oel = np.sqrt(9 * visko_gemessen * v_0 / (2 * g * dichte_oel))
r_oel = r_oel.to('millimeter')

#print(r_oel)

## korrigierte Ladung
p = Q_(1.01325, 'bar') ## Druck während der Messung
B = Q_(6.17 * 10**(-3), 'torr * cm')
korrektur = (1 + B / (p * r_oel))**(-3/2)  ## dimensionslos

E_feld = U_gleichgewicht / d_Kondensator


## Ladung bestimmen aus Kräftegleichgewicht

q  = 4 * np.pi / 3 * dichte_oel * r_oel**3 * g * 1 / E_feld
q = q.to('coulomb')
q_korrigiert = q * korrektur


## Ladungen im Vergleich zur Elementarladung

plt.clf()
ax1 = plt.subplot(2, 1, 2)
plt.plot(range(1, len(noms(q_korrigiert.magnitude)) + 1), np.sort(noms(q_korrigiert.magnitude)), 'kx', label = r'Messdaten')
#plt.axhline(y = e_0.magnitude, color = 'r', linewidth = 2, label = 'Elementarladung')
plt.yticks([e_0.magnitude, 2 * e_0.magnitude, 3 *  e_0.magnitude, 4 * e_0.magnitude, 5 * e_0.magnitude, 6 * e_0.magnitude, 7 * e_0.magnitude, 8 * e_0.magnitude, 9 * e_0.magnitude],
          [r"$e_0$", r"$2e_0$", r"$3e_0$" ,r"$4e_0$", r"$5e_0$", r"$6e_0$", r"$7e_0$", r"$8e_0$", r"$9e_0$"])
plt.grid()
plt.xlabel('Messreihe')
plt.ylabel('Elementaladungen')
plt.legend(loc='best')
plt.tight_layout()

ax2 = plt.subplot(2, 1, 1, sharex = ax1)
plt.plot(range(1, len(noms(q_korrigiert.magnitude)) + 1), noms(q_korrigiert.magnitude), 'kx', label = r'Messdaten')
#plt.axhline(y = e_0.magnitude, color = 'r', linewidth = 2, label = 'Elementarladung')
plt.yticks([e_0.magnitude, 2 * e_0.magnitude, 3 *  e_0.magnitude, 4 * e_0.magnitude, 5 * e_0.magnitude, 6 * e_0.magnitude, 7 * e_0.magnitude, 8 * e_0.magnitude, 9 * e_0.magnitude],
          [r"$e_0$", r"$2e_0$", r"$3e_0$" ,r"$4e_0$", r"$5e_0$", r"$6e_0$", r"$7e_0$", r"$8e_0$", r"$9e_0$"])
plt.grid()
plt.ylabel('Elementaladungen')
plt.xlim(-1, 31)
plt.legend(loc='best')
plt.tight_layout()
#plt.show()
plt.savefig('Ladungen_E_0.pdf')


## Bestimmung der eigenen Elementarladung
## Abstand der Ladungen untereinander bestimmen. zu geringe Abstände
## weglassen, da Resultat aus Messungenauigkeit


##sortieren der Messdaten
q_sortiert = Q_(np.sort(q_korrigiert), 'coulomb')
q_sort = noms(q_sortiert.magnitude)
#print(np.argmin(abs(q_sortiert.magnitude / e_0.magnitude - 1)))
n = q_sortiert[0]
q_sortiert[0] = q_sortiert[2]
q_sortiert[2] = n

#def round_dist(q, q_test):
#    test = np.zeros(len(q))
#    for i in range(len(q) - 1):
#        test[i] = np.round(q[i] / q_test)
#    return sum(test)

for i in range(len(noms(q_sortiert.magnitude)) - 1):
    if np.abs(q_sortiert[i + 1] - q_sortiert[i]) < e_0/2:
        q_sortiert[i + 1] = q_sortiert[i]

#best_value = np.zeros(len(noms(q_sortiert.magnitude)))
dist = 10**-19
e = const.e
q_test = np.linspace(e - dist, e + dist, len(q_sort)) ## testladungsarray
best_value = np.array([])

for i in range(len(q_sort) - 1): ## raussortieren der besten gemessenen werte
    if np.abs(q_sort[i + 1] - q_sort[i]) > e_0.magnitude /2:
        best_value = np.append(best_value, q_sort[i])

q_best = np.array([])

for i in range(len(best_value)): ## ladung mit geringestem abstand ist der Kandidat für die elementarladung
    q_best = np.append(q_best, np.abs(np.around(best_value[i] / q_test) - best_value[i] / q_test))

print(len(q_best))
print(best_value)
print(q_best[np.argmin(q_best)], np.argmin(q_best), np.abs(np.around(best_value[3] / q_test[14]) - best_value[3] / q_test[14]))
print(q_test[14], best_value[3])

print('bester wert für e_0:', q_test[14])
print('absoluter Fehler: ', q_test[14] - const.e)
print('relativer Fehler: ', np.abs(q_test[14] - const.e) / const.e)
print(q_test[14] / e)
#for i in range(len(noms(q_sortiert.magnitude))):
#    best_value[i] = round_dist(q_sortiert, q_sortiert[i])
#
#print(np.argmin(best_value))



plt.clf()
plt.plot(range(0, len(noms(q_sortiert.magnitude))), noms(q_sortiert.magnitude), 'kx', label = r'Messdaten')
#plt.axhline(y = e_0.magnitude, color = 'r', linewidth = 2, label = 'Elementarladung')
plt.yticks([e_0.magnitude, 2 * e_0.magnitude, 3 *  e_0.magnitude, 4 * e_0.magnitude, 5 * e_0.magnitude, 6 * e_0.magnitude, 7 * e_0.magnitude, 8 * e_0.magnitude, 9 * e_0.magnitude],
          [r"$e_0$", r"$2e_0$", r"$3e_0$" ,r"$4e_0$", r"$5e_0$", r"$6e_0$", r"$7e_0$", r"$8e_0$", r"$9e_0$"])
plt.grid()
plt.xlabel('Nummer der Messung')
plt.ylabel('Elementaladungen')
plt.xlim(-1, 31)
plt.legend(loc='best')
plt.tight_layout()
#plt.show()
#plt.savefig('sortierte_Ladungen_E_0.pdf')

## Messdaten auslagern
np.savetxt('Messdaten.txt', np.column_stack([widerstand_gemessen, t_0, U_gleichgewicht.magnitude, noms(r_oel.magnitude), stds(r_oel.magnitude), noms(q_korrigiert.magnitude), stds(q_korrigiert.magnitude)]), header = "widerstand t_0 U_g r_oel err q err")

import numpy as np
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
print(np.max(q), np.min(q))


## Ladungen im Vergleich zur Lementarladung

plt.clf()
plt.plot(range(0, len(noms(q_korrigiert.magnitude))), noms(q_korrigiert.magnitude), 'kx', label = r'Messdaten')
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
plt.savefig('Ladungen_E_0.pdf')


## Bestimmung der eigenen Elementarladung
## Abstand der Ladungen untereinander bestimmen. zu geringe Abstände
## weglassen, da Resultat aus Messungenauigkeit

import numpy as np
from scipy.stats import sem
import scipy.constants as const
from uncertainties import ufloat
import uncertainties.unumpy as unp
from uncertainties.unumpy import (nominal_values as noms, std_devs as stds)
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from PIL import Image
import scipy.misc
from pint import UnitRegistry

u = UnitRegistry()
Q_ = u.Quantity

## Wellenlängen in nm

lambda_b = Q_(480.0, 'nanometer')
n_b = 1.4635
h = Q_(const.h, 'joule * second')
e_0 = Q_(const.e, 'coulomb')
mu_bohr = Q_(const.physical_constants['Bohr magneton'][0], 'joule/tesla')
c = Q_(const.c, 'meter / second')
d = Q_(4, 'millimeter')

dispsgebiet_b = lambda_b**2 / (2 * d) * np.sqrt(1 / (n_b**2 - 1))


## Hysterese, B in mT


def poly(x, a, b, c, d):
    return a * x**3 + b * x**2 + c * x + d


B_auf = np.array([4, 87, 112,174, 230, 290, 352, 419,
476, 540, 600, 662, 714, 775, 823,872, 916, 959, 987,
1015, 1046, 1072])

B_ab = np.array([7, 57, 120, 180, 251, 306, 361, 428,
480, 550, 612, 654, 715, 780, 830, 878, 924, 962,
993, 1020, 1050, 1072])

I = np.linspace(0, 21, 22)

params_B_auf, covariance_B_auf = curve_fit(poly, I, B_auf)
params_B_ab, covariance_B_ab = curve_fit(poly, I, B_ab)

### BLAU ###

## Bild eins Zeitstempel 10:33

## Bild zwei I = 5.6 A Pol = +-1
## Abstände zwischen zwei Linien zu den benachbarten
## beiden Linien gemessen +->  |*|   |*| (so wurde 1 gemessen)
## zwei beinhaltet die Abstände der Peaks von einer gespaltenen Linie


##  Pixelbreiten der 3 + 13 Linie

pixel_03_b = np.array([(495 + 374) / 2, (830 + 714) / 2, (1118 +
1003) / 2, (1366 + 1265) / 2, (1573 + 1496) / 2, (1802 + 1715) / 2,
(1972 + 1911) / 2, (2156 + 2096) / 2, (2335 + 2272) / 2, (2499 + 2436) / 2])

pixel_04_b = np.array([(395 + 287) / 2, (568 + 468) / 2, (735 +
656) / 2, (876 + 803) / 2, (1028 + 958) / 2, (1143 + 1078) / 2, (1292 + 1216) / 2,
(1383 + 1330) / 2, (1515 + 1468) / 2, (1614 + 1553) / 2, (1726 + 1682) / 2,
(1820 + 1770) / 2, (1932 + 1881) / 2, (2011 + 1970) / 2, (2116 + 2069) / 2,
(2192 + 2160) / 2, (2298 + 2254) / 2, (2374 + 2333) / 2, (2465 + 2418) / 2,
(2538 + 2503) / 2])


delta_S_b = np.zeros(len(pixel_03_b) - 1)

for i in range(0, len(pixel_03_b) - 1, 1):
    delta_S_b[i] = pixel_03_b[i + 1] - pixel_03_b[i]


#print(delta_S_b)

del_S_b = np.zeros(9)
n = 0

for i in range(0, 9, 1):
        del_S_b[i] = pixel_04_b[n + 1] - pixel_04_b[n]
        n += 2


del_lambda_b = (1 / 2 * dispsgebiet_b * del_S_b / delta_S_b)

delta_E_b = (h * c / lambda_b**2 * del_lambda_b).to('eV')

g_b = (delta_E_b / (mu_bohr * Q_(poly(21, *params_B_auf), 'millitesla'))).to('dimensionless')

g_b_best = ufloat(np.mean(g_b), np.std(g_b, ddof=1))

print(g_b,'##',  g_b_best)
print(del_S_b, '##', delta_S_b)

print('Hysterese 5.2 A', poly(21, *params_B_auf))

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

pixel_01_b = np.array([(1405 + 1244) / 2, (1690 + 1541) / 2, (1952
+ 1852) / 2, (2170 + 2055) / 2, (2399 + 2278) / 2, (2596 + 2481) / 2, (2781 +
2673) / 2, (2961 + 2861) / 2, (3130 + 3033) / 2, (3294 + 3202) / 2])

pixel_02_b_1 = np.array([(1419 + 1060) / 2, (1728 + 1419) / 2, (1973
+ 1728) / 2, (1973 + 1728) / 2, (2215 + 1973) / 2, (2435 + 2215) / 2, (2638 +
2435) / 2, (2816 + 2638) / 2, (3013 + 2816) / 2, (3176 + 3010) / 2, (3342 +
3176) / 2])

pixel_02_b_2 = np.array([(1494 -1339), (1776 - 1657), (2035 - 1910), (2273 - 2154), (2478 - 2377),
(2677 - 2582), (2873 - 2769), (3045 - 2959), 3217 - 3135, 3383 - 3303])


delta_S_b = np.zeros(len(pixel_01_b) - 1)

for i in range(0, len(pixel_01_b) - 1, 1):
    delta_S_b[i] = pixel_01_b[i + 1] - pixel_01_b[i]


#print(delta_S_b)

del_S_b = pixel_02_b_2[1:10]#np.zeros(9)

#for i in range(0, len(pixel_02_b_2) - 1, 1):
#    del_S_b[i] = pixel_02_b_2[i + 1] - pixel_02_b_2[i]


del_lambda_b = (1 / 2 * dispsgebiet_b * del_S_b / delta_S_b)

delta_E_b = (h * c / lambda_b**2 * del_lambda_b).to('eV')

g_b = (delta_E_b / (mu_bohr * Q_(poly(5.6, *params_B_auf), 'millitesla'))).to('dimensionless')

g_b_best = ufloat(np.mean(g_b), np.std(g_b, ddof=1))

print(g_b,'##',  g_b_best)
print(del_S_b, '##', delta_S_b)

print('Hysterese 5.6 A', poly(5.6, *params_B_auf))
print((2 + 3/2) / 2)

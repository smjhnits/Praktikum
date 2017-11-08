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

lambda_r = Q_(643.2, 'nanometer')
n_r = 1.4567
h = Q_(const.h, 'joule * second')
e_0 = Q_(const.e, 'coulomb')
mu_bohr = Q_(const.physical_constants['Bohr magneton'][0], 'joule/tesla')
c = Q_(const.c, 'meter / second')
d = Q_(4, 'millimeter')

dispsgebiet_r = lambda_r**2 / (2 * d) * np.sqrt(1 / (n_r**2 - 1))


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

#### ROT ####

## Pixelbreiten der 2 bis 11 Linie ROT
pixel_01_r = np.array([(875 + 784) / 2, (1162 + 1059) / 2, (1408 +
1320) / 2, (1648 + 1555) / 2, (1869 + 1787) / 2, (2077 + 1998) / 2, (2282 +
2188) / 2, (2470 + 2385) / 2, (2655 + 2572) / 2, (2824 + 2754) / 2])


## pixel drei I = 9.2 A Pol = 0

pixel_03_r = np.array([(925 + 796) / 2, (1193 + 1064) / 2, (1437 +
1331) / 2, (1675 + 1560) / 2, (1887 + 1793) / 2, (2105 + 2011) / 2, (2299 +
2205) / 2, (2499 + 2393) / 2, (2675 + 2572) / 2, (2852 + 2760) / 2])


delta_S_r = np.zeros(len(pixel_01_r) - 1)

for i in range(0, len(pixel_01_r) - 1, 1):
    delta_S_r[i] = pixel_01_r[i + 1] - pixel_01_r[i]


#print(delta_S_r)

del_S_r = np.zeros(9)

for i in range(0, len(pixel_03_r) - 1, 1):
    del_S_r[i] = pixel_03_r[i + 1] - pixel_03_r[i]


del_lambda_r = (1 / 2 * dispsgebiet_r * del_S_r / delta_S_r)

delta_E_r = (h * c / lambda_r**2 * del_lambda_r).to('eV')

g_r = (delta_E_r / (mu_bohr * Q_(poly(9.2, *params_B_auf), 'millitesla'))).to('dimensionless')

g_r_best = ufloat(np.mean(g_r), np.std(g_r, ddof=1))

print(delta_E_r)
print((Q_(1, 'eV') / (mu_bohr * Q_(poly(9.2, *params_B_auf), 'millitesla'))).to('dimensionless'))
print(del_lambda_r.to('nanometer'))
print(g_r,'##',  g_r_best)
print(del_S_r / delta_S_r)
print('Hysterese 9.2 A', poly(9.2, *params_B_auf))

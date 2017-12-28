import numpy as np
from scipy.stats import sem
import scipy.constants as const
from uncertainties import ufloat
import uncertainties.unumpy as unp
from uncertainties.unumpy import (nominal_values as noms, std_devs as stds)
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import scipy.misc
from pint import UnitRegistry

u = UnitRegistry()
Q_ = u.Quantity

mu_bohr = Q_(const.physical_constants['Bohr magneton'][0], 'joule/tesla')
e_0 = Q_(const.e, 'coulomb')
e_0_dimlos = const.e
m_0 = Q_(const.m_e, 'kg')
m_0_dimlos = const.m_e
mu_0 = Q_(const.mu_0, 'N / A**2')

### Angaben aus Protokoll ###

N_sweep = 11
N_horizontal = 154
N_vertical = 20
R_sweep = Q_(16.39, 'cm').to('m')
R_horizontal = Q_(15.79, 'cm').to('m')
R_vertical = Q_(11.735, 'cm').to('m')

### Quantenzahlen ###

J = 1 / 2
S = 1 / 2
L = 0

### Vertikalfeld ###
I_vertical = Q_(2.28 * 0.1, 'A')

### Messdaten aus Messprogramm c.) ###


frequenz = Q_(np.array([101, 210, 300, 400, 502, 600, 700, 800, 904, 1001]), 'kHz')

I_sweep_1 = Q_(np.array([5.4, 3.75, 5.53, 4.71, 1.13, 1.77, 0.92, 3.55, 3.97, 5.17]) * 0.1, 'A')
I_sweep_2 = Q_(np.array([6.61, 6.32, 9.04, 9.41, 7.10, 8.86, 9.19, 7.51, 7.65, 7.21]) * 0.1, 'A')

I_seven_horizontal = Q_(np.array([0, 29, 31, 53, 93, 105, 128]), 'mA')
I_ten_horizontal_1 = Q_(np.array([126, 140, 148]), 'mA')
I_ten_horizontal_2 = Q_(np.array([164, 188, 216]), 'mA')

### Magnetfelder aus Spulenstrom berechnen ###

def B_Helmholtz(I, N, R):
    return mu_0 * 8 * I * N / (np.sqrt(125) * R)


### ERDMAGNETFELD Vertikalfeld ###

erdmag_vertical = B_Helmholtz(I_vertical, N_vertical, R_vertical).to('tesla')

print('Erdmagnetfeld: ', erdmag_vertical)

### B-Feld sweep, horizontal ###

B_sweep_1 = B_Helmholtz(I_sweep_1, N_sweep, R_sweep).to('tesla')
B_sweep_2 = B_Helmholtz(I_sweep_2, N_sweep, R_sweep).to('tesla')

B_seven_horizontal = B_Helmholtz(I_seven_horizontal, N_horizontal, R_horizontal).to('tesla')
B_ten_horizontal_1 = B_Helmholtz(I_ten_horizontal_1, N_horizontal, R_horizontal).to('tesla')
B_ten_horizontal_2 = B_Helmholtz(I_ten_horizontal_2, N_horizontal, R_horizontal).to('tesla')

### g_F bestimmen. g_F = a in poly ###

def poly (x, a, b):
    return a * x + b

### Sweep Lande sind die, die zu den Übergängen gehören
params_lande_sweep_1, covariance_B_sweep_1 = curve_fit(poly, frequenz.magnitude, B_sweep_1.magnitude)
params_lande_sweep_2, covariance_B_sweep_2 = curve_fit(poly, frequenz.magnitude, B_sweep_2.magnitude)

print(frequenz[0:7], len(B_ten_horizontal_1))

params_lande_seven_horizontal, covariance_B_seven_horizontal = curve_fit(poly, frequenz.magnitude[0:7], B_seven_horizontal.magnitude)
params_lande_ten_horizontal_1, covariance_B_ten_horizontal_1 = curve_fit(poly, frequenz.magnitude[7:10], B_ten_horizontal_1.magnitude)
params_lande_ten_horizontal_2, covariance_B_ten_horizontal_2 = curve_fit(poly, frequenz.magnitude[7:10], B_ten_horizontal_2.magnitude)

#plt.clf()
#plt.plot(frequenz.magnitude, poly(frequenz.magnitude, *params_lande_sweep_1), "gx", #label=r"")
##plt.plot(frequenz.magnitude, 4 * np.pi * m_0.magnitude * 1 / (e_0.magnitude) * #B_sweep_1.magnitude, "kx", label=r"")
#plt.plot(frequenz.magnitude, poly(frequenz.magnitude, *params_lande_sweep_2), "gx", #label=r"")
##plt.plot(frequenz.magnitude, 4 * np.pi * m_0.magnitude * 1 / (e_0.magnitude) * #B_sweep_2.magnitude, "kx", label=r"")
#plt.xlabel('Frequenz in kHz')
#plt.ylabel('Magnetfeldstärke in mT')
#plt.legend(loc='best')
#plt.tight_layout()
#plt.show()

### Ermitteln des Kernspins ### ?????????
print(params_lande_sweep_2[1], params_lande_sweep_2[1])

g_J = (3.0023 * J * (J + 1) + 1.0023 * (S * (S + 1) - L * (L + 1))) / (2 * J * (J * 1))

Kernspin_1 = 1 / 2 * (g_J / (1 / params_lande_sweep_1[0] *  4 * np.pi * m_0.magnitude / e_0.magnitude) - 1)
Kernspin_2 = 1 / 2 * (g_J / (1 / params_lande_sweep_2[0] *  4 * np.pi * m_0.magnitude / e_0.magnitude) - 1)

print(Kernspin_1, Kernspin_2, g_J)

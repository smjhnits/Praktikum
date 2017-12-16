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

mu_bohr = Q_(const.physical_constants['Bohr magneton'][0], 'joule/tesla')
e_0 = Q_(const.e, 'coulomb')

### Angaben aus Protokoll ###

N_sweep = 11
N_horizontal = 154
N_vertical = 20
R_sweep = Q_(16.39, 'cm')
R_horizontal = Q_(15.79, 'cm')
R_vertical = Q_(11.735, 'cm')

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
    return mu_bohr * 8 / (np.sqrt(125) * R) * I * N


### ERDMAGNETFELD Vertikalfeld ###

erdmag_vertical = B_Helmholtz(I_vertical, N_vertical, R_vertical)

print('Erdmagnetfeld: ', erdmag_vertical)

### B-Feld sweep, horizontal ###

B_sweep_1 = B_Helmholtz(I_sweep_1, N_sweep, R_sweep)
B_sweep_2 = B_Helmholtz(I_sweep_2, N_sweep, R_sweep)

B_seven_horizontal = B_Helmholtz(I_seven_horizontal, N_horizontal, R_horizontal)
B_ten_horizontal_1 = B_Helmholtz(I_ten_horizontal_1, N_horizontal, R_horizontal)
B_ten_horizontal_2 = B_Helmholtz(I_ten_horizontal_2, N_horizontal, R_horizontal)

### g_F bestimmen. g_F = a in poly ###

def poly (x, a, b):
    return 4 * np.pi * e_0 * 1 / a * x + b

params_lande_sweep_1, covariance_B_sweep_1 = curve_fit(poly, frequenz, B_sweep_1)
params_lande_sweep_2, covariance_B_sweep_2 = curve_fit(poly, frequenz, B_sweep_2)

params_lande_seven_horizontal, covariance_B_seven_horizontal = curve_fit(poly, frequenz, B_seven_horizontal)
params_lande_ten_horizontal_1, covariance_B_ten_horizontal_1 = curve_fit(poly, frequenz, B_ten_horizontal_1)
params_lande_ten_horizontal_2, covariance_B_ten_horizontal_2 = curve_fit(poly, frequenz, B_ten_horizontal_2)


### Ermitteln des Kernspins ###

g_J = (3.0023 * J * (J + 1) + 1.0023(S * (S + 1) - L * (L + 1))) / (2 * J * (J * 1))
  
Kernspin =

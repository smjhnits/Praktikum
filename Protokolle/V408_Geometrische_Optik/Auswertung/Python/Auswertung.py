import numpy as np
from scipy.stats import sem
from uncertainties import ufloat
import uncertainties.unumpy as unp
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import scipy.constants as const
from uncertainties.unumpy import (nominal_values as noms, std_devs as stds)

G = ufloat(2.9, 0.05) * 10**-2 # Gegenstandsgröße
# Ablesefehler wird angegeben mit 0.05cm
err = np.ones(10) * 0.05 * 10**(-2)
err_5 = np.ones(5) * 0.05 * 10**(-2)


# Messung 1 Brennweite bekannt 100mmAngaben in cm

g_1 = unp.uarray(np.linspace(15, 60, 5) * 10**(-2), err) # cm in m
b_1 = unp.uarray(np.array([27.8, 18.4, 15.3, 13.85, 13.1, 12.5, 12.05, 11.7, 11.4, 11.25]) * 10**(-2), err) # cm in m
B_1 = unp.uarray(np.array([2.8, 1.9, 1.45, 1.15, 0.95])* 10**(-2), err_5) # cm in m

# Messung bei unbekannter Brennweite

g_2 = unp.uarray(np.linspace(15, 60, 5) * 10**2, err)
b_2 = unp.uarray(np.array([18.55, 14.3, 12.5, 11.7, 11.1, 10.5, 10.3, 10.1, 9.95, 9.9]) * 10**(-2), err)

# Messung nach Bessel

b_plus_g_3 = unp.uarray(np.array([40, 45, 50, 52.5, 57.5, 60, 62.5, 65, 70]) * 10**(-2), err)
g_eins_3 = unp.uarray(np.array([16.6, 14.15, 13.2, 12.9, 12.6, 12.2, 12.2, 12, 11.8]) * 10**(-2), err) # erster Brennpkt
b_eins_3 = b_plus_g_3 - g_eins_3
g_zwei_3 = unü.uarray(np.array([23.7, 31.05, 37, 40, 42.6, 45.35, 48, 50.75, 53.35, 58.45]) * 10**(-2), err) # zweiter Brennpkt
b_zwei_3 = b_plus_g_3 - g_zwei_3

# chromatische Abberation

b_plus_g_4 = unp.uarray(np.linspace(45, 65, 5) * 10**(-2), err_5)
g_eins_rot_4 = unp.uarray(np.array([14.35, 13.2, 12.6, 12.35, 12]) * 10**(-2), err_5)
b_eins_rot_4 = b_plus_g_4 - g_eins_rot_4
g_zwei_rot_4 = unp.uarray(np.array([31, 37, 42.5, 48.1, 53.5]) * 10**(-2), err_5)
b_zwei_rot_4 = b_plus_g_4 - g_zwei_rot_4

g_eins_blau_4 = np.array([14.1, 13.25, 12.7, 12.4, 12.1]) * 10**(-2)
b_eins_blau_4 = b_plus_g_4 - b_eins_blau_4
g_zwei_blau_4 = np.array([31.2, 37.1, 42.7, 48.2, 53.3]) * 10**(-2)
b_zwei_blau_4 = b_plus_g_4 - g_zwei_blau_4

# Nach Abbe Streulinse -100 mm, Sammellinse 100mm

B_5 = unp.uarray(np.array([5.2, 3.9, 2.8, 2.2, 1.8, 1.5, 1.3, 1.2, 1, 0.95]) * 10**(-2), err)
b_plus_g_5 = unp.uarray(np.array([70, 67.3, 66.6, 68.1, 71.4, 75, 79, 83.3, 87.5, 92.1]) * 10**(-2), err)
g_5 = unp.uarray(np.array([17, 20, 25, 30, 35, 40, 45, 50, 55, 60]) * 10**(-2), err)
b_5 = b_plus_g_5 - g_5

# Abbildungsgesetz

b_mean_1 = ufloat(np.mean(noms(b_1)), np.mean(stds(b_1)))
g_mean_1 = ufloat(np.mean(noms(g_1)), np.mean(stds(b_1)))
V_aus_gb = b_mean_1 / g_mean_1
print('Abbildungsgesetz aus g und b: ', V_aus_gb)
B_mean_1 = ufloat(np.mean(noms(B_1)), np.mean(stds(B_1)))
print('Aus abgemessenen Werten Bund G: ', B_mean_1 / G)

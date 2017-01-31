import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
# import scipy.constants as const
from uncertainties import ufloat
import uncertainties.unumpy as unp

# Apparaturdaten

L = unp.ufloat(3.53, 0.03) * 10^(-3) # Henry
C = unp.ufloat(5.015, 0.015) * 10^(-9) # Farad
R_1 = unp.ufloat(30.3, 0.1) # Ohm
R_2 = unp.ufloat(271.6, 0.3) # Ohm

# Messung a.) bei Widerstand R_1
nu_a = 5.820 # Hertz
maxima = np.array([11, 9.12, 7.84, 6.88, 6.16, 5.6, 5.28, 4.96, 4.80, 4.68, 4.56, 4.44])
zeit = np.array([27.5, 27.5, 27.5, 30, 30, 30, 30, 32.5, 32.5, 35, 35]) * 10^(-6) # Zeit in Sekunden zwischen den Maxima

# Messung b.)
R = 13.5 * 1000 # Ohm (gefundener Widerstand für den aperiodischen Grenzfall)
nu_b = 5.815 # Hertz

# Messung c.)
nu_c = np.array([10, 15, 20, 25, 30, 34, 35, 36, 36.5, 37, 40, 45, 50, 55, 60, 70]) * 10^(3) # Hertz Generatorfrequenz
lamda = np.array([98, 67, 50.8, 40, 33.2, 29.6, 28.4, 28, 27.2, 26.4, 25.2, 22.2, 19.8, 18.2, 16.6, 14]) * 10^(-6) # Sekunden Wellenlänge
phasenversch = np.array([0, 1.2, 1.6, 2, 3.2, 4.8, 5.2, 6.4, 6, 6.8, 7.8, 8.4, 8.6, 8.2, 8, 7]) * 10^(-6) # Sekunde Phasenverschiebung
U_G = np.array([5.4, 5.4, 5.12, 5.04, 4.8, 4.48, 4.4, 4.4, 4.4, 4.32, 4.48, 4.72, 4.88, 4.96, 4.96, 5.04]) # Volt Generatorspannung
U_C = np.array([5.44, 5.92, 6.64, 8.4, 10.8, 12.8, 13, 13.2, 13, 12.8, 11.2, 7.6, 5.2, 4, 3, 2]) # Volt Kondensatorspannung

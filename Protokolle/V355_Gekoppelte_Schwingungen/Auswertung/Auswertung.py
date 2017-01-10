import numpy as np
from scipy.stats import sem
from uncertainties import ufloat
import uncertainties.unumpy as unp
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

L   = 32.51 * 10 ** (-3)
C   = 0.801 * 10 ** (-9)
Csp = 0.037 * 10 ** (-9)
R = 50

#L = ufloat(32.51 * 10 ** (-3), 0.01 * 10 ** (-3))
#C = ufoat(0.801 * 10 ** (-9), 0.001 * 10 ** (-9))
#Csp = ufloat(0.037 * 10 ** (-9), 0.001 * 10 ** (-9))

Kopplungskapazitäten = np.array([9.99, 8, 6.47, 5.02, 4.00, 3.00, 2.03])
Anzahl Maxima = np.array([14, 12, 10, 8, 6, 5, 4])
Resonanzfrequenz = 31.10 * 10 ** (3)

Nü_negativ = np.array([33.16, 33.66, 34.25, 35.12, 36.08, 37.60, 40.28, 47.33]) * 10 ** (3)
Nü_positiv = np.array([30.77, 30.79, 30.80, 30.81, 30.82, 30.83, 30.84, 30.85])

Start = np.array([30.85, 30.84, 30.83, 30.82, 30.81, 30.80, 30.79, 30.77]) * 10 ** (3)
Stopp = np.array([55.05, 50, 40, 40, 40, 40, 40, 40])

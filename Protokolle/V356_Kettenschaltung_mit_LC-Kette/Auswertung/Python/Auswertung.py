import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
# import scipy.constants as const
from uncertainties import ufloat
import uncertainties.unumpy as unp

# a.) Durchlasskurve

def function(x, a, b):
    return a * x + b

Abstaende_1 = np.array([0, 3, 6, 9, 12, 15, 18])
Abstaende_2 = np.array([0, 2, 4, 6, 8, 11, 14])
nu_C_Duchlasskurve = np.array([1338, 2055, 2843, 3730, 5023, 6471, 8624])
nu_C1C2_Durchlasskurve = np.array([7345, 10478, 21072,30336, 50353, 79169])

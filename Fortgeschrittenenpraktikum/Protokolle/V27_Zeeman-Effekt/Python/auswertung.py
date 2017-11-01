import numpy as np
from scipy.stats import sem
from uncertainties import ufloat
import uncertainties.unumpy as unp
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

## Fit Polynom 3. Grades

def poly(x, a, b, c, d):
    return a * x**3 + b * x**2 + c * x + d

## Hysterese, B in mT

B_auf = np.array([4, 87, 112,174, 230, 290, 352, 419, 476, 540, 600, 662, 714, 775, 823,872, 916, 959, 987, 1015, 1046, 1072])

B_ab = np.array([7, 57, 120, 180, 251, 306, 361, 428, 480, 550, 612, 654, 715, 780, 830, 878, 924, 962, 993, 1020, 1050, 1072])

I = np.linspace(0, 21, 22)
I_fit = np.linspace(-1, 22, 24)

## Plot + Fit Hysterese

params_B_auf, covariance_B_auf = curve_fit(poly, I, B_auf)
params_B_ab, covariance_B_ab = curve_fit(poly, I, B_ab)

plt.clf()
plt.plot(I, B_auf, "gx", label=r"Messdaten B_auf")
plt.plot(I_fit, poly(I_fit, *params_B_auf), "g-", label=r"Fit B_auf")
plt.plot(I, B_ab, "bx", label=r'Messdaten B_ab')
plt.plot(I_fit, poly(I_fit, *params_B_ab), "b-", label=r"Fit B_ab")
plt.xlabel('Stromstärke in A')
plt.ylabel('Magnetfeldstärke in mT')
plt.xlim(-0.5, 21.5)
plt.ylim(-10, 1090)
plt.legend(loc='best')
plt.tight_layout()
plt.savefig('Hysterese.pdf')


## Bild eins Zeitstempel 10:01 Uhr

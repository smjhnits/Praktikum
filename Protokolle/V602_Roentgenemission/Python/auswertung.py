import numpy as np
from scipy.stats import sem
from uncertainties import ufloat
import uncertainties.unumpy as unp
import matplotlib.pyplot as plt
import scipy.constants as sc
from scipy.optimize import curve_fit
import operator

# Messung a

Winkel2A, RateA = np.genfromtxt('M_A_T.txt', unpack=True) #skip_header = 1, unpack=True)
WinkelA = Winkel2A/2
MaximumA = np.argmax(RateA)

plt.clf()
plt.plot(WinkelA, RateA, 'bx', label = r'Gemessene Impulsrate')
plt.ylabel(r'R in $\frac{\mathrm{Imp}}{\mathrm{s}}$')
plt.xlabel(r'$\alpha$ in $\mathrm{DEG}$')
plt.axvline(WinkelA[MaximumA])
plt.xlim(12.5, 15.5)
#plt.show()
plt.savefig('MessungA.pdf')

# Messung b

Winkel2B, RateB = np.genfromtxt('M_B_T.txt', unpack=True) #skip_header = 1, unpack=True)
WinkelB = Winkel2B/2

MaximumB1 = 81
MaximumB2 = 93

plt.clf()
plt.plot(WinkelB, RateB, 'bx', label = r'Gemessene Impulsrate')
plt.ylabel(r'R in $\frac{\mathrm{Imp}}{\mathrm{s}}$')
plt.xlabel(r'$\alpha$ in $\mathrm{DEG}$')
plt.axvline(WinkelB[MaximumB1], color='k')
plt.axvline(WinkelB[MaximumB2], color='k')
plt.xlim(3.5, 26.5)
#plt.show()
plt.savefig('MessungB.pdf')

import numpy as np
from scipy.stats import sem
from uncertainties import ufloat
import uncertainties.unumpy as unp
import matplotlib.pyplot as plt
import scipy.constants as sc
from scipy.optimize import curve_fit
from numpy.linalg import inv

Werte = np.genfromtxt('Messungen.txt', unpack=True)
Fehler = np.sqrt(Werte)
Fehler_Komplett = np.array([Fehler[25:80], Fehler[25:80]])

Kanäle = np.linspace(0,511,512)

plt.errorbar(Kanäle[25:80], Werte[25:80], yerr = Fehler_Komplett, fmt = 'x', color = 'k', label = r'$\#$ Counts')
plt.ylabel(r'Anzahl Counts')
plt.xlabel(r'Kanal (~Energie)')
plt.legend(loc = 'best')
plt.savefig('Spektrum.pdf')
plt.show()

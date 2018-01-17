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
Fehler_Komplett = np.array([Fehler[0:100], Fehler[0:100]])

Kanäle = np.linspace(0,511,512)

plt.errorbar(Kanäle[0:100], Werte[0:100], yerr = Fehler_Komplett, fmt = 'x', color = 'k', label = r'$\#$ Counts')
plt.ylabel(r'Anzahl Counts')
plt.xlabel(r'Kanal')
plt.legend(loc = 'best')
plt.show()

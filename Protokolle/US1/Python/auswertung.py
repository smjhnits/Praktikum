import numpy as np
import math
from scipy.stats import sem
from uncertainties import ufloat
import uncertainties.unumpy as unp
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import scipy.constants as const


def linReg(x, m, b):
    return m * x + b

c_acryl_lit = 2730 ### Literaturwert von Acryl

Zylinder_laengen = np.array([40.35, 88.55, 88.45, 102.1, 31.1, 39.7, 61.5])

### Impuls-Echo-Verfahren ###

puls_1 = np.array([[0.9, 0.97, 0.98, 1, 0.97, 0.98, 0.97, 1],
                   [0.4, 0.4, 0.5, 0.4, 0.4, 0.5, 0.4, 0.5]
                   ])

puls_2 = np.array([[0.17, 0.02, 0.01, 0.12, 0.25, 0.19, 0.04, 0.12],
                  [30.3, 59.8, 59.8, 76.49, 23.7, 29.8, 46.2, 75.7]
                  ])


### Durchschallungsverfahren ###

laufzeit_2 = np.array([15.21, 29.78, 30.18, 38.48, 11.98, 15.21, 23.27])

### Spektrale Analyse und Cepstrum ###

peakdifferenzen = np.array([37.1 - 29.8, 41.6 - 37.1, 41.6 - 29.8])

### Auge ###

auge = np.array([[0.2, 6.22, 4.61, 5.76, 41.7],
                [0.2, 6.64, 11.05, 16.81, 70.26]]) # erster Eintrag Peakabstände, zweiter Eintrag die Absoluten Abstände

# Auge = (Hornhaut, Iris, Linseneingang, Linsenausgang, Retina)

### Schallgeschwindigkeit bestimmen ###
print(len(puls_2[0, 0:7]), len(Zylinder_laengen))

### Impuls-Echo ###

params_c, covariance_c = curve_fit(linReg, np.sort(puls_2[1, 0:7]), np.sort(Zylinder_laengen * 2))

plt.clf()
plt.plot(np.linspace(20, 80), linReg(np.linspace(20, 80), *params_c), 'r-', label = r'Ausgleichgerade')
plt.plot(np.sort(puls_2[1, 0:7]), np.sort(Zylinder_laengen * 2), 'kx', label = r'Messdaten')
plt.xlabel(r'$t$ in $\mu$s')
plt.ylabel('Doppelte Zylinderlänge in mm')
plt.xlim(20, 80)
plt.legend(loc='best')
plt.grid()
plt.tight_layout()
plt.savefig('schallgesch_echo.pdf')


c_gemessen = params_c[0] * 10**3

print('Schallgesch in [m/s]: ', c_gemessen)
print('systematische Fehler der Sonde: ', params_c[1])

### Durchschallungsverfahren ###

params_c_d, covariance_c_d = curve_fit(linReg, np.sort(laufzeit_2), np.sort(Zylinder_laengen))


plt.clf()
plt.plot(np.linspace(10, 40), linReg(np.linspace(10, 40), *params_c_d), 'r-', label = r'Ausgleichgerade')
plt.plot(np.sort(laufzeit_2), np.sort(Zylinder_laengen), 'kx', label = r'Messdaten')
plt.xlabel(r'$t$ in $\mu$s')
plt.ylabel('Zylinderlänge in mm')
plt.xlim(10, 40)
plt.legend(loc='best')
plt.grid()
plt.tight_layout()
plt.savefig('schallgesch_durch.pdf')

c_gemessen_d = params_c_d[0] * 10**3

print('Schallgesch in [m/s]: ', c_gemessen_d)
print('systematische Fehler der Sonde: ', params_c_d[1])

### Dämpfungsfaktor ###

amplituden_puls_1 = np.append(puls_1[0, 0:2], puls_1[0, 4:6])
amplituden_puls_2 = np.append(puls_2[0, 0:2], puls_2[0, 4:6])

def exp(x, I, a):
    return I * np.exp(a * x)

params_ungedämpft, covariance_ungedämpft = curve_fit(exp, np.sort(2 * Zylinder_laengen), np.sort(puls_2[0, 0:7]))

print('Dämpfung: ', params_ungedämpft[1], params_ungedämpft[0])

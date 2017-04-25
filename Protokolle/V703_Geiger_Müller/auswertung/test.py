import numpy as np
from scipy.stats import sem
from uncertainties import ufloat
import uncertainties.unumpy as unp
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

testXAchse = np.linspace(320, 700, 39)

def mean(x, name):
    print(name, np.mean(x))
    return np.mean(x)

def std(x, name):
    print(name, np.std(x))
    return np.std(x)

Zählrate = np.array([33062, 33816, 33883, 34142, 34549, 34491, 34815, 34818,
                     34975, 35219, 34923, 35100, 34947, 35133, 35390, 35342,
                     35359, 35363, 35234, 35695, 35722, 35332, 35523, 35617,
                     35747, 35433, 35827, 35757, 35908, 35868, 35853, 36340,
                     36405, 36758, 37352, 37824, 38535, 39689, 41082]) # Zählrate pro min

Stromstärken = np.array([0.3, 0.45, 0.6, 0.7, 0.85, 0.95, 1.1, 1.2,  1.25, 1.4,
                         1.6,  1.7, 1.8, 1.9,  2.1,  2.3, 2.4, 2.5,  2.6, 2.8,
                         2.9,  3.0, 3.0, 3.2,  3.3,  3.4, 3.5, 3.6, 3.8, 3.95,
                         4.0,  4.1, 4.4, 4.5,  4.7,  4.8, 4.9, 5.2, 5.4]) # in mikro Ampere

Zählrate_err = np.sqrt(Zählrate)

Totzeit = np.array([3.5 * 50, 3.8 * 50, 4 * 50, 4.2 * 50, 4.3 * 50]) #  mikrosec

Erholungszeit = np.array([4.6 * 0.5, 4.6 * 0.5, 4.8 * 0.5, 4.9 * 0.5, 5 * 0.5]) #  millisec

#  2 Quellen-Methode

Quelle_1 = ufloat(25692 / 60, np.sqrt(25692) / 60)
Quelle_1_2 = ufloat(26775 / 60, np.sqrt(26775) / 60)
Quelle_2 = ufloat(1109 / 60, np.sqrt(1109) / 60)

plt.errorbar(testXAchse, Zählrate/60, yerr=Zählrate_err/60, fmt='kx', label = r'$Gezählte \,\, \beta -Teilchen$')
plt.plot(np.ones(200) * 630, np.linspace(540, 700, 200), 'g--', label = r'Beginn des Entladungsbereiches')
plt.plot(np.ones(200) * 380, np.linspace(540, 700, 200), 'b--', label = r'Beginn des Pleateau-Bereiches')
plt.xlabel(r'$U \,\, in \,\, V$')
plt.ylabel(r'$\frac{N}{\Delta t} \,\, in \,\, \frac{1}{s}$')
plt.xlim(300, 710)
plt.legend(loc='best')
plt.grid()
plt.tight_layout()
plt.savefig('Charakteristik.pdf')

plt.clf()
plt.plot(testXAchse, Stromstärken, 'kx', label = r'$Gemessene \,\, Stromstärken$')
plt.xlabel(r'$U \,\, in \,\, V$')
plt.ylabel(r'$I \,\, in \,\, A$')
plt.xlim(300, 710)
plt.legend(loc='best')
plt.grid()
plt.tight_layout()
plt.savefig('Spannung_gege_Strom.pdf')

#  Plateubereich von 380 - 620 V

plateau_y = Zählrate[7:31]
plateau_x = np.linspace(380, 620, 24)

#  lineareRegression an die Plateau-Ebene

def function(x, a, b):
    return a * x + b

params, covariance = curve_fit(function, np.linspace(370, 630, 24), plateau_y / 60)

print('Plateau_steigung: ', params)

plt.clf()
plt.plot(plateau_x, plateau_y / 60, 'kx', label = r'$Gemessene \,\, \beta - Teilchen$')
plt.plot(np.linspace(370, 630, 24), function(np.linspace(370, 630, 24), *params), 'r-', label = r'$lineare \,\, Regression$')
plt.xlabel(r'$U \,\, in \,\, V$')
plt.ylabel(r'$\frac{N}{\Delta t} \,\, in \,\, \frac{1}{s}$')
plt.xlim(370, 630)
plt.ylim(560, 620)
plt.legend(loc='best')
plt.grid()
plt.tight_layout()
plt.savefig('plateau.pdf')


mean(Totzeit, 'Totenzeit_mean: ')
std(Totzeit, 'Totzeit_std: ')
mean(Erholungszeit, 'Erholungszeit_mean: ')
std(Erholungszeit, 'Erholungszeit_std: ')

#  2 Quellen-Methode

Totzeit_2 = (Quelle_1 + Quelle_2 - Quelle_1_2) / (2 * Quelle_1 * Quelle_2)

print('Totzeit aus 2 Q M: ', Totzeit_2)


#  Aufgabe e



params_2, covariance_2 = curve_fit(function, plateau_y, Stromstärken[7:31])

plt.clf()
plt.plot(plateau_y, Stromstärken[7:31],'kx', label = r'$Gemessene \,\, Daten$')
plt.plot(np.linspace(34700, 36000), function(np.linspace(34700, 36000), *params_2), 'r-', label = r'$lineare \,\, Regression$')
plt.xlabel(r'$\frac{N}{\Delta t} \,\, in \,\, \frac{1}{s}$')
plt.ylabel(r'$I \,\, in \,\, \mu A$')
plt.ylim(1, 4.3)
plt.xlim(34700, 36000)
plt.legend(loc='best')
plt.grid()
plt.tight_layout()
plt.savefig('Stromstärke_gegen_Anzahl.pdf')

print(params_2, np.diag(np.sqrt(covariance_2)))

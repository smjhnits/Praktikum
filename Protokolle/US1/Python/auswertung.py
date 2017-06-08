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

### Impuls-Echo ###

params_c, covariance_c = curve_fit(linReg, np.sort(puls_2[1, 0:7] - puls_1[1, 0:7]), np.sort(Zylinder_laengen * 2))

plt.clf()
plt.plot(np.linspace(20, 80), linReg(np.linspace(20, 80), *params_c), 'r-', label = r'Ausgleichgerade')
plt.plot(np.sort(puls_2[1, 0:7] - puls_1[1, 0:7]), np.sort(Zylinder_laengen * 2), 'kx', label = r'Messdaten')
plt.xlabel(r'$t$ in $\mu$s')
plt.ylabel('Doppelte Zylinderlänge in mm')
plt.xlim(20, 80)
plt.legend(loc='best')
plt.grid()
plt.tight_layout()
plt.savefig('../Pics/schallgesch_echo.pdf')


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
plt.savefig('../Pics/schallgesch_durch.pdf')

c_gemessen_d = params_c_d[0] * 10**3

print('Schallgesch in [m/s]: ', c_gemessen_d)
print('systematischer Fehler der Sonde: ', params_c_d[1])

### Dämpfungsfaktor ###

amplituden_puls_1 = np.append(puls_1[0, 0:2], puls_1[0, 4:6])
amplituden_puls_2 = np.append(puls_2[0, 0:2], puls_2[0, 4:6])
puls_laufstrecke_dämpfung = 2 * np.append(Zylinder_laengen[0:2], Zylinder_laengen[4:6]) * 10**-3 ## in Metern

def exp(x, I, a):
    return I * np.exp(a * x)



#params_ungedämpft, covariance_ungedämpft = curve_fit(exp, np.sort(2 * Zylinder_laengen), np.sort())

#print('Dämpfung: ', params_ungedämpft[1], params_ungedämpft[0])

dämpfung = -np.log(amplituden_puls_2 / amplituden_puls_1) * 1 / puls_laufstrecke_dämpfung

print('Dämpfungsfaktor: ', dämpfung, np.std(dämpfung) / np.sqrt(len(dämpfung)))

print('Dämpfungsfaktor: ', np.mean(dämpfung), np.std(dämpfung) / np.sqrt(len(dämpfung)))


plt.clf()
plt.plot(np.linspace(-0.03, 0.2), exp(np.linspace(-0.03, 0.2), np.mean(amplituden_puls_1), -np.mean(dämpfung)), 'r-', label = r'Ausgleichsfunktion')
plt.plot(np.zeros(len(amplituden_puls_1)), np.sort(amplituden_puls_1), 'kx', label = r'Messdaten')
plt.plot(np.sort(puls_laufstrecke_dämpfung), np.sort(amplituden_puls_2), 'kx')
plt.xlabel(r'Strecke $x$ in mm')
plt.ylabel('Amplituden in V')
plt.xlim(-0.03, 0.2)
plt.legend(loc='best')
plt.grid()
plt.tight_layout()
#plt.show()
plt.savefig('../Pics/Dämpfung.pdf')


### Spektrale Analyse und Cepstrum ###
fehler = np.abs((params_c_d[1] + params_c[1]) / 2)
dicke = peakdifferenzen * 10**(-6) * (c_gemessen + c_gemessen_d) / 4 ## s * meter / s = meter
fehler_dicke = peakdifferenzen * 10**(-6) * fehler / 4
dicke_lit = peakdifferenzen * 10**(-6) * c_acryl_lit / 2

print('Dicke der Platten: ', dicke, fehler_dicke)
print('Dicke mit Literaturwerten: ', dicke_lit)
print('vermessene Werte der Platten: 6 mm, 9.9 mm')


### Auge ###
fehler = np.abs((params_c_d[1] + params_c[1]) / 2)
c_linse = ufloat(2500, fehler) ## m / s
c_glaskörper = ufloat(1410, fehler) ## m / s

augen_peakdiff = auge * 10**(-3) / 2 ## peakdifferenzen in ms

hornhaut = 0
iris = augen_peakdiff[0, 1] * c_glaskörper
linse_eingang = iris + augen_peakdiff[0, 2] * c_linse
linse_ausgang = linse_eingang + augen_peakdiff[0, 3] * c_linse
retina = linse_ausgang + augen_peakdiff[0, 4] * c_glaskörper

print('##Auge Abstände## ## in mm ##',  'Hornhaut: ', hornhaut,  'Iris: ', iris,
      'Linseneigang: ', linse_eingang,  'Linsenausgang: ', linse_ausgang,
      'Retina: ', retina)


### schcllageschdifferenz ###

print(c_gemessen_d - c_gemessen, params_c_d[1] - params_c[1])
print(c_acryl_lit - (c_gemessen_d + c_gemessen) / 2, (params_c_d[1] + params_c[1]) / 2)

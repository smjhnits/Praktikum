import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from uncertainties import ufloat
import uncertainties.unumpy as unp
from uncertainties.unumpy import (nominal_values as noms, std_devs as stds)
from pint import UnitRegistry

u = UnitRegistry()
Q_ = u.Quantity

def Polarisationsmessung(phi, I_0, phi_0):
    return I_0 * np.sin(phi - phi_0)**2

def Grundmode(d, I_0, d_0, omega):
    return I_0 * np.exp(-2 * ((d - d_0) / omega)**2) ## 10 ist der abgelesen x-Wert zu dem Hochpunkt der Messung

def erste_angeregte_Mode(d, I_1, d_1, omega_1, I_2, d_2, omega_2):
    return I_1 * np.exp(-2 * ((d - d_1) / omega_1)**2) + I_2 * np.exp(-2 * ((d - d_2) / omega_2)**2)

def Wellenlänge(g, L, n, d):
    return g * unp.sin(unp.arctan(d / L)) / n

### FITFUNKTIONEN ###

def lin(x, a, b):
    return a * x + b

def quad(x, a, b, c):
    return a * x**2 + b * x + c

### Polarisationsmessung ###

winkel = Q_(np.linspace(0, 360, 37), 'degree') #in deg

I_pol = Q_(np.array([0.116, 0.067, 0.034, 0.011, 0.001, 0.004, 0.020, 0.049, 0.086,
0.137, 0.187, 0.238, 0.281, 0.307, 0.308, 0.288, 0.251, 0.198, 0.137, 0.083, 0.040,
0.013, 0.001, 0.005, 0.024, 0.053, 0.094, 0.146, 0.208, 0.264, 0.295, 0.296, 0.279,
0.252, 0.214, 0.167, 0.111]), 'mA') #in mA

params_pol, covariance_pol = curve_fit(Polarisationsmessung, winkel.to('rad').magnitude, I_pol.magnitude)

winkel_fit = np.linspace(-0.1, 2 * np.pi + 0.1, 1000)

plt.clf()
plt.plot(winkel_fit, Polarisationsmessung(winkel_fit, *params_pol), 'r-', label=r'Fit')
plt.plot(winkel.to('rad'), I_pol.magnitude, 'bx', label=r'Messdaten')
plt.xlabel('$\phi$ in rad')
plt.xlim(-0.1, 2 * np.pi + 0.1)
plt.ylabel('$I(\phi)$ in mA')
plt.xticks([0, np.pi / 2, np.pi, 3 * np.pi / 2, 2 * np.pi],
           [r"$0$", r"$\frac{1}{2}\pi$", r"$\pi$", r"$\frac{3}{2}\pi$", r"$2\pi$"])
plt.tight_layout()
plt.legend(loc = 'best')
#plt.show()
#plt.savefig('../Pics/Polarisationsmessung.pdf')

print('Parameter Fit Polarisation:(I_0, phi_0) ', *params_pol, '\n')
print('Parameter Fehler Fit Polarisation: ', np.sqrt(np.diag(covariance_pol)), '\n')

### Grundmode ###

verschiebung_grundmode = Q_(np.linspace(0, 22, 23), 'mm') #in mm

I_grundmode = Q_(np.array([0.12, 0.26, 0.47, 0.90, 1.48, 2.17, 3.28, 4.41, 4.95, 5.79,
6.09, 5.86, 5.48, 5.19, 4.54, 3.76, 2.76, 2.17, 1.55, 0.96, 0.54, 0.32, 0.18]), 'microampere') #in muA

d_grundmode = Q_(10, 'mm') # x-Wert zu aus Daten abgelesenen Hochpunkt

params_grundmode, covariance_grundmode = curve_fit(Grundmode, verschiebung_grundmode.magnitude, I_grundmode.magnitude)

grundmode_fit = np.linspace(-0.4, 22.3, 1000)

plt.clf()
plt.plot(grundmode_fit, Grundmode(grundmode_fit, *params_grundmode), 'r-', label=r'Fit')
plt.plot(verschiebung_grundmode, I_grundmode.magnitude, 'bx', label=r'Messdaten')
plt.xlabel('Verschiebung $L$ in mm')
plt.xlim(-0.4, 22.3)
plt.ylabel('$I_{T_{0,0}}(L)$ in mA')
plt.tight_layout()
plt.legend(loc = 'best')
#plt.savefig('../Pics/Grundmode.pdf')

print('Parameter Fit Grundmode:(I_0, b, omega) ', *params_grundmode, '\n')
print('Parameter Fehler Fit Grundmode:(I_0, b, omega) ', np.sqrt(np.diag(covariance_grundmode)), '\n')

### Erste angeregte Mode ###

verschiebung_mode = Q_(np.linspace(0, 25, 26), 'mm')

I_mode = Q_(np.array([0.23, 0.33, 0.40, 0.49, 0.56, 0.65, 0.66, 0.53, 0.30, 0.15,
0.04, 0.02, 0.03, 0.08, 0.17, 0.26, 0.34, 0.39, 0.43, 0.47, 0.39, 0.32, 0.29, 0.19,
0.10, 0.04]), 'microampere') #in muA

erster_gauß = verschiebung_mode[0:12]
I_erster_gauß = I_mode[0:12]
zweiter_gauß = verschiebung_mode[0:14]
I_zweiter_gauß = I_mode[11:25]

params_mode_1, covariance_mode_1 = curve_fit(Grundmode, erster_gauß.magnitude, I_erster_gauß.magnitude)
params_mode_2, covariance_mode_2 = curve_fit(Grundmode, zweiter_gauß.magnitude, I_zweiter_gauß.magnitude)

mode_fit = np.linspace(-0.5, 25.5)
mode_fit_1 = np.linspace(-0.5, 12)
mode_fit_2 = np.linspace(10, 25.5)

plt.clf()
plt.plot(mode_fit, erste_angeregte_Mode(mode_fit, *params_mode_1, params_mode_2[0], params_mode_2[1] + 11, params_mode_2[2]), 'b-', label = r'Doppelter Gauß Fit')
#plt.plot(mode_fit_1, Grundmode(mode_fit_1, *params_mode_1), 'r--', label=r'Einzelne Gauß Fits')
#plt.plot(mode_fit_2, Grundmode(np.linspace(0, 13.5), *params_mode_2), 'r--')
plt.plot(verschiebung_mode, I_mode.magnitude, 'kx', label=r'Messdaten')
#plt.fill_between(mode_fit_1, 0, Grundmode(mode_fit_1, *params_mode_1),  color='red', alpha = 0.5)
#plt.fill_between(mode_fit_2, 0, Grundmode(np.linspace(0, 13.5), *params_mode_2),  color='red', alpha = 0.5)
plt.xlabel('Verschiebung $L$ in mm')
plt.xlim(-0.5, 25.5)
plt.ylabel('$I_{T_{0,1}}(L)$ in $\mu$A')
plt.tight_layout()
plt.legend(loc = 'best')
#plt.savefig('../Pics/erste_angeregte_Mode.pdf')

plt.clf()
plt.plot(mode_fit, erste_angeregte_Mode(mode_fit, *params_mode_1, params_mode_2[0], params_mode_2[1] + 11, params_mode_2[2]), 'b-', label = r'Doppelter Gauß Fit')
plt.plot(mode_fit_1, Grundmode(mode_fit_1, *params_mode_1), 'r--', label=r'Einzelne Gauß Fits')
plt.plot(mode_fit_2, Grundmode(np.linspace(0, 13.5), *params_mode_2), 'r--')
plt.plot(verschiebung_mode, I_mode.magnitude, 'kx', label=r'Messdaten')
#plt.fill_between(mode_fit_1, 0, Grundmode(mode_fit_1, *params_mode_1),  color='red', alpha = 0.5)
#plt.fill_between(mode_fit_2, 0, Grundmode(np.linspace(0, 13.5), *params_mode_2),  color='red', alpha = 0.5)
plt.xlabel('Verschiebung $\Delta L$ in mm')
plt.xlim(-0.5, 25.5)
plt.ylabel('$I_{T_{0,1}}(\Delta L)$ in $\mu$A')
plt.tight_layout()
plt.legend(loc = 'best')
#plt.savefig('../Pics/Vergleich_summe_doppelter_gauß.pdf')


print('Parameter Fit erste angeregte Mode: (I_1, d_1, omega_1) ', *params_mode_1, '\n')
print('Parameter Fehler Fit erste angeregte Mode: ', np.sqrt(np.diag(covariance_mode_1)), '\n')
print('Parameter Fit erste angeregte Mode: (I_2, d_2, omega_2) ', *params_mode_1, '\n')
print('Parameter Fehler Fit erste angeregte Mode: ', np.sqrt(np.diag(covariance_mode_2)), '\n')
print('Parameter doppelter Gauß: (I_1, d_1, omega_1, I_2, d_2, omega_2) ', *params_mode_1, params_mode_2[0], params_mode_2[1] + 11, params_mode_2[2], '\n')


### Wellenlängenmessung ###
a = Q_(1 / 100, 'mm').to('cm') # Gitterkonstante Drähte pro mm
abstand = Q_(75.7, 'cm') #in cm, Abstand Gitter-Schirm
# Abstand des zentralen Hauptmaxima zu den anderen Hauptmaxima

H_m2 = Q_(ufloat(9.8, 0.05), 'cm') #cm
H_m1 = Q_(ufloat(4.9, 0.05), 'cm') #cm
H_p1 = Q_(ufloat(5.1, 0.05), 'cm') #cm
H_p2 = Q_(ufloat(9.7, 0.05), 'cm') #cm


wellenlänge = np.array([Wellenlänge(a, abstand, 2, H_m2).to('nanometer').magnitude, Wellenlänge(a, abstand, 1,
H_m1).to('nanometer').magnitude,
Wellenlänge(a, abstand, 1, H_p1).to('nanometer').magnitude, Wellenlänge(a, abstand, 2, H_p2).to('nanometer').magnitude])

print('Wellenlängenmessung (Mittelwert) in nm: (Hm2 Hm1 Hp1 Hp2) ', wellenlänge, '\n')
print('Wellenlängenmessung (Mittelwert) in nm: ', np.mean(wellenlänge), '\n')

### Stabilitätsmessung ###

# konkav-konkav

L_außen_anfang_kk = Q_(76.9, 'cm')
L_innen_anfang_kk = Q_(67.0, 'cm')

L_linse = (L_außen_anfang_kk - L_innen_anfang_kk)

L_konkav_konkav = Q_(np.array([76.9, 82.2, 87.0, 91.9, 97.0, 101.6, 107.0, 112.0,
116.9, 122.0, 132.0]) - L_linse.magnitude, 'cm') #in cm

I_konkav_konkav = Q_(np.array([0.14, 0.145, 0.161, 0.17, 0.18, 0.208, 0.207, 0.224,
0.211, 0.234, 0.257]), 'mA') #in mA

print('letzten Messwert aus Messung genommen, da nicht nach justiert: (L, I in mA): ', 151.5, 0.01, '\n')

params_kk, covariance_kk = curve_fit(quad, L_konkav_konkav.magnitude, I_konkav_konkav.magnitude)

kk_fit = np.linspace(65, 125)

plt.clf()
plt.plot(kk_fit, quad(kk_fit, *params_kk), 'r-', label=r'Fit')
plt.plot(L_konkav_konkav, I_konkav_konkav.magnitude, 'bx', label=r'Messdaten')
plt.xlabel('Resonatorlänge $L$ in cm')
plt.xlim(65, 125)
plt.ylabel('$I(L)$ in mA')
plt.tight_layout()
plt.legend(loc = 'best')
#plt.savefig('../Pics/Stabilität_kk.pdf')

print('Parameter Fit Stabilität_kk: (a, b, c)', *params_kk, '\n')
print('Parameter Fehler Fit Stabilität_kk: ', np.sqrt(np.diag(covariance_kk)), '\n')

# konkav-planar

L_außen_anfang_kp = Q_(68.8, 'cm') #in cm

L_konkav_planar = Q_(np.array([68.8, 72.8, 78.0, 83.0, 88.0]) - L_linse.magnitude, 'cm')

I_konkav_planar = Q_(np.array([2.57, 2.40, 1.83, 1.48, 1.40]), 'microampere') #in muA

params_kp, covariance_kp = curve_fit(lin, L_konkav_planar.magnitude, I_konkav_planar.magnitude)

kk_fit = np.linspace(58, 79)

plt.clf()
plt.plot(kk_fit, lin(kk_fit, *params_kp), 'r-', label=r'Fit')
plt.plot(L_konkav_planar, I_konkav_planar.magnitude, 'bx', label=r'Messdaten')
plt.xlabel('Resonatorlänge $L$ in cm')
plt.xlim(58, 79)
plt.ylabel('$I(L)$ in $\mu$A')
plt.tight_layout()
plt.legend(loc = 'best')
#plt.savefig('../Pics/Stabilität_kp.pdf')

print('Parameter Fit Stabilität_kp: (a, b)', *params_kp)
print('Parameter Fehler Fit Stabilität_kp: ', np.sqrt(np.diag(covariance_kp)), '\n')

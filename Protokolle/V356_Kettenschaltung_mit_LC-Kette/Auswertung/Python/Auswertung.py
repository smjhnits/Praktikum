import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
# import scipy.constants as const
from uncertainties import ufloat
import uncertainties.unumpy as unp
# from mpl_toolkits.axes_grid1 import host_subplot
# import mpl_toolkits.axisartist as AA

L  = 1.217 * 10**(-3)
C_1 = 20.13 * 10**(-9)
C_2 = 9.41 * 10**(-9)
Wellenwiderstand_C = np.sqrt(L / C_1)
Wellenwiderstand_C1C2 = np.sqrt(2 * L / (C_1 + C_2))
print('Wellenwiderstand_C: ', Wellenwiderstand_C)
print('Wellenwiderstand_C1C2: ', Wellenwiderstand_C1C2)
theta = np.linspace(0, np.pi, 100)

# a.) Durchlasskurve


def exp(x, a, b, c):
    return a * np.exp(b * x) + c

Abstaende_1 = np.array([0, 3, 6, 9, 12, 15, 18])
Abstaende_2 = np.array([0, 2, 4, 6, 8, 11, 14])
omega_C_Duchlasskurve = np.array([1338, 2055, 2843, 3730, 5023, 6471, 8624]) / (2 * np.pi)
omega_C1C2_Durchlasskurve = np.array([7345, 10478, 15169, 21072,30336, 50353, 79169]) / (2 * np.pi)

params_omega_C, covariance_omega_C = curve_fit(exp, Abstaende_1, omega_C_Duchlasskurve)
LC_Fehler = np.sqrt(np.diag(covariance_omega_C))
params_omega_C1C2, covariance_omega_C1C2 = curve_fit(exp, Abstaende_2, omega_C1C2_Durchlasskurve)
LC1C2_Fehler = np.sqrt(np.diag(covariance_omega_C1C2))

print('expo Regression CL-Kette: ', params_omega_C, LC_Fehler)
print('expo Regression C1C2L-Kette: ', params_omega_C1C2, LC1C2_Fehler)

grenzfrequenz_theo_C = 2 / np.sqrt(L * C_1) * np.ones(100)
grenzfrequenz_theo_C1C2_1 = np.sqrt(2 / (L * C_2)) * np.ones(100)
grenzfrequenz_theo_C1C2_2 = np.sqrt(2 / (L * C_1)) * np.ones(100)

print('Grenzfrequenz_theo_C: ', grenzfrequenz_theo_C[0])
print('Grenzfrequenz_theo_C1C2_1: ', grenzfrequenz_theo_C1C2_1[0])
print('Grenzfrequenz_theo_C1C2_2: ', grenzfrequenz_theo_C1C2_2[0])


def Dispersionskurve_C(theta):
    return np.sqrt(2 / (L * C_1) * (1 - np.cos(theta)))


def Dispersionskurve_C1C2_1(theta):
    return np.sqrt(1 / L * (1 / C_1 + 1 / C_2) + 1 / L * np.sqrt((1 / C_1 + 1 / C_2)**2 - 4 * np.sin(theta)**2 / (C_1 * C_2)))


def Dispersionskurve_C1C2_2(theta):
    return np.sqrt(1 / L * (1 / C_1 + 1 / C_2) - 1 / L * np.sqrt((1 / C_1 + 1 / C_2)**2 - 4 * np.sin(theta)**2 / (C_1 * C_2)))


dispersion_C = np.zeros(100)
dispersion_C1C2_1 = np.zeros(100)
dispersion_C1C2_2 = np.zeros(100)

for i in range(0, 100):
    dispersion_C[i] = Dispersionskurve_C(theta[i])

for i in range(0, 100):
    dispersion_C1C2_1[i] = Dispersionskurve_C1C2_1(theta[i])

for i in range(0, 100):
    dispersion_C1C2_2[i] = Dispersionskurve_C1C2_2(theta[i])

plt.plot(theta, dispersion_C, 'b-', label=r'Dispersionskurve C')
# plt.plot(theta, exp(theta ,*params_omega_C), 'rx')
plt.plot(theta, grenzfrequenz_theo_C, 'b--')
plt.ylabel(r'$\omega$ in $1/s$')
plt.xlabel(r'$\theta$')
plt.xticks([0, np.pi / 2, np.pi],
          [r'$0$', r'$\frac{\pi}{2}$', r'$\pi$'])
plt.xlim(0, np.pi)
plt.legend(loc='best')
plt.grid()
plt.tight_layout()
plt.savefig('Dispersionskurve_C_theorie.pdf')

plt.clf()
plt.plot(theta, dispersion_C1C2_1, 'r-', label=r'Dispersionskurve $\omega_1$')
plt.plot(theta, grenzfrequenz_theo_C1C2_1, 'r--')
plt.plot(theta, dispersion_C1C2_2, 'b-', label=r'Dispersionskurve $\omega_2$')
plt.plot(theta, grenzfrequenz_theo_C1C2_2, 'b--')
plt.ylabel(r'$\omega$ in $1/s$')
plt.xlabel(r'$\theta$')
plt.xticks([0, np.pi / 2, np.pi],
          [r'$0$', r'$\frac{\pi}{2}$', r'$\pi$'])
plt.xlim(0, np.pi)
plt.legend(loc='best')
plt.grid()
plt.tight_layout()
plt.savefig('Dispersionskurve_C1C2_theorie.pdf')

# Bestimmen der Grenzfrequenz

# Abstand abgeschätzt 17.2 cm = 5 + 11 / 15 LE
grenzfrequenz_C = exp(17.2, *params_omega_C)
print('Gemessene Grenzfrequenz LC: ', grenzfrequenz_C / (2 * np.pi))
# Abstand gemessen 11 cm = 6 LE
grenzfrequenz_C1C2_1 = exp(11, *params_omega_C1C2)
print('Gemessene Grenzfrequenz C1C2_1: ',  grenzfrequenz_C1C2_1 / (2 * np.pi))
# Abstand gemessen 13.2 cm
grenzfrequenz_C1C2_2 = exp(13.2, *params_omega_C1C2)
print('Gemessene Grenzfrequenz C1C2_2: ',  grenzfrequenz_C1C2_2 / (2 * np.pi))

# Dispersionsrelation

# ??????

# d.) Messung der Spannungsamplituden der offenen LC-Kette

nu_1 = 7133
Kettenglieder_C = np.array([1.55, 1.425, 1.2, 0.95, 0.66, 0.3, 0.027, 0.3, 0.95, 1.2, 1.4, 1.55, 1.575])
nu_2 = 14307
Kettenglieder_C1C2 = np.array([0.925, 0.65, 0.25, 0.2, 0.61, 0.9, 1, 0.98, 0.71, 0.28, 0.17, 0.65, 1, 1.05])

# e.) Messung der Spannungsamplituden einer abgeschlossenen LC-Kette

nu_3 = 7337
Kettenglieder_C_e = np.array([25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 24.5, 24.5, 24.5])

plt.clf()
plt.plot(range(Kettenglieder_C_e), Kettenglieder_C_e, 'rx', label=r'abgeschlossene Welle')
plt.ylabel(r'Spannung in $mV$')
plt.xlabel(r'Kettenglieder')
plt.legend(loc='best')
plt.grid()
plt.tight_layout()
plt.savefig('Messung_e.pdf')

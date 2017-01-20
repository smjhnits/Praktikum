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
omega_C_Durchlasskurve = np.array([1338, 2055, 2843, 3730, 5023, 6471, 8624]) * (2 * np.pi)
omega_C1C2_Durchlasskurve = np.array([7345, 10478, 15169, 21072,30336, 50353, 79169]) * (2 * np.pi)

params_omega_C, covariance_omega_C = curve_fit(exp, Abstaende_1, omega_C_Durchlasskurve)
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
grenzfrequenz_C_err = exp(17.2, *LC_Fehler)
print('Gemessene Grenzomega LC: ', grenzfrequenz_C, grenzfrequenz_C_err)
# Abstand gemessen 11 cm = 6 LE
grenzfrequenz_C1C2_1 = exp(11, *params_omega_C1C2)
grenzfrequenz_C1C2_1_err = exp(11, *LC1C2_Fehler)
print('Gemessene Grenzomega C1C2_1: ',  grenzfrequenz_C1C2_1, grenzfrequenz_C1C2_1_err)
# Abstand gemessen 12.2 cm
grenzfrequenz_C1C2_2 = exp(12.2, *params_omega_C1C2)
grenzfrequenz_C1C2_2_err = exp(12.2, *LC1C2_Fehler)
print('Gemessene Grenzomega C1C2_2: ',  grenzfrequenz_C1C2_2, grenzfrequenz_C1C2_2_err)

# Durchlasskurve exponentialer Fit mit Messdaten
plt.clf()
plt.plot(Abstaende_1, exp(Abstaende_1, *params_omega_C), 'b-', label=r'Dispersionskurve C gemessen')
plt.plot(Abstaende_1, omega_C_Durchlasskurve, 'rx')
plt.ylabel(r'$\omega$ in $1/s$')
plt.xlabel(r'Abstand in $cm$')
plt.legend(loc='best')
plt.grid()
plt.tight_layout()
plt.savefig('Durchlasskurve_C.pdf')

plt.clf()
plt.plot(Abstaende_2, exp(Abstaende_2, *params_omega_C1C2), 'b-', label=r'Dispersionskurve C1C2 gemessen')
plt.plot(Abstaende_2, omega_C1C2_Durchlasskurve, 'rx')
plt.ylabel(r'$\omega$ in $1/s$')
plt.xlabel(r'Abstand in $cm$')
plt.legend(loc='best')
plt.grid()
plt.tight_layout()
plt.savefig('Durchlasskurve_C1C2.pdf')

# Dispersionsrelation
x_Werte_Disperion_1 = np.array([0, np.pi, 2 * np.pi, 3 * np.pi, 4 * np.pi, 5 * np.pi, 6 * np.pi, 7 * np.pi]) / 14
nu_C_Dispersion = np.array([0, 7927, 15610, 23372, 30703, 38072, 43171, 49000])
omega_C_Dispersion = nu_C_Dispersion * (2 * np.pi)
x_Werte_Disperion_2 = np.array([0, np.pi, 2 * np.pi, 3 * np.pi, 4 * np.pi, 5 * np.pi, 6 * np.pi, 7 * np.pi, 8 * np.pi, 9 * np.pi, 10 * np.pi, 11 * np.pi, 12 * np.pi, 13 * np.pi]) / 14
nu_C1C2_Dispersion = np.array([0, 7158, 14188, 15169, 21078, 27714, 34188, 40094, 45378, 50298, 54295, 57976, 60550, 62625])
omega_C1C2_Dispersion = nu_C1C2_Dispersion * (2 * np.pi)
# Werte die Größer als pi / 2 sind 'umklappen'
for i in range(0, len(omega_C1C2_Dispersion)):
    if (x_Werte_Disperion_2[i] > np.pi/2):
        x_Werte_Disperion_2[i] -= 2 * (x_Werte_Disperion_2[i] - np.pi/2)

plt.clf()
plt.plot(theta, dispersion_C, 'b-', label=r'Dispersionskurve C')
plt.plot(theta, grenzfrequenz_theo_C, 'b--')
plt.plot(x_Werte_Disperion_1, omega_C_Dispersion, 'bx', label=r'Messdaten')
plt.ylabel(r'$\omega$ in $1/s$')
plt.xlabel(r'$\theta$')
plt.xticks([0, np.pi/8, np.pi / 4, 3*np.pi/8 , np.pi/2, 5 * np.pi/8, 3*np.pi/4, 7*np.pi/8, np.pi],
           [r"$0$", r"$\frac{\pi}{8}$", r"$\frac{\pi}{4}$", r"$\frac{3\pi}{8}$", r"$\frac{\pi}{2}$",
           r"$\frac{5\pi}{8}$", r"$\frac{3\pi}{4}$", r"$\frac{7\pi}{8}$", r"$\pi$"])
plt.xlim(0, np.pi)
plt.legend(loc='best')
plt.grid()
plt.tight_layout()
plt.savefig('Dispersionskurve_C.pdf')

plt.clf()
plt.plot(theta, dispersion_C1C2_1, 'b-', label=r'Dispersionskurve $C_1C_2$')
plt.plot(theta, dispersion_C1C2_2, 'r-', label=r'Dispersionskurve $C_1C_2$')
plt.plot(x_Werte_Disperion_2, omega_C1C2_Dispersion, 'gx', label=r'Messdaten')
plt.plot(theta, grenzfrequenz_theo_C1C2_2, 'r--')
plt.plot(theta, grenzfrequenz_theo_C1C2_1, 'b--')
plt.ylabel(r'$\omega$ in $1/s$')
plt.xlabel(r'$\theta$')
plt.xticks([0, np.pi / 8, np.pi / 4, 3 * np.pi / 8, np.pi / 2],
          [r'$0$', r'$\frac{\pi}{8}$', r'$\frac{\pi}{4}$', r'$\frac{3\pi}{8}$', r'$\frac{\pi}{2}$'])
plt.xlim(0, np.pi / 2)
plt.legend(loc='best')
plt.grid()
plt.tight_layout()
plt.savefig('Dispersionskurve_C1C2.pdf')

# d.) Messung der Spannungsamplituden der offenen LC-Kette

nu_1 = 7133
Kettenglieder_C = np.array([1.55, 1.425, 1.2, 0.95, 0.66, 0.3, 0.027, 0.3, 0.95, 1.2, 1.4, 1.55, 1.575])
nu_2 = 14307
Kettenglieder_C_2 = np.array([0.925, 0.65, 0.25, 0.2, 0.61, 0.9, 1, 0.98, 0.71, 0.28, 0.17, 0.65, 1, 1.05])

Kettenglieder_C_x = range(0, len(Kettenglieder_C))
plt.clf()
plt.plot(Kettenglieder_C_x, Kettenglieder_C, 'bo', label=r'Messdaten')
plt.ylabel(r'Spannung in $mV$')
plt.xlabel(r'Kettenglieder')
plt.legend(loc='best')
plt.grid()
plt.tight_layout()
plt.savefig('Messung_d_1.pdf')

Kettenglieder_C_2_x = range(0, len(Kettenglieder_C_2))
plt.clf()
plt.plot(Kettenglieder_C_2_x, Kettenglieder_C_2, 'bo', label=r'Messdaten')
plt.ylabel(r'Spannung in $mV$')
plt.xlabel(r'Kettenglieder')
plt.legend(loc='best')
plt.grid()
plt.tight_layout()
plt.savefig('Messung_d_2.pdf')

# e.) Messung der Spannungsamplituden einer abgeschlossenen LC-Kette

nu_3 = 7337
Kettenglieder_C_e = np.array([25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 24.5, 24.5, 24.5])

Kettenglieder_C_e_x = range(0, len(Kettenglieder_C_e))
plt.clf()
plt.plot(Kettenglieder_C_e_x, Kettenglieder_C_e, 'bo', label=r'Messdaten')
plt.ylabel(r'Spannung in $mV$')
plt.xlabel(r'Kettenglieder')
plt.ylim(24, 25.6)
plt.legend(loc='best')
plt.grid()
plt.tight_layout()
plt.savefig('Messung_e.pdf')

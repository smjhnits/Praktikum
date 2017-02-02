import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
# import scipy.constants as const
from uncertainties import ufloat
import uncertainties.unumpy as unp

# Apparaturdaten

L = ufloat(3.53, 0.03) * 10**(-3) # Henry
C = ufloat(5.015, 0.015) * 10**(-9) # Farad
R_1 = ufloat(30.3, 0.1) # Ohm
R_2 = ufloat(271.6, 0.3) # Ohm

# Messung a.) bei Widerstand R_1
nu_a = 5.820 # Hertz
maxima = np.array([11, 9.12, 7.84, 6.88, 6.16, 5.6, 5.28, 4.96, 4.80, 4.68, 4.56, 4.44]) + 4.08 # Volt
zeit = np.array([0, 27.5, 27.5, 27.5, 30, 30, 30, 30, 32.5, 32.5, 35, 35]) * 10**(-6) # Zeit in Sekunden zwischen den Maxima
zeit_ges = np.array([0, 27.5, 55, 82.5, 112.5, 142.5, 172.5, 202.5, 235, 267.5, 302.5, 337.5]) * 10**(-6)

# Messung b.)
R_ap = 13.5 * 1000 # Ohm (gefundener Widerstand für den aperiodischen Grenzfall)
nu_b = 5.815 # Hertz

# Messung c.)
nu_c = np.array([10, 15, 20, 25, 30, 34, 35, 36, 36.5, 37, 40, 45, 50, 55, 60, 70]) * 10**(3) # Hertz Generatorfrequenz
lamda = np.array([98, 67, 50.8, 40, 33.2, 29.6, 28.4, 28, 27.2, 26.4, 25.2, 22.2, 19.8, 18.2, 16.6, 14]) * 10**(-6) # Sekunden Wellenlänge
phasenversch = np.array([0, 1.2, 1.6, 2, 3.2, 4.8, 5.2, 6.4, 6, 6.8, 7.8, 8.4, 8.6, 8.2, 8, 7]) * 10**(-6) # Sekunde Phasenverschiebung
U_G = np.array([5.4, 5.4, 5.12, 5.04, 4.8, 4.48, 4.4, 4.4, 4.4, 4.32, 4.48, 4.72, 4.88, 4.96, 4.96, 5.04]) # Volt Generatorspannung
U_C = np.array([5.44, 5.92, 6.64, 8.4, 10.8, 12.8, 13, 13.2, 13, 12.8, 11.2, 7.6, 5.2, 4, 3, 2]) # Volt Kondensatorspannung
phase = phasenversch / lamda * 2 * np.pi

# zu a.)


def e(x, a, b, c):
    return a * np.exp(b * x) + c

params, covariance = curve_fit(e, zeit_ges, maxima)

plt.clf()
plt.plot(zeit_ges, maxima, 'bx', label=r'Messdaten')
plt.plot(zeit_ges, e(zeit_ges, *params), 'r-', label=r'Ausgleichsrechnung')
plt.title('Ausgleichrechnung')
plt.legend(loc='best')
plt.savefig('ausgleichsrechnung.pdf')

print('Auslgeichsrechnung: ', params, np.diag(np.sqrt(covariance)))

fehler_exp = np.diag(np.sqrt(covariance))[1]
wert_exp = params[1]
exponent = - ufloat(wert_exp, fehler_exp)

R_eff = exponent * 2 * L
T_ex = 1 / exponent

print('Effektiv Widerstand: ', R_eff)
print('Abklingdauer: ', T_ex)

# zu b.)

R_ap_theo = 2 * unp.sqrt(L / C)

print('Theoriewert für R_ap: ', R_ap_theo)
print('gemessener Wert für R aperiodischer Grenzfall: ', R_ap)
print('Abweichung: ', R_ap / R_ap_theo)

# zu c.)

Uc_U = U_C / U_G

# halblogarithmisch
plt.clf()
plt.plot(nu_c, Uc_U, 'rx', label=r'$\frac{U_c}{U}(\nu)$')
plt.xscale('log')
plt.xlabel(r'$\nu$ in $Hz$')
plt.ylabel(r'$\frac{U_c}{U}$ in $V$')
plt.legend(loc='best')
plt.tight_layout()
plt.savefig('messung_c.pdf')

plt.clf()
plt.plot(nu_c, phase, 'bx', label=r'$\phi (\nu$)')
plt.xscale('log')
plt.xlabel(r'$\nu$ in $Hz$')
plt.ylabel(r'$\phi$ in $rad$')
plt.legend(loc='best')
plt.tight_layout()
plt.savefig('phase_gegen_nu.pdf')

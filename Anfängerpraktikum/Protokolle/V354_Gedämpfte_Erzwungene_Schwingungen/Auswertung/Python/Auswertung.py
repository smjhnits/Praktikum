import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
# import scipy.constants as const
from uncertainties import ufloat
import uncertainties.unumpy as unp
from uncertainties.unumpy import (nominal_values as noms, std_devs as stds)

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


def f(x, m, b):
    return m * x + b

# zu a.)


def e(x, a, b, c):
    return a * np.exp(b * x) + c

params, covariance = curve_fit(e, zeit_ges, maxima)

plt.clf()
plt.plot(zeit_ges * 10**6, maxima, 'bx', label=r'Messdaten')
plt.plot(zeit_ges * 10**6, e(zeit_ges, *params), 'r-', label=r'Ausgleichsrechnung')
plt.xlabel(r'Zeit in $\mu$s')
plt.ylabel(r'$U_C(t_i)$ in V')
plt.xlim(-5, 350)
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

U_c_max = 13.2 # Volt

U_c_abgesunken = U_c_max / np.sqrt(2) / 4.4


# halblogarithmisch ? kein ersichtlicher Vorteil
plt.clf()
plt.plot(nu_c / 10**3, Uc_U, 'rx', label=r'$\frac{U_c}{U}(\nu)$')
plt.plot(noms(R_eff / L) * np.ones(20) / 10**3 + 3.5, np.linspace(0, 3.2, 20), 'b--', label=r'Breite')
plt.plot(2 * noms(R_eff / L) * np.ones(20) / 10**3 - 3.5, np.linspace(0, 3.2, 20), 'b--')
plt.plot(nu_c / 10**3, U_c_abgesunken * np.ones(16), 'g--', label=r'$\frac{1}{\sqrt{2}}U_{C,max}$')
# plt.xscale('log')
plt.xlabel(r'$\nu$ in kHz')
plt.ylabel(r'$\frac{U_c}{U}$')
plt.xlim(9.2, 71)
plt.ylim(0, 3.2)
plt.grid()
plt.legend(loc='best')
plt.tight_layout()
plt.savefig('messung_c.pdf')

print('nu_res: ', nu_c[7])
print('Breite in kHz: ', 2 * noms(R_eff / L) / 10**3 - 3.5 - (noms(R_eff / L)/ 10**3 + 3.5))
print('nu_+, nu_-: ', noms(R_eff / L) / 10**3 + 3.5, 2 * noms(R_eff / L) / 10**3 - 3.5)
print('nu_+theo - nu_-theo: ', R_eff / L / 10**3)

nu_res = np.array([nu_c[5], nu_c[6], nu_c[7], nu_c[8], nu_c[9]]) # Frequenz um Resonanzfrequenz
Uc_U_res = np.array([Uc_U[5], Uc_U[6], Uc_U[7], Uc_U[8], Uc_U[9]]) # Spannung um Resonanzfrequenz

nu_res_theo = unp.sqrt(1 / (L * C) - R_eff**2 / (2 * L**2)) / (2 * np.pi)

print('nu_res: ', nu_res_theo)

plt.clf()
plt.plot(nu_res / 10**3, Uc_U_res, 'rx', label=r'$\frac{U_c}{U}(\nu)$')
plt.xlabel(r'$\nu$ in kHz')
plt.ylabel(r'$\frac{U_c}{U}$ in V')
plt.xlim(33.9, 37.1)
plt.ylim(2.84, 3.1)
plt.legend(loc='best')
plt.grid()
plt.tight_layout()
plt.savefig('messung_c_linear.pdf')

# zu d.)

nu_1_gemessen = nu_c[4]
nu_2_gemessen = nu_c[11]

plt.clf()
plt.plot(nu_c / 10**3, phase, 'bx', label=r'$\phi (\nu$)')
# plt.xscale('log')
plt.plot(nu_1_gemessen * np.ones(20) / 10**3, np.linspace(-0.5, 5 * np.pi * 4, 20), 'g--', label=r'$\nu_1$ bzw. $\nu_2$')
plt.plot(nu_2_gemessen * np.ones(20) / 10**3, np.linspace(-0.5, 5 * np.pi * 4, 20), 'g--')
plt.plot(nu_c[9] * np.ones(20) / 10**3, np.linspace(-0.5, 5 * np.pi * 4, 20), 'r--', label=r'$\nu_{res}$')
plt.xlabel(r'$\nu$ in kHz')
plt.ylabel(r'$\varphi$ in rad')
plt.yticks([0, np.pi / 4, np.pi / 2, 3 * np.pi / 4, np.pi],
          [r'$0$', r'$\frac{\pi}{4}$', r'$\frac{\pi}{2}$', r'$\frac{3\pi}{4}$', r'$\pi$'])
plt.legend(loc='best')
plt.grid()
plt.xlim(8, 72)
plt.ylim(-0.5, np.pi + 0.5)
plt.tight_layout()
plt.savefig('phase_gegen_nu.pdf')

nu_1 = R_eff / (2 * L) + unp.sqrt(R_eff**2 / (4 * L**2) + 1 / (L * C)) / 2 * np.pi
nu_2 = - R_eff / (2 * L) + unp.sqrt(R_eff**2 / (4 * L**2) + 1 / (L * C)) / 2 * np.pi

print('nu_1,gemessen ; nu_2,gemessen: ', nu_1_gemessen, nu_2_gemessen)
print('nu_resgemessen: ', nu_c[9])
print('nu_1 - nu_2: ', nu_1 - nu_2)
print('nu_1,theo; nu_2,theo: ', nu_1, nu_2)
print('theo nu_1 - nu_2 = R / L: ', R_eff / L)

print('Güte, theo: ', 1 / R_eff * unp.sqrt(L / C) / (np.pi))
print('Güte, gemessen: ', Uc_U[7])

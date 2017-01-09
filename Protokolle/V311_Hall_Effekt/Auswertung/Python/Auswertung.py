import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import scipy.constants as const
from uncertainties import ufloat
import uncertainties.unumpy as unp

# Strom gegen B-Feld auftragen

I_aufsteigend = np.linspace(0, 5, 11)
I_abfallend = np.linspace(5, 0, 11)
B_aufsteigend = np.array([7.7, 142, 272, 420, 556, 700, 840, 975, 1077, 1158, 1220])
B_abfallend = np.array([1220, 1169, 1095, 977, 845, 703, 563, 422, 279, 138, 8.3])

plt.plot(I_aufsteigend, B_aufsteigend, 'r-', label=r'Aufsteigende Stromstärke')
plt.plot(I_abfallend, B_abfallend, 'b-', label=r'Abfallende Stromstärke')
plt.ylabel(r'B-Feld Stärke in $mT$')
plt.xlabel(r'Stromstärke in $A$')
plt.legend(loc='best')
plt.tight_layout()
plt.savefig('Hysterese.pdf')

# lineare Regression


def function(x, a, b):
    return a * x + b

params, covariance = curve_fit(function, I_aufsteigend, B_aufsteigend)

plt.clf()
plt.plot(I_aufsteigend, B_aufsteigend, 'kx', label=r'Messdaten von aufsteigendem I')
plt.plot(I_aufsteigend, function(I_aufsteigend, *params), 'g-', label=r'Lineare Regression')
plt.ylabel(r'B-Feld Stärke in $mT$')
plt.xlabel(r'Stromstärke in $A$')
plt.legend(loc='best')
plt.tight_layout()
plt.savefig('lineareRegression.pdf')

print('Proportionalitätsfaktor alpha zwischen B und I: ', params[0])

# Widerstand berechnen

I = np.linspace(0, 10, 11)
U_Zink = np.array([-0.02, 14.13, 27.7, 41.1, 55.5, 68.3, 81.5, 94.7, 107.1, 120.3, 133.7])
U_Kupfer = np.array([0, 7.83, 15.54, 23.3, 30.9, 38.6, 46.3, 53.9, 61.5, 68.8, 76.5])

params_Zink, covariance_Zink = curve_fit(function, I, U_Zink)
params_Kupfer, covariance_Kupfer = curve_fit(function, I, U_Kupfer)

plt.subplot(2, 1, 1)
plt.plot(I, U_Zink, 'kx', label=r'Zink')
plt.plot(I, function(I, *params_Zink), 'g-', label=r'Lineare Regression an Zink')
plt.ylim(0, 140)
plt.ylabel(r'Spannung U in $mV$')
plt.xlabel(r'Stromstärke in $A$')
plt.legend(loc='best')

plt.subplot(2, 1, 2)
plt.plot(I, U_Kupfer, 'kx', label=r'Kupfer')
plt.plot(I, function(I, *params_Kupfer), 'b-', label=r'Lineare Regression an Kupfer')
plt.ylabel(r'Spannung U in $mV$')
plt.xlabel(r'Stromstärke in $A$')
plt.legend(loc='best')

plt.tight_layout()
plt.savefig('Widerstandsmessung.pdf')

print('Widerstand von Zink:[in mv/A] ', params_Zink[0])
print('Fehler: ', np.sqrt(np.diag(covariance_Zink))[0])
print('Widerstand von Kupfer: ', params_Kupfer[0])
print('Fehler: ', np.sqrt(np.diag(covariance_Kupfer))[0])
R_Zink = ufloat(params_Zink[0], np.sqrt(np.diag(covariance_Zink))[0])
R_Kupfer = ufloat(params_Kupfer[0], np.sqrt(np.diag(covariance_Kupfer))[0])

# Messung der Hall-Spannung bei konstantem Probenstrom U_H in mV, Zink I_p: = 8 A, Kupfer: I_p = 10 A
B_s_Zink = np.zeros(11)
B_s_Kupfer = np.zeros(8)


def I_umwandeln_B(I):
    return I * params[0]

I_s_Zink = np.linspace(0, 5, 11)
for i in range(11):
    B_s_Zink[i] = I_umwandeln_B(I_s_Zink[i])

I_s_Kupfer = np.linspace(0, 3.5, 8)
for i in range(8):
    B_s_Kupfer[i] = I_umwandeln_B(I_s_Kupfer[i])

Zink_Is_U_H_1 = np.array([0.644, 0.648, 0.651, 0.654, 0.657, 0.659, 0.661, 0.663, 0.664, 0.665, 0.666])
Kupfer_Is_U_H_1 = - np.array([0.342, 0.340, 0.338, 0.336, 0.334, 0.332, 0.330, 0.328])

# Umpolen

Zink_Is_U_H_2 = np.array([0.647, 0.646, 0.645, 0.644, 0.642, 0.641, 0.639, 0.638, 0.636, 0.635, 0.634])
Kupfer_Is_U_H_2 = - np.array([0.340, 0.342, 0.343, 0.345, 0.347, 0.349, 0.351, 0.3530])


U_H_Zink_s = 1 / 2 * (Zink_Is_U_H_1 - Zink_Is_U_H_2)
U_H_Kupfer_s = 1 / 2 * (Kupfer_Is_U_H_1 - Kupfer_Is_U_H_2)

paramsU_H_I_Zink_s, covariance_U_H_I_Zink_s = curve_fit(function, I_s_Zink, U_H_Zink_s)
paramsU_H_I_Kupfer_s, covariance_U_H_I_Kupfer_s = curve_fit(function, I_s_Kupfer, U_H_Kupfer_s)
paramsU_H_B_Zink_s, covariance_U_H_B_Zink_s = curve_fit(function, B_s_Zink, U_H_Zink_s)
paramsU_H_B_Kupfer_s, covariance_U_H_B_Kupfer_s = curve_fit(function, B_s_Kupfer, U_H_Kupfer_s)

plt.clf()
plt.subplot(2, 1, 1)
plt.plot(I_s_Zink, U_H_Zink_s, 'kx')
plt.plot(I_s_Zink, function(I_s_Zink, *paramsU_H_I_Zink_s), 'r-', label=r'lineare Regression')
plt.title('Hall-Spannung von Zink gegenüber I bei konstantem Probenstrom $8 A$')
plt.ylabel(r'Hall-Spannung in $mV$')
plt.xlabel(r'Stromstärke in $A$')
plt.legend(loc='best')
plt.subplot(2, 1, 2)
plt.plot(I_s_Kupfer, U_H_Kupfer_s, 'kx')
plt.plot(I_s_Kupfer, function(I_s_Kupfer, *paramsU_H_I_Kupfer_s), 'b-', label=r'lineare Regression')
plt.title('Hall-Spannung von Kupfer gegenüber I bei konstantem Probenstrom $10 A$')
plt.ylabel(r'Hall-Spannung in $mV$')
plt.xlabel(r'Stromstärke in $A$')
plt.legend(loc='best')

plt.tight_layout()
plt.savefig('Hall_Spannung_gegenueber_I_s.pdf')

plt.clf()
plt.subplot(2, 1, 1)
plt.plot(B_s_Zink, U_H_Zink_s, 'kx')
plt.plot(B_s_Zink, function(B_s_Zink, *paramsU_H_B_Zink_s), 'r-', label=r'lineare Regression')
plt.title('Hall-Spannung von Zink gegenüber B bei konstantem Probenstrom von $8 A$')
plt.ylabel(r'Hall-Spannung in $mV$')
plt.xlabel(r'$B$-Feldstärke in $mT$')
plt.legend(loc='best')
plt.subplot(2, 1, 2)
plt.plot(B_s_Kupfer, U_H_Kupfer_s, 'kx')
plt.plot(B_s_Kupfer, function(B_s_Kupfer, *paramsU_H_B_Kupfer_s), 'b-', label=r'lineare Regression')
plt.title('Hall-Spannung von Kupfer gegenüber B bei konstantem Probenstrom von $10 A$')
plt.ylabel(r'Hall-Spannung in $mV$')
plt.xlabel(r'$B$-Feldstärke in $mT$')
plt.legend(loc='best')

plt.tight_layout()
plt.savefig('Hall_Spannung_gegenueber_B_s.pdf')

# print(,paramsU_H_I_Zink_s)
# print(,paramsU_H_I_Kupfer_s)
# print(,paramsU_H_B_Zink_s)
# print(,paramsU_H_B_Kupfer_s)

# Messung der Hall-Spannung bei konstantem Spulenstrom U_H in mV, Zink: I_s = 5 A, Kupfer: I_s = 3 A

B_p_Zink = np.zeros(11)
B_p_Kupfer = np.zeros(11)

I_p = np.linspace(0, 8, 11)
I_p_Kupfer = np.linspace(0, 10, 11)
Zink_Ip_U_H_1 = np.array([-0.020, 0.045, 0.109, 0.174, 0.234, 0.304, 0.365, 0.431, 0.495, 0.560, 0.626])
Kupfer_Ip_U_H_1 = - np.array([0.336, 0.338, 0.340, 0.342, 0.343, 0.345, 0.347, 0.348, 0.350, 0.351, 0.352])

# Umpolen
Zink_Ip_U_H_2 = np.array([-0.020, 0.047, 0.116, 0.184, 0.250, 0.318, 0.389, 0.456, 0.527, 0.597, 0.666])
Kupfer_Ip_U_H_2 = - np.array([0.338, 0.337, 0.336, 0.335, 0.335, 0.334, 0.333, 0.332, 0.332, 0.332, 0.330])

U_H_Zink_p = 1 / 2 * (Zink_Ip_U_H_1 - Zink_Ip_U_H_2)
U_H_Kupfer_p = 1 / 2 * (Kupfer_Ip_U_H_1 - Kupfer_Ip_U_H_2)

# for i in range(11):
#    B_p_Zink[i] = I_umwandeln_B(I_p[i])
# for i in range(11):
#    B_p_Kupfer[i] = I_umwandeln_B(I_p_Kupfer[i])

paramsU_H_I_Zink_p, covariance_U_H_I_Zink_p = curve_fit(function, I_p, U_H_Zink_p)
paramsU_H_I_Kupfer_p, covariance_U_H_I_Kupfer_p = curve_fit(function, I_p_Kupfer, U_H_Kupfer_p)
# paramsU_H_B_Zink_p, covariance_U_H_B_Zink_p = curve_fit(function, B_p_Zink, U_H_Zink_p)
# paramsU_H_B_Kupfer_p, covariance_U_H_B_Kupfer_p = curve_fit(function, B_p_Kupfer, U_H_Kupfer_p)

plt.clf()
plt.subplot(2, 1, 1)
plt.plot(I_p, U_H_Zink_p, 'kx')
plt.plot(I_p, function(I_p, *paramsU_H_I_Zink_p), 'r-', label=r'lineare Regression')
plt.title('Hall-Spannung von Zink gegenüber I bei konstanten Spulenstrom $5 A$')
plt.legend(loc='best')
plt.ylabel(r'Hall-Spannung in $mV$')
plt.xlabel(r'Stromstärke in $A$')
plt.subplot(2, 1, 2)
plt.plot(I_p_Kupfer, U_H_Kupfer_p, 'kx')
plt.plot(I_p_Kupfer, function(I_p_Kupfer, *paramsU_H_I_Kupfer_p), 'b-', label=r'lineare Regression')
plt.title('Hall-Spannung von Kupfer gegenüber I bei konstanten Spulenstrom $3 A$')
plt.ylabel(r'Hall-Spannung in $mV$')
plt.xlabel(r'Stromstärke in $A$')
plt.legend(loc='best')

plt.tight_layout()
plt.savefig('Hall_Spannung_gegenueber_I_p.pdf')

# plt.clf()
# plt.subplot(2, 1, 1)
# plt.plot(B_p_Zink, U_H_Zink_p, 'kx')
# plt.plot(B_p_Zink, function(B_p_Zink, *paramsU_H_B_Zink_p), 'r-', label=r'lineare Regression')
# plt.title('Hall-Spannung von Zink gegenüber B bei konstanten Spulenstrom')
# plt.legend(loc='best')
# plt.ylabel(r'Hall-Spannung in $mV$')
# plt.xlabel(r'$B$-Feldstärke in $mT$')
# plt.subplot(2, 1, 2)
# plt.plot(B_p_Kupfer, U_H_Kupfer_p, 'kx')
# plt.plot(B_p_Kupfer, function(B_p_Kupfer, *paramsU_H_B_Kupfer_p), 'b-', label=r'lineare Regression')
# plt.title('Hall-Spannung von Kupfer gegenüber B bei konstanten Spulenstrom')
# plt.ylabel(r'Hall-Spannung in $mV$')
# plt.xlabel(r'$B$-Feldstärke in $mT$')
# plt.legend(loc='best')

# plt.tight_layout()
# plt.savefig('Hall_Spannung_gegenüber_B_p.pdf')

# Bestimmen der Ladungsträger pro Volumen n
# Abmessungen der Proben [1] = Höhe, [2] = Breite, [3] = Dicke, Angaben in cm

Zink = np.array([0.02603, 0.04406, 0.00043])
Kupfer = np.array([0.0280, 0.0253, 0.000018])
Zink_Querschnitt = Zink[0] * Zink[2]
Kupfer_Querschnitt = Kupfer[0] * Kupfer[2]

# U_H_Zink = 1 / 2 * (U_H_Zink_p + U_H_Zink_s)
# U_H_Kupfer = 1 / 2 * (U_H_Kupfer_p + U_H_Kupfer_s)
# B_Zink = 1 / 2 * (B_p_Zink + B_s_Zink)
# B_Kupfer = 1 / 2 * (B_p_Kupfer + B_s_Kupfer)

# n_Zink_constI = 1 / (const.e * U_H_Zink_p * Zink[2] * params[0]) * I_p[10]
# n_Zink_constB = 1 / (const.e * U_H_Zink_s * Zink[2] * params[0]) * I_s_Zink[10]
# n_Kupfer_constI = 1 / (const.e * U_H_Kupfer_p * Zink[2] * params[0]) * I_p_Kupfer[10]
# n_Kupfer_constB = 1 / (const.e * U_H_Kupfer_s * Zink[2] * params[0]) * I_s_Kupfer[10]

# n_Zink_p = - 1 / (Zink[2] * const.e * U_H_Zink_p[10]) * (I_p[10])**2 * params[0]
# n_Zink_s = 1 / (Zink[2] * const.e * U_H_Zink_s[10]) * (I_s_Zink[10])**2 * params[0]
# n_Kupfer_p = - 1 / (Kupfer[2] * const.e * U_H_Kupfer_p[10]) * (I_p_Kupfer[10])**2 * params[0]
# n_Kupfer_s = 1 / (Kupfer[2] * const.e * U_H_Kupfer_s[7]) * (I_s_Kupfer[7])**2 * params[0]

m_U_H_B_Zink_s = ufloat(paramsU_H_B_Zink_s[0], np.sqrt(np.diag(covariance_U_H_B_Zink_s))[0])
m_U_H_B_Kupfer_s = ufloat(paramsU_H_B_Kupfer_s[0], np.sqrt(np.diag(covariance_U_H_B_Kupfer_s))[0])
m_U_H_I_Zink_p = ufloat(paramsU_H_I_Zink_p[0], np.sqrt(np.diag(covariance_U_H_I_Zink_p))[0])
m_U_H_I_Kupfer_p = ufloat(paramsU_H_I_Kupfer_p[0], np.sqrt(np.diag(covariance_U_H_I_Kupfer_p))[0])

n_Zink_s = 8 / (const.e * m_U_H_B_Zink_s * Zink[2])
n_Kupfer_s = 10 / (const.e * m_U_H_B_Kupfer_s * Kupfer[2])
n_Zink_p = (5 * params[0]) / (m_U_H_I_Zink_p * const.e * Zink[2])
n_Kupfer_p = (3 * params[0]) / (m_U_H_I_Kupfer_p * const.e * Kupfer[2])

print('n_Zink bei konstantem Probenstrom: ', n_Zink_s)
print('n_Kupfer bei konstantem Probenstrom: ', n_Kupfer_s)
print('n_Zink bei konstantem Spulenstrom: ', n_Zink_p)
print('n_Kupfer bei konstantem Spulenstrom: ', n_Kupfer_p)

# Bestimmen der Ladungsträger pro Atom

molareMasse_Zink = 26
dichte_Zink = 7.14
molareMasse_Kupfer = 63.5
dichte_Kupfer = 8.96
Ladungsträgerdichte_Zink_theorie = molareMasse_Zink / (Zink[0] * Zink[1] * Zink[2] * dichte_Zink)
Ladungsträgerdichte_Kupfer_theorie = molareMasse_Kupfer / (Kupfer[0] * Kupfer[1] * Kupfer[2] * dichte_Kupfer)
print('Ladungsträgerdichte Zink_theo: ', Ladungsträgerdichte_Zink_theorie)
print('Ladungsträgerdichte Kupfer_theo: ', Ladungsträgerdichte_Kupfer_theorie)
print('Ladungsträgerdichte_Zink_theorie_pro_atom: ', Ladungsträgerdichte_Zink_theorie / const.Avogadro)
print('Ladungsträgerdichte_Kupfer_theorie_pro_atom: ', Ladungsträgerdichte_Kupfer_theorie / const.Avogadro)

molVol_Zink = molareMasse_Zink / (dichte_Zink * 10**6)
molVol_Kupfer = molareMasse_Kupfer / (dichte_Kupfer * 10**6)


def z(Name, n, molVol):
    print(Name, n * molVol / const.Avogadro)
    return (n * molVol / const.Avogadro)

z_Zink_s = z('z_Zink_s', n_Zink_s, molVol_Zink)
z_Zink_p = z('z_Zink_p', n_Zink_p, molVol_Zink)
z_Kupfer_s = z('z_Kupfer_s', n_Kupfer_s, molVol_Kupfer)
z_Kupfer_p = z('z_Kupfer_p', n_Kupfer_p, molVol_Kupfer)

# mittlere Flugzeit


def tau(Name, l, b, d, n, R):
    print(Name, (2 * const.m_e * l * 100) / ((const.e)**2 * n * b * d * R))
    return (2 * const.m_e * l * 100) / ((const.e)**2 * n * b * d * R)

tau_Zink_s = tau('tau_Zink_s: ', Zink[1], Zink[0], Zink[2], n_Zink_s, R_Zink * 10**(-3))
tau_Kupfer_s = tau('tau_Kupfer_s: ', Kupfer[1], Kupfer[0], Kupfer[2], n_Kupfer_s, R_Kupfer * 10**(-3))
tau_Zink_p = tau('tau_Zink_p: ', Zink[1], Zink[0], Zink[2], n_Zink_p, R_Zink * 10**(-3))
tau_Kupfer_p = tau('tau_Kupfer_p: ', Kupfer[1], Kupfer[0], Kupfer[2], n_Kupfer_p, R_Kupfer * 10**(-3))

# mittlere Driftgeschwindigkeit


def v_drift(Name, n):
    print(Name, (1000000) / (n * const.e))
    return ((1000000) / (n * const.e))

v_drift_Zink_s = v_drift('v_drift_Zink_s: ', n_Zink_s)
v_drift_Zink_p = v_drift('v_drift_Zink_p: ', n_Zink_p)
v_drift_Kupfer_s = v_drift('v_drift_Kupfer_s: ', n_Kupfer_s)
v_drift_Kupfer_p = v_drift('v_drift_Kupfer_p: ', n_Kupfer_p)

# Fermi-Energie


def Fermi(Name, n):
    print(Name, (const.h**2 / (2 * const.m_e)) * (3 * n / (8 * np.pi))**(2/3))
    return ((const.h**2 / (2 * const.m_e)) * ((3 * n) / 8 * np.pi)**(2/3))

Fermi_Zink_s = Fermi('Fermi_Zink_s', n_Zink_s)
Fermi_Zink_p = Fermi('Fermi_Zink_p', n_Zink_p)
Fermi_Kupfer_s = Fermi('Fermi_Kupfer_s', n_Kupfer_s)
Fermi_Kupfer_p = Fermi('Fermi_Kupfer_p', n_Kupfer_p)

# Totalgeschwindigkeit


def v_T(Name, E_F):
    print(Name, unp.sqrt(2 * E_F / const.m_e))
    return unp.sqrt(2 * E_F / const.m_e)

v_T_Zink_s = v_T('v_T_Zink_s', Fermi_Zink_s)
v_T_Zink_p = v_T('v_T_Zink_p', Fermi_Zink_p)
v_T_Kupfer_s = v_T('v_T_Kupfer_s', Fermi_Kupfer_s)
v_T_Kupfer_p = v_T('v_T_Kupfer_p', Fermi_Kupfer_p)

# mittlere freie Weglänge


def l(Name, tau, E_F):
    print(Name, tau * unp.sqrt(2 * E_F / const.m_e))
    return (Name, tau * unp.sqrt(2 * E_F / const.m_e))

l_Zink_s = l('l_Zink_s', tau_Zink_s, Fermi_Zink_s)
l_Zink_p = l('l_Zink_p', tau_Zink_p, Fermi_Zink_p)
l_Kupfer_s = l('l_Kupfer_s', tau_Kupfer_s, Fermi_Kupfer_s)
l_Kupfer_p = l('l_Kupfer_p', tau_Kupfer_p, Fermi_Kupfer_p)

# Beweglichkeit


def mu(Name, tau):
    print(Name, 1/2 * const.e * tau / const.m_e)
    return(Name, 1/2 * const.e * tau / const.m_e)

mu_Zink_s = mu('mu_Zink_s', tau_Zink_s)
mu_Zink_p = mu('mu_Zink_p', tau_Zink_p)
mu_Kupfer_s = mu('mu_Kupfer_s', tau_Kupfer_s)
mu_Kupfer_p = mu('mu_Kupfer_p', tau_Kupfer_p)

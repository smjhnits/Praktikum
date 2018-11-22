import numpy as np
import matplotlib.pyplot as plt
import scipy.constants as const
from pint import UnitRegistry
from scipy.optimize import curve_fit
import scipy.integrate as integrate
from uncertainties import ufloat
import uncertainties.unumpy as unp
from uncertainties.unumpy import (nominal_values as noms, std_devs as stds)
import data
u = UnitRegistry()
Q_ = u.Quantity

################## Konstanten für Kupfer ##################

# Molmasse Wikipedia
M_cu = Q_(63.546 * const.N_A, 'dalton / mol').to('kg / mol').magnitude
# Probenmasse Versuchsanleitung
m_probe = Q_(342, 'g').to('kg').magnitude
# Molvolumen Wikipedia
V_0 = Q_(7.11 / 10**(6), 'm**3 / mol').magnitude
# Kompressionsmodul http://www.periodensystem-online.de/index.php?show=list&id=modify&prop=Kompressionsmodul&sel=oz&el=68
kappa = Q_(140, 'gigapascal').to('pascal').magnitude

################## Funktionen ##################

def poly_3(x, a, b, c, d):
    return a * x**3 + b * x**2 + c * x + d

def T(R):
    return 0.00134 * R**2 + 2.296 * R - 243.02 + 273.15

def C_p_cu(U, I, dt, dT):
    return M_cu / m_probe * (U * I * dt) / dT

def C_v_cu(C_p, alpha, T):
    return C_p - 9 * alpha**2 * kappa * V_0 * T

def korrektur(array, index):
    for i in index:
        array = np.delete(array, i, None)
    return array

def plot(x_array, y_array, x_label, y_label, x_lim, pfad, plot_label, graphstyle):
    plt.plot(x_array, y_array, graphstyle, label = plot_label)
    plt.xlim(x_lim)
    plt.xlabel(x_label, fontsize = 'large')
    plt.ylabel(y_label, fontsize = 'x-large')
    plt.legend(loc = 'best', fontsize = 'large')
    plt.savefig(pfad)

################## Daten einlesen ##################

R_probe = Q_(data.R_probe, "kiloohm").to('ohm').magnitude
R_zylinder = Q_(data.R_zylinder, 'kiloohm').to('ohm').magnitude

U = Q_(np.array(data.U[:len(data.U) - 1]), 'volt').magnitude
I = Q_(np.array(data.I[:len(data.I) - 1]), 'milliampere').to('ampere').magnitude

I_err = unp.uarray(I, 0.0001 * np.ones(len(I)))
U_err = unp.uarray(U, 0.01 * np.ones(len(U)))

time = Q_(np.array(data.time_min) * 60 + np.array(data.time_sec), 's').magnitude

delta_t = Q_(time[1:] - time[:len(time) - 1], 's').magnitude

delta_T_probe = Q_(T(R_probe[1:]) - T(R_probe[:len(R_probe) - 1]), 'kelvin').magnitude
delta_T_zylinder = Q_(T(R_zylinder[1:]) - T(R_zylinder[:len(R_zylinder) - 1]), 'kelvin').magnitude

################## C_p bestimmen ##################

C_p_cu = C_p_cu(U, I, delta_t, delta_T_probe)
C_p_cu_err = I_err * U_err * delta_t / delta_T_probe * M_cu / m_probe

print("\n", "###############################################################################", "\n", "\n",'C_p Mittelwert, STD: ', np.mean(C_p_cu), np.std(C_p_cu))
print('C_p: ', C_p_cu_err)

plt.clf()
plot(T(R_probe)[1:], C_p_cu, r'$T_{Probe}$ / K', r"$C_p(T)\cdot$ K $\cdot$ mol / J", [min(T(R_probe))-3, max(T(R_probe)) + 3], '../Plots/C_p.pdf', r"$C_p(T)$", "bx")

################## Temperaturen plotten ##################

plt.clf()
plot(time, T(R_probe), r'$t$ / s', r"$T$ / K", [min(time)-3, max(time) + 3], '../Plots/temp.pdf', r"$T_{Probe}$", "bx")
plt.yticks([80, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300])
plot(time, T(R_zylinder), r'$t$ / s', r"$T$ / K", [min(time)- 100, max(time) + 100], '../Plots/temp.pdf', r"$T_{Zylinder}$", "rx")

################## C_V bestimmen ##################
# Dafür erst alpha(T) bestimmen
# alpha = list(alpha, T)

params_alpha, cov_alpha = curve_fit(poly_3, np.array(data.alpha[1]), np.array(data.alpha[0]))

x_min = 65
x_max = 305
x = np.linspace(x_min, x_max)

plt.clf()
plot(data.alpha[1], data.alpha[0], r'$T$ / K', r"$\alpha\cdot 10^{-6} \cdot$K", [x_min, x_max], '../Plots/alpha_T.pdf', "Gegebene Daten", "bx")
plot(x, poly_3(x, *params_alpha), r'$T$ / K', r"$\alpha\cdot 10^{-6} \cdot$K", [x_min, x_max], '../Plots/alpha_T.pdf', "Fit", 'r-')

params_err = np.sqrt(np.diag(cov_alpha))

a = ufloat(params_alpha[0], params_err[0])
b = ufloat(params_alpha[1], params_err[1])
c = ufloat(params_alpha[2], params_err[2])
d = ufloat(params_alpha[3], params_err[3])
x = T(R_probe)

alpha_von_T = (a * x**3 + b * x**2 + c * x + d) / 10**6

#C_p - 9 * alpha**2 * kappa * V_0 * T
C_V_cu = C_v_cu(C_p_cu_err, alpha_von_T[1:], T(R_probe)[1:])

print("\n", "###############################################################################", "\n", "\n", 'C_V: ', C_V_cu)
#print('C_V Mittelwert, STD: ', np.mean(C_V_cu), np.std(C_V_cu))

plt.clf()
plot(T(R_probe)[1:], noms(C_V_cu), r'$T_{Probe}$ $/$ K', r"$C_V(T)\cdot$ K $\cdot$ mol / J", [min(T(R_probe))-3, max(T(R_probe)) + 3], '../Plots/C_V.pdf', r"$C_V(T)$", "bx")

################## omega_debye bestimmen ##################

N_L = m_probe / M_cu * const.N_A
V = V_0 * m_probe / M_cu
v_long = Q_(4.7, 'km / s').to('m / s').magnitude
v_trans = Q_(2.26, 'km / s').to('m / s').magnitude

omega_debye = (18 * np.pi**2 * N_L / V / (1 / v_long**3 + 2 / v_trans**3))**(1 / 3)

T_debye = (Q_(const.hbar, 'J * s') * omega_debye / Q_(const.k, 'J / kelvin')).magnitude

print("\n", "###############################################################################",
"\n", "\n", 'omega_debye: ', omega_debye)
print('T_debye: ', T_debye)

################## Schlechte Werte rausnehmen ##################

for i in range(len(C_p_cu)):
    if C_p_cu[i] == max(C_p_cu):
        index_max = i
    elif C_p_cu[i] == min(C_p_cu):
        index_min = i

index_korrektur = np.array([index_max, index_min])
C_p_cu_korrektur = korrektur(C_p_cu_err, index_korrektur)
temp_korrektur = korrektur(T(R_probe)[1:], index_korrektur)

alpha_von_T_korrektur = korrektur(alpha_von_T[1:], index_korrektur)

C_V_cu_korrektur = C_v_cu(C_p_cu_korrektur, alpha_von_T_korrektur, temp_korrektur)

print("\n", "###############################################################################", "\n", "\n", 'C_V: ', C_V_cu_korrektur)
#print('C_V Mittelwert, STD: ', np.mean(C_V_cu_korrektur), np.std(C_V_cu_korrektur))

plt.clf()
plot(temp_korrektur, noms(C_p_cu_korrektur), r'$T_{Probe}$ / K', r"$C_p(T)\cdot$ K $\cdot$ mol / J", [min(temp_korrektur)-3, max(temp_korrektur) + 3], '../Plots/C_p_korrektur.pdf', r"$C_p(T)$", "bx")

plt.clf()
plot(T(R_probe)[1:], noms(C_V_cu), r'$T_{Probe}$ $/$ K', r"$C_V(T)\cdot$ K $\cdot$ mol / J", [min(T(R_probe))-3, max(T(R_probe)) + 3], '../Plots/C_V_korrektur.pdf', r"", "rx")
plot(temp_korrektur, noms(C_V_cu_korrektur), r'$T_{Probe}$ / K', r"$C_V(T)\cdot$ K $\cdot$ mol / J", [min(temp_korrektur)-3, max(temp_korrektur) + 3], '../Plots/C_V_korrektur.pdf', r"$C_V(T)$", "bx")

################## Debye-Temperatur bestimmen ##################

# nur T Werte bis 170K

T_probe_bis170K = Q_(T(R_probe)[T(R_probe)<=170], 'kelvin').magnitude

delta_T_probe_bis170K = T_probe_bis170K[1:] - T_probe_bis170K[:len(T_probe_bis170K) - 1]

C_V_cu_debye = C_V_cu[:len(T_probe_bis170K) - 1]

debye_experimentell = data.debye_tabelle * T_probe_bis170K[1:]
debye_err  = np.ones(len(data.debye_tabelle)) * 0.03 * T_probe_bis170K[1:]

print("\n", "###############################################################################", "\n", "\n", 'C_V: ', C_V_cu_debye)
print("\n", "###############################################################################", "\n", "\n", 'T: ', T_probe_bis170K)
print("\n", "###############################################################################", "\n", "\n", 'T_debye experimentell: ', debye_experimentell)
print('T_debye experimentell Mittelwert, STD: ', np.mean(debye_experimentell), np.std(debye_experimentell))
print('T_debye Abweichung: ', 1 - np.mean(debye_experimentell) / np.mean(T_debye))
print(f'T_debye Fehler: {debye_err}, {np.mean(debye_err)}')

np.average(debye_experimentell, weights=1 / debye_err)
print(np.average(debye_experimentell, weights=1 / debye_err))
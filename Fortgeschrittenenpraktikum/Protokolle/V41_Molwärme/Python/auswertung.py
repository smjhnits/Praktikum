import numpy as np
import matplotlib.pyplot as plt
import scipy.constants as const
from pint import UnitRegistry
from scipy.optimize import curve_fit
import scipy.integrate as integrate
import data
u = UnitRegistry()
Q_ = u.Quantity

################## Konstanten für Kupfer ##################

# Molmasse Wikipedia
M_cu = Q_(63.546 * const.N_A, 'dalton / mol').to('kg / mol')
# Probenmasse Versuchsanleitung
m_probe = Q_(342, 'g').to('kg')
# Molvolumen Wikipedia
V_0 = Q_(7.11 / 10**(6), 'm**3 / mol')
# Kompressionsmodul http://www.periodensystem-online.de/index.php?show=list&id=modify&prop=Kompressionsmodul&sel=oz&el=68
kappa = Q_(140, 'gigapascal').to('pascal')

################## Funktionen ##################

def poly_3(x, a, b, c, d):
    return a * x**3 + b * x**2 + c * x + d

def T(R):
    return 0.00134 * R**2 + 2.296 * R - 243.02 + 273.15

def C_p_cu(U, I, dt, dT):
    return M_cu / m_probe * (U * I * dt) / dT

def C_v_cu(C_p, alpha, T):
    return C_p - 9 * alpha**2 * kappa * V_0 * T

def korrektur(array, unit, index):
    for i in index:
        array = np.delete(array, i, None)
    return array * unit

def plot(x_array, y_array, x_label, y_label, x_lim, pfad, plot_label, graphstyle):
    plt.plot(x_array, y_array, graphstyle, label = plot_label)
    plt.xlim(x_lim)
    plt.xlabel(x_label, fontsize = 'large')
    plt.ylabel(y_label, fontsize = 'x-large')
    plt.legend(loc = 'best', fontsize = 'large')
    plt.savefig(pfad)

################## Daten einlesen ##################

R_probe = Q_(data.R_probe, "kiloohm").to('ohm')
R_zylinder = Q_(data.R_zylinder, 'kiloohm').to('ohm')

U = Q_((np.array(data.U[1:]) + np.array(data.U[:len(data.U) - 1])) / 2, 'volt')
I = Q_((np.array(data.I[1:]) + np.array(data.I[:len(data.I) - 1])) / 2, 'milliampere').to('ampere')

time = Q_(np.array(data.time_min) * 60 + np.array(data.time_sec), 's')

delta_t = Q_(time.magnitude[1:] - time.magnitude[:len(time.magnitude) - 1], 's')

delta_T_probe = Q_(T(R_probe.magnitude[1:] - R_probe.magnitude[:len(R_probe.magnitude) - 1]), 'kelvin')
delta_T_zylinder = Q_(T(R_zylinder.magnitude[1:] - R_zylinder.magnitude[:len(R_zylinder.magnitude) - 1]), 'kelvin')

################## C_p bestimmen ##################

C_p_cu = Q_(C_p_cu(U.magnitude, I.magnitude, delta_t.magnitude, delta_T_probe.magnitude).magnitude, 'volt * ampere * s / kelvin / mol').to('joule / kelvin / mol')

print("\n", "###############################################################################", "\n", "\n",'C_p Mittelwert, STD: ', np.mean(C_p_cu), np.std(C_p_cu))
print('C_p: ', C_p_cu)

plt.clf()
plot(T(R_probe.magnitude)[1:], C_p_cu, r'T $\cdot$ K', r"$C_p(T)\cdot$ K $\cdot$ mol / J", [min(T(R_probe.magnitude))-3, max(T(R_probe.magnitude)) + 3], '../Plots/C_p.pdf', r"$C_p(T)$", "bx")

################## C_V bestimmen ##################
# Dafür erst alpha(T) bestimmen
# alpha = list(alpha, T)

params_alpha, cov_alpha = curve_fit(poly_3, np.array(data.alpha[1]), np.array(data.alpha[0]))

x_min = 65
x_max = 305
x = np.linspace(x_min, x_max)

plt.clf()
plot(data.alpha[1], data.alpha[0], r'T $\cdot$ K', r"$\alpha\cdot 10^{-6} \cdot$K", [x_min, x_max], '../Plots/alpha_T.pdf', "Gegebene Daten", "bx")
plot(x, poly_3(x, *params_alpha), r'T $\cdot$ K', r"$\alpha\cdot 10^{-6} \cdot$K", [x_min, x_max], '../Plots/alpha_T.pdf', "Fit", 'r-')


alpha_von_T = Q_(poly_3(T(R_probe.magnitude), *params_alpha) / 10**6, '1 / kelvin')


C_V_cu = C_v_cu(C_p_cu, alpha_von_T[1:], Q_(T(R_probe.magnitude)[1:], 'kelvin'))

print("\n", "###############################################################################", "\n", "\n", 'C_V: ', C_V_cu)
print('C_V Mittelwert, STD: ', np.mean(C_V_cu), np.std(C_V_cu))

plt.clf()
plot(T(R_probe.magnitude)[1:], C_V_cu, r'T $\cdot$ K', r"$C_V(T)\cdot$ K $\cdot$ mol / J", [min(T(R_probe.magnitude))-3, max(T(R_probe.magnitude)) + 3], '../Plots/C_V.pdf', r"$C_V(T)$", "bx")


################## omega_debye bestimmen ##################

N_L = m_probe / M_cu * const.N_A * u('1 / mol')
V = V_0 * m_probe / M_cu
v_long = Q_(4.7, 'km / s').to('m / s')
v_trans = Q_(2.26, 'km / s').to('m / s')

omega_debye = (18 * np.pi**2 * N_L / V / (1 / v_long**3 + 2 / v_trans**3))**(1 / 3)

T_debye = Q_(const.hbar, 'J * s') * omega_debye / Q_(const.k, 'J / kelvin')

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
C_p_cu_korrektur = korrektur(C_p_cu.magnitude, C_p_cu.units, index_korrektur).to('joule / kelvin / mol')
temp_korrektur = korrektur(T(R_probe.magnitude)[1:], u('kelvin'), index_korrektur)

alpha_von_T_korrektur = korrektur(alpha_von_T[1:].magnitude, alpha_von_T.units, index_korrektur)

C_V_cu_korrektur = C_v_cu(C_p_cu_korrektur, alpha_von_T_korrektur, temp_korrektur).to('joule / kelvin / mol')

print("\n", "###############################################################################", "\n", "\n", 'C_V: ', C_V_cu_korrektur)
print('C_V Mittelwert, STD: ', np.mean(C_V_cu_korrektur), np.std(C_V_cu_korrektur))

plt.clf()
plot(temp_korrektur.magnitude, C_p_cu_korrektur.magnitude, r'T $\cdot$ K', r"$C_p(T)\cdot$ K $\cdot$ mol / J", [min(temp_korrektur.magnitude)-3, max(temp_korrektur.magnitude) + 3], '../Plots/C_p_korrektur.pdf', r"$C_p(T)$", "bx")

plt.clf()
plot(temp_korrektur.magnitude, C_V_cu_korrektur.magnitude, r'T $\cdot$ K', r"$C_p(T)\cdot$ K $\cdot$ mol / J", [min(temp_korrektur.magnitude)-3, max(temp_korrektur.magnitude) + 3], '../Plots/C_V_korrektur.pdf', r"$C_V(T)$", "bx")

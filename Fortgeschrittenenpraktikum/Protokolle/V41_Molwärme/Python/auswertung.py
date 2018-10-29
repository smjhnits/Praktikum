import numpy as np
import matplotlib.pyplot as plt
import scipy.constants as const
from pint import UnitRegistry
from scipy.optimize import curve_fit
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

print('C_p Mittelwert, STD: ', np.mean(C_p_cu), np.std(C_p_cu))
print('C_p: ', C_p_cu)

################## C_V bestimmen ##################
# Dafür erst alpha(T) bestimmen
# alpha = list(alpha, T)

params_alpha, cov_alpha = curve_fit(poly_3, np.array(data.alpha[1]), np.array(data.alpha[0]))

x_min = 65
x_max = 305
x = np.linspace(x_min, x_max)

plt.clf()
plt.plot(data.alpha[1], data.alpha[0], "bx", label = "Gegebene Daten")
plt.plot(x, poly_3(x, *params_alpha), 'r-', label = 'Fit')
plt.xlim(x_min, x_max)
plt.xlabel(r'T $\cdot$ K', fontsize = 'large')
plt.ylabel(r"$\alpha\cdot 10^{-6} \cdot$K", fontsize = 'x-large')
plt.legend(loc = 'best', fontsize = 'large')
plt.savefig('../Plots/alpha_T.pdf')

alpha_von_T = Q_(poly_3(T(R_probe.magnitude), *params_alpha) / 10**6, '1 / kelvin')

C_V_cu = C_v_cu(C_p_cu, alpha_von_T[:len(alpha_von_T) - 1], Q_(T(R_probe.magnitude)[:len(T(R_probe.magnitude)) - 1], 'kelvin'))

print('C_V: ', C_V_cu)
print('C_V Mittelwert, STD: ', np.mean(C_V_cu), np.std(C_V_cu))

plt.clf()
plt.plot(T(R_probe.magnitude)[:len(T(R_probe.magnitude)) - 1], C_V_cu, "bx", label = r"$C_V(T)$")
plt.xlim(min(T(R_probe.magnitude))-3, max(T(R_probe.magnitude)) + 3)
plt.xlabel(r'T $\cdot$ K', fontsize = 'large')
plt.ylabel(r"$C_V(T)\cdot$ K $\cdot$ mol / J", fontsize = 'x-large')
plt.legend(loc = 'best', fontsize = 'large')
plt.savefig('../Plots/C_V.pdf')

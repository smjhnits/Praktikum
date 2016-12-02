import numpy as np
from scipy.optimize import curve_fit
import scipy.constants as const

c_V_Vergleich = 3 * const.gas_constant
c_w = 4.18
m_Graphit = 247.79 - 139.77
m_Blei2 = 526.29 - 140.45
m_Kupfer = 379.00 - 140.05

U = np.array([0.0, 3.88])
T = np.array([0.0, 100.0])


def f(x, A, B):
    return A * x + B

params, covariance = curve_fit(f, U, T)


def Kalorimeter(m_x, m_y, T_x, T_y, T_m):
    return ((c_w * m_y * (T_y - T_m) - c_w * m_x * (T_m - T_x)) / (T_m - T_x))


def Wärmekapazität(m_w, m_k, T_m, T_w, T_k, c_gm_g):
    return ((c_w * m_w + c_gm_g) * (T_m - T_w)) / (m_k * (T_k - T_m))


def FehlerTemp(U):
    return np.sqrt(np.diag(covariance))[0] * U + np.sqrt(np.diag(covariance))[1]


def Temp(U):
    return params[0] * U + params[1] + 273.15

cgmg = Kalorimeter(278.97, 298.98, Temp(0.82), Temp(3.16), Temp(1.91))

graphit = np.array([Wärmekapazität(772.50, m_Graphit, Temp(0.89), Temp(0.80), Temp(4.04), cgmg), Wärmekapazität(772.50, m_Graphit, Temp(1.03), Temp(0.94), Temp(3.93), cgmg), Wärmekapazität(772.50, m_Graphit, Temp(1.14), Temp(1.04), Temp(3.97), cgmg)])

blei2 = np.array([Wärmekapazität(765.89, m_Blei2, Temp(0.92), Temp(0.86), Temp(3.82), cgmg), Wärmekapazität(765.89, m_Blei2, Temp(0.98), Temp(0.92), Temp(3.73), cgmg), Wärmekapazität(765.89, m_Blei2, Temp(1.04), Temp(0.98), Temp(3.78), cgmg)])

kupfer = Wärmekapazität(769.56, m_Kupfer, Temp(0.84), Temp(0.80), Temp(4.06), cgmg)

print('Spezifische Wärmekapazität des Kalorimeters: ', Kalorimeter(278.97, 298.98, Temp(0.82), Temp(3.16), Temp(1.91)))
print('Temperaturen: ', 'T_x = ', Temp(0.82), 'T_y = ', Temp(3.16), 'T_m = ', Temp(1.91))
# print('Fehler: ', Kalorimeter(278.97, 298.98, FehlerTemp(0.82), FehlerTemp(3.16), FehlerTemp(1.91)))
print('Spezifische Wärmekapazität von Graphit: ', np.mean(graphit))
print('Fehler: ', np.std(graphit, ddof=1) / np.sqrt(len(graphit)))
print('C_p: ', np.mean(graphit) * 12)
print('Fehler: ', 12 * np.std(graphit, ddof=1) / np.sqrt(len(graphit)))
print('Temperaturen1: ', Temp(0.80), Temp(4.04), Temp(0.89))
print('Temperaturen2: ', Temp(0.94), Temp(3.93), Temp(1.03))
print('Temperaturen3: ', Temp(1.04), Temp(3.97), Temp(1.14))
print('Spezifische Wärmekapazität von Blei2: ', np.mean(blei2))
print('Fehler: ', np.std(blei2, ddof=1) / np.sqrt(len(blei2)))
print('C_p: ', np.mean(blei2) * 207.2)
print('Fehler: ', 207.2 * np.std(blei2, ddof=1) / np.sqrt(len(blei2)))
print('Temperaturen1: ', Temp(0.86), Temp(3.82), Temp(0.92))
print('Temperaturen2: ', Temp(0.92), Temp(3.73), Temp(0.98))
print('Temperaturen3: ', Temp(0.98), Temp(3.78), Temp(1.04))
print('Spezifische Wärmekapazität von Kupfer: ', kupfer)
print('C_p: ', np.mean(kupfer) * 63.5)
print('Temperaturen: ', Temp(0.80), Temp(4.06), Temp(0.84))


def Molaresvolumen(M, Dichte):
    return M / (Dichte * 10**6)


def c_V(c_p, alpha, kappa, Molvolumen, T):
    return (c_p - 9 * (alpha * 10**(-6))**2 * kappa * 10**(9) * Molvolumen * T)

cV_graphit = np.array([c_V(12 * np.mean(graphit), 8, 33, Molaresvolumen(12, 2.25), Temp(0.89)), c_V(12 * np.mean(graphit), 8, 33, Molaresvolumen(12, 2.25), Temp(1.03)), c_V(12 * np.mean(graphit), 8, 33, Molaresvolumen(12, 2.25), Temp(1.14))])

cV_blei2 = np.array([c_V(207.2 * np.mean(blei2), 29, 42, Molaresvolumen(207.2, 11.35), Temp(0.92)), c_V(207.2 * np.mean(blei2), 29, 42, Molaresvolumen(207.2, 11.35), Temp(0.98)), c_V(207.2 * np.mean(blei2), 29, 42, Molaresvolumen(207.2, 11.35), Temp(1.04))])

cV_kupfer = c_V(63.5 * kupfer, 16.8, 136, Molaresvolumen(63.5, 8.95), Temp(0.84))

print('cV von Graphit: ', np.mean(cV_graphit))
print('Fehler: ', np.std(cV_graphit, ddof=1) / np.sqrt(len(cV_graphit)))
print('cV von Blei2: ', np.mean(cV_blei2))
print('Fehler: ', np.std(cV_blei2, ddof=1) / np.sqrt(len(cV_blei2)))
print('cV von Kupfer: ', np.mean(cV_kupfer))
print('Ausgleichgerade der Temperatur: ', *params)
print('3R: ', c_V_Vergleich)

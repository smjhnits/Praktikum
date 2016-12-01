import numpy as np
from scipy.optimize import curve_fit

c_w = 4.18
m_Graphit = 208.02
m_Blei2 = 385.84
m_Kupfer = 238.95

U = np.array([0.0, 3.88])
T = np.array([0.0, 100.0])


def f(x, A, B):
    return A * x + B

params, covariance = curve_fit(f, U, T)

x_plot = np.linspace(0, 4, 1000)


def Molaresvolumen(Dichte, M, masse):
    return masse * M / Dichte


def c_V(c_p, alpha, kappa, Molvolumen, T):
    return c_p - 9 * alpha**2 * kappa * Molvolumen * T


def Kalorimeter(m_x, m_y, T_x, T_y, T_m):
    return (c_w * m_y * (T_y - T_m) - c_w * m_x * (T_m - T_x)) / (T_m - T_x)


def Wärmekapazität(m_w, m_k, T_m, T_w, T_k, c_gm_g):
    return ((c_w * m_w + c_gm_g) * (T_m - T_w)) / (m_k(T_k - T_m))


def FehlerTemp(T):
    return np.sqrt(np.diag(covariance))[0] * T + np.sqrt(np.diag(covariance))[1]

print('Spezifische Wärmekapazität des Kalorimeters: ', Kalorimeter(278.97, 298.98, params[0] * 0.82 + params[1], params[0] * 3.16 + params[1], params[0] * 1.91 + params[1]))
print('Fehler: ', FehlerTemp())

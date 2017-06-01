import numpy as np
from scipy.stats import sem
from uncertainties import ufloat
import uncertainties.unumpy as unp
import matplotlib.pyplot as plt
import scipy.constants as sc
from scipy.optimize import curve_fit

#Auswertung der x-Achsen

M_A_27_x = np.array([19, 40, 61, 81, 103, 123, 143, 164, 185, 208, 228])
M_A_27_y = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])

M_A_144_x = np.array([20, 43, 64, 84, 104, 126, 146, 168, 189, 211, 229])
M_A_144_y = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])

M_B_186_x = np.array([18, 39, 57, 75, 91, 110, 128, 146, 165, 184, 205, 215])
M_B_186_y = np.array([5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 57])

M_C_107_x = np.array([19, 43, 64, 85, 104, 121, 142, 163, 183, 201, 221, 132])
M_C_107_y = np.array([5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 57])

def f(x, A, B):
    return A*x + B

ParamsA_1, covarianceA_1 = curve_fit(f, M_A_27_x, M_A_27_y)
errorsA_1 = np.sqrt(np.diag(covarianceA_1))
MessungA_1 = ufloat(ParamsA_1[0], errorsA_1[0])

ParamsA_2, covarianceA_2 = curve_fit(f, M_A_144_x, M_A_144_y)
errorsA_2 = np.sqrt(np.diag(covarianceA_2))
MessungA_2 = ufloat(ParamsA_2[0], errorsA_2[0])

ParamsB, covarianceB = curve_fit(f, M_B_186_x, M_B_186_y)
errorsB = np.sqrt(np.diag(covarianceB))
MessungB = ufloat(ParamsB[0], errorsB[0])

ParamsC, covarianceC = curve_fit(f, M_C_107_x, M_C_107_y)
errorsC = np.sqrt(np.diag(covarianceC))
MessungC = ufloat(ParamsC[0], errorsC[0])

print("Steigung und Fehler für Messung a) bei 27 °C: ", MessungA_1)
print("Steigung und Fehler für Messung a) bei 144 °C: ", MessungA_2)
print("Steigung und Fehler für Messung b) bei 107 °C: ", MessungB,)
print("Steigung und Fehler für Messung c) bei 186 °C: ", MessungC, '\n')

#Auswertung der Temnperaturen für die mittlere freie Weglänge

def p_saet(T):
    return 5.5 * 10**7 * np.exp(-6876/T)

T_A_1 = 27  + 273.15
T_A_2 = 144 + 273.15
T_B   = 186 + 273.15
T_C   = 107 + 273.15

w_A_1 = 0.0029 / p_saet(T_A_1)
w_A_2 = 0.0029 / p_saet(T_A_2)
w_B   = 0.0029 / p_saet(T_B)
w_C   = 0.0029 / p_saet(T_C)

print("Die mittlere freie Weglänge für Messung a) bei 27 °C in cm: ", w_A_1)
print("Die mittlere freie Weglänge für Messung a) bei 144 °C in cm: ", w_A_2)
print("Die mittlere freie Weglänge für Messung b) bei 186 °C in cm: ", w_B)
print("Die mittlere freie Weglänge für Messung a) bei 107 °C in cm: ", w_C, '\n')

# Bestimmung der Steigungen bei Messung a) bei Raumtemperatur

M_A27_x = np.array([1, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130,
                    140, 146, 152, 157, 162, 164, 166, 168, 170, 172, 174, 176,
                    178, 185, 195, 206]) * 0.04792

M_A27_y = np.array([3, 2, 2.5, 2, 2, 1.5, 2, 2, 1.5, 1.5, 1.5, 1.5, 1, 1, 1, 1.5,
                    1, 1, 1, 1, 1.5, 2, 2, 2, 1.5, 1, 1, 0, 0, 0])/ParamsA_1[0]

plt.clf()
plt.plot(M_A27_x, M_A27_y/2, 'k--', label = r'Abgelesene Steigungswerte des Auffängerstroms bei 27 °C')
plt.plot(M_A27_x, M_A27_y/2, 'rx')
plt.legend(loc = 'best')
plt.xlabel(r'$U$ in $\mathrm{V}$')
plt.ylabel(r'$\frac{N}{U}$ in $\frac{1}{\mathrm{V}}$')
plt.xlim(0, 10)
#plt.ylim(-0.5, 2)
plt.show()

# Bestimmung der Steigung bei Messung b) bei Raumtemperatur

M_A144_x = np.array([4, 8, 12, 18, 22, 28, 32, 36, 40, 44, 47, 51, 54, 57, 60, 64,
                   67, 69, 71, 73, 75, 77, 79, 81, 83, 85, 87, 95, 106]) * 0.04778
M_A144_y = np.array([6, 5, 6, 4, 5, 4, 5, 3, 4, 3, 3, 3, 2, 2, 1.5, 2.5, 2, 1, 1,
                    1, 1, 1, 0, 0, 0, 0, 0, 0, 0])/ParamsA_2[0]
plt.clf()
plt.plot(M_A144_x, M_A144_y/2, 'k--', label = r'Abgelesene Steigungswerte des Auffängerstroms bei 144 °C')
plt.plot(M_A144_x, M_A144_y/2, 'rx')
plt.legend(loc = 'best')
plt.xlabel(r'$U$ in $\mathrm{V}$')
plt.ylabel(r'$\frac{N}{U}$ in $\frac{1}{\mathrm{V}}$')
plt.xlim(0, 5.3)
#plt.ylim(-0.5, 4)
plt.show()

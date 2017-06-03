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

M_C_107_x = np.array([19, 43, 64, 85, 104, 121, 142, 163, 183, 201, 221, 232])
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

#print("Steigung und Fehler für Messung a) bei 27 °C: ", MessungA_1)
#print("Steigung und Fehler für Messung a) bei 144 °C: ", MessungA_2)
#print("Steigung und Fehler für Messung b) bei 107 °C: ", MessungB,)
#print("Steigung und Fehler für Messung c) bei 186 °C: ", MessungC, '\n')

#Auswertung der Temnperaturen für die mittlere freie Weglänge

a = 1

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

#print("Sättigungsdruck Messung a) bei 27°C: ", p_saet(T_A_1))
#print("Sättigungsdruck Messung a) bei 144°C: ", p_saet(T_A_2))
#print("Sättigungsdruck Messung b) bei 186°C: ", p_saet(T_B))
#print("Sättigungsdruck Messung c) bei 107°C: ", p_saet(T_C), '\n')


#print("Die mittlere freie Weglänge für Messung a) bei 27 °C in cm: ", w_A_1)
#print("Die mittlere freie Weglänge für Messung a) bei 144 °C in cm: ", w_A_2)
#print("Die mittlere freie Weglänge für Messung b) bei 186 °C in cm: ", w_B)
#print("Die mittlere freie Weglänge für Messung c) bei 107 °C in cm: ", w_C, '\n')

#print("Verhältniss a/w für Messung a) bei 27 °C in cm: ", a/w_A_1)
#print("Verhältniss a/w für Messung a) bei 144 °C in cm: ", a/w_A_2)
#print("Verhältniss a/w für Messung b) bei 186 °C in cm: ", a/w_B)
#print("Verhältniss a/w für Messung c) bei 107 °C in cm: ", a/w_C, '\n')

# Bestimmung der Steigungen bei Messung a) bei Raumtemperatur

M_A27_x = np.array([1, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130,
                    140, 146, 152, 157, 162, 164, 166, 168, 170, 172, 174, 176,
                    178, 185, 195, 206]) * ParamsA_1[0]
M_A27_y = np.array([3, 2, 2.5, 2, 2, 1.5, 2, 2, 1.5, 1.5, 1.5, 1.5, 1, 1, 1, 1.5,
                    1, 1, 1, 1, 1.5, 2, 2, 2, 1.5, 1, 1, 0, 0, 0])/ParamsA_1[0]

#print("M_A27_X: ", M_A27_x, '\n')
#print("M_A27_y: ", M_A27_y, '\n')

plt.clf()
#plt.plot(M_A27_x, M_A27_y/2, 'k--', label = r'Abgelesene Steigungswerte des Auffängerstroms bei 27 °C')
plt.plot(M_A27_x, M_A27_y/2, 'rx', label = r'Steigungswerte von $I_{\mathrm{A}}$ bei 27 °C')
plt.legend(loc = 'best')
plt.xlabel(r'$U$ in $\mathrm{V}$')
plt.ylabel(r'$\frac{N}{U}$ in $\frac{1}{\mathrm{V}}$')
plt.xlim(0, 10)
plt.ylim(-2, 35)
#plt.show()
#plt.savefig('Messung_A_27.pdf')

Kontakt_A = 11 - 170 * 0.04792

print("Das Kontaktpotential nach Messung a) beträgt ca. :", Kontakt_A, '\n')

# Bestimmung der Steigung bei Messung a) bei 144 °C

M_A144_x = np.array([4, 8, 12, 18, 22, 28, 32, 36, 40, 44, 47, 51, 54, 57, 60, 64,
                   67, 69, 71, 73, 75, 77, 79, 81, 83, 85, 87, 95, 106]) * ParamsA_2[0]
M_A144_y = np.array([6, 5, 6, 4, 5, 4, 5, 3, 4, 3, 3, 3, 2, 2, 1.5, 2.5, 2, 1, 1,
                    1, 1, 1, 0, 0, 0, 0, 0, 0, 0])/ParamsA_2[0]

#print("M_A144_X: ", M_A144_x, '\n')
#print("M_A144_X: ", M_A144_y, '\n')

plt.clf()
#plt.plot(M_A144_x, M_A144_y/2, 'k--', label = r'Abgelesene Steigungswerte des Auffängerstroms bei 144 °C')
plt.plot(M_A144_x, M_A144_y/2, 'rx',  label = r'Steigungswerte von $I_{\mathrm{A}}$ bei 144 °C')
plt.legend(loc = 'best')
plt.xlabel(r'$U$ in $\mathrm{V}$')
plt.ylabel(r'$\frac{N}{U}$ in $\frac{1}{\mathrm{V}}$')
plt.xlim(0, 5.3)
plt.ylim(-2, 70)
#plt.show()
#plt.savefig("Messung_A_144.pdf")

# Bestimmung der Energiedifferenz E1 - E0 Messung b)

M_B_Abstaende = np.array([19, 19, 18 , 19, 21, 19, 19]) * ParamsB[0]

print("Abstaende der Maxima: ", M_B_Abstaende, )

Mittelwert = np.mean(M_B_Abstaende)
Abweichung = 1/len(M_B_Abstaende) * np.std(M_B_Abstaende, ddof = 1)

Differenz = ufloat(Mittelwert, Abweichung)

print("Die berechnete Energiedifferenz beträgt: ", Differenz)

Frequenz = Differenz * sc.e / sc.h
Lambda = sc.c / Frequenz

print("Die berechnete Wellenlänge ist beträgt: ", Lambda)

Kontakt_B = 46 * ParamsB[0] - 2 * Differenz

print("Das Kontaktpotential nach Messung b) liegt bei:", Kontakt_B, '\n')

# Bestimmung der Ionisierungsspannung bei Messung c)

M_C_x = np.array([20, 50, 80, 110, 140, 170, 199, 230]) * ParamsC[0]
M_C_y = np.array([0, 0, 1, 9, 25, 50, 81, 127])

print(M_C_x)

def g(x, A, B):
    return A*x + B

Params_C_Messung, covariance_C_Messung = curve_fit(g, M_C_x, M_C_y)
errors_C_Messung = np.sqrt(np.diag(covariance_C_Messung))

xplot = np.linspace(0, 350, 1000) * ParamsC[0]

#Steigung_C = ufloat(Params_C_Messung[0], errors_C_Messung[0])
#Abschnitt_C = ufloat(Params_C_Messung[1], errors_C_Messung[1])
Steigung_C = Params_C_Messung[0]
Abschnitt_C = Params_C_Messung[1]

Nullstelle = - Abschnitt_C / Steigung_C

plt.clf()
plt.plot(M_C_x, M_C_y, 'rx', label = 'Messwerte')
plt.plot(xplot, f(xplot, *Params_C_Messung), 'b-', label = 'lineare Regression')
plt.plot(xplot, np.zeros(1000), 'k-')
#plt.plot(unp.nominal_values(Nullstelle), 0, 'ro')
plt.plot(Nullstelle, 0, 'ro')
plt.ylabel(r'$N_{\mathrm{y}}$ in $\mathrm{mm}$')
plt.xlabel(r'$U$ in $\mathrm{V}$')
plt.legend(loc = 'best')
plt.ylim(-15, 150)
plt.xlim(0, 70)
#plt.show()
#plt.savefig('Ionisationsspannung.pdf')


print("Nullstelle des Graphen bei: ", Nullstelle, '\n')

UI_1 = Nullstelle - Kontakt_A
UI_2 = Nullstelle - Kontakt_B

print("Ionisierungsspannung für das Kontaktpotenzial aus Messung a): ", UI_1)
print("Ionisierungsspannung für das Kontaktpotenzial aus Messung b): ", UI_2)

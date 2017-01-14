import numpy as np
from scipy.stats import sem
from uncertainties import ufloat
import uncertainties.unumpy as unp
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

L   = 32.51 * 10 ** (-3)
C   = 0.801 * 10 ** (-9)
Csp = 0.037 * 10 ** (-9)
R = 48

print("Verwendete Komponenten: ", '\n', "L= ", L, '\n', "C= ", C, '\n', "Csp = ", Csp, '\n', "R= ", R, '\n')

#L = ufloat(32.51 * 10 ** (-3), 0.01 * 10 ** (-3))
#C = ufoat(0.801 * 10 ** (-9), 0.001 * 10 ** (-9))
#Csp = ufloat(0.037 * 10 ** (-9), 0.001 * 10 ** (-9))

Kopplungskapazitäten = np.array([9.99, 8, 6.47, 5.02, 4.00, 3.00, 2.03, 1.01]) * 10 ** (-9)
Maxima = np.array([14, 12, 10, 8, 6, 5, 4])
Anzahl_Maxima = np.array([ufloat(n, 1) for n in Maxima])
Resonanzfrequenz = 31.10 * 10 ** (3)

Nü_negativ = np.array([33.16, 33.66, 34.25, 35.12, 36.08, 37.60, 40.28, 47.33]) * 10 ** (3)
Nü_positiv = np.array([30.77, 30.79, 30.80, 30.81, 30.82, 30.83, 30.84, 30.85]) * 10 ** (3)

Start = np.array([30.85, 30.84, 30.83, 30.82, 30.81, 30.80, 30.79, 30.77]) * 10 ** (3)
Stop = np.array([55.05, 50, 40, 40, 40, 40, 40, 40]) * 10 ** (3)
Sweep_Zeit = 2
Zeiten = np.array([1.36, 1, 1.475, 1.125, 0.925, 0.740, 0.6, 0.5])

C_K_Error = np.array([ufloat(n, 0.003*n) for n in Kopplungskapazitäten])

Nu_p_gemessen = 31100

print("Kapazitäten mit Fehler: ", '\n', C_K_Error, '\n')

#Abweichung gemessenes Nu+ und theroretischer Wert

nu_p_theo = 1 / ( 2 * np.pi * np.sqrt( L * ( C + Csp) ) )
print("Die Abweichung von gemessenem zu berechnetem Wert: ", Nu_p_gemessen/nu_p_theo, '\n')

# Bestimmung des Verhältnisses Schwingung/ Schwebung

Messfrequenz = 305.1

# Theoretisches Verhältnisses

nu_m_theo = np.array([1 / ( 2 * np.pi * unp.sqrt( L * ( (1/C + 2/n)**(-1) + Csp) ) ) for n in C_K_Error])

print("Theoretische Wert für nu+: ", nu_p_theo, '\n')
print("Theoretische Werte für nu-: ", nu_m_theo, '\n')

Verhältniss_theo = (nu_p_theo + nu_m_theo) / ( 2 * (nu_m_theo - nu_p_theo))

print("Experimentell bestimmte Verhältnisse: ", '\n', Anzahl_Maxima, '\n')
print("Theoretisch bestimmte Verhältnisse: ", Verhältniss_theo, '\n')

Abweichungen = (Anzahl_Maxima - Verhältniss_theo[:7]) / Anzahl_Maxima

print("Abweichungen der Verhältnisse: ", '\n', Abweichungen, '\n')

# Vergleich der gemessenen Frequenzen mit den berechneten Werten

Abweichungen_m = np.array([ (n - nu_m_theo[i])/n  for i,n in enumerate(Nü_negativ)])
Abweichungen_p = np.array([ (n - nu_p_theo)/n for n in Nü_positiv])

print("Abweichungen nu+: ", Abweichungen_p, '\n')
print("Abweichungen nu-: ", Abweichungen_m, '\n')

# Messung mit der Sweep Methode

Differenzen = np.array([ Stop[i]-n for i,n in enumerate(Start)])
Zeitverhältniss = np.array([n/Sweep_Zeit for n in Zeiten])

Abstände = np.array([Differenzen[i]*n for i,n in enumerate(Zeitverhältniss)])

nu_m_expC = np.array([n + Abstände[i] for i,n in enumerate(Start)])
Abweichungen_Sweep = np.array([ (n - nu_m_theo[7-i])/n  for i,n in enumerate(nu_m_expC)])

print("Berechnete Abstände: ", Abstände, '\n')
print("Mit der Sweep-Methode berechnete Werte für nu-: ", nu_m_expC, '\n')
print("Abweichungen nu-: ", Abweichungen_Sweep, '\n')

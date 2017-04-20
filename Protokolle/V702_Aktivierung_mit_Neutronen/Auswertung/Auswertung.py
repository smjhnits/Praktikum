import numpy as np
from scipy.stats import sem
from uncertainties import ufloat
import uncertainties.unumpy as unp
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def Mean_Std(Werte):
    s = 1/np.sqrt(len(Werte))
    return ufloat(np.mean(Werte), s * np.std(Werte, ddof = 1))

#Dunkelmessung

dt_vormessung = 900
DM = np.array([218, 224])
DM_W = Mean_Std(DM)

DM_indium = unp.nominal_values(DM_W) * (240/900)
DM_rhodium = unp.nominal_values(DM_W) * (20/900)

#Indium

Zeiten_Indium = np.linspace(240, 3600, 15)
dt_indium = 240
tge_indium = 3600
Werte_Indium = np.array([2995, 2485, 2465, 2346, 2345, 2268, 2076, 1943, 1894,
                         1827, 1686, 1555, 1525, 1512, 1417])

Werte_Indium_korrigiert = Werte_Indium - DM_indium

Werte_I_Fehler = np.array([np.sqrt(n) for n in Werte_Indium_korrigiert])

Werte_I_log = np.array([np.log(n) for n in Werte_Indium_korrigiert])

Fehler_I_log_plus = np.array([np.log(n + Werte_I_Fehler[i]) - np.log(n) for i,n in enumerate(Werte_Indium_korrigiert)])
Fehler_I_log_minus = np.array([np.log(n + Werte_I_Fehler[i]) - np.log(n) for i,n in enumerate(Werte_Indium_korrigiert)])

Fehler_I_log = np.array([Fehler_I_log_minus, Fehler_I_log_plus])

def f(x, a, b):
    return a * x + b

params, covariance = curve_fit(f, Zeiten_Indium, Werte_I_log)

plt.errorbar( Zeiten_Indium, Werte_I_log,  yerr=Fehler_I_log, fmt='x')
plt.plot(Zeiten_Indium, f(Zeiten_Indium, *params), 'b-', label='linearer Fit', linewidth=0.3)
plt.savefig('Indium_log.pdf')

plt.clf()
plt.errorbar( Zeiten_Indium, Werte_Indium_korrigiert,  Werte_I_Fehler, fmt='x')
plt.plot(Zeiten_Indium, np.exp(params[1])*np.exp(params[0]*Zeiten_Indium), 'r-')
plt.savefig('Indium_normal.pdf')

#Rhodium

Zeiten_rhodium = np.linspace(15, 720, 48)
dt_rhodium = 20
tge_rhodium = 900
Werte_Rhodium = np.array([630, 517, 445, 330, 265, 212, 192, 176,
                          152, 116,  99,  98,  92,  64,  55,  60,
                           55,  61,  51,  51,  33,  40,  48,  28,
                           32,  35,  33,  25,  22,  29,  18,  27,
                           22,  22,  25,  25,  22,  20,  22,  23,
                           24,  23,  12,  21,  19,  18,  15,  14 ])

Werte_Rhodium_korrigiert = Werte_Rhodium - DM_rhodium
Werte_R_Fehler = np.array([np.sqrt(n) for n in Werte_Rhodium_korrigiert])

#Rhodium linker Teil

Werte_R_links_korrigiert = Werte_Rhodium_korrigiert[0:5]
Zeiten_R_links = Zeiten_rhodium[0:5]
Werte_R_links_Fehler = Werte_R_Fehler[0:5]
Werte_R_links_log = np.array([np.log(n) for n in Werte_R_links_korrigiert])
Fehler_R_links_log_plus = np.array([np.log(n + Werte_R_links_Fehler[i]) - np.log(n) for i,n in enumerate(Werte_R_links_korrigiert)])
Fehler_R_links_log_minus = np.array([np.log(n + Werte_R_links_Fehler[i]) - np.log(n) for i,n in enumerate(Werte_R_links_korrigiert)])

Fehler_R_links_log = np.array([Fehler_R_links_log_minus, Fehler_R_links_log_plus])

params, covariance = curve_fit(f, Zeiten_R_links, Werte_R_links_log)

N_0_Rhodium_links = params[1]
Lamba_Rhodium_links = -params[0]

plt.clf()
plt.errorbar( Zeiten_R_links, Werte_R_links_log,  yerr=Fehler_R_links_log, fmt='x')
plt.plot(Zeiten_R_links, f(Zeiten_R_links, *params), 'b-', label='linearer Fit', linewidth=0.3)
plt.savefig('Rhodium_links_log.pdf')

Fit_X_Rhodium_links = np.linspace(15, 75, 1000)

plt.clf()
plt.errorbar( Zeiten_R_links, Werte_R_links_korrigiert,  Werte_R_links_Fehler, fmt='x')
plt.plot(Fit_X_Rhodium_links, np.exp(N_0_Rhodium_links)*np.exp(-Lamba_Rhodium_links*Fit_X_Rhodium_links), 'r-')
plt.savefig('Rhodium_normal_links.pdf')

#Rhodium rechter Teil

Werte_R_rechts_korrigiert = Werte_Rhodium_korrigiert[23:49]
Zeiten_R_rechts = Zeiten_rhodium[23:49]
Werte_R_rechts_Fehler = Werte_R_Fehler[23:49]
Werte_R_rechts_log = np.array([np.log(n) for n in Werte_R_rechts_korrigiert])
Fehler_R_rechts_log_plus = np.array([np.log(n + Werte_R_rechts_Fehler[i]) - np.log(n) for i,n in enumerate(Werte_R_rechts_korrigiert)])
Fehler_R_rechts_log_minus = np.array([np.log(n + Werte_R_rechts_Fehler[i]) - np.log(n) for i,n in enumerate(Werte_R_rechts_korrigiert)])

Fehler_R_rechts_log = np.array([Fehler_R_rechts_log_minus, Fehler_R_rechts_log_plus])

params, covariance = curve_fit(f, Zeiten_R_rechts, Werte_R_rechts_log)

N_0_Rhodium_rechts = params[1]
Lamba_Rhodium_rechts = -params[0]

Fit_X_Rhodium_rechts = np.linspace(360, 720, 1000)

plt.clf()
plt.errorbar( Zeiten_R_rechts, Werte_R_rechts_log,  yerr=Fehler_R_rechts_log, fmt='x')
plt.plot(Zeiten_R_rechts, f(Zeiten_R_rechts, *params), 'b-', label='linearer Fit', linewidth=0.3)
plt.savefig('Rhodium_rechts_log.pdf')

plt.clf()
plt.errorbar( Zeiten_R_rechts, Werte_R_rechts_korrigiert,  Werte_R_rechts_Fehler, fmt='x')
plt.plot(Fit_X_Rhodium_rechts, np.exp(N_0_Rhodium_rechts)*np.exp(-Lamba_Rhodium_rechts*Fit_X_Rhodium_rechts), 'r-')
plt.savefig('Rhodium_normal_rechts.pdf')

#Rhodium normal

plt.clf()
plt.plot(Zeiten_rhodium, Werte_Rhodium_korrigiert, 'bx')
plt.plot(Zeiten_rhodium, np.exp(N_0_Rhodium_links)*np.exp(-Lamba_Rhodium_links*Zeiten_rhodium) + np.exp(N_0_Rhodium_rechts)*np.exp(-Lamba_Rhodium_rechts*Zeiten_rhodium) , 'r-')
plt.savefig('Rhodium_normal.pdf')

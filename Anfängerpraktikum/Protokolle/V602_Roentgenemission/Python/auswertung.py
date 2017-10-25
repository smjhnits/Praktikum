import numpy as np
from scipy.stats import sem
from uncertainties import ufloat
import uncertainties.unumpy as unp
import matplotlib.pyplot as plt
import scipy.constants as sc
from scipy.optimize import curve_fit
import operator

d = 201.4 * 10 **(-12)
Ryd = 13.6
a = 7.297 * 10 **(-3)

def Wellenlaenge(x):
    return 2 * d * np.sin(x)

def WellenlaengeUNP(x):
    return 2 * d * unp.sin(x)

def Energie(x):
    return sc.h * sc.c / (x * 10**3 * sc.e)

# Messung a

WinkelA, RateA = np.genfromtxt('M_A_T.txt', unpack=True) #skip_header = 1, unpack=True)
MaximumA = np.argmax(RateA)

plt.clf()
plt.plot(WinkelA, RateA, 'bx', label = r'Gemessene Impulsrate')
plt.ylabel(r'R in $\frac{\mathrm{Imp}}{\mathrm{s}}$')
plt.xlabel(r'$\alpha$ in $\mathrm{DEG}$')
plt.axvline(WinkelA[MaximumA])
plt.xlim(25.9, 30.1)
#plt.show()
#plt.savefig('MessungA.pdf')

WL_A = Wellenlaenge(WinkelA[MaximumA]/360*2*np.pi)
E_A = Energie(WL_A)

print("-----------------Messung A----------------- ")
print("Winkel:      ", WinkelA[MaximumA])
print("Wellenlänge: ", WL_A)
print("Energie:     ", E_A, '\n', '\n')

# Messung b

print("-----------------Messung B----------------- ")

def G(x, A, x0, sigma1, B, x1, sigma2):
    return A * np.exp(-(x-x0)**2/(2*sigma1**2)) +  B * np.exp(-(x-x1)**2/(2*sigma2**2))

def Untergrund(x, A, B, C, D):
    return A*x**3 + B*x**2 + C*x + D

x_plotB = np.linspace(0,27,1000)

Winkel2B, RateB = np.genfromtxt('M_B_T.txt', unpack=True) #skip_header = 1, unpack=True)
WinkelB = Winkel2B/2

WinkelU = np.append(np.append(WinkelB[0:80], WinkelB[86:90]), WinkelB[97:11])
RateU = np.append(np.append(RateB[0:80], RateB[86:90]), RateB[97:11])

#WinkelU = np.append(WinkelB[0:80], WinkelB[97:11])
#RateU = np.append(RateB[0:80], RateB[97:11])

MaximumB1 = 81
MaximumB2 = 93

sigma_1 = np.std(WinkelB[70:91], ddof = 1) * 1 / len(WinkelB[70:91])
sigma_2 = np.std(WinkelB[84:111], ddof = 1) * 1 / len(WinkelB[84:111])

Params_U, covariance_U = curve_fit(Untergrund, WinkelU, RateU)
errors_U = np.sqrt(np.diag(covariance_U))
RateBNeu = RateB - Untergrund(WinkelB, *Params_U)

Untergrund_A = ufloat(Params_U[0], errors_U[0])
Untergrund_B = ufloat(Params_U[1], errors_U[1])
Untergrund_C = ufloat(Params_U[2], errors_U[2])
Untergrund_D = ufloat(Params_U[3], errors_U[3])

print("---Untergrund---")
print("A: ", Untergrund_A)
print("B: ", Untergrund_B)
print("C: ", Untergrund_C)
print("D: ", Untergrund_D, '\n')

Params_MB1, covariance_MB1 = curve_fit(G, WinkelB[60:111], RateBNeu[60:111], p0 =[1, WinkelB[81], sigma_1, 1, WinkelB[93], sigma_2])
errors_MB1 = np.sqrt(np.diag(covariance_MB1))
#Params_MB2, covariance_MB2 = curve_fit(G, WinkelB[84:111], RateBNeu[84:111], p0 =[1, WinkelB[93], sigma_2])
#errors_MB2 = np.sqrt(np.diag(covariance_MB2))

Amplitude_MB2 = ufloat(Params_MB1[0], errors_MB1[0])
Amplitude_MB1 = ufloat(Params_MB1[3], errors_MB1[3])
#Amplitude_MB2 = ufloat(Params_MB2[0], errors_MB2[0])

Maximum_MB2 = ufloat(Params_MB1[1], errors_MB1[1])
Maximum_MB1 = ufloat(Params_MB1[4], errors_MB1[4])
#Maximum_MB2 = ufloat(Params_MB2[1], errors_MB2[1])

sigma_MB2 = 2*ufloat(Params_MB1[2], errors_MB1[2])
sigma_MB1 = 2*ufloat(Params_MB1[5], errors_MB1[5])
#sigma_MB2 = ufloat(Params_MB2[2], errors_MB2[2])

WL_MB1 = WellenlaengeUNP(Maximum_MB1/360*2*np.pi)
WL_MB2 = WellenlaengeUNP(Maximum_MB2/360*2*np.pi)

E_MB1 = Energie(WL_MB1) *10**3
E_MB2 = Energie(WL_MB2) *10**3

E_Sigma1_1 = Energie(WellenlaengeUNP((Maximum_MB1-sigma_MB1)/360*2*np.pi)) *10**3
E_Sigma1_2 = Energie(WellenlaengeUNP((Maximum_MB1+sigma_MB1)/360*2*np.pi)) *10**3
E_Sigma1 = E_Sigma1_2 - E_Sigma1_1

E_Sigma2_1 = Energie(WellenlaengeUNP((Maximum_MB2-sigma_MB2)/360*2*np.pi)) *10**3
E_Sigma2_2 = Energie(WellenlaengeUNP((Maximum_MB2+sigma_MB2)/360*2*np.pi)) *10**3
E_Sigma2 = E_Sigma2_2 - E_Sigma2_1

Z_CU = 29

E_kb = E_MB1
E_ka = E_MB2

Abschirm_1 = Z_CU - unp.sqrt(E_kb/Ryd)
Abschirm_2 = Z_CU - unp.sqrt(2*(E_kb-E_ka)/Ryd)

E_Sigma = np.array([unp.nominal_values(E_Sigma1), unp.nominal_values(E_Sigma2)])

Mittelwert = ufloat(np.mean(E_Sigma), np.std(E_Sigma, ddof = 1) * 1 / np.sqrt(len(E_Sigma)))

print("Erster Piek (Kb): ")
print("Amplitude:              ", Amplitude_MB1)
print("Winkel:                 ", Maximum_MB1)
print("Wellenlänge:            ", WL_MB1)
print("Energie:                ",  E_MB1)
print("Halbbreite:             ", sigma_MB1)
print("Energie der Halbbreite: ", E_Sigma1, '\n' )

print("Zweiter Piek (Ka): ")
print("Amplitude:              ", Amplitude_MB2)
print("Winkel:                 ", Maximum_MB2)
print("Wellenlänge:            ", WL_MB2)
print("Energie:                ", E_MB2)
print("Halbbreite:             ", sigma_MB2)
print("Energie der Halbbreite: ", E_Sigma2, '\n' )

print("Energiedifferenz:   ", E_Sigma2 - E_Sigma1)
print("Auflösungsvermögen: ", Mittelwert)
print("Güte des Versuches: ", E_Sigma1 / E_Sigma2, '\n')

print("Abschirmkonstante K-Kante: ", Abschirm_1)
print("Abschirmkonstante L-Kante: ", Abschirm_2, '\n')

plt.clf()
plt.plot(WinkelB, RateB , 'rx', label = r'Gemessene Impulsrate')
#plt.plot(x_plotB, G(x_plotB, *Params_MB1) + G(x_plotB, *Params_MB2) + Untergrund(x_plotB, *Params_U), 'r-', label = '2-facher Gauß Fit')
plt.plot(x_plotB, G(x_plotB, *Params_MB1) + Untergrund(x_plotB, *Params_U), 'r-', label = '2-facher Gauß Fit')
plt.ylabel(r'R in $\frac{\mathrm{Imp}}{\mathrm{s}}$')
plt.xlabel(r'$\alpha$ in $\mathrm{DEG}$')
plt.axvline(Params_MB1[4], color='c', ls = '--', label = r'$K_{\mathrm{\beta}}$')
plt.axvline(Params_MB1[1], color='g', ls = '--', label = r'$K_{\mathrm{\alpha}}$')
plt.legend(loc = 'best')
plt.xlim(3.5, 26.5)
#plt.show()
#plt.savefig('MessungB.pdf')

def Seb(x, A, B):
    return A*x + B

Winkel_Emax = WinkelB[0:15]
Rate_Emax = RateB[0:15]

Params_Emax, covariance_Emax = curve_fit(Seb, Winkel_Emax[5:13], Rate_Emax[5:13])
errors_Emax =  np.sqrt(np.diag(covariance_Emax))
Emax_plot = np.linspace(2, 8, 1000)

Steigung_Emax = ufloat(Params_Emax[0], errors_Emax[0])
Abschnitt_Emax = ufloat(Params_Emax[1], errors_Emax[1])

Winkel_Null = - Abschnitt_Emax/Steigung_Emax
Nullstelle = unp.nominal_values(Winkel_Null)

Lambda_Null = WellenlaengeUNP(Winkel_Null/360*2*np.pi)
Energie_Null = Energie(Lambda_Null) * 10 ** 3

print("Parameter Fit: ", Steigung_Emax, Abschnitt_Emax)
print("Winkel Nullstelle:      ", Winkel_Null)
print("Wellenlänge Nullstelle: ", Lambda_Null)
print("Maximale Energie:       ", Energie_Null, '\n')

plt.clf()
plt.plot(Winkel_Emax, Rate_Emax, 'rx', label = r'Gemessene Impulsrate')
plt.plot(Emax_plot, Seb(Emax_plot, *Params_Emax), 'b-', label = r'linearer Fit')
plt.plot(Nullstelle, 0, 'kx', label = r'$\vartheta_{\mathrm{Emax}}$')
plt.ylabel(r'R in $\frac{\mathrm{Imp}}{\mathrm{s}}$')
plt.xlabel(r'$\alpha$ in $\mathrm{DEG}$')
plt.axhline(0, color = 'g', ls = '--')
plt.legend(loc = 'best')
plt.xlim(3.5, 8.0)
plt.ylim(-5, 140)
#plt.savefig('SpektrumEnergie.pdf')
#plt.show()


# Messung c

print("-----------------Messung C----------------- ")

O_ZN = 30
O_GE = 32
O_BR = 35
O_SR = 38
O_ZR = 40

Winkel_2GE, Rate_GE = np.genfromtxt('M_C_GE.txt', unpack = True)
Winkel_GE = Winkel_2GE/2
Winkel_2AU, Rate_AU = np.genfromtxt('M_C_AU.txt', unpack = True)
Winkel_AU = Winkel_2AU/2
Winkel_2SR, Rate_SR = np.genfromtxt('M_C_SR.txt', unpack = True)
Winkel_SR = Winkel_2SR/2
Winkel_2ZN, Rate_ZN = np.genfromtxt('M_C_ZN.txt', unpack = True)
Winkel_ZN = Winkel_2ZN/2
Winkel_2ZR, Rate_ZR = np.genfromtxt('M_C_ZR.txt', unpack = True)
Winkel_ZR = Winkel_2ZR/2
Winkel_2BR, Rate_BR = np.genfromtxt('M_C_BR.txt', unpack = True)
Winkel_BR = Winkel_2BR/2

def f(x, A, B):
    return A*x + B;

def Fit(x, y, x1, x2, f):
    params, covariance = curve_fit(f, x[x1:x2], y[x1:x2])
    errors = np.sqrt(np.diag(covariance))
    return params, errors

def Plot(Winkel, Rate, x1, x2, Beschriftung, Name):
    plt.clf()
    plt.plot(Winkel, Rate, 'rx', label = Beschriftung, )
    plt.axvline(Winkel[x1], color = 'b', ls = '--', label = r'$\vartheta_{\mathrm{min}}$')
    plt.axvline(Winkel[x2], color = 'g', ls = '--', label = r'$\vartheta_{\mathrm{max}}$')
    plt.ylabel(r'R in $\frac{\mathrm{Imp}}{\mathrm{s}}$')
    plt.xlabel(r'$\alpha$ in $\mathrm{DEG}$')
    plt.xlim(Winkel[0]-0.3, Winkel[-1]+0.2)
    plt.ylim(min(Rate)-10, max(Rate)+10)
    plt.legend(loc = 'best')
    #plt.savefig(Name+'.pdf', format = 'pdf')

def Abschirm(E,Z):
    return Z - np.sqrt(E/Ryd - a**2 * Z**4 / 4)

def AbschirmUNP(E,Z):
    return Z - np.sqrt(E/Ryd - a**2 * Z**4 / 4)



P_GE, Error_GE = Fit(Winkel_GE, Rate_GE, 19, 25, f)
Plot(Winkel_GE, Rate_GE, 19, 24, 'Impulsrate bei Germanium', 'Germanium')
Kante_GE = (Winkel_GE[19] + Winkel_GE[24])/2
Lambda_GE = Wellenlaenge(Kante_GE/360*2*np.pi)
Energie_GE = Energie(Lambda_GE) *10**3
sigma_GE = Abschirm(Energie_GE, O_GE)

print("--------Germanium--------")
print("Winkel           : ",Kante_GE)
print("Wellenlänge      : ", Lambda_GE)
print("Energie          : ", Energie_GE)
print("Abschirmkonstante: ", sigma_GE, '\n')


P_SR, Error_SR = Fit(Winkel_SR, Rate_SR, 18, 23, f)
Plot(Winkel_SR, Rate_SR, 18, 22, 'Impulsrate bei Strontium', 'Strontium')
Kante_SR = (Winkel_SR[18] + Winkel_SR[22])/2
Lambda_SR = Wellenlaenge(Kante_SR/360*2*np.pi)
Energie_SR = Energie(Lambda_SR)*10**3
sigma_SR = Abschirm(Energie_SR, O_SR)

print("--------Strontium--------")
print("Winkel           : ",Kante_SR)
print("Wellenlänge      : ",Lambda_SR)
print("Energie          : ",Energie_SR)
print("Abschirmkonstante: ",sigma_SR, '\n')


P_ZR, Error_ZR = Fit(Winkel_ZR, Rate_ZR, 16, 22, f)
Plot(Winkel_ZR, Rate_ZR, 16, 21, 'Impulsrate bei Zirkonium', 'Zirkonium')
Kante_ZR = (Winkel_ZR[16] + Winkel_ZR[21])/2
Lambda_ZR = Wellenlaenge(Kante_ZR/360*2*np.pi)
Energie_ZR = Energie(Lambda_ZR)*10**3
sigma_ZR = Abschirm(Energie_ZR, O_ZR)

print("--------Zirkonium--------")
print("Winkel           : ",Kante_ZR)
print("Wellenlänge      : ",Lambda_ZR)
print("Energie          : ",Energie_ZR)
print("Abschirmkonstante: ",sigma_ZR, '\n')

P_BR, Error_BR = Fit(Winkel_BR, Rate_BR, 20, 25, f)
Plot(Winkel_BR, Rate_BR, 20, 24, 'Impulsrate bei Brom', 'Brom')
Kante_BR = (Winkel_BR[20] + Winkel_BR[24])/2
Lambda_BR = Wellenlaenge(Kante_BR/360*2*np.pi)
Energie_BR = Energie(Lambda_BR)*10**3
sigma_BR = Abschirm(Energie_BR, O_BR)

print("--------Brom--------")
print("Winkel           : ",Kante_BR)
print("Wellenlänge      : ",Lambda_BR)
print("Energie          : ",Energie_BR)
print("Abschirmkonstante: ",sigma_BR, '\n')

P_ZN, Error_ZN = Fit(Winkel_ZN, Rate_ZN, 14, 19, f)
Plot(Winkel_ZN, Rate_ZN, 14, 18, 'Impulsrate bei Zink', 'Zink')
Kante_ZN = (Winkel_ZN[14] + Winkel_ZN[18])/2
Lambda_ZN = Wellenlaenge(Kante_ZN/360*2*np.pi)
Energie_ZN = Energie(Lambda_ZN)*10**3
sigma_ZN = Abschirm(Energie_ZN, O_ZN)

print("--------Zink--------")
print("Winkel           : ",Kante_ZN)
print("Wellenlänge      : ",Lambda_ZN)
print("Energie          : ",Energie_ZN)
print("Abschirmkonstante: ",sigma_ZN, '\n')

Energien_MC = np.sqrt(np.array([Energie_ZN, Energie_GE, Energie_BR, Energie_SR, Energie_ZR]))
Ordnungszahlen = np.array([O_ZN, O_GE, O_BR, O_SR, O_ZR])

def fit(x, A, B):
    return A * x + B

Params_Ryd, covariance_Ryd = curve_fit(fit, Ordnungszahlen, Energien_MC)
errors_Ryd = np.sqrt(np.diag(covariance_Ryd))

Z_plot = np.linspace(27,43,1000)

plt.clf()
plt.plot(Ordnungszahlen, Energien_MC, 'rx', label = 'bestimmte Bindungsenergien')
plt.plot(Z_plot, fit(Z_plot, *Params_Ryd), 'b-', label = 'linearer Fit')
plt.xlabel(r'$Z$')
plt.ylabel(r'$\sqrt{E_{\mathrm{n}}}$ in $\mathrm{eV}$')
plt.legend(loc = 'best')
plt.xlim(29, 41)
plt.ylim(90,150 )
#plt.grid()
#plt.show()
#plt.savefig('Rydberg.pdf')

Ryd_A = ufloat(Params_Ryd[0], errors_Ryd[0])
Ryd_B = ufloat(Params_Ryd[1], errors_Ryd[1])

print("-------Rydberg Energie-------")
print("Parameter A:              ", Ryd_A)
print("Parameter B:              ", Ryd_B)
Ryd_exp = (ufloat(Params_Ryd[0], errors_Ryd[0]))**2

print("Bestimmte Rydbergenergie: ", Ryd_exp, '\n')

# Gold

O_AU = 79
plt.clf()
plt.plot(Winkel_AU, Rate_AU, 'rx', label = 'Impulsrate bei Gold', )
plt.axvline(Winkel_AU[38], color = 'b', ls = '--', label = r'$\vartheta_{\mathrm{L2,min}}$')
plt.axvline(Winkel_AU[43], color = 'g', ls = '--', label = r'$\vartheta_{\mathrm{L2,max}}$')
plt.axvline(Winkel_AU[18], color = 'c', ls = '--', label = r'$\vartheta_{\mathrm{L3,min}}$')
plt.axvline(Winkel_AU[21], color = 'y', ls = '--', label = r'$\vartheta_{\mathrm{L3,max}}$')
plt.ylabel(r'R in $\frac{\mathrm{Imp}}{\mathrm{s}}$')
plt.xlabel(r'$\alpha$ in $\mathrm{DEG}$')
plt.xlim(Winkel_AU[0]-0.3, Winkel_AU[-1]+0.2)
plt.ylim(min(Rate_AU)-10, max(Rate_AU)+10)
plt.legend(loc = 'best')
#plt.savefig('Gold.pdf')

Kante_AU_L2 = (Winkel_AU[43]+Winkel_AU[38])/2
Kante_AU_L3 = (Winkel_AU[21]+Winkel_AU[18])/2
Lambda_AU_L2 = Wellenlaenge(Kante_AU_L2/360*2*np.pi)
Lambda_AU_L3 = Wellenlaenge(Kante_AU_L3/360*2*np.pi)
Energie_AU_L2 = Energie(Lambda_AU_L2)*10**3
Energie_AU_L3 = Energie(Lambda_AU_L3)*10**3

Energie_Delta = (Energie_AU_L3 - Energie_AU_L2)
Abschirm_AU = O_AU - unp.sqrt((4/a * unp.sqrt(Energie_Delta/Ryd_exp) - 5 * Energie_Delta/Ryd_exp) * ( 1 + 19/32 * a**2 * Energie_Delta/Ryd_exp))

print("--------Gold--------", '\n')
print("----L_2----")
print("Winkel           : ",Kante_AU_L2)
print("Wellenlänge      : ",Lambda_AU_L2)
print("Energie          : ",Energie_AU_L2, '\n')

print("----L_3----")
print("Winkel           : ",Kante_AU_L3)
print("Wellenlänge      : ",Lambda_AU_L3)
print("Energie          : ",Energie_AU_L3, '\n')

print("Abschirmkonstante L-Linie: ", Abschirm_AU)

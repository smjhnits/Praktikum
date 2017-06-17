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
plt.savefig('MessungA.pdf')

WL_A = Wellenlaenge(WinkelA[MaximumA]/360*2*np.pi)
E_A = Energie(WL_A)

print("-----------------Messung A----------------- ")
print("Winkel:      ", WinkelA[MaximumA])
print("Wellenlänge: ", WL_A)
print("Energie:     ", E_A, '\n', '\n')

# Messung b


def G(x, A, x0, sigma1):#, B, x1, sigma2):
    return A * np.exp(-(x-x0)**2/(2*sigma1**2))# +  B * np.exp(-(x-x1)**2/(2*sigma2**2))

def Untergrund(x, A, B, C, D):
    return A*x**3 + B*x**2 + C*x + D

x_plotB = np.linspace(0,27,1000)

Winkel2B, RateB = np.genfromtxt('M_B_T.txt', unpack=True) #skip_header = 1, unpack=True)
WinkelB = Winkel2B/2

WinkelU = np.append(np.append(WinkelB[0:80], WinkelB[87:92]), WinkelB[97:11])
RateU = np.append(np.append(RateB[0:80], RateB[87:92]), RateB[97:11])

MaximumB1 = 81
MaximumB2 = 93

sigma_1 = np.std(WinkelB[70:91], ddof = 1) * 1 / len(WinkelB[70:91])
sigma_2 = np.std(WinkelB[84:111], ddof = 1) * 1 / len(WinkelB[84:111])

Params_U, covariance_U = curve_fit(Untergrund, WinkelU, RateU)
RateBNeu = RateB - Untergrund(WinkelB, *Params_U)

Params_MB1, covariance_MB1 = curve_fit(G, WinkelB[70:91], RateBNeu[70:91], p0 =[1, WinkelB[81], sigma_1]) #1, WinkelB[93], sigma_2])
Params_MB2, covariance_MB2 = curve_fit(G, WinkelB[84:111], RateBNeu[84:111], p0 =[1, WinkelB[93], sigma_2])

Maximum1 = Params_MB1[1]
Maximum2 = Params_MB2[1]

WL_MB1 = Wellenlaenge(Maximum1/360*2*np.pi)
WL_MB2 = Wellenlaenge(Maximum2/360*2*np.pi)

E_MB1 = Energie(WL_MB1)
E_MB2 = Energie(WL_MB2)


Z_CU = 29

E_kb = E_MB1
E_ka = E_MB2

Abschirm_1 = Z_CU - np.sqrt(E_kb*10**3/Ryd)
Abschirm_2 = Z_CU - np.sqrt(2*(E_kb-E_ka)*10**3/Ryd)

print("-----------------Messung B----------------- ")
print("Erster Piek (Kb): ")
print("Winkel:            ", Maximum1)
print("Wellenlänge:       ", WL_MB1)
print("Energie:           ",  E_MB1)
print("Abschirmkonstante: ", Abschirm_1, '\n')

print("Zweiter Piek (Ka): ")
print("Winkel:            ", Maximum2)
print("Wellenlänge:       ", WL_MB2)
print("Energie:           ", E_MB2)
print("Abschirmkonstante: ", Abschirm_2, '\n')

print("Energiedifferenz: ", E_MB2 - E_MB1, '\n')


plt.clf()
plt.plot(WinkelB, RateBNeu , 'rx', label = r'Gemessene Impulsrate')
plt.plot(x_plotB, G(x_plotB, *Params_MB1) + G(x_plotB, *Params_MB2), 'r-', label = '2-facher Gauß Fit')
#plt.plot(x_plotB, G(x_plotB, *Params_MB1), 'r-', label = '2-facher Gauß Fit')
plt.ylabel(r'R in $\frac{\mathrm{Imp}}{\mathrm{s}}$')
plt.xlabel(r'$\alpha$ in $\mathrm{DEG}$')
plt.axvline(WinkelB[MaximumB1], color='c', ls = '--', label = r'$K_{\mathrm{\beta}}$')
plt.axvline(WinkelB[MaximumB2], color='g', ls = '--', label = r'$K_{\mathrm{\alpha}}$')
plt.legend(loc = 'best')
plt.xlim(3.5, 26.5)
#plt.show()
plt.savefig('MessungB.pdf')


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

Z_plot = np.linspace(29,41,1000)

plt.clf()
plt.plot(Ordnungszahlen, Energien_MC, 'rx', label = 'bestimmte Energien')
plt.plot(Z_plot, fit(Z_plot, *Params_Ryd), 'b-', label = 'linearer Fit')
plt.grid()
#plt.show()

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

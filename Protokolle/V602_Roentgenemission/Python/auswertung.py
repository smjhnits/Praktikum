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
plt.xlim(12.5, 15.5)
#plt.show()
plt.savefig('MessungA.pdf')

# Messung b


def G(x, A, x0, sigma1):
    return A * np.exp(-(x-x0)**2/(2*sigma1**2)) #+  B * np.exp(-(x-x1)**2/(2*sigma2**2))

x_plotB = np.linspace(0,27,1000)


Winkel2B, RateB = np.genfromtxt('M_B_T.txt', unpack=True) #skip_header = 1, unpack=True)
WinkelB = Winkel2B/2

MaximumB1 = 81
MaximumB2 = 93

sigma_1 = np.std(WinkelB[70:91], ddof = 1) * 1 / len(WinkelB[70:91])
sigma_2 = np.std(WinkelB[84:111], ddof = 1) * 1 / len(WinkelB[84:111])

Params_MB1, covariance_MB1 = curve_fit(G, WinkelB[70:91], RateB[70:91], p0 =[1, WinkelB[81], sigma_1])
Params_MB2, covariance_MB2 = curve_fit(G, WinkelB[84:111], RateB[84:111], p0 =[1, WinkelB[93], sigma_2])

print(sigma_1)
print(sigma_2)

plt.clf()
plt.plot(WinkelB, RateB , 'rx', label = r'Gemessene Impulsrate')
plt.plot(x_plotB, G(x_plotB, *Params_MB1) + G(x_plotB, *Params_MB2), 'r-', label = '2-facher Gauß Fit')
plt.ylabel(r'R in $\frac{\mathrm{Imp}}{\mathrm{s}}$')
plt.xlabel(r'$\alpha$ in $\mathrm{DEG}$')
plt.axvline(WinkelB[MaximumB1], color='c', ls = '--', label = r'$K_{\mathrm{\beta}}$')
plt.axvline(WinkelB[MaximumB2], color='g', ls = '--', label = r'$K_{\mathrm{\alpha}}$')
plt.legend(loc = 'best')
plt.xlim(3.5, 26.5)
#plt.show()
#plt.savefig('MessungB.pdf')


# Messung c

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

print(Kante_GE)
print(Lambda_GE)
print(Energie_GE)
print(sigma_GE, '\n')


P_SR, Error_SR = Fit(Winkel_SR, Rate_SR, 18, 23, f)
Plot(Winkel_SR, Rate_SR, 18, 22, 'Impulsrate bei Strontium', 'Strontium')
Kante_SR = (Winkel_SR[18] + Winkel_SR[22])/2
Lambda_SR = Wellenlaenge(Kante_SR/360*2*np.pi)
Energie_SR = Energie(Lambda_SR)*10**3
sigma_SR = Abschirm(Energie_SR, O_SR)

print(Kante_SR)
print(Lambda_SR)
print(Energie_SR)
print(sigma_SR, '\n')


P_ZR, Error_ZR = Fit(Winkel_ZR, Rate_ZR, 16, 22, f)
Plot(Winkel_ZR, Rate_ZR, 16, 21, 'Impulsrate bei Zirkonium', 'Zirkonium')
Kante_ZR = (Winkel_ZR[16] + Winkel_ZR[21])/2
Lambda_ZR = Wellenlaenge(Kante_ZR/360*2*np.pi)
Energie_ZR = Energie(Lambda_ZR)*10**3
sigma_ZR = Abschirm(Energie_ZR, O_ZR)

print(Kante_ZR)
print(Lambda_ZR)
print(Energie_ZR)
print(sigma_ZR, '\n')

P_BR, Error_BR = Fit(Winkel_BR, Rate_BR, 20, 25, f)
Plot(Winkel_BR, Rate_BR, 20, 24, 'Impulsrate bei Brom', 'Brom')
Kante_BR = (Winkel_BR[20] + Winkel_BR[24])/2
Lambda_BR = Wellenlaenge(Kante_BR/360*2*np.pi)
Energie_BR = Energie(Lambda_BR)*10**3
sigma_BR = Abschirm(Energie_BR, O_BR)

print(Kante_BR)
print(Lambda_BR)
print(Energie_BR)
print(sigma_BR, '\n')

P_ZN, Error_ZN = Fit(Winkel_ZN, Rate_ZN, 14, 19, f)
Plot(Winkel_ZN, Rate_ZN, 14, 18, 'Impulsrate bei Zink', 'Zink')
Kante_ZN = (Winkel_ZN[14] + Winkel_ZN[18])/2
Lambda_ZN = Wellenlaenge(Kante_ZN/360*2*np.pi)
Energie_ZN = Energie(Lambda_ZN)*10**3
sigma_ZN = Abschirm(Energie_ZN, O_ZN)

print(Kante_ZN)
print(Lambda_ZN)
print(Energie_ZN)
print(sigma_ZN, '\n')

# Gold

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
Energie_AU_L2 = Energie(Lambda_AU_L2)
Energie_AU_L3 = Energie(Lambda_AU_L3)

print(Kante_AU_L2)
print(Lambda_AU_L2)
print(Energie_AU_L2, '\n')

print(Kante_AU_L3)
print(Lambda_AU_L3)
print(Energie_AU_L3, '\n')

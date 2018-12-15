import numpy as np
import matplotlib.pyplot as plt
import uncertainties
from scipy.signal import find_peaks
from scipy.optimize import curve_fit
import scipy.constants as sc
import scipy.integrate as integrate
from uncertainties import ufloat
from uncertainties import unumpy as unp
from uncertainties.unumpy import nominal_values as nomval
from uncertainties.unumpy import std_devs as std

# Loading experimental data and results of further calculations

r = 0.5*45*10**(-3)
L = (73.5+15)*10**(-3)
Omega = 0.5 * ( 1- L/np.sqrt(L**2+r**2))

C_Ca = np.genfromtxt('2018-12-10_Nitschke_Pape/caesium1.Spe', unpack = True)
Channels = np.linspace(0,len(C_Ca[:4000])-1, len(C_Ca[:4000]))
params_energy, covariance_energy_0, covariance_energy_1, params_Q, covariance_Q_0, covariance_Q_1= np.genfromtxt('Europium.txt', unpack = True)

covariance_energy = np.array([covariance_energy_0, covariance_energy_1])
errors_energy = np.sqrt(np.diag(covariance_energy))
covariance_Q = np.array([covariance_Q_0,covariance_Q_1])
errors_Q = np.sqrt(np.diag(covariance_Q))

def Energy(C):
    return ufloat(params_energy[0], errors_energy[0])*C + ufloat(params_energy[1], errors_energy[1])

def Gauss(x, A, xmu, sigma, B):
    return A * np.exp(-0.5*(x-xmu)**2/sigma**2) + B

def Gauss_Ufloat(x, A, xmu, sigma):
    return A * unp.exp(-0.5*(x-xmu)**2/sigma**2)

def AreaGaus(A, sigma):
    return np.sqrt(2*np.pi)*sigma*A

def Efficiency(E):
    return ufloat(params_Q[0], errors_Q[0])*E**ufloat(params_Q[1], errors_Q[1])

# first step again: finding the full energy peaks of caesium
print("----- Find Peaks -----", '\n')

Spektrum = C_Ca[:4000]
tges = 3066
Peaks = find_peaks(Spektrum, height = 1000)


# Like before, the full energy peaks will be fitted with a gaussian function to calculate
# the radioactivity

n = np.int(np.round(Peaks[0],0))
params_Ca, covariance_Ca = curve_fit(Gauss, Channels[n-30:n+30], Spektrum[n-30:n+30], p0 = [C_Ca[n], n, 1, 0])
errors_Ca = np.sqrt(np.diag(covariance_Ca))
l_u = np.int(Channels[n-30])
l_o = np.int(Channels[n+30])

Params_Ufloat = np.array([ufloat(n, errors_Ca[i]) for i,n in enumerate(params_Ca)])

print("-- Fit Parameter --")
print(f"amplitude: {Params_Ufloat[0]}")
print(f"mean:  {Energy(Params_Ufloat[1])}")
print(f"sigma:  {Params_Ufloat[2]}")
print(f"constant:  {Params_Ufloat[3]}", '\n')

# Photopeak of Caesium137 with the calculated gaussian fit

plt.clf()
plt.hist(unp.nominal_values(Energy(np.arange(l_u, l_o, 1))),
         bins=unp.nominal_values(Energy(np.linspace(l_u, l_o, len(Spektrum[n-30:n+30])))),
         weights=Spektrum[n-30:n+30], label='Spektrum')
Channel_FWHM = np.linspace(n-30,n+30,1000)
plt.xlim(654,668)
plt.plot(unp.nominal_values(Energy(Channel_FWHM)), Gauss(Channel_FWHM,*params_Ca), label = 'Gauß-Fit')
plt.xlabel("E / keV")
plt.ylabel("Zählungen pro Energie")
plt.legend()
plt.savefig('Plots/Caesium_Gauß.pdf')
#plt.show()

# Full Width Half Maximum and Full Wisth at a tenth of maximum

Channel_FWHM = np.linspace(n-30,n+30,1000)
Energies = Energy(Channel_FWHM)
Gauswerte = Gauss(Channel_FWHM, *params_Ca[0:3], 0)
FWHM_Channel = Channel_FWHM[np.abs(Gauswerte-0.5*params_Ca[0]) < 20]
FWZM_Channel = Channel_FWHM[np.abs(Gauswerte-0.1*params_Ca[0]) < 5]
FWHM = Energy(FWHM_Channel[1])-Energy(FWHM_Channel[0])
FWZM = Energy(FWZM_Channel[1])-Energy(FWZM_Channel[0])
print("----- FWHM and FWZM from Bins -----",'\n')

Channel_Bins = Channels[n-30:n+30]
Bins_FWHM = Channel_Bins[np.abs(Spektrum[n-30:n+30]-0.5*params_Ca[0])<248]
Bins_FWZM = Channel_Bins[np.abs(Spektrum[n-30:n+30]-0.1*params_Ca[0])<117]
print(Energy(Bins_FWHM))
print(Energy(Bins_FWZM))
FWHM = Energy(Bins_FWHM[0])-Energy(Bins_FWHM[1])
FWZM = Energy(Bins_FWZM[0])-Energy(Bins_FWZM[3])
print(f"x1/2: {FWHM}")
print(f"x1/10: {FWZM}")

# comparison between FWHM and FWZM
print(f"Quotient: {nomval(FWZM/FWHM)}, {std(FWZM/FWHM)}", '\n')

# Calculation of both parameters with the variance of the gaussian fit

x_05 = np.sqrt(2*np.log(2))*params_Ca[2]
x_01 = 1.823*x_05

FWHM_calc = Energy(params_Ca[1]+x_05) - Energy(params_Ca[1]-x_05)
FWZM_calc = Energy(params_Ca[1]+x_01) - Energy(params_Ca[1]-x_01)
print("----- FWHM and FWZM calculated from the Standard Derivation -----",'\n')
print(f"FWHM: {FWHM_calc}")
print(f"FWZM: {FWZM_calc}", '\n')

# Visualisation of FWHM, not necessary

# plt.clf()
# plt.hist(unp.nominal_values(Energy(np.arange(l_u, l_o, 1))),
#          bins=unp.nominal_values(Energy(np.linspace(l_u, l_o, len(Spektrum[n-30:n+30])))),
#          weights=Spektrum[n-30:n+30], label='Spektrum')
# Channel_FWHM = np.linspace(n-30,n+30,1000)
# plt.plot(unp.nominal_values(Energy(Channel_FWHM)), Gauss(Channel_FWHM,*params_Ca))
# plt.axhline(0.5*params_Ca[0])
# plt.axvline(nomval(Energy(params_Ca[1]+x_05)), color = 'r')
# plt.axvline(nomval(Energy(FWHM_Channel[0])))
# #plt.show()

# Calculation of the energy resolution with Gamma and Excitation Energy

E_y = Energy(params_Ca[1]) * 10**3
E_El = 2.9
Res_Calc = 2.35 * unp.sqrt(0.1*E_y*E_El)

print("----- Theoretical Resolution -----", '\n')
print(f"calculated resolution: {Res_Calc*10**(-3)}",'\n')

# Calculation of the Compton Edge and the backscatter peak

Channel_bs = Channels[400:600]
Peak_bs = Channel_bs[Spektrum[400:600]==np.max(Spektrum[400:600])]
Channel_ce = Channels[1100:1300]
Peak_ce = Channel_ce[Spektrum[1100:1300]==np.max(Spektrum[1100:1300])]
print("----- Energy of Compton Edge and Backscatter Peak -----",'\n')
print(f"backscatter peak: {Energy(Peak_bs[0])}")
print(f"compton edge: {Energy(Peak_ce[0])}",'\n')

# Theoretical Calculations of the backscatter peak and the compton Edge

eps = E_y*10**(-3)/511
Theo_bs = E_y*10**(-3)*1/(1+2*eps)
Theo_ce = E_y*10**(-3)*2*eps/(1+2*eps)
print(f"-- Theoretical Calculations --")
print(f"backscatter peak: {Theo_bs}")
print(f"Compton Edge: {Theo_ce}", '\n')


# Calculation of the absorption probability

mu_compton = ufloat(0.37, 0.01)*100
mu_photo = ufloat(0.008,0.001)*100
d = 39 *10**(-3)

P_compton = (1 - unp.exp(-mu_compton*d))*100
P_photo = (1 - unp.exp(-mu_photo*d))*100

print("----- Probabilities -----", '\n')
print(f"Compton: {P_compton}")
print(f"Photo: {P_photo}")
print(f"Quotient: {P_compton/P_photo}", '\n')

# comparison of the areas under the full energy peak and under the compton continuum

print("----- Interaction comparison -----")


E_photo = nomval(E_y) * 10**(-3)

def compton(E, A, eps):
    return A * 1/eps**2 *(2 + (E/(E_photo-E))**2*(1/eps**2 + (E_photo-E)/E_photo - 2/eps*((E_photo-E)/E_photo) ) )

params_compton, covariance_compton = curve_fit(compton, nomval(Energy(Channels[1000:np.int(Peak_ce[0]-2)])), Spektrum[1000:np.int(Peak_ce[0]-2)])
erros_compton = np.sqrt(np.diag(covariance_compton))

def compton_integrate(E):
    A = params_compton[0]
    eps = params_compton[1]
    return A * 1/eps**2 *(2 + (E/(E_photo-E))**2*(1/eps**2 + (E_photo-E)/E_photo - 2/eps*((E_photo-E)/E_photo) ) )

print("-- Compton Kontinuum Fit --")
print(f"Fitted A: {params_compton[0]}, {erros_compton[0]}")
print(f"Fitted eps: {params_compton[1]}, {erros_compton[1]}", '\n')

plt.clf()
plt.hist(unp.nominal_values(Energy(np.arange(0, len(Spektrum[0:np.int(Peak_ce[0]+200)]), 1))),
         bins=unp.nominal_values(Energy(np.linspace(0, len(Spektrum[0:np.int(Peak_ce[0]+200)]), len(Spektrum[0:np.int(Peak_ce[0]+200)])))),
         weights=Spektrum[0:np.int(Peak_ce[0]+200)], label='Spektrum')
plt.plot(nomval(Energy(np.int(np.round(Peak_bs)))), Spektrum[np.int(np.round(Peak_bs))], '.',
         markersize=2, label='Rückstreupeak', color='C1', alpha=0.8)
plt.plot(nomval(Energy(np.int(np.round(Peak_ce)))), Spektrum[np.int(np.round(Peak_ce))], '.',
         markersize=2, label='Compton Kante', color='C4', alpha=0.8)
plt.plot(nomval(Energy(Channels[60:np.int(Peak_ce[0]-2)])), nomval(compton(nomval(Energy(Channels[60:np.int(Peak_ce[0]-2)])), *params_compton)), 'k-', label = 'Compton Kontinuum Fit')
plt.ylabel('Zählungen pro Energie')
plt.xlabel('E / keV')
plt.legend()
plt.savefig('Plots/Caesium_Compton.pdf')
#plt.show()

Area_c = integrate.quad(compton_integrate, nomval(Energy(60)), nomval(Energy(Peak_ce-2)))
Area_compton = ufloat(Area_c[0], Area_c[1])
Area_photo = AreaGaus(params_Ca[0], params_Ca[2])
C_Ca_fehler = np.array([ufloat(n, np.sqrt(n)) for n in C_Ca])
Area_compton2 = sum(C_Ca_fehler[60:np.int(Peak_ce[0]-2)])

print("-- Different Areas --")
print(f"Area_compton with integrate: {Area_compton}")
print(f"Area_compton with sum: {nomval(Area_compton2)},{std(Area_compton2)} ")
print(f"Area_photon: {Area_photo}",'\n')

print("-- Quotient of both areas --")
print(f"Area_compton/Area_photo: {Area_compton/Area_photo}")
print(f"Area_compton/Area_photo: {Area_compton2/Area_photo}")

plt.clf()
plt.hist(unp.nominal_values(Energy(np.arange(0, len(Spektrum), 1))),
         bins=unp.nominal_values(Energy(np.linspace(0, len(Spektrum), len(Spektrum)))),
         weights=Spektrum, label='Spektrum')
plt.yscale('log')
plt.plot(nomval(Energy(np.int(np.round(Peaks[0],0)))), Spektrum[np.int(np.round(Peaks[0],0))], '.',
         markersize=2, label='Gauß-Peaks', color='C1', alpha=0.8)
plt.ylabel('Zählungen pro Energie')
plt.xlabel('E / keV')
plt.xlim(0,800)
plt.legend()
plt.savefig('Plots/Caesium.pdf')
#plt.show()

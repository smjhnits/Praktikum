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

C_u1 = np.genfromtxt('2018-12-10_Nitschke_Pape/Probe_11.Spe', unpack = True)
Peaks_Eu, Q_Eu = np.genfromtxt('EuropiumQ.txt', unpack = True)
Channels = np.linspace(0,len(C_u1[:3000])-1, len(C_u1[:3000]))
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

Spektrum = C_u1[:3000]
tges = 4281
Peaks = find_peaks(Spektrum, height = 200)

plt.clf()
plt.hist(unp.nominal_values(Energy(np.arange(0, len(Spektrum[0:1500]), 1))),
         bins=unp.nominal_values(Energy(np.linspace(0, len(Spektrum[0:1500]), len(Spektrum[0:1500])))),
         weights=Spektrum[0:1500], label='Spektrum')
plt.yscale('log')
plt.plot(nomval(Energy(Peaks[0][:])), Spektrum[Peaks[0][:]], '.',
         markersize=4, label='Gauß-Peaks', color='C1', alpha=0.8)
plt.xlim(0,500)
plt.ylabel('Zählungen pro Energie')
plt.xlabel('E / keV')
plt.legend()
plt.savefig('Plots/unbekannt1.pdf')

Peaks_Energy = Energy(Peaks[0][:])
Energy_ba = np.array([80.997,  276.398, 302.85, 356.02, 383.85 ]) # den 2. 160.61 Peak entfernt
#print(Peaks_Energy-Energy_ba)

Params_u1 = []
errors_u1 = []



for n in Peaks[0]:
    Params, covariance = curve_fit(Gauss, Channels[n-30:n+30], Spektrum[n-30:n+30], p0 = [C_u1[n], n, 1, 0])
    Params_u1.append(Params.tolist())
    errors = np.sqrt(np.diag(covariance))
    errors_u1.append(errors.tolist())

for i,n in enumerate(Peaks[0]):
    l_u = np.int(Channels[n-30])
    l_o = np.int(Channels[n+30])
    plt.clf()
    plt.hist(unp.nominal_values(Energy(np.arange(l_u, l_o, 1))),
            bins=unp.nominal_values(Energy(np.linspace(l_u, l_o, len(Spektrum[n-30:n+30])))),
            weights=Spektrum[n-30:n+30], label='Spektrum')
    Channel_Gauss = np.linspace(n-30,n+30,1000)
    plt.plot(unp.nominal_values(Energy(Channel_Gauss)), Gauss(Channel_Gauss,*Params_u1[i]))
    #plt.show()

Peaks_mittel = np.round(np.asarray(Params_u1)[:,1],0)
Amplitudes = np.asarray(Params_u1)[:,0]
Amplitudes_ufloat = np.asarray([ufloat(n, np.asarray(errors_u1)[i,0]) for i,n in enumerate(np.asarray(Params_u1)[:,0])])
Means_ufloat = np.asarray([ufloat(n, np.asarray(errors_u1)[i,1]) for i,n in enumerate(np.asarray(Params_u1)[:,1])])
sigmas = np.asarray(Params_u1)[:,2]
sigmas_ufloat =  np.asarray([ufloat(n, np.asarray(errors_u1)[i,2]) for i,n in enumerate(np.asarray(Params_u1)[:,2])])
Area_Params = np.array([[n,sigmas[i]] for i,n in enumerate(Amplitudes)])
Area_params_ufloat = np.array([[n,sigmas_ufloat[i]] for i,n in enumerate(Amplitudes_ufloat)])

print("--- Find Peaks and gaussian fit---")
print(f"Channel Peaks: {np.round(Peaks_mittel,0)}")
#print(f"Energy Peaks: {Energy(np.round(Peaks_mittel,0))}")
print(f"Energy Literature: {Energy_ba}", '\n')

Area = AreaGaus(Area_Params[:,0], Area_Params[:,1])
Area_ufloat = AreaGaus(Area_params_ufloat[:,0], Area_params_ufloat[:,1])
Area_norm = Area/tges
Area_norm_ufloat = Area_ufloat/tges

print("-- Fit Parameter --")
print(f"Amplituden: {Amplitudes_ufloat}")
print(f"Means: {Energy(Means_ufloat)}")
print(f"Sigmas: {sigmas_ufloat}", '\n')

print("--- Calculating the activity ---")

r = 0.5*45*10**(-3)
L = (73.5+15)*10**(-3)
Omega = 0.5 * ( 1- L/np.sqrt(L**2+r**2))

W = np.asarray([0.341, 0.072, 0.183, 0.621, 0.089]) # zweite 0.06 entfernt
Q = Efficiency(Energy(np.round(Peaks_mittel,0)))

Aktivität = np.array([Area_norm[i]/(W[i]*n*Omega) for i,n in enumerate(Q)])

print(f"emission probability: {W}")
print(f"Area under Gaussian Fit: {Area_ufloat}")
print(f"Efficiency: {Q}", '\n')
print(f"resulting acitivity: {Aktivität}")

A_all = sum(Aktivität)/len(Aktivität)#ufloat(np.mean(nomval(Aktivität)),np.std(std(Aktivität)))
A_4 = sum(Aktivität[1:4])/len(Aktivität[1:4])#ufloat(np.mean(nomval(Aktivität[1:4])),np.std(std(Aktivität[1:4])))

print(f"Mean with all values: {nomval(A_all)}, {std(A_all)}")
print(f"Mean without 1st: {nomval(A_4)}, {std(A_4)}")

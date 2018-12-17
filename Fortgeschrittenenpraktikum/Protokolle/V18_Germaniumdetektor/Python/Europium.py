import numpy as np
import matplotlib.pyplot as plt
import uncertainties
from scipy.signal import find_peaks
from scipy.optimize import curve_fit
import scipy.integrate as integrate
from uncertainties import ufloat
from uncertainties import unumpy as unp
from uncertainties.unumpy import nominal_values as nomval

C_Eu = np.genfromtxt('2018-12-10_Nitschke_Pape/Europium1.Spe', unpack = True)
Spektrum = C_Eu[:4000]
tges = 3393
Channels = np.linspace(0,len(C_Eu[:4000])-1, len(C_Eu[:4000]))

print("----- Find Peaks -----")

Peaks_low = find_peaks(Spektrum[:1000], height = 209)
Peaks_high = find_peaks(Spektrum[1000:], height = 40)
Peaks = []
for n in Peaks_low[0]:
    Peaks.append(n)
for n in Peaks_high[0]:
    Peaks.append(n+1000)


# to find Peaks which are equivalent to the specific energies, the difference
# between two peaks will be used to differentiate the different peaks

Diff = []
Peaks_rein = []
for i,n in enumerate(Peaks[:-1]):
    Diff.append(Peaks[i+1]-n)
    if Diff[i] > 5:
        Peaks_rein.append(Peaks[i+1])

#print(Peaks_rein)

# for an optimized analysis of the dependence between channel and energy, the
# different Peaks will be fitted with a Gaussian Function

def Gauss(x, A, xmu, sigma, B):
    return A * np.exp(-0.5*(x-xmu)**2/sigma**2) + B

Params_Eu = []
errors_Eu = []

print(f"Kanäle der Peaks: {Peaks_rein}", '\n')

for n in Peaks_rein:
    Params, covariance = curve_fit(Gauss, Channels[n-30:n+30], Spektrum[n-30:n+30], p0 = [C_Eu[n], n, 1, 0])
    Params_Eu.append(np.abs(Params.tolist()))
    errors = np.sqrt(np.diag(covariance))
    errors_Eu.append(np.abs(errors.tolist()))
    #print(f"{n}, {Params}")
    plt.clf()
    plt.plot(Channels[n-30:n+30], Spektrum[n-30:n+30])
    plt.axvline(Params[1])
    plt.plot(Channels[n-30:n+30], Gauss(Channels[n-30:n+30],*Params))
    #plt.savefig('Plots/Peak'+str(n)+'.pdf')
    #plt.show()

Peaks_mittel = np.round(np.asarray(Params_Eu)[:,1],0)
Amplitudes = np.asarray(Params_Eu)[:,0]
Amplitudes_ufloat = np.asarray([ufloat(n, np.asarray(errors_Eu)[i,0]) for i,n in enumerate(np.asarray(Params_Eu)[:,0])])
Means_ufloat = np.asarray([ufloat(n, np.asarray(errors_Eu)[i,1]) for i,n in enumerate(np.asarray(Params_Eu)[:,1])])
sigmas = np.asarray(Params_Eu)[:,2]
sigmas_ufloat =  np.asarray([ufloat(n, np.asarray(errors_Eu)[i,2]) for i,n in enumerate(np.asarray(Params_Eu)[:,2])])
Constants_ufloat = np.asarray([ufloat(n, np.asarray(errors_Eu)[i,3]) for i,n in enumerate(np.asarray(Params_Eu)[:,3])])

print(f"-- Amplitudes--:",'\n'f" {Amplitudes_ufloat}",'\n')
print(f"-- Means --:",'\n'f"  {Means_ufloat}",'\n')
print(f"-- Standard derivation --:",'\n'f"  {sigmas_ufloat}",'\n')
print(f"-- Constants --: ",'\n'f" {Constants_ufloat}",'\n')

# Plots for calibration and a single gaussian fit

# Spectrum of Europium
Peaks_plot = np.asarray([np.int(n) for n in Peaks_mittel])
plt.clf()
plt.hist(range(0, len(Spektrum), 1),
        bins=np.linspace(0, len(Spektrum), len(Spektrum)),
        weights=Spektrum, label='Spektrum')
plt.yscale('log')
plt.plot(Peaks_plot, Spektrum[Peaks_plot], '.',
         markersize=4, label='Gauß-Peaks', color='C1', alpha=0.8)
plt.ylabel('Zählungen pro Kanal')
plt.xlabel('Kanal')
plt.xlim(0,4000)
plt.legend()
plt.savefig('Plots/Europium.pdf')
#plt.show()

# single Gaussian Fit

n = Peaks_rein[0]
l_u = np.int(Channels[n-30])
l_o = np.int(Channels[n+30])
Gauß_x = np.linspace(l_u, l_o, 1000)

plt.clf()
plt.hist(range(l_u, l_o, 1),
        bins=np.linspace(l_u, l_o, len(Spektrum[n-30:n+30])),
        weights=Spektrum[n-30:n+30], label='Spektrum')
plt.ylabel('Zählungen pro Kanal')
plt.xlabel('Kanal')
plt.xlim(290,330)
plt.plot(Gauß_x, Gauss(Gauß_x,*Params_Eu[0]), label = 'Gauß-Fit')
plt.legend()
#plt.savefig('Plots/Europium_Gauß.pdf')
#plt.show()

# the mean-values of each Gaussian Peak will be used as the equivalent channels
# for the characteristic energies of Europium. With both values the dependence
# (in this case the gradiant of a linear Fit) between channel and energy
# can be calculated

E_lit = np.asarray([121.78, 244.4, 344.3, 411.12, 443.96, 778.90,867.37, 964.08, 1085.90, 1112.20, 1408.00])

print(f"Used Literaturvalues: {E_lit}",'\n')

def Energy(x, m, b):
    return m*x + b


params_energy, covariance_energy = curve_fit(Energy, Peaks_mittel, E_lit)
errors_energy = np.sqrt(np.diag(covariance_energy))

def Energy_u(C):
    return ufloat(params_energy[0], errors_energy[0])*C + ufloat(params_energy[1], errors_energy[1])

Energy_ufloat = np.array([ufloat(n, errors_energy[i]) for i,n in enumerate(params_energy)])

x = np.linspace(0, Peaks_mittel[-1]+200, 1000)

print(f"-- Fit Paramter of the linear Fit --")
print(f"Gradient: {Energy_ufloat[0]}")
print(f"Constants: {Energy_ufloat[1]}",'\n')

plt.clf()
plt.plot(Peaks_mittel, E_lit, '.', markersize = 8, label = 'Fitpunkte')
plt.plot(x, Energy(x, *params_energy), '-', label = 'linearer Fit')
plt.ylabel(r'E / keV')
plt.xlabel('Kanal')
plt.xlim(Peaks_mittel[0]-100, Peaks_mittel[-1]+100)
plt.legend()
#plt.show()
plt.savefig('Plots/Kalibrierung.pdf')

Energie_experimentell = np.array([Energy_u(n) for n in Peaks_rein])
print(f"Energie der Kanäle: {Energie_experimentell}",'\n')

# Bestimmung des Inhaltes der Vollenergiepeaks

print("----- efficiency -----",'\n')

Area_Params = np.array([[n,sigmas[i]] for i,n in enumerate(Amplitudes)])
Area_params_ufloat = np.array([[n,sigmas_ufloat[i]] for i,n in enumerate(Amplitudes_ufloat)])

def AreaGaus(A, sigma):
    return np.sqrt(2*np.pi)*sigma*A

Area = AreaGaus(Area_Params[:,0], Area_Params[:,1])
Area_ufloat = AreaGaus(Area_params_ufloat[:,0], Area_params_ufloat[:,1])
Area_norm = Area/tges
Area_norm_ufloat = Area_ufloat/tges

print("-- Areas --")
print(f"Areas: ")
print(Area_ufloat,'\n')
print(f"Normed Areas: ")
print(Area_norm_ufloat,'\n')

# Calculation of radioactivity

Ak_0 = ufloat(4130, 60)
tau = ufloat(4943, 5)
delta_t = 6644
Ak = Ak_0 * unp.exp( -delta_t * np.log(2) / tau)
print(f"Time Delta: {delta_t}")
print(f"Acitvity today: {Ak}")

# calculation if solid angle

r = 0.5*45*10**(-3)
L = (73.5+15)*10**(-3)
Omega = 0.5 * ( 1- L/np.sqrt(L**2+r**2))
print(f"solid angle: {Omega}", '\n')

# Emission probabilities

W = np.array([0.286, 0.076, 0.265, 0.022, 0.031, 0.129,0.042, 0.146, 0.102, 0.136, 0.210])
print("Emission probabilities:",'\n', f" {W}",'\n')

# Calculation of the efficiency for the different Peaks

Q = np.array([n/(Omega * W[i] * Ak) for i,n in enumerate(Area_norm)])
Q_ufloat = np.array([n/(Omega * W[i] * Ak) for i,n in enumerate(Area_norm_ufloat)])
print(f"Efficiency: {Q_ufloat}",'\n')

def Effizienz(E, A, B):
     return A*E**B

# only values above 150 keV will be used for the following fit of the efficiency

params_Q, covariance_Q = curve_fit(Effizienz, E_lit[1:], unp.nominal_values(Q[1:]))
errors_Q = np.sqrt(np.diag(covariance_Q))
Params_Q_ufloat = np.array([ufloat(n, errors_Q[i]) for i,n in enumerate(params_Q)])

e = np.linspace(90, E_lit[-1]+100,1000)
plt.clf()
#plt.plot(E_lit, unp.nominal_values(Q), 'rx', label = 'bestimmte Effizienzen')
plt.errorbar(E_lit, unp.nominal_values(Q_ufloat), yerr = unp.std_devs(Q_ufloat), fmt='.', ecolor = 'k', color = 'k',  label = 'bestimmte Effizienzen')
plt.plot(e, Effizienz(e, *params_Q), color = 'C1', label = 'gefittete Effizienz')
plt.ylabel('Effizienz')
plt.xlabel(r'E / keV')
plt.xlim(100, E_lit[-1]+100)
plt.ylim(0,0.6)
plt.legend()
plt.savefig('Plots/Effizienz.pdf')
#plt.show()

print("Fit Parameter")
print(Params_Q_ufloat)

np.savetxt('Europium.txt', np.column_stack([params_energy, covariance_energy[0], covariance_energy[1], params_Q, covariance_Q[0], covariance_Q[1]]))
np.savetxt('EuropiumQ.txt', np.column_stack([Peaks_mittel, nomval(Q)]))

#print(params_energy, covariance_energy)

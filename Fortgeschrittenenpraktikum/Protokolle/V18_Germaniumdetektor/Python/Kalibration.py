import numpy as np
import matplotlib.pyplot as plt
import uncertainties
from scipy.signal import find_peaks
from scipy.optimize import curve_fit

C_Eu = np.genfromtxt('2018-12-10_Nitschke_Pape/Europium1.Spe', unpack = True)
Spektrum = C_Eu[:4000]
Channels = np.linspace(0,len(C_Eu[:4000])-1, len(C_Eu[:4000]))

Peaks_low = find_peaks(Spektrum[:1000], height = 209)
Peaks_high = find_peaks(Spektrum[1000:], height = 60)
Peaks = []
for n in Peaks_low[0]:
    Peaks.append(n)
for n in Peaks_high[0]:
    Peaks.append(n+1000)

plt.hist(range(0, len(Spektrum), 1),
         bins=np.linspace(0, len(Spektrum), len(Spektrum)),
         weights=Spektrum, label='Spektrum')
plt.yscale('log')
for n in Peaks:
    plt.axvline(n, color = 'r')
plt.legend()
#plt.show()

# to find Peaks which are equivalent to the specific energies, the difference
# between two peaks will be used to differentiate the different peaks

Diff = []
Peaks_rein = []
for i,n in enumerate(Peaks[:-1]):
    Diff.append(Peaks[i+1]-n)
    if Diff[i] > 5:
        Peaks_rein.append(Peaks[i+1])

# for an optimized analysis of the dependence between channel and energy, the
# different Peaks will be fitted with a Gaussian Function

def Gauss(x, A, xmu, sigma):
    return A * np.exp(-0.5*(x-xmu)**2/sigma**2)

def Fit(x, y, Limit_down, Limit_up ):
    Params, covariance = curve_fit()

Params_Eu = []

for n in Peaks_rein:
    Params, covariance = curve_fit(Gauss, Channels[n-30:n+30], Spektrum[n-30:n+30], p0 = [C_Eu[n], n, 1])
    Params_Eu.append(Params.tolist())
    plt.clf()
    plt.plot(Channels[n-30:n+30], Spektrum[n-30:n+30])
    plt.plot(Channels[n-30:n+30], Gauss(Channels[n-30:n+30],*Params))
    #plt.savefig('Plots/Peak'+str(n)+'.pdf')
    #plt.show()

Peaks_mittel = np.asarray(Params_Eu)[:,1]

# the mean-values of each Gaussian Peak will be used as the equivalent channels
# for the characteristic energies of Europium. With both values the dependence
# (in this case the gradiant of a linear Fit) between channel and energy
# can be calculated

E_lit = [121.78, 244.4, 344.3, 411.12, 443.96, 778.90, 964.08, 1085.90, 1112.20, 1408.00]

def LinFit(x, m, b):
    return m*x + b

params_energy, covariance_energy = curve_fit(LinFit, Peaks_mittel, E_lit)

x = np.linspace(0, Peaks_mittel[-1], 1000)

plt.clf()
plt.plot(Peaks_mittel, E_lit, 'rx', label = 'Messwerte')
plt.plot(x, LinFit(x, *params_energy), 'b-', label = 'Fit')
plt.legend()
plt.show()

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from uncertainties import ufloat
import scipy.constants as sc
import csv
import pint
from pint import UnitRegistry
u = UnitRegistry()
Q_ = u.Quantity

# Justagewerte

t90 = Q_(5.6, 'microsecond').to('second')
t180 = Q_(10.3, ',microsecond').to('second')
w = Q_(21.70788, 'MHz').to('Hz')
gamma = 2.68 * 10**8 # in rad / (s*T)
r = 4.4 * 10 **(-3) # in m

# Messdaten

T1_tau, T1_U = np.genfromtxt('T1.txt', unpack = True)
D_tau, D_U, D_t12 = np.genfromtxt('D.txt', unpack = True)
T1_tau = T1_tau * 10 **(-3)
T1_U = T1_U * 10 **(-3)
T2_tau = []
T2_U = []

t12 = ufloat(np.mean(D_t12)*10**(-6), np.std(D_t12)*10**(-6))

with open('meiboom_gill.csv') as csvfile:
     T2 = csv.reader(csvfile, delimiter = ',', quoting=csv.QUOTE_NONNUMERIC)
     for row in T2:
         T2_tau.append(row[0])
         T2_U.append(row[1])
T2U_max = []
T2tau_max = []

T2tau_CP = []
T2U_CP = []
with open('scope_4.csv') as csvfile:
     CP = csv.reader(csvfile, delimiter = ',', quoting=csv.QUOTE_NONNUMERIC)
     for row in CP:
         T2tau_CP.append(row[0])
         T2U_CP.append(row[1])

# Bestimmung von T2

for n in range(5,96):
    selection = T2_tau[20*n+10:20*(n+1)+10]
    selection2 = T2_U[20*n+10:20*(n+1)+10]
    max = np.max(selection2)
    i = selection2.index(max)
    T2U_max.append(max)
    T2tau_max.append(selection[i])

def FitT2(t, T2, M0, M1):
    return M0*np.exp(-t/T2)+M1

paramsT2, covarianceT2 = curve_fit(FitT2, T2tau_max[2::2], T2U_max[2::2])
errorsT2 = np.sqrt(np.diag(covarianceT2))
T2_f = ufloat( paramsT2[0], errorsT2[0])
M0 = ufloat( paramsT2[1], errorsT2[1])
M1 = ufloat( paramsT2[2], errorsT2[2])
T2 = paramsT2[0]
print('Parameter für T2:', '\n', 'M0 = ', M0, ' V', '\n',
     'M1 = ', M1, ' V', '\n', 'T2 = ', T2_f, ' s', '\n')

# Bestimmung von T1

def FitT1(t, T1, M0, M1):
    return M0*(1-2*np.exp(-t/T1)) + M1

paramsT1, covarianceT1 = curve_fit(FitT1, T1_tau, T1_U)
errorsT1 = np.sqrt(np.diag(covarianceT1))
T1 = ufloat( paramsT1[0], errorsT1[0])
M0 = ufloat( paramsT1[1], errorsT1[1])
M1 = ufloat( paramsT1[2], errorsT1[2])
print('Parameter für T1:', '\n', 'M0 = ', M0, ' V', '\n',
     'M1 = ', M1, ' V', '\n', 'T1 = ', T1, ' s', '\n')

# Bestimmung von TD

def FitD(t, M0, M1, d):
    return M0*np.exp(-t/(T2*1000))*np.exp(-t**3*2*d) + M1

paramsD, covarianceD = curve_fit(FitD, D_tau, D_U, p0=[-800, 100, 0.0004])
errorsD = np.sqrt(np.diag(covarianceD))
M0 = ufloat( paramsD[0], errorsD[0])
M1 = ufloat( paramsD[1], errorsD[1])
d = ufloat( paramsD[2], errorsD[2])
#b = ufloat( paramsD[2], errorsD[2])
#d = ufloat( paramsD[3], errorsD[3])
print('Parameter für TD:', '\n', 'M0 = ', M0, ' mV', '\n',
      'M1 = ', M1, '\n', 'd = ', d, ' 1/ms^3',  '\n')


# Bestimmung der Diffusionskonstante

print('t12: ', t12, '\n')
G = 8.8 / (r * gamma * t12)
D = 3 * d * 10**9/ (G**2 * gamma**2)
print('Parameter für die Diffusionskonstante: ', '\n', 'G = ', G, '\n', 'D = ', D,'\n')

# Viskosität und Bestimmung der Radien

alpha = 1.024 * 10 ** (-9) # m^2/s^2
rho = 997 # kg/m^3
delta = 0.5
time = 14*60 + 58

def Viskos(t):
    return alpha*rho*(t-delta)

Viskos = Viskos(time)
print('Die Viskosität von Wasser beträgt :', Viskos, '\n')

temp = 273.15 + 20 # Raumtemperatur

def Radius(n):
    return sc.k*temp/(D*6*np.pi*n)

RadV = Radius(Viskos)

M = 18 * 10 **(-3) # kg/mol
Na = 6.022 * 10 ** (23) # 1/mol
b = 30.49*10**(-6) # m^3/mol VdW-Kovolumen Quelle: https://home.uni-leipzig.de/energy/pdf/freumd2.pdf

RadMol = (3/(4*np.pi)*0.74*M/(rho*Na))**(1/3)
RadVdW = (3/(4*np.pi)*b/(4*Na))**(1/3)


print('Die verschiedenen Radien lauten:' , '\n', 'Viskositätsradius: ', RadV , '\n',
        'Molekülgewicht: ' , RadMol, '\n', 'Van der Waal: ', RadVdW, '\n')

# Plot T1

t1 = np.linspace(0, 15, 10000)
plt.plot(T1_tau, T1_U, 'rx', label = 'T1 Werte')
plt.plot(t1, FitT1(t1, paramsT1[0], paramsT1[1], paramsT1[2]), 'g-', label = 'Fit')
plt.legend(loc = 'best')
plt.xlim(0.6*10**(-3), 15)
plt.ylabel(r'$U$ / $V$')
plt.xlabel(r'$t$ / $s$')
plt.xscale('log')
#plt.savefig('../Plots2/T1.pdf')
#plt.show()

# Plot T2

# Plot der Carr-Purcells Burstsequenz

plt.clf()
plt.plot(T2tau_CP, T2U_CP, 'b-', label = 'Signalhöhe')
plt.xlabel(r'$\tau$ / $s$')
plt.ylabel(r'$U$ / $V$')
plt.legend(loc = 'best')
plt.xlim(np.min(T2tau_CP), np.max(T2tau_CP) )
#plt.savefig('../Plots2/T2CP.pdf')
#plt.show()


t2 = np.linspace(-0.5,2,100)
plt.clf()
plt.plot(T2_tau, T2_U, 'b-', label = 'Meiboom Gill')
plt.plot(T2tau_max[2::2], T2U_max[2::2], 'rx', label = r'$U(2n\tau)$')
plt.plot(t2, FitT2(t2, paramsT2[0], paramsT2[1], paramsT2[2]), 'g-', label = 'Fit')
plt.legend(loc = 'best')
plt.ylabel(r'$U\,/\,V$')
plt.xlabel(r'$t\,/\,s$')
plt.xlim(T2_tau[0], T2_tau[-1])
#plt.savefig('../Plots2/T2.pdf')
#plt.show()

# Log Plot T2

plt.clf()
plt.plot(T2tau_max[2::2], np.log(T2U_max[2::2]), 'rx', label = r'$U(2n\tau)$')
plt.plot(t2, np.log(FitT2(t2, paramsT2[0], paramsT2[1], paramsT2[2])), 'g-', label = 'Fit')
plt.xlabel(r'$t\, / \,s$')
plt.ylabel(r'$\log{(U \,/\, V)}$')
plt.xlim(-0.1,2)
plt.legend()
#plt.savefig('../Plots2/T2Log.pdf')
#plt.show()

# Plot D

td = np.linspace(0,16)
plt.clf()
plt.plot(D_tau, D_U, 'rx', label = 'Messwerte')
#plt.plot(td, FitD(td, paramsD[0], paramsD[1], paramsD[2], paramsD[3]), 'g-', label = 'Fit')
plt.plot(td, FitD(td, paramsD[0], paramsD[1], paramsD[2]), 'g-', label = 'Fit')
plt.ylabel(r'$U\,/\,mV$')
plt.xlabel(r'$t\,/\,ms$')
plt.xlim(0,16)
plt.legend()
plt.savefig('../Plots2/TD.pdf')
#plt.show()

np.savetxt('T2ExD.txt', np.column_stack([T2tau_max[2::2], T2U_max[2::2]]))#

# Korrektur

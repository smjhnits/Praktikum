import numpy as np
from scipy.stats import sem
from uncertainties import ufloat
import uncertainties.unumpy as unp
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

Zeiten = np.array([0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2, 2.25, 2.5, 2.75, 3]) * 10 ** (-3)
Amplitudea = np.array([12.4, 10, 8.2, 6.6, 5.8, 4.6, 4, 3.4, 2.8, 2.4, 2, 1.8, 1.6])

U0 = np.array([14.35, 14.25, 14.20, 14.25, 14.2, 14.13, 14.1, 14.1, 14.1, 14.1, 14.09, 14.1, 14.1, 14.0, 13.9])
Amplitudeb = np.array([ 14.1, 13.62, 12.91, 11.88, 10.77, 7.29, 5.39, 4.20, 3.48, 3.01, 2.61, 2.30, 2.14, 1.90, 1.74])

Frequenzen = np.array([10, 30, 50, 75, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100])

a = np.array([99.2, 32, 18.40, 12.00, 8.8, 4.2, 2.68, 2.00, 1.6, 1.32, 1.12, 1, 0.88, 0.76, 0.66]) * 10 ** (-3)
b = np.array([100.08, 33.34, 20.01, 13.34, 10.0, 5, 3.33, 2.5, 2, 1.67, 1.43, 1.25, 1.11, 1, 0.91]) * 10 ** (-3)

# Messung a

yPlota = np.log(Amplitudea)

def FitMessungA(x, a, b):
	return a*x + b

laufvariableA = np.linspace(0, 3, 1000) * 10 ** (-3)

params_a, covariance_a = curve_fit(FitMessungA, Zeiten, yPlota)
error_params_a = np.sqrt(np.diag(covariance_a))
params_a_u = 1/ufloat(params_a[0], error_params_a[0])

plt.plot(Zeiten, yPlota, 'bx', label = r'$\mathrm{Messwerte}$')
plt.plot(laufvariableA, FitMessungA(laufvariableA, *params_a), 'r-', label = r'$\mathrm{Regressionsgerade}$')
plt.ylabel(r'$\mathrm{ln(U_0)}$')
plt.xlabel(r'$\mathrm{Frequenz}\, \mathrm{in} \,\mathrm{Hz}$')
plt.legend(loc = 'best')
plt.savefig('Messunga.pdf')
#plt.show()

print('Parameter RC aus der Messung a',params_a_u)
print('\n')

# Messung b
yPlotb = Amplitudeb / U0

#print(np.log(yPlotb))

def Theoriekurve(x,a):
	return 1/(np.sqrt(1+(2*np.pi*x)**2*a**2))

params_b, covariance_b = curve_fit(Theoriekurve, Frequenzen, yPlotb)
error_params_b = np.sqrt(np.diag(covariance_b))
params_b_u = ufloat(params_b, error_params_b[0])

print('Parameter RC aus der Messung b',params_b_u)
print('\n')

laufvariable = np.linspace(5, 1200, 1000)

plt.clf()
plt.plot(Frequenzen, yPlotb, 'bx', label = r'$\mathrm{Messwerte}$')
plt.plot(laufvariable, Theoriekurve(laufvariable, *params_b), 'r-', label = r'$\mathrm{Regressionskurve}$')
plt.xlabel(r'$\mathrm{Frequenz}\, \mathrm{in} \,\mathrm{Hz}$')
plt.ylabel(r'$ \mathrm{Verhältnis} \,\, \frac{U_c}{U_g}$')
plt.legend(loc = 'best')
plt.xscale('log')
plt.savefig('Messungb.pdf')
#plt.show()

# Messung c

phase = np.array([ n/b[i]*2*np.pi for i, n in enumerate(a) ])
phase2 = 2*np.pi - phase

def phasen_fit(x, a):
    return np.arctan(-(2*np.pi*x)*a)

params_c,covariance_c = curve_fit(phasen_fit, Frequenzen , phase2)
error_params_c = np.sqrt(np.diag(covariance_c))
params_c_u = ufloat(params_c, error_params_c[0])

params_c_K,covariance_c_K = curve_fit(phasen_fit, Frequenzen[0:14] , phase2[0:14])
error_params_c_K = np.sqrt(np.diag(covariance_c_K))
params_c_u_K = ufloat(params_c_K, error_params_c_K[0])

print('Parameter RC aus der Messung c',params_c_u)
print('\n')

print('Parameter RC aus der Messung c mit Korrektur',params_c_u_K)
print('\n')

plt.clf()
plt.plot(Frequenzen, phase2, 'bx', label = r'$\mathrm{Messwerte}$')
plt.plot(laufvariable, phasen_fit(laufvariable, *params_c), 'r-', label = r'$\mathrm{Regressionskurve}$')
plt.legend(loc = 'best')
plt.xlabel(r'$\nu \, \mathrm{in} \,\mathrm{Hz}$')
plt.ylabel(r'$ Phasenverschiebung $')
plt.yticks([0,1/16*np.pi,1/8*np.pi,3/16*np.pi,1/4*np.pi,5/16*np.pi,3/8*np.pi,7/16*np.pi,1/2*np.pi,9/16*np.pi,5/8*np.pi,11/16*np.pi,3/4*np.pi,13/16*np.pi],
['0','$\\frac{1}{16}\\pi$', '$\\frac{1}{8}\\pi$','$\\frac{3}{16}\\pi$' ,'$\\frac{1}{4}\\pi$','$\\frac{5}{16}\\pi$','$\\frac{3}{8}\\pi$','$\\frac{7}{16}\\pi$','$\\frac{1}{2}\\pi$','$\\frac{9}{16}\\pi$','$\\frac{5}{8}\\pi$','$\\frac{11}{16}\\pi$','$\\frac{3}{4}\\pi$','$\\frac{13}{16}\\pi$'])
plt.grid()
plt.savefig('Messungc.pdf')
#plt.show()

print("Phasenverschiebung in Radiant: ", phase2, '\n')

# Messung bzw. Plot d

def VerhältnissMessungD(phase,frequenz):
	return (np.sin(phase)/(2*np.pi*frequenz*0.00136))

AmplitudenD = VerhältnissMessungD(phase2, Frequenzen)

print("Berechnete Amplituden: ", AmplitudenD, '\n')

plt.clf()
plt.polar(phase2, AmplitudenD ,'gx',label=r'$\mathrm{Messdaten}$')
plt.polar(phase2, yPlotb, 'bx', label = r'$\mathrm{Daten \, Messung \, x.2}$')
winkel=np.linspace(0,phase[-1],1000)
plt.polar(winkel,np.cos(winkel),'r-',label=r'$\mathrm{Theoriekurve}$')
plt.xticks([0,0.25*np.pi,0.5*np.pi,0.75*np.pi,np.pi,1.25*np.pi,1.5*np.pi,1.75*np.pi],['0','$\\frac{1}{4}\\pi$', '$\\frac{1}{2}\\pi$','$\\frac{3}{4}\\pi$' ,'$\\pi$','$\\frac{5}{4}\\pi$','$\\frac{3}{2}\\pi$','$\\frac{7}{4}\\pi$'])
plt.legend(loc= [0.05,0.25])
plt.ylim(0,1.2)
plt.savefig('Messungd.pdf')
#plt.show()

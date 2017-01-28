import numpy as np
from scipy.stats import sem
from uncertainties import ufloat
import uncertainties.unumpy as unp
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

U0 = np.array([14.35, 14.25, 14.20, 14.25, 14.2, 14.13, 14.1, 14.1, 14.1, 14.1, 14.09, 14.1, 14.1, 14.0, 13.9])
Amplitude = np.array([ 14.1, 13.62, 12.91, 11.88, 10.77, 7.29, 5.39, 4.20, 3.48, 3.01, 2.61, 2.30, 2.14, 1.90, 1.74])

Frequenzen = np.array([10, 30, 50, 75, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100])

a = np.array([99.2, 32, 18.40, 12.00, 8.8, 4.2, 2.68, 2.00, 1.6, 1.32, 1.12, 1, 0.88, 0.76, 0.66]) * 10 ** (-3)
b = np.array([100.08, 33.34, 20.01, 13.34, 10.0, 5, 3.33, 2.5, 2, 1.67, 1.43, 1.25, 1.11, 1, 0.91]) * 10 ** (-3)

# Messung a


# Messung b
yPlotb = Amplitude / U0

print(np.log(yPlotb))

def Theoriekurve(x,a):
	return 1/(np.sqrt(1+(2*np.pi*x)**2*a**2))

params_b, covariance_b = curve_fit(Theoriekurve, Frequenzen, yPlotb)
error_params_b = np.sqrt(np.diag(covariance_b))
params_b_u = ufloat(params_b,covariance_b)

print('Parameter RC aus der Messung b',params_b_u)
print('\n')

laufvariable = np.linspace(5, 1200, 1000)

plt.plot(Frequenzen, yPlotb, 'bx', label = r'$Messkurve$')
plt.plot(laufvariable, Theoriekurve(laufvariable, *params_b), 'r-', label = r'$Theoriekurve Messung b$')
plt.legend(loc = 'best')
#plt.show()

# Messung c

phase = np.array([ n/b[i]*2*np.pi for i, n in enumerate(a) ])
phase2 = 2*np.pi - phase

def phasen_fit(x, a):
    return np.arctan(-(2*np.pi*x)*a)

params_c,covariance_c = curve_fit(phasen_fit, Frequenzen , phase2)
error_params_c = np.sqrt(np.diag(covariance_c))
params_c_u = ufloat(params_c,covariance_c)

print('Parameter RC aus der Messung c',params_c_u)
print('\n')

plt.clf()
plt.plot(Frequenzen, phase2, 'bx', label = r'$Messkurve$')
plt.plot(laufvariable, phasen_fit(laufvariable, *params_c), 'r-', label = r'$Theoriekurve$')
plt.legend(loc = 'best')
plt.xlabel(r'$\nu \, \mathrm{in} \,\mathrm{Hz}$')
plt.ylabel(r'$ Phasenverschiebung $')
plt.yticks([0,1/16*np.pi,1/8*np.pi,3/16*np.pi,1/4*np.pi,5/16*np.pi,3/8*np.pi,7/16*np.pi,1/2*np.pi,9/16*np.pi,5/8*np.pi,11/16*np.pi,3/4*np.pi,13/16*np.pi],
['0','$\\frac{1}{16}\\pi$', '$\\frac{1}{8}\\pi$','$\\frac{3}{16}\\pi$' ,'$\\frac{1}{4}\\pi$','$\\frac{5}{16}\\pi$','$\\frac{3}{8}\\pi$','$\\frac{7}{16}\\pi$','$\\frac{1}{2}\\pi$','$\\frac{9}{16}\\pi$','$\\frac{5}{8}\\pi$','$\\frac{11}{16}\\pi$','$\\frac{3}{4}\\pi$','$\\frac{13}{16}\\pi$'])
plt.grid()
#plt.show()

# Messung bzw. Plot d

plt.clf()
plt.polar(phase2, Theoriekurve(Frequenzen, *params_b) ,'rx',label=r'$\mathrm{Messdaten}$')
winkel=np.linspace(0,phase[-1],1000)
plt.polar(winkel,np.cos(winkel),'b-',label=r'$\mathrm{Theoriekurve}$')
plt.xticks([0,0.25*np.pi,0.5*np.pi,0.75*np.pi,np.pi,1.25*np.pi,1.5*np.pi,1.75*np.pi],['0','$\\frac{1}{4}\\pi$', '$\\frac{1}{2}\\pi$','$\\frac{3}{4}\\pi$' ,'$\\pi$','$\\frac{5}{4}\\pi$','$\\frac{3}{2}\\pi$','$\\frac{7}{4}\\pi$'])
plt.legend(loc=[0.05,0.95])
plt.show()

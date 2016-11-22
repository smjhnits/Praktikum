import numpy as np
from scipy.stats import sem
from uncertainties import ufloat
import uncertainties.unumpy as unp
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

Viskos = np.array([1791, 1308, 1003, 797.7, 653.1, 547.1, 466.8, 404.5, 355.0, 315.0,])

Viskos *= 10**(-6)

Temperature = np.array([0.01, 10, 20, 30, 40 , 50, 60, 70, 80, 90, ])
Temperature += 273.15

print(Viskos)
#print(len(Temperature))

def f( x, A, B):
    return A * np.exp( B / x )

x_plot = np.linspace(270, 380, num = 1000)

params, covariance = curve_fit(f, Temperature, Viskos)

errors = np.sqrt(np.diag(covariance))

plt.plot(Temperature, Viskos, 'rx', label = "dyn Viskosität")
plt.xlim(270, 380)
plt.ylim(0, 0.002)
plt.plot(x_plot, f(x_plot, *params), 'b-', label = "Fit")
plt.legend(loc="best")
plt.title(r" dynamische Viskosität $\nu$ von destilliertem Wasser")



plt.show()
print(params)

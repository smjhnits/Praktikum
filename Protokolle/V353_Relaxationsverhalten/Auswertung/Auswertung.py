import numpy as np
from scipy.stats import sem
from uncertainties import ufloat
import uncertainties.unumpy as unp
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

U0 = np.array([14.35, 14.25, 14.20, 14.25, 14.2, 14.13, 14.1, 14.1, 14.1, 14.1, 14.09, 14.1, 14.1, 14.0, 13.9])
Amplitude = np.array([ 14.1, 13.62, 12.91, 11.88, 10.77, 7.29, 5.39, 4.20, 3.48, 3.01, 2.61, 2.30, 2.14, 1.90, 1.74])

Frequenzen = np.array([10, 30, 50, 75, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100])

a = np.array([99.2, 32, 18.40, 12.00, 8.8, 4.2, 2.68, 2.00, 1.6, 1.32, 1.12, 1, 0.88, 0.76, 0.66])
b = np.array([110.08, 33.34, 20.01, 13.34, 10.0, 5, 3.33, 2.5, 2, 1.67, 1.43, 1.25, 1.11, 1, 0.91])

yPlotb = Amplitude / U0

print(np.log(yPlotb))

plt.plot(Frequenzen, yPlotb, 'bx', label = r'$Messkurve$')
plt.plot(Frequenzen, np.log(yPlotb), 'bx', label = r'$Messkurve$')
plt.legend(loc = 'best')
plt.show()

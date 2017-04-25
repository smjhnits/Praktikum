import numpy as np
from scipy.stats import sem
from uncertainties import ufloat
import uncertainties.unumpy as unp
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

testXAchse = np.linspace(320, 700, 39)

Zählrate = np.array([33062, 33816, 33883, 34142, 34549, 34491, 34815, 34818,
                     34975, 35219, 34923, 35100, 34947, 35133, 35390, 35342,
                     35359, 35363, 35234, 35695, 35722, 35332, 35523, 35617,
                     35747, 35433, 35827, 35757, 35908, 35868, 35853, 36340,
                     36405, 36758, 37352, 37824, 38535, 39689, 41082])

Stromstärken = np.array([0.3, 0.45, 0.6, 0.7, 0.85, 0.95, 1.1, 1.2,  1.25, 1.4,
                         1.6,  1.7, 1.8, 1.9,  2.1,  2.3, 2.4, 2.5,  2.6, 2.8,
                         2.9,  3.0, 3.0, 3.2,  3.3,  3.4, 3.5, 3.6, 3.8, 3.95,
                         4.0,  4.1, 4.4, 4.5,  4.7,  4.8, 4.9, 5.2, 5.4])

print(testXAchse)

plt.plot(testXAchse, Zählrate/60, 'kx', label = r'$Gezählte \,\, Zerfälle$')
#plt.plot(testXAchse, Stromstärken, 'rx', label = r'$Gemessene \,\, Stromstärken$')
plt.xlabel(r'$U \,\, in \,\, V$')
plt.ylabel(r'$\frac{N}{t} \,\, in \,\, \frac{1}{s}$')
#plt.ylabel(r'$I \,\, in \,\, A$')
plt.legend(loc='best')
plt.grid()
plt.show()

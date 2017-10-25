import numpy as np
from scipy.stats import sem
from uncertainties import ufloat
import uncertainties.unumpy as unp
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

L   = 32.51 * 10 ** (-3)
C   = 0.801 * 10 ** (-9)
Csp = 0.037 * 10 ** (-9)
R = 48


Nü_negativ = np.array([33.16, 33.66, 34.25, 35.12, 36.08, 37.60, 40.28, 47.33]) * 10 ** (3)
Nü_positiv = np.array([30.77, 30.79, 30.80, 30.81, 30.82, 30.83, 30.84, 30.85]) * 10 ** (3)

Kopplungskapazitäten = np.array([9.99, 8, 6.47, 5.02, 4.00, 3.00, 2.03, 1.01]) * 10 ** (-9)
C_K_Error = np.array([ufloat(n, 0.003*n) for n in Kopplungskapazitäten])

nu_m_theo = np.array([1 / ( 2 * np.pi * unp.sqrt( L * ( (1/C + 2/n)**(-1) + Csp) ) ) for n in C_K_Error])
nu_p_theo = 1 / ( 2 * np.pi * np.sqrt( L * ( C + Csp) ) )
nu_p_theo1 = np.array([nu_p_theo, nu_p_theo, nu_p_theo, nu_p_theo, nu_p_theo, nu_p_theo, nu_p_theo, nu_p_theo ])

nu_m_theo1 = np.array([unp.nominal_values(n) for n in nu_m_theo])

plt.plot(Kopplungskapazitäten, Nü_negativ*10**(-3), 'bx', label = r'Messung 3.2: $\nu_{-}$')
plt.plot(Kopplungskapazitäten, nu_m_theo1*10**(-3), 'rx', label = r'Theoriewerte: $\nu_{-}$')
plt.plot(Kopplungskapazitäten, Nü_positiv*10**(-3), 'mx', label = r'Messung 3.2: $\nu_{+}$')
plt.plot(Kopplungskapazitäten, nu_p_theo1*10**(-3), 'yx', label = r'Theoriewerte: $\nu_{+}$')
plt.xlabel(r'$Kopplungskapazität \,\, C_k \,\, in \,\, \mathrm{F}$')
plt.ylabel(r'$Frequenzen \,\, \nu \,\, in \,\, \mathrm{kHz}$')

plt.legend(loc = 'best')
#plt.show()
plt.savefig('Messungb_Plot1.pdf')

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

Start = np.array([30.85, 30.84, 30.83, 30.82, 30.81, 30.80, 30.79, 30.77]) * 10 ** (3)
Stop = np.array([55.05, 50, 40, 40, 40, 40, 40, 40]) * 10 ** (3)
Sweep_Zeit = 2
Zeiten = np.array([1.36, 1, 1.475, 1.125, 0.925, 0.740, 0.6, 0.5])

Nü_positiv = np.array([30.77, 30.79, 30.80, 30.81, 30.82, 30.83, 30.84, 30.85]) * 10 ** (3)

Kopplungskapazitäten = np.array([9.99, 8, 6.47, 5.02, 4.00, 3.00, 2.03, 1.01]) * 10 ** (-9)
C_K_Error = np.array([ufloat(n, 0.003*n) for n in Kopplungskapazitäten])

nu_m_theo = np.array([1 / ( 2 * np.pi * unp.sqrt( L * ( (1/C + 2/n)**(-1) + Csp) ) ) for n in C_K_Error])
nu_p_theo = 1 / ( 2 * np.pi * np.sqrt( L * ( C + Csp) ) )
nu_p_theo1 = np.array([nu_p_theo, nu_p_theo, nu_p_theo, nu_p_theo, nu_p_theo, nu_p_theo, nu_p_theo, nu_p_theo ])
nu_m_theo1 = np.array([unp.nominal_values(n) for n in nu_m_theo])

Differenzen = np.array([ Stop[i]-n for i,n in enumerate(Start)])
Zeitverhältniss = np.array([n/Sweep_Zeit for n in Zeiten])
Abstände = np.array([Differenzen[i]*n for i,n in enumerate(Zeitverhältniss)])

nu_m_expC = np.array([n + Abstände[i] for i,n in enumerate(Start)])
nu_m_expC1 = nu_m_expC[::-1]

plt.plot(Kopplungskapazitäten, unp.nominal_values(nu_m_expC1)*10**(-3), 'bx', label = r'Messung 3.3.1: $\nu_{-}$')
plt.plot(Kopplungskapazitäten, nu_m_theo1*10**(-3), 'rx', label = r'Theoriewerte: $\nu_{-}$')
plt.plot(Kopplungskapazitäten, Nü_positiv*10**(-3), 'mx', label = r'Messung 3.3.1: $\nu_{+}$')
plt.plot(Kopplungskapazitäten, nu_p_theo1*10**(-3), 'yx', label = r'Theoriewerte: $\nu_{+}$')
plt.xlabel(r'$Kopplungskapazität \,\, C_k \,\, in \,\, \mathrm{F}$')
plt.ylabel(r'$Frequenzen \,\, \nu \,\, in \,\, \mathrm{kHz}$')

plt.legend(loc = 'best')
plt.savefig('Messungc_Plot1.pdf')
plt.show()

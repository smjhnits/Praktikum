import numpy as np
from scipy.stats import sem
from uncertainties import ufloat
import uncertainties.unumpy as unp
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

Spektral_gelb_komplett = np.array([8.3, 8, 7.65, 7.3, 6.6, 6.4, 6.15, 5.9, 5.5,
                                   5.1, 4.8, 4.3, 3.9, 2.7, 2, 1.4, 0.7, 0.45,
                                   0.32, 0.14, 0.05, 0])
Spannung_gelb_komplett = np.array([-19.15, -17.05, -15.01, -13.02, -10.99, -9.99,
                                   -9.0, -8.05, -7.05, -6.02, -5.05, -4.04, -3.05,
                                   -2.02, -1.01, -0.5, 0, 0.1, 0.2, 0.31, 0.4, 0.55])

Spannung_gelb = Spannung_gelb_komplett[16:21]
Spektral_gelb = Spektral_gelb_komplett[16:21]

Spektral_grün = np.array([1.2, 1, 0.5, 0.8, 0.22, 0.09, 0.02, 0])
Spannung_grün = np.array([0.01, 0.1, 0.3, 0.2, 0.4, 0.5, 0.6, 0.64])

Spektral_blau_grün = np.array([0.3, 0.29, 0.22, 0.2, 0.2, 0.18, 0.15, 0.12, 0.08,
                               0.04, 0.03, 0.02, 0.01, 0.01, 0])
Spannung_blau_grün = np.array([0.01, 0.05, 0.1, 0.151, 0.202, 0.253, 0.3, 0.35,
                               0.45, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8])

Spektral_blau = np.array([7.4, 6.6, 6.4, 5.6, 4.0, 3.2, 2.3, 1.4, 0.6, 0.33, 0.1, 0])
Spannung_blau = np.array([0.01, 0.1, 0.21, 0.31, 0.4, 0.5, 0.6, 0.7, 0.81, 0.9,
                          1.0, 1.07])

Spektral_UV1 = np.array([2.7, 2.4, 2.2, 1.9, 1.7, 1.1, 0.7, 0.52, 0.28, 0.16,
                         0.08, 0.01, 0])
Spannung_UV1 = np.array([0.001, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9,
                         1, 1.1 ,1.12])

Spektral_UV2 = np.array([0.3, 0.26, 0.23, 0.19, 0.16, 0.12, 0.09, 0.06, 0.04,
                         0.02, 0])
Spannung_UV2 = np.array([0.001, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])

#Messung a

def f(x, A, B):
    return A * x + B

def Parameter(Spannung, Spektral):
    params, covariance = curve_fit(f, np.sqrt(Spannung), Spektral)
    a = np.array([params[0], params[1]])
    return

P_ge, covariance_ge = curve_fit(f, Spannung_gelb, np.sqrt(Spektral_gelb))
P_gr, covariance_gr = curve_fit(f, Spannung_grün, np.sqrt(Spektral_grün))
P_b_g, covariance_b_g = curve_fit(f, Spannung_blau_grün, np.sqrt(Spektral_blau_grün))
P_b, covariance_b = curve_fit(f, Spannung_blau, np.sqrt(Spektral_blau))
P_UV1, covariance_UV1 = curve_fit(f, Spannung_UV1, np.sqrt(Spektral_UV1))
P_UV2, covariance_UV2 = curve_fit(f, Spannung_UV2, np.sqrt(Spektral_UV2))

print(P_ge)

x_plot = np.linspace(-20, 20, 1000)
y_plot = np.zeros(1000)

x_gelb = -P_ge[1]/P_ge[0]
x_grün = -P_gr[1]/P_gr[0]
x_blau = -P_b[1]/P_b[0]
x_b_g = -P_b_g[1]/P_b_g[0]
x_UV1 = -P_UV1[1]/P_UV1[0]
x_UV2 = -P_UV2[1]/P_UV2[0]


plt.clf()
plt.plot(Spannung_gelb, np.sqrt(Spektral_gelb), 'kx', label = 'Messwerte gelbe Spektralfarbe')
plt.plot(x_plot, f(x_plot, *P_ge), 'r-', label = 'Lineare Regression')
plt.plot(x_plot, y_plot, 'k--')
plt.plot(x_gelb, 0, 'bo', label = 'Nullstelle der linearen Regression',)
plt.xlabel(r'angelegte Spannung $U$ in $V$')
plt.ylabel(r'gemessene Stromstärke $I$ in $A$ ')
plt.xlim(-0.1, 0.8)
plt.ylim(-0.1, 1)
plt.legend(loc = 'best')
plt.savefig('gelbe_Spektrallinie.pdf')

plt.clf()
plt.plot(Spannung_grün, np.sqrt(Spektral_grün), 'kx', label = 'Messwerte grüne Spektralfarbe')
plt.plot(x_plot, f(x_plot, *P_gr), 'r-', label = 'Lineare Regression')
plt.plot(x_plot, y_plot, 'k--')
plt.plot(x_grün, 0, 'bo', label = 'Nullstelle der linearen Regression',)
plt.xlabel(r'angelegte Spannung $U$ in $V$')
plt.ylabel(r'$\sqrt{I}$ in $A$ ')
plt.xlim(0, 0.8)
plt.ylim(-0.2, 1.8)
plt.legend(loc = 'best')
plt.savefig('gruene_Spektrallinie.pdf')


plt.clf()
plt.plot(Spannung_blau_grün, np.sqrt(Spektral_blau_grün), 'kx', label = 'Messwerte blau-grüne Spektralfarbe')
plt.plot(x_plot, f(x_plot, *P_b_g), 'r-', label = 'Lineare Regression')
plt.plot(x_plot, y_plot, 'k--')
plt.plot(x_b_g, 0, 'bo', label = 'Nullstelle der linearen Regression',)
plt.xlabel(r'angelegte Spannung $U$ in $V$')
plt.ylabel(r'$\sqrt{I}$ in $A$ ')
plt.xlim(0, 0.9)
plt.ylim(-0.1, 1)
plt.legend(loc = 'best')
plt.savefig('blau_gruene_Spektrallinie.pdf')

plt.clf()
plt.plot(Spannung_blau, np.sqrt(Spektral_blau), 'kx', label = 'Messwerte blaue Spektralfarbe')
plt.plot(x_plot, f(x_plot, *P_b), 'r-', label = 'Lineare Regression')
plt.plot(x_plot, y_plot, 'k--')
plt.plot(x_blau, 0, 'bo', label = 'Nullstelle der linearen Regression',)
plt.xlabel(r'angelegte Spannung $U$ in $V$')
plt.ylabel(r'$\sqrt{I}$ in $A$ ')
plt.xlim(0, 1.3)
plt.ylim(-0.2, 3)
plt.legend(loc = 'best')
plt.savefig('blaue_Spektrallinie.pdf')


plt.clf()
plt.plot(Spannung_UV1, np.sqrt(Spektral_UV1), 'kx', label = 'Messwerte der Spektralfarbe UV1')
plt.plot(x_plot, f(x_plot, *P_UV1), 'r-', label = 'Lineare Regression')
plt.plot(x_plot, y_plot, 'k--')
plt.plot(x_UV1, 0, 'bo', label = 'Nullstelle der linearen Regression',)
plt.xlabel(r'angelegte Spannung $U$ in $V$')
plt.ylabel(r'$\sqrt{I}$ in $A$ ')
plt.xlim(0, 1.2)
plt.ylim(-0.2, 2)
plt.legend(loc =  'best')
plt.savefig('UV1_Spektrallinie.pdf')


plt.clf()
plt.plot(Spannung_UV2, np.sqrt(Spektral_UV2), 'kx', label = 'Messwerte der Spektralfarbe UV1')
plt.plot(x_plot, f(x_plot, *P_UV2), 'r-', label = 'Lineare Regression')
plt.plot(x_plot, y_plot, 'k--')
plt.plot(x_UV2, 0, 'bo', label = 'Nullstelle der linearen Regression',)
plt.xlabel(r'angelegte Spannung $U$ in $V$')
plt.ylabel(r'$\sqrt{I}$ in $A$ ')
plt.xlim(-0.1, 1.2)
plt.ylim(-0.1, 0.8)
plt.legend(loc = 'best')
plt.savefig('UV2_Spektrallinie.pdf')


#Messung b

U_g = np.array([x_gelb, x_grün, x_blau, x_b_g, x_UV1, x_UV2])
Frequenzen = np.array([577.579, 546, 492, 435, 405, 366])

xf_plot = np.linspace(350, 600, 1000)

NoPlan, covariances_np = curve_fit(f, Frequenzen, U_g)

plt.clf()
plt.plot(Frequenzen, U_g, 'kx', label = r'$U_{\mathrm{g}}$')
plt.plot(xf_plot, f(xf_plot, *NoPlan), 'r-', label = 'lineare Regression')
plt.xlabel(r'$\nu$ in Hz')
plt.ylabel(r'$U_{\mathrm{g}}$ in V')
plt.legend(loc = 'best')
plt.savefig('U_g_gegen_Frequenz')

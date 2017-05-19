import numpy as np
from scipy.stats import sem
from uncertainties import ufloat
import uncertainties.unumpy as unp
import matplotlib.pyplot as plt
import scipy.constants as sc
from scipy.optimize import curve_fit

Spektral_gelb_komplett = np.array([8.3, 8, 7.65, 7.3, 6.6, 6.4, 6.15, 5.9, 5.5,
                                   5.1, 4.8, 4.3, 3.9, 2.7, 2, 1.4, 0.7, 0.45,
                                   0.32, 0.14, 0.05, 0]) *10**(-9)
Spannung_gelb_komplett = np.array([-19.15, -17.05, -15.01, -13.02, -10.99, -9.99,
                                   -9.0, -8.05, -7.05, -6.02, -5.05, -4.04, -3.05,
                                   -2.02, -1.01, -0.5, 0, 0.1, 0.2, 0.31, 0.4, 0.55])

Spannung_gelb = Spannung_gelb_komplett[16:21]
Spektral_gelb = Spektral_gelb_komplett[16:21]

Spektral_grün = np.array([1.2, 1, 0.5, 0.8, 0.22, 0.09, 0.02, 0])*10**(-9)
Spannung_grün = np.array([0.01, 0.1, 0.3, 0.2, 0.4, 0.5, 0.6, 0.64])

Spektral_blau_grün = np.array([0.3, 0.29, 0.22, 0.2, 0.2, 0.18, 0.15, 0.12, 0.08,
                               0.04, 0.03, 0.02, 0.01, 0.01, 0])*10**(-9)
Spannung_blau_grün = np.array([0.01, 0.05, 0.1, 0.151, 0.202, 0.253, 0.3, 0.35,
                               0.45, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8])

Spektral_blau = np.array([7.4, 6.6, 6.4, 5.6, 4.0, 3.2, 2.3, 1.4, 0.6, 0.33, 0.1, 0])*10**(-9)
Spannung_blau = np.array([0.01, 0.1, 0.21, 0.31, 0.4, 0.5, 0.6, 0.7, 0.81, 0.9,
                          1.0, 1.07])

Spektral_UV1 = np.array([2.7, 2.4, 2.2, 1.9, 1.7, 1.1, 0.7, 0.52, 0.28, 0.16,
                         0.08, 0.01, 0])*10**(-9)
Spannung_UV1 = np.array([0.001, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9,
                         1, 1.1 ,1.12])

Spektral_UV2 = np.array([0.3, 0.26, 0.23, 0.19, 0.16, 0.12, 0.09, 0.06, 0.04,
                         0.02, 0])*10**(-9)
Spannung_UV2 = np.array([0.001, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])

#Messung a

def f(x, A, B):
    return A * x + B

def Parameter(Spannung, Spektral):
    params, covariance = curve_fit(f, np.sqrt(Spannung), Spektral)
    a = np.array([params[0], params[1]])
    return

P_ge, covariance_ge = curve_fit(f, Spannung_gelb, np.sqrt(Spektral_gelb))
errors_ge = np.sqrt(np.diag(covariance_ge))

P_gr, covariance_gr = curve_fit(f, Spannung_grün, np.sqrt(Spektral_grün))
errors_gr = np.sqrt(np.diag(covariance_gr))

P_b_g, covariance_b_g = curve_fit(f, Spannung_blau_grün, np.sqrt(Spektral_blau_grün))
errors_b_g = np.sqrt(np.diag(covariance_b_g))

P_b, covariance_b = curve_fit(f, Spannung_blau, np.sqrt(Spektral_blau))
errors_b = np.sqrt(np.diag(covariance_b))

P_UV1, covariance_UV1 = curve_fit(f, Spannung_UV1, np.sqrt(Spektral_UV1))
errors_UV1 = np.sqrt(np.diag(covariance_UV1))

P_UV2, covariance_UV2 = curve_fit(f, Spannung_UV2, np.sqrt(Spektral_UV2))
errors_UV2 = np.sqrt(np.diag(covariance_UV2))

x_plot = np.linspace(-20, 20, 1000)
y_plot = np.zeros(1000)

#print("Parameter gelb: ",      ufloat(P_ge[0], errors_ge[0]),   ufloat(P_ge[1], errors_ge[1]),   '\n')
#print("Parameter grün: ",      ufloat(P_gr[0], errors_gr[0]),   ufloat(P_gr[1], errors_gr[1]),   '\n')
#print("Parameter blau: ",      ufloat(P_b[0], errors_b[0]),     ufloat(P_b[1], errors_b[1]),     '\n')
#print("Parameter blau-grün: ", ufloat(P_b_g[0], errors_b_g[0]), ufloat(P_b_g[1], errors_b_g[1]), '\n')
#print("Parameter UV1: ",       ufloat(P_UV1[0], errors_UV1[0]), ufloat(P_UV1[1], errors_UV1[1]), '\n')
#print("Parameter UV2: ",       ufloat(P_UV2[0], errors_UV2[0]), ufloat(P_UV2[1], errors_UV2[1]), '\n')

x_gelb = - ufloat(P_ge[1], errors_ge[1])/ufloat(P_ge[0], errors_ge[0])
#print("Schnittpunkt gelb: ", x_gelb, '\n')
x_grün = - ufloat(P_gr[1], errors_gr[1])/ufloat(P_gr[0], errors_gr[0])
#print("Schnittpunkt grün: ", x_grün, '\n')
x_blau = - ufloat(P_b[1], errors_b[1])/ufloat(P_b[0], errors_b[0])
#print("Schnittpunkt blau: ", x_blau, '\n')
x_b_g = - ufloat(P_b_g[1], errors_b_g[1])/ufloat(P_b_g[0], errors_b_g[0])
#print("Schnittpunkt blau-grün: ", x_b_g, '\n')
x_UV1 = - ufloat(P_UV1[1], errors_UV1[1])/ufloat(P_UV1[0], errors_UV1[0])
#print("Schnittpunkt UV1: ", x_UV1, '\n')
x_UV2 = - ufloat(P_UV2[1], errors_UV2[1])/ufloat(P_UV2[0], errors_UV2[0])
#print("Schnittpunkt UV2: ", x_UV2, '\n')

plt.clf()
plt.plot(Spannung_gelb, np.sqrt(Spektral_gelb)*10**(4), 'kx', label = r'Messwerte gelbe Spektralfarbe')
plt.plot(x_plot, f(x_plot, *P_ge)*10**(4), 'r-', label = 'Lineare Regression')
plt.plot(x_plot, y_plot, 'k--')
plt.plot(unp.nominal_values(x_gelb), 0, 'bo', label = 'Nullstelle der linearen Regression',)
plt.xlabel(r' $U$ in $\mathrm{V}$')
plt.ylabel(r' $\sqrt{I}\cdot 10^4$ in $\mathrm{A}$ ')
plt.xlim(-0.1, 0.7)
plt.ylim(-0.1, 0.4)
plt.legend(loc = 'best')
#plt.savefig('gelbe_Spektrallinie.pdf')

plt.clf()
plt.plot(Spannung_grün, np.sqrt(Spektral_grün)*10**(4), 'kx', label = 'Messwerte grüne Spektralfarbe')
plt.plot(x_plot, f(x_plot, *P_gr)*10**(4), 'r-', label = 'Lineare Regression')
plt.plot(x_plot, y_plot, 'k--')
plt.plot(unp.nominal_values(x_grün), 0, 'bo', label = 'Nullstelle der linearen Regression',)
plt.xlabel(r' $U$ in $\mathrm{V}$')
plt.ylabel(r'$\sqrt{I}\cdot 10^4$ in $\mathrm{A}$ ')
plt.xlim(0, 0.8)
plt.ylim(-0.1, 0.5)
plt.legend(loc = 'best')
#plt.savefig('gruene_Spektrallinie.pdf')


plt.clf()
plt.plot(Spannung_blau_grün, np.sqrt(Spektral_blau_grün)*10**(4), 'kx', label = 'Messwerte blau-grüne Spektralfarbe')
plt.plot(x_plot, f(x_plot, *P_b_g)*10**(4), 'r-', label = 'Lineare Regression')
plt.plot(x_plot, y_plot, 'k--')
plt.plot(unp.nominal_values(x_b_g), 0, 'bo', label = 'Nullstelle der linearen Regression',)
plt.xlabel(r' $U$ in $\mathrm{V}$')
plt.ylabel(r'$\sqrt{I}\cdot 10^4$ in $\mathrm{A}$ ')
plt.xlim(0, 0.9)
plt.ylim(-0.05, 0.2)
plt.legend(loc = 'best')
#plt.savefig('blau_gruene_Spektrallinie.pdf')

plt.clf()
plt.plot(Spannung_blau, np.sqrt(Spektral_blau)*10**(4), 'kx', label = 'Messwerte blaue Spektralfarbe')
plt.plot(x_plot, f(x_plot, *P_b)*10**(4), 'r-', label = 'Lineare Regression')
plt.plot(x_plot, y_plot, 'k--')
plt.plot(unp.nominal_values(x_blau), 0, 'bo', label = 'Nullstelle der linearen Regression',)
plt.xlabel(r' $U$ in $\mathrm{V}$')
plt.ylabel(r'$\sqrt{I}\cdot 10^4$ in $\mathrm{A}$ ')
plt.xlim(0, 1.3)
plt.ylim(-0.2, 1.1)
plt.legend(loc = 'best')
#plt.savefig('blaue_Spektrallinie.pdf')


plt.clf()
plt.plot(Spannung_UV1, np.sqrt(Spektral_UV1)*10**(4), 'kx', label = 'Messwerte der Spektralfarbe UV1')
plt.plot(x_plot, f(x_plot, *P_UV1)*10**(4), 'r-', label = 'Lineare Regression')
plt.plot(x_plot, y_plot, 'k--')
plt.plot(unp.nominal_values(x_UV1), 0, 'bo', label = 'Nullstelle der linearen Regression',)
plt.xlabel(r' $U$ in $\mathrm{V}$')
plt.ylabel(r'$\sqrt{I}\cdot 10^4$ in $\mathrm{A}$ ')
plt.xlim(0, 1.2)
plt.ylim(-0.1, 0.6)
plt.legend(loc =  'best')
#plt.savefig('UV1_Spektrallinie.pdf')


plt.clf()
plt.plot(Spannung_UV2, np.sqrt(Spektral_UV2)*10**(4), 'kx', label = 'Messwerte der Spektralfarbe UV2')
plt.plot(x_plot, f(x_plot, *P_UV2)*10**(4), 'r-', label = 'Lineare Regression')
plt.plot(x_plot, y_plot, 'k--')
plt.plot(unp.nominal_values(x_UV2), 0, 'bo', label = 'Nullstelle der linearen Regression',)
plt.xlabel(r' $U$ in $\mathrm{V}$')
plt.ylabel(r'$\sqrt{I}\cdot 10^4$ in $\mathrm{A}$ ')
plt.xlim(-0.1, 1.2)
plt.ylim(-0.05, 0.22)
plt.legend(loc = 'best')
#plt.savefig('UV2_Spektrallinie.pdf')


#Messung b

U_g = np.array([unp.nominal_values(x_gelb), unp.nominal_values(x_grün),
                unp.nominal_values(x_b_g), unp.nominal_values(x_blau),
                unp.nominal_values(x_UV1), unp.nominal_values(x_UV2)])
Wellenlängen = np.array([577.579, 546, 492, 435, 405, 365]) * 10**(-9)
Frequenzen = np.array([sc.c/n for n in Wellenlängen])

def g(x, A, B):
    return A * x + B


xf_plot = np.linspace(4.5*10**(14), 9*10**(14), 1000)

NoPlan, covariances_np = curve_fit(g, Frequenzen, U_g)
errors_np = np.sqrt(np.diag(covariances_np))

plt.clf()
plt.plot(Frequenzen, U_g, 'kx', label = r'$U_{\mathrm{g}}$')
plt.plot(xf_plot, g(xf_plot, *NoPlan), 'r-', label = 'lineare Regression')
plt.xlabel(r'$\nu$ in $\mathrm{Hz}$')
plt.ylabel(r'$U_{\mathrm{g}}$ in $\mathrm{V}$')
plt.legend(loc = 'best')
plt.ylim(0.4, 1.4)
plt.xlim(5*10**(14), 8.5*10**(14))
#plt.savefig('U_g_gegen_Frequenz.pdf')

Steigung = ufloat(NoPlan[0], errors_np[0])
Achsenabschnitt = ufloat(NoPlan[1], errors_np[1])

Steigung_eV = Steigung / sc.e
Austrittsarbeit = Achsenabschnitt * sc.e

#print("Die Steigung der Geraden beträgt: ", Steigung, '\n' )
#print("In Elektronenvolt: ", Steigung_eV, '\n')
#print("Austrittsarbeit: ", Austrittsarbeit , '\n')
#print("In Elektronenvolt: ", Austrittsarbeit / sc.e, '\n')

#Messung c

plt.clf()
plt.plot(Spannung_gelb_komplett, Spektral_gelb_komplett*10**9, 'kx', label = 'Messwerte gelbe Spektralfarbe')
plt.xlabel(r' $U$ in $\mathrm{V}$')
plt.ylabel(r'$I\cdot 10^9$ in $\mathrm{A}$ ')
plt.legend(loc = 'best')
#plt.savefig('gelbe_Spektrallinie_komplett.pdf')

plt.clf()
plt.plot(Spannung_gelb_komplett, Spektral_gelb_komplett*10**9, 'kx', label = 'Messwerte gelbe Spektralfarbe')
plt.xlabel(r' $U$ in $\mathrm{V}$')
plt.ylabel(r'$I\cdot 10^9$ in $\mathrm{A}$ ')
plt.xlim(-3, 1)
plt.ylim(0, 3)
plt.axvline(0)
plt.legend(loc = 'best')
plt.savefig('gelbe_Spektrallinie_komplett2.pdf')

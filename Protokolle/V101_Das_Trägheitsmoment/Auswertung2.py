import numpy as np
from scipy.stats import sem
from uncertainties import ufloat
import uncertainties.unumpy as unp
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

Zeiten = np.genfromtxt("Eigentraeg.txt", unpack = True)

MasseZ = ufloat(0.261545, 0)
HöheZ = ufloat(0.02, 0)
RadiusZ = ufloat(0.0225, 0)

Längen = Zeiten.T[0]
Längen = Längen.T

Zeiten = Zeiten.T[1:4]
Zeiten = Zeiten.T/5

Mittelwerte = np.array([np.mean(row) for row in Zeiten])
Fehler = np.array([np.std(row, ddof = 1) for row in Zeiten])
s = 1/np.sqrt(len(Zeiten[0]))
Fehler = s*Fehler

u = np.array([ufloat(x, Fehler[index]) for index, x in np.ndenumerate(Mittelwerte)])

#print(Längen)
#print(u)

TqM = np.array(unp.nominal_values(u**2))
TqF = np.array(unp.std_devs(u**2))
Lq = Längen**2

#print(TqM)
#print(Lq)

def f(x, a, b):
    return a * x + b

params, covariance = curve_fit(f, Lq, TqM)

errors = np.sqrt(np.diag(covariance))

#print('a=', params[0], '+/-', errors[0])
#print('b=', params[1], '+/-', errors[1])

x_plot = np.linspace(0.001, 0.095)

plt.plot(Lq, TqM, 'rx', label="Differenzen")
plt.plot(x_plot, f(x_plot, *params), 'b-', label='linearer Fit', linewidth=1)
plt.legend(loc="best")
plt.title(r"$T^2 \, gegen \, r^2$")
plt.xlabel(r"$r^2 \, in \, m^2$")
plt.ylabel(r"$T^2 \, in \, s^2$")

plt.savefig("plot1.pdf")
plt.show()

Steigung = ufloat(params[0], errors[0])
Abschnitt = ufloat(params[1], errors[1])

Iz = MasseZ*((RadiusZ**2)/4 + (HöheZ**2)/12)

WRGd = 8 * (np.pi**2) * MasseZ/Steigung
Id = Abschnitt * WRGd/ (4 * np.pi**2) - 2*Iz

#print(Iz)
#print(WRGd)
#print(Id)

#np.savetxt("WRGdyn.txt", np.column_stack([WRGd.n, WRGd.s]), header = "dynamische Winkelrichtgröße")

def linregress(x, y):
    x = np.array(x)
    y = np.array(y)

    n = len(y)
    d = n * np.sum(x**2) - (np.sum(x))**2

    m = (n * np.sum(x * y) - np.sum(x) * np.sum(y)) / d
    b = (np.sum(x**2) * np.sum(y) - np.sum(x) * np.sum(x * y)) / d

    #print(m, b)

linregress(Lq, TqM)

import numpy as np
from scipy.stats import sem
from uncertainties import ufloat
import uncertainties.unumpy as unp
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

Frequenzen = np.array([390, 395, 400, 405, 410, 415, 420, 430, 440, 460, 480, 500, 550, 600, 700, 800, 1000, 1200, 1500, 2000, 3000, 5000, 10000, 20000, 30000, 370, 360, 340, 320, 270, 200, 100, 20])
BrückenSP  = np.array([53, 84, 94, 136, 140, 166, 184, 210, 254, 328, 384, 468, 590, 740, 1020, 1150, 1450, 1660, 1860, 2000, 2140, 2180, 2040, 1660, 1180, 44, 78, 172, 260, 524, 1000, 1960, 2480])
SpeiseSP   = np.array([165, 165, 165, 165, 160, 160, 160, 160, 155, 150, 145, 140, 125, 120, 110, 95, 75, 68, 54, 41, 28.5, 17.5, 9, 6, 5.5, 170, 170, 180, 180, 200, 220, 255, 270 ])

R = 1000
C = 415.7 * 10**(-9)

BrückenSP = BrückenSP * 10**(-3)
BrückenSP /= 2
BrückenSP /= np.sqrt(2)

SpeiseSpkorrektur = 1.6

SpeiseSP  /= 100

v0 = 1 / (R * C * 2 * np.pi)

xAchse = Frequenzen / v0
yAchse = BrückenSP / SpeiseSP

def f(x):
    return unp.sqrt( 1/9*((x**2-1)**2/((1-x**2)**2+9*x**2)))

laufvariabel = np.linspace(1e-1, 210, 10000)

Werteneu = xAchse[0:8]
print(Werteneu)

plt.plot(xAchse, yAchse, "bx", label = "Funktionswerte")
plt.plot(laufvariabel, f(laufvariabel), "r-", label = "Funktionsfit")
plt.legend( loc = "best")
plt.xlabel(r'$\mathrm{\nu} / \mathrm{\nu_0}$' )
plt.ylabel(r'$\mathrm{U_{Br}} / \mathrm{U_{Sp}}$')
plt.ylim(0, 0.4)
plt.xscale("log")
#plt.show()

plt.clf()

plt.plot(xAchse, yAchse, "bx", label = "Funktionswerte")
plt.plot(laufvariabel, f(laufvariabel), "r-", label = "Funktionsfit")
plt.legend( loc = "best")
plt.xlabel(r'$\mathrm{\nu} / \mathrm{\nu_0}$' )
plt.ylabel(r'$\mathrm{U_{Br}} / \mathrm{U_{Sp}}$')
plt.xscale("log")
#plt.show()

U2 = (0.018 / 2 / np.sqrt(2)) / f(2)
k = U2 / 1.6
print(U2, k)

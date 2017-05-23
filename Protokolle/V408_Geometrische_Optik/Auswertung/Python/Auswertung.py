import numpy as np
from scipy.stats import sem
from uncertainties import ufloat
import uncertainties.unumpy as unp
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import scipy.constants as const
from uncertainties.unumpy import (nominal_values as noms, std_devs as stds)


def Brennweite_Bessel(e, d):
    return (e**2- d**2) / (4 * e)

def function(x, a, b):
    return a * x + b

def Brennweite(b, g):
    return 1 / (1/g + 1/b)

def Abbildungssgesetz(b, g):
    return b / g

G = ufloat(2.9, 0.05) * 10**-2 # Gegenstandsgröße
# Ablesefehler wird angegeben mit 0.05cm
err = np.ones(10) * 0.05 * 10**(-2)
err_5 = np.ones(5) * 0.05 * 10**(-2)
err_6 = np.ones(6) * 0.05 * 10**(-2)


# Messung 1 Brennweite bekannt 100mmAngaben in cm
print(len(np.linspace(15, 60, 10)), np.ones(10))

g_1 = unp.uarray(np.linspace(15, 60, 10) * 10**(-2), err) # Gegenstandsweite erste Messung cm in m
b_1 = unp.uarray(np.array([27.8, 18.4, 15.3, 13.85, 13.1, 12.5, 12.05, 11.7, 11.4, 11.25]) * 10**(-2), err) # Bildweite erste Messung cm in m
B_1 = unp.uarray(np.array([0, 2.8, 1.9, 1.45, 1.15, 0.95])* 10**(-2), err_6) # cm in m

# Messung bei unbekannter Brennweite

g_2 = unp.uarray(np.linspace(15, 60, 10) * 10**(-2), err)
b_2 = unp.uarray(np.array([18.55, 14.3, 12.5, 11.7, 11.1, 10.5, 10.3, 10.1, 9.95, 9.9]) * 10**(-2), err)

# Messung nach Bessel

b_plus_g_3 = unp.uarray(np.array([40, 45, 50, 52.5, 55, 57.5, 60, 62.5, 65, 70]) * 10**(-2), err)
g_eins_3 = unp.uarray(np.array([16.6, 14.15, 13.2, 12.9, 12.6, 12.4, 12.2, 12.2, 12, 11.8]) * 10**(-2), err) # erster Brennpkt
b_eins_3 = b_plus_g_3 - g_eins_3
g_zwei_3 = unp.uarray(np.array([23.7, 31.05, 37, 40, 42.6, 45.35, 48, 50.75, 53.35, 58.45]) * 10**(-2), err) # zweiter Brennpkt
b_zwei_3 = b_plus_g_3 - g_zwei_3

d_eins_3 = g_eins_3 - b_eins_3
d_zwei_3 = g_zwei_3 - b_zwei_3

# chromatische Abberation

b_plus_g_4 = unp.uarray(np.linspace(45, 65, 5) * 10**(-2), err_5)
g_eins_rot_4 = unp.uarray(np.array([14.35, 13.2, 12.6, 12.35, 12]) * 10**(-2), err_5)
b_eins_rot_4 = b_plus_g_4 - g_eins_rot_4
g_zwei_rot_4 = unp.uarray(np.array([31, 37, 42.5, 48.1, 53.5]) * 10**(-2), err_5)
b_zwei_rot_4 = b_plus_g_4 - g_zwei_rot_4
d_eins_rot_4 = g_eins_rot_4 - b_eins_rot_4
d_zwei_rot_4 = g_zwei_rot_4 - b_zwei_rot_4

g_eins_blau_4 = np.array([14.1, 13.25, 12.7, 12.4, 12.1]) * 10**(-2)
b_eins_blau_4 = b_plus_g_4 - g_eins_blau_4
g_zwei_blau_4 = np.array([31.2, 37.1, 42.7, 48.2, 53.3]) * 10**(-2)
b_zwei_blau_4 = b_plus_g_4 - g_zwei_blau_4
d_eins_blau_4 = g_eins_blau_4 - b_eins_blau_4
d_zwei_blau_4 = g_zwei_blau_4 - b_zwei_blau_4

# Nach Abbe Streulinse -100 mm, Sammellinse 100mm

B_5 = unp.uarray(np.array([5.2, 3.9, 2.8, 2.2, 1.8, 1.5, 1.3, 1.2, 1, 0.95]) * 10**(-2), err)
b_plus_g_5 = unp.uarray(np.array([70, 67.3, 66.6, 68.1, 71.4, 75, 79, 83.3, 87.5, 92.1]) * 10**(-2), err)
g_5 = unp.uarray(np.array([17, 20, 25, 30, 35, 40, 45, 50, 55, 60]) * 10**(-2), err)
b_5 = b_plus_g_5 - g_5

# Abbildungsgesetz


V_aus_gb = Abbildungssgesetz(b_1, g_1)

print('Abbildungsgesetz aus g und b: ', V_aus_gb)
print('Mittelwert V_gb: ', np.mean(V_aus_gb))
print(noms(B_1), len(noms(B_1)))
print(noms(B_1)[1:len(noms(B_1))] / G, stds(B_1)[1:len(noms(B_1))] / G)

B_G = unp.uarray(noms(B_1[1:len(noms(B_1))] / G), stds(B_1[1:len(noms(B_1))] / G))

print('Aus abgemessenen Werten B und G: ', B_G)
print('Mittelwert V: ', np.mean(B_G))

# Linsengleichung

brennpkt_1 = Brennweite(b_1, g_1)

print('Brennpunkt: ', brennpkt_1)
print('Mittelwert f_1: ', np.mean(brennpkt_1))

plt.clf()
plt.plot(np.array([0, noms(g_1)[0]]), np.array([noms(b_1)[0], 0]), 'b-')#, label=r'Messung 1')
plt.plot(np.array([0, noms(g_1)[1]]), np.array([noms(b_1)[1], 0]), 'b-')#, label=r'Messung 2')
plt.plot(np.array([0, noms(g_1)[2]]), np.array([noms(b_1)[2], 0]), 'b-')#, label=r'Messung 3')
plt.plot(np.array([0, noms(g_1)[3]]), np.array([noms(b_1)[3], 0]), 'b-')#, label=r'Messung 4')
plt.plot(np.array([0, noms(g_1)[4]]), np.array([noms(b_1)[4], 0]), 'b-')#, label=r'Messung 5')
plt.plot(np.array([0, noms(g_1)[5]]), np.array([noms(b_1)[5], 0]), 'b-')#, label=r'Messung 6')
plt.plot(np.array([0, noms(g_1)[6]]), np.array([noms(b_1)[6], 0]), 'b-')#, label=r'Messung 7')
plt.plot(np.array([0, noms(g_1)[7]]), np.array([noms(b_1)[7], 0]), 'b-')#, label=r'Messung 8')
plt.plot(np.array([0, noms(g_1)[8]]), np.array([noms(b_1)[8], 0]), 'b-')#, label=r'Messung 9')
plt.plot(np.array([0, noms(g_1)[9]]), np.array([noms(b_1)[9], 0]), 'b-')#, label=r'Messung 10')
plt.plot(np.ones(10) * noms(brennpkt_1), np.linspace(0, 0.3, 10), 'g--', label='Brennpunkt aus Mittelwerten')
plt.plot(np.ones(10) * 0.099, np.linspace(0, 0.3, 10), 'k--', label='Abgelesene Brennweite')
plt.ylabel(r'Bildweite in Metern')
plt.xlabel(r'Gegenstandsweite in Metern, $g_i$ sind äquidistant')
#plt.yticks([noms(b_1)[0], noms(b_1)[1], noms(b_1)[2], noms(b_1)[3], noms(b_1)[4], noms(b_1)[5], #noms(b_1)[6], noms(b_1)[7], noms(b_1)[8], noms(b_1)[9]],
#           [r"$b_1$", r"$b_2$", r"$b_3$" ,r"$b_4$", r"$b_5$", r"$b_6$", r"$b_7$", r"$b_8$", r"$b_9$"])
plt.xticks([noms(g_1)[0], noms(g_1)[1], noms(g_1)[2], noms(g_1)[3], noms(g_1)[4], noms(g_1)[5], noms(g_1)[6], noms(g_1)[7], noms(g_1)[8], noms(g_1)[9]],
          [r"$g_1 = 0.05$", r"$g_2$", r"$g_3$" ,r"$g_4$", r"$g_5$", r"$g_6$", r"$g_7$", r"$g_8$", r"$g_9$", r"$g_{10} = 0.60$"])
plt.legend(loc='best')
plt.grid()
plt.tight_layout()
plt.savefig('Messung1_brennnweite_bekannt.pdf')
#plt.show()

print('schnittpkt abgelesen: ', 'x=0.099(0.003), y=0.094(0.003) Fehler sehr genau mit mauscourser abzulesen')

# unbekannte Brennweite

brennpkt_2 = Brennweite(b_2, g_2)
print('Brennpunkt_2: ', brennpkt_2)
print('Mittelwert f_2: ', np.mean(brennpkt_2))


plt.clf()
plt.plot(np.array([0, noms(g_2)[0]]), np.array([noms(b_2)[0], 0]), 'b-')#, label=r'Messung 1')
plt.plot(np.array([0, noms(g_2)[1]]), np.array([noms(b_2)[1], 0]), 'b-')#, label=r'Messung 2')
plt.plot(np.array([0, noms(g_2)[2]]), np.array([noms(b_2)[2], 0]), 'b-')#, label=r'Messung 3')
plt.plot(np.array([0, noms(g_2)[3]]), np.array([noms(b_2)[3], 0]), 'b-')#, label=r'Messung 4')
plt.plot(np.array([0, noms(g_2)[4]]), np.array([noms(b_2)[4], 0]), 'b-')#, label=r'Messung 5')
plt.plot(np.array([0, noms(g_2)[5]]), np.array([noms(b_2)[5], 0]), 'b-')#, label=r'Messung 6')
plt.plot(np.array([0, noms(g_2)[6]]), np.array([noms(b_2)[6], 0]), 'b-')#, label=r'Messung 7')
plt.plot(np.array([0, noms(g_2)[7]]), np.array([noms(b_2)[7], 0]), 'b-')#, label=r'Messung 8')
plt.plot(np.array([0, noms(g_2)[8]]), np.array([noms(b_2)[8], 0]), 'b-')#, label=r'Messung 9')
plt.plot(np.array([0, noms(g_2)[9]]), np.array([noms(b_2)[9], 0]), 'b-')#, label=r'Messung 10')
plt.plot(np.ones(10) * noms(brennpkt_2), np.linspace(0, 0.3, 10), 'g--', label='Brennpunkt aus Mittelwerten')
plt.plot(np.ones(10) * 0.081, np.linspace(0, 0.3, 10), 'k--', label='Abgelesene Brennweite')
plt.ylabel(r'Bildweite in Metern')
plt.xlabel(r'Gegenstandsweite in Metern, $g_i$ sind äquidistant')
#plt.yticks([noms(b_1)[0], noms(b_1)[1], noms(b_1)[2], noms(b_1)[3], noms(b_1)[4], noms(b_1)[5], #noms(b_1)[6], noms(b_1)[7], noms(b_1)[8], noms(b_1)[9]],
#           [r"$b_1$", r"$b_2$", r"$b_3$" ,r"$b_4$", r"$b_5$", r"$b_6$", r"$b_7$", r"$b_8$", r"$b_9$"])
plt.xticks([noms(g_2)[0], noms(g_2)[1], noms(g_2)[2], noms(g_2)[3], noms(g_2)[4], noms(g_2)[5], noms(g_2)[6], noms(g_2)[7], noms(g_2)[8], noms(g_2)[9]],
           [r"$g_1 = 0,05$", r"$g_2$", r"$g_3$" ,r"$g_4$", r"$g_5$", r"$g_6$", r"$g_7$", r"$g_8$", r"$g_9$", r"$g_{10} = 0,60$"])
plt.legend(loc='best')
plt.grid()
plt.tight_layout()
plt.savefig('Messung2_unbekannte_brennweite.pdf')
#plt.show()


print('schnittpkt_2 abgelesen: ', 'x=0.081(0.003), y=0.084(0.003) Fehler sehr genau mit mauscourser abzulesen')

# Bessel

brennweite_3 = Brennweite_Bessel(np.append(b_plus_g_3, b_plus_g_3), np.append(d_eins_3, d_zwei_3))

print('Brennweite nach Bessel: ', brennweite_3)
print('Mittelwert Brennweite nach Bessel: ', np.mean(brennweite_3))

# chromatische Abberration

brennweite_rot_4 = Brennweite_Bessel(np.append(b_plus_g_4, b_plus_g_4), np.append(d_eins_rot_4, d_zwei_rot_4))

brennweite_blau_4 = Brennweite_Bessel(np.append(b_plus_g_4, b_plus_g_4), np.append(d_eins_blau_4, d_zwei_blau_4))

print('brennweite_rot: ', np.mean(brennweite_rot_4))
print('brennweite_blau: ', np.mean(brennweite_blau_4))

# Abbe

V_abbe = B_5 / G

params_g, covariance_g = curve_fit(function, 1 + 1 / noms(V_abbe), noms(g_5))
params_b, covariance_b = curve_fit(function, 1 + noms(V_abbe), noms(b_5))


plt.clf()
plt.plot(np.linspace(1.5, 4.5, 10), function(np.linspace(1.5, 4.5, 10), *params_g), 'r-', label = r'lineare Regression')
plt.plot(1 + 1 / noms(V_abbe), noms(g_5), 'kx', label=r'Messdaten')
plt.xlabel(r'(1+$\frac{1}{V}$)')
plt.ylabel(r'g´')
plt.ylim(0, 0.62)
plt.xlim(1.5, 4.2)
plt.legend(loc='best')
plt.grid()
plt.tight_layout()
plt.savefig('Messung_abbe_g.pdf')

plt.clf()
plt.plot(np.linspace(1, 3, 10), function(np.linspace(1, 3, 10), *params_b), 'r-', label = r'lineare Regression')
plt.plot(1 + noms(V_abbe), noms(b_5), 'kx', label=r'Messdaten')
plt.xlabel(r'(1 + V)')
plt.ylabel(r'b´')
plt.xlim(1.3, 2.9)
plt.legend(loc='best')
plt.grid()
plt.tight_layout()
plt.savefig('Messung_abbe_b.pdf')

print('Brennweite_abbe_g, Hauptebene :', params_g)
print('fehler: ', np.sqrt(np.diag(covariance_g)))
print('Brennweite_abbe_b, Hauptebene :', params_b)
print('fehler: ', np.sqrt(np.diag(covariance_b)))

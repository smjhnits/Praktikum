import numpy as np
from scipy.stats import sem
import scipy.constants as const
from uncertainties import ufloat
import uncertainties.unumpy as unp
from uncertainties.unumpy import (nominal_values as noms, std_devs as stds)
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import scipy.misc
from pint import UnitRegistry
from PIL import Image

u = UnitRegistry()
Q_ = u.Quantity

mu_bohr = Q_(const.physical_constants['Bohr magneton'][0], 'joule/tesla')
e_0 = Q_(const.e, 'coulomb')
e_0_dimlos = const.e
m_0 = Q_(const.m_e, 'kg')
m_0_dimlos = const.m_e
mu_0 = Q_(const.mu_0, 'N / A**2')

### Angaben aus Protokoll ###

N_sweep = 11
N_horizontal = 154
N_vertical = 20
R_sweep = Q_(16.39, 'cm').to('m')
R_horizontal = Q_(15.79, 'cm').to('m')
R_vertical = Q_(11.735, 'cm').to('m')

### Quantenzahlen ###

J = 1 / 2
S = 1 / 2
L = 0

### Vertikalfeld ###
I_vertical = Q_(2.28 * 0.1, 'A')

### Messdaten aus Messprogramm c.) ###


frequenz = Q_(np.array([101, 210, 300, 400, 502, 600, 700, 800, 904, 1001]), 'kHz')

I_sweep_1 = Q_(np.array([5.4, 3.75, 5.53, 4.71, 1.13, 1.77, 0.92, 3.55, 3.97, 5.17]) * 0.1, 'A')
I_sweep_2 = Q_(np.array([6.61, 6.32, 9.04, 9.41, 7.10, 8.86, 9.19, 7.51, 7.65, 7.21]) * 0.1, 'A')

I_seven_horizontal = Q_(np.array([0, 29, 31, 53, 93, 105, 128]), 'mA')
I_ten_horizontal_1 = Q_(np.array([126, 140, 148]), 'mA')
I_ten_horizontal_2 = Q_(np.array([164, 188, 216]), 'mA')

### Magnetfelder aus Spulenstrom berechnen ###

def B_Helmholtz(I, N, R):
    return mu_0 * 8 * I * N / (np.sqrt(125) * R)


### ERDMAGNETFELD Vertikalfeld ###

erdmag_vertical = B_Helmholtz(I_vertical, N_vertical, R_vertical).to('millitesla')

print('Erdmagnetfeld: ', erdmag_vertical)

### B-Feld sweep, horizontal ###

B_sweep_1 = B_Helmholtz(I_sweep_1, N_sweep, R_sweep).to('millitesla')
B_sweep_2 = B_Helmholtz(I_sweep_2, N_sweep, R_sweep).to('millitesla')


B_seven_horizontal = B_Helmholtz(I_seven_horizontal, N_horizontal, R_horizontal).to('millitesla')
B_ten_horizontal_1 = B_Helmholtz(I_ten_horizontal_1, N_horizontal, R_horizontal).to('millitesla')
B_ten_horizontal_2 = B_Helmholtz(I_ten_horizontal_2, N_horizontal, R_horizontal).to('millitesla')

### B-Felder an Resonanzstelle ###

B_Resonanz_1 = Q_(np.append(B_sweep_1.magnitude[0:7] + B_seven_horizontal.magnitude, B_sweep_1.magnitude[7:] + B_ten_horizontal_1.magnitude), 'millitesla')
B_Resonanz_2 = Q_(np.append(B_sweep_2.magnitude[0:7] + B_seven_horizontal.magnitude, B_sweep_2.magnitude[7:] + B_ten_horizontal_2.magnitude), 'millitesla')

print('B-Felder_resonanz: ',B_Resonanz_1.to('tesla'), B_Resonanz_2.to('tesla'))
### g_F bestimmen. g_F steckt in a von poly ###

def poly (x, a, b):
    return a * x + b

### Sweep Lande sind die, die zu den Übergängen gehören
params_lande_sweep_1, covariance_B_sweep_1 = curve_fit(poly, frequenz.to('Hz').magnitude, B_Resonanz_1.to('tesla').magnitude)
params_lande_sweep_2, covariance_B_sweep_2 = curve_fit(poly, frequenz.to('Hz').magnitude, B_Resonanz_2.to('tesla').magnitude)

plt.clf()
plt.plot(np.array([0, 1200]), poly(np.array([0, 1200000]), *params_lande_sweep_1) * 1000, "r-")
plt.plot(frequenz.magnitude, poly(frequenz.to('Hz').magnitude, *params_lande_sweep_1) * 1000, "rx", label=r"Resonanzstelle 1")
#plt.plot(frequenz.magnitude, 4 * np.pi * m_0.magnitude * 1 / (e_0.magnitude) * B_sweep_1.magnitude, "kx", label=r"")
plt.plot(np.array([0, 1200]), poly(np.array([0, 1200000]), *params_lande_sweep_2) * 1000, "g-")
plt.plot(frequenz.magnitude, poly(frequenz.to('Hz').magnitude, *params_lande_sweep_2) * 1000, "gx", label=r"Resonanzstelle 2")
#plt.plot(frequenz.magnitude, 4 * np.pi * m_0.magnitude * 1 / (e_0.magnitude) * B_sweep_2.magnitude, "kx", label=r"")
plt.xlabel('Frequenz in kHz')
plt.ylabel('Magnetfeldstärke in mT')
plt.xlim(75, 1025)
plt.legend(loc='best')
plt.tight_layout()
plt.savefig('frequenz_B_feld.pdf')

### Ermitteln des Kernspins ###
print(params_lande_sweep_1[0], params_lande_sweep_2[0])

def lande(x):
    return 1 / x * 4 * np.pi * m_0.magnitude / e_0.magnitude

Isotop_1 = ufloat(params_lande_sweep_1[0], np.sqrt(np.diag(covariance_B_sweep_1))[0])
Isotop_2 = ufloat(params_lande_sweep_2[0], np.sqrt(np.diag(covariance_B_sweep_2))[0])
g_F_1 = lande(Isotop_1)
g_F_2 = lande(Isotop_2)
g_J = (3.0023 * (J**2 + J) + 1.0023 * ((S**2 + S) - (L**2 + L))) / (2 * (J**2 + J))

print('g_F_1: ',g_F_1, 'g_F_2: ',g_F_2)


Kernspin_1 = g_J / (4 * g_F_1) - 1 + unp.sqrt((g_J / (4 * g_F_1) - 1)**2 + 3 * g_J / (4 * g_F_1) - 3 / 4)
Kernspin_2 = g_J / (4 * g_F_2) - 1 + unp.sqrt((g_J / (4 * g_F_2) - 1)**2 + 3 * g_J / (4 * g_F_2) - 3 / 4)


print(Kernspin_1, Kernspin_2, g_J)
# vgl mit Literatur => Rb87 = Kernspin_1, Rb85 = Kernspin_2

### Verhältnis der Rb Isotope ###

#plt.clf()
#img_01 = Image.open("../Pics/TEK0002.JPG")
#plt.imshow(img_01)
#plt.show()

# abgelesene Werte: peak1: 218 - 336 , peak2: 98 - 363 Angebena in Pixel
R = (336 - 218) / (363 - 98)
p_2 = 1 / (1 + R)
p_1 = 1 - p_2
print('Verhältnis: ', (336 - 218) / (363 - 98))
print('p_1: ', p_1, 'p_2: ', p_2)

### Quadratische Zeeman-Effekt ###
# F_1 = J + I = 1 / 2  + 3 / 2 = 2, F_2 = 1 / 2 + 5 / 2 = 3

def qzeeman(B, g_F, M_F , dE):
    lin = g_F * mu_bohr * B
    quad = lin**2 * (1 - 2 * M_F) / dE
    return lin, quad

hyperfine_lin_1 ,hyperfine_quad_1 = qzeeman(max(B_Resonanz_1.to('tesla')), g_F_1, 2, 4.53*10**(-24))
hyperfine_lin_2 ,hyperfine_quad_2 = qzeeman(max(B_Resonanz_2.to('tesla')), g_F_2, 3, 2.01*10**(-24))

print('B-Feldstärken: ', max(B_Resonanz_1.to('tesla')), max(B_Resonanz_2.to('tesla')))

print('Hyperfeinstruktur_1: ', hyperfine_lin_1, hyperfine_quad_1, hyperfine_quad_1 / hyperfine_lin_1)
print('Hyperfeinstruktur_2: ', hyperfine_lin_2, hyperfine_quad_2, hyperfine_quad_2 / hyperfine_lin_2)

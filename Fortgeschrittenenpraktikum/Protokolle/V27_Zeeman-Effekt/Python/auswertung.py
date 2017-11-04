import numpy as np
from scipy.stats import sem
import scipy.constants as const
from uncertainties import ufloat
import uncertainties.unumpy as unp
from uncertainties.unumpy import (nominal_values as noms, std_devs as stds)
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from PIL import Image
import scipy.misc
from pint import UnitRegistry

u = UnityRegistry()
Q_ = u.Quantity

## Wellenlängen in nm

lambda_r = Q_(643.2, 'nanometer)
lambda_b = Q_(480.0, 'nanometer')
n_r = 1.4567
n_b = 1.4635
h = Q_(const.h, 'joule * second')
e_0 = Q_(const.e, 'coulomb')
mu_bohr = -1 / 2 * e_0 * h / 2*np.pi / const.m_e

dispsgebiet_r = lambda_r**2 / (2 * 2 * 10**(-6)) * np.sqrt(1 / (n_r**2 - 1))
dispsgebiet_b = lambda_b**2 / (2 * 2 * 10**(-6)) * np.sqrt(1 / (n_b**2 - 1))

## Fit Polynom 3. Grades

def poly(x, a, b, c, d):
    return a * x**3 + b * x**2 + c * x + d

## Hysterese, B in mT

B_auf = np.array([4, 87, 112,174, 230, 290, 352, 419,
476, 540, 600, 662, 714, 775, 823,872, 916, 959, 987,
1015, 1046, 1072])

B_ab = np.array([7, 57, 120, 180, 251, 306, 361, 428,
480, 550, 612, 654, 715, 780, 830, 878, 924, 962,
993, 1020, 1050, 1072])

I = np.linspace(0, 21, 22)
I_fit = np.linspace(-1, 22, 24)

## Plot + Fit Hysterese

params_B_auf, covariance_B_auf = curve_fit(poly, I, B_auf)
params_B_ab, covariance_B_ab = curve_fit(poly, I, B_ab)

plt.clf()
plt.subplot(2, 1, 1)
plt.plot(I, B_auf, "gx", label=r"Messdaten B_auf")
plt.plot(I_fit, poly(I_fit, *params_B_auf), "g-", label=r"Fit B_auf")
plt.xlabel('Stromstärke in A')
plt.ylabel('Magnetfeldstärke in mT')
plt.xlim(-0.5, 21.5)
plt.ylim(-10, 1090)
plt.legend(loc='best')
plt.subplot(2, 1, 2)
plt.plot(I, B_ab, "bx", label=r'Messdaten B_ab')
plt.plot(I_fit, poly(I_fit, *params_B_ab), "b-", label=r"Fit B_ab")
plt.xlabel('Stromstärke in A')
plt.ylabel('Magnetfeldstärke in mT')
plt.xlim(-0.5, 21.5)
plt.ylim(-10, 1090)
plt.legend(loc='best')
plt.tight_layout()
plt.savefig('Hysterese.pdf')
#
#plt.clf()
#plt.plot(I, B_auf, "kx", label=r"Messdaten B_auf")
#plt.plot(I, B_ab, "k+", label=r'Messdaten B_ab')
#plt.xlabel('Stromstärke in A')
#plt.ylabel('Magnetfeldstärke in mT')
#plt.xlim(-0.5, 21.5)
#plt.ylim(-10, 1090)
#plt.legend(loc='best')
#plt.tight_layout()
#plt.savefig('Hysterese_Messdaten.pdf')

print('fit auf',params_B_auf, np.sqrt(np.diag(covariance_B_auf)))
print('fit ab',params_B_ab, np.sqrt(np.diag(covariance_B_ab)))

#### ROT ####


## Bild eins Zeitstempel 10:01 Uhr

#plt.clf()
#img_01 = Image.open("../Pics/IMG_0733.JPG")
#plt.imshow(img_01)
#plt.show()


## Bild zwei I = 9.2 A Pol = +- 1

#plt.clf()
#img_01 = Image.open("../Pics/IMG_0734.JPG")
#plt.imshow(img_01)
#plt.show()

## Bild drei I = 9.2 A Pol = 0

#plt.clf()
#img_01 = Image.open("../Pics/IMG_0735.JPG")
#plt.imshow(img_01)
#plt.show()



## Pixelbreiten der 2 bis 11 Linie ROT
pixel_01_r = np.array([(875 + 784) / 2, (1162 + 1059) / 2, (1408 +
1320) / 2, (1648 + 1555) / 2, (1869 + 1787) / 2, (2077 + 1998) / 2, (2282 +
2188) / 2, (2470 + 2385) / 2, (2655 + 2572) / 2, (2824 + 2754) / 2])

pixel_02_r = np.array([(642 + 587) / 2, (800 + 727)/ 2, (947 +
864) / 2, (1084 + 998) / 2, (1211 + 1135) / 2, (1346 + 1279) / 2, (1458 +
1388) / 2, (1580 + 1522) / 2, (1687 + 1631) / 2, (1803 + 1751) / 2, (1906 +
1854) / 2, (2019 + 1961) / 2, (2119 + 2058) / 2, (2220 + 2162) / 2, (2317 +
2256) / 2, (2409 + 2354) / 2, (2500 + 2448) / 2, (2591 + 2540) / 2, (2680 +
2631) / 2, (2774 + 2722) / 2])

pixel_03_r = np.array([(925 + 796) / 2, (1193 + 1064) / 2, (1437 +
1331) / 2, (1675 + 1560) / 2, (1887 + 1793) / 2, (2105 + 2011) / 2, (2299 +
2205) / 2, (2499 + 2393) / 2, (2675 + 2572) / 2, (2852 + 2760) / 2])

### BLAU ###

## Bild eins Zeitstempel 10:33

#plt.clf()
#img_01 = Image.open("../Pics/IMG_0740.JPG")
#plt.imshow(img_01)
#plt.show()

## Bild zwei I = 5.6 A Pol = +-1
## Abstände zwischen zwei Linien zu den benachbarten
## beiden Linien gemessen +->  |*|   |*| (so wurde 1 gemessen)
## zwei beinhaltet die Abstände der Peaks von einer gespaltenen Linie

#plt.clf()
#img_01 = Image.open("../Pics/IMG_0743.JPG")
#plt.imshow(img_01)
#plt.show()

##  Pixelbreiten der 3 + 13 Linie

pixel_01_b = np.array([(1405 + 1244) / 2, (1690 + 1541) / 2, (1952
+ 1852) / 2, (2170 + 2055) / 2, (2399 + 2278) / 2, (2596 + 2481) / 2, (2781 +
2673) / 2, (2961 + 2861) / 2, (3130 + 3033) / 2, (3294 + 3202) / 2])

pixel_02_b_1 = np.array([(1419 + 1060) / 2, (1728 + 1419) / 2, (1973
+ 1728) / 2, (1973 + 1728) / 2, (2215 + 1973) / 2, (2435 + 2215) / 2, (2638 +
2435) / 2, (2816 + 2638) / 2, (3013 + 2816) / 2, (3176 + 3010) / 2, (3342 +
3176) / 2])

pixel_02_b_2 = np.array([(745 + 501) / 2, (1170 + 983) / 2, (1494 +
1339) / 2, (1776 + 1657) / 2, (2035 + 1910) / 2, (2273 + 2154) / 2, (2478 + 2377) / 2,
(2677 + 2582) / 2, (2873 + 2769) / 2, (3045 + 2959) / 2])

## Neue Messung BLAU

## Bild drei I = 0 A

#plt.clf()
#img_01 = Image.open("../Pics/IMG_0745.JPG")
#plt.imshow(img_01)
#plt.show()

## Bild vier I = 21 A Pol = 0

#plt.clf()
#img_01 = Image.open("../Pics/IMG_0746.JPG")
#plt.imshow(img_01)
#plt.show()

pixel_03_b = np.array([(495 + 374) / 2, (830 + 714) / 2, (1118 +
1003) / 2, (1366 + 1265) / 2, (1573 + 1496) / 2, (1802 + 1715) / 2,
(1972 + 1911) / 2, (2156 + 2096) / 2, (2335 + 2272) / 2, (2499 + 2436) / 2])

pixel_04_b = np.array([(395 + 287) / 2, (568 + 468) / 2, (735 +
656) / 2, (876 + 803) / 2, (1028 + 958) / 2, (1143 + 1078) / 2, (1292 + 1216) / 2,
(1383 + 1330) / 2, (1515 + 1468) / 2, (1614 + 1553) / 2, (1726 + 1682) / 2,
(1820 + 1770) / 2, (1932 + 1881) / 2, (2011 + 1970) / 2, (2116 + 2069) / 2,
(2192 + 2160) / 2, (2298 + 2254) / 2, (2374 + 2333) / 2, (2465 + 2418) / 2,
(2538 + 2503) / 2])

#img = Image.open("../Pics/IMG_0733.JPG")
#pixels_01 = list(img.getdata())
#pixels_01 = np.asarray(img)

#peaks_01 = findpeaks(pixels_01[0])

#print(pixels_01)

### Auswertung ROT ###

delta_S_r = np.zeros(len(pixel_01_r) - 1)

for i in range(0, len(pixel_01_r) - 1, 1):
    delta_S_r[i] = pixel_01_r[i + 1] - pixel_01_r[i]


#delta_S_r = ufloat(np.mean(delta_S_r), np.std(delta_S_r, ddof = 1))

print(delta_S_r)

del_S_r = np.zeros(9)
n = 1

for i in range(0, 9, 1):
    del_S_r[i] = pixel_02_r[n + 1] - pixel_02_r[n]
    n += 2


print(del_S_r)
#del_S_r = ufloat(np.mean(del_S_r), np.std(del_S_r, ddof = 1))

print(len(del_S_r), len(delta_S_r))
del_lambda_r = 1 / 2 * del_S_r / delta_S_r * dispsgebiet_r

del_lambda_r = ufloat(np.mean(del_lambda_r), np.std(del_lambda_r, ddof=1))

delta_E_r = Q_(h * del_lambda_r).to('eV')
print(delta_E_r)
B_auf_rot = Q_(ufloat(poly(9.2, *params_B_auf), poly(9.2, *np.sqrt(np.diag(covariance_B_auf)))), 'millietesla')
lande_r_sigma = np.abs(delta_E_r / (mu_bohr * B_auf_rot))

print(lande_r_sigma)
### Auswertung ROT ###

rot_01_sw = scipy.misc.imread("../Pics/IMG_0733-LAB.png", flatten=True, mode=None)
rot_02_sw = scipy.misc.imread("../Pics/IMG_0734-LAB.png", flatten=True, mode=None)
rot_03_sw = scipy.misc.imread("../Pics/IMG_0735-LAB.png", flatten=True, mode=None)

plt.clf()
plt.plot(range(0, 4000), rot_01_sw[450], 'r-', linewidth = 0.5, label = '$I = 0$')
plt.plot(range(0, 4000), rot_02_sw[450], 'g-', linewidth = 0.5, label = '$I = 9.2$A')
#plt.plot(range(0, 4000), rot_03_sw[450], 'b-', linewidth = 0.5, label = '$I = 9,2$A, Pol = 0')
plt.xlim(460, 4000)
#plt.ylim(60, 160)
plt.xlabel('$x$/px')
plt.ylabel('Helligkeit')
plt.legend(loc='best')
plt.grid()
plt.savefig('plots/rot_sigma_intensitaet.pdf')


plt.clf()
plt.plot(range(0, 4000), rot_01_sw[450], 'r-', linewidth = 0.5, label = '$I = 0$')
#plt.plot(range(0, 4000), rot_02_sw[450], 'g-', linewidth = 0.5, label = '$I = 9.2$A')
plt.plot(range(0, 4000), rot_03_sw[450], 'b-', linewidth = 0.5, label = '$I = 9,2$A, Pol = 0')
plt.xlim(460, 4000)
#plt.ylim(60, 160)
plt.xlabel('$x$/px')
plt.ylabel('Helligkeit')
plt.legend(loc='best')
plt.grid()
plt.savefig('plots/rot_pi_intensitaet.pdf')

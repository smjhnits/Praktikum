import numpy as np
import matplotlib.pyplot as plt
from uncertainties import ufloat
import uncertainties.unumpy as unp
from uncertainties.unumpy import (nominal_values as noms, std_devs as stds)
from pint import UnitRegistry

u = UnityRegistry()
Q_ = u.Quantity

### Polarisationsmessung ###

winkel = Q_(np.linspace(0, 290, 37), 'degre') #in deg

I_pol = Q_(np.array([0.116, 0.067, 0.034, 0.011, 0.001, 0.004, 0.020, 0.049, 0.086, 0.137, 0.187, 0.238, 0.281, 0.307, 0.308, 0.288, 0.251, 0.198, 0.137, 0.083, 0.040, 0.013, 0.001, 0.005, 0.024, 0.053, 0.094, 0.146, 0.208, 0.264, 0.295, 0.296, 0.279, 0.252, 0.214, 0.167, 0.111]), 'mA') #in mA

### Grundmode ###

verschiebung_grundmode = Q_(np.linspace(0, 22, 23), 'mm') #in mm

I_grundmode = Q_(np.array([0.12, 0.26, 0.47, 0.90, 1.48, 2.17, 3.28, 4.41, 4.95, 5.79, 6.09, 5.86, 5.48, 5.19, 4.54, 3.76, 2.76, 2.17, 1.55, 0.96, 0.54, 0.32, 0.18]), 'micro ampere') #in muA

### Erste angeregte Mode ###

verschiebung_mode = Q_(np.linspace(0, 25, 26), 'mm')

I_mode = Q_(np.array([0.23, 0.33, 0.40, 0.49, 0.56, 0.65, 0.66, 0.53, 0.30, 0.15, 0.04, 0.02, 0.03, 0.08, 0.17, 0.26, 0.34, 0.39, 0.43, 0.47, 0.39, 0.32, 0.29, 0.19, 0.10, 0.04]), 'micro ampere') #in muA

### Wellenlängenmessung ###
a = 100 # Gitterkonstante Drähte pro mm
abstand = Q_(75.7, 'cm') #in cm, Abstand Gitter-Schirm
# Abstand des zentralen Hauptmaxima zu den anderen Hauptmaxima

H_m2 = Q_(9.8, 'cm') #cm
H_m1 = Q_(4.9, 'cm') #cm
H_p1 = Q_(5.1, 'cm') #cm
H_p2 = Q_(9.7, 'cm') #cm

### Stabilitätsmessung ###

# konkav-konkav

L_außen_anfang_kk = Q_(76.9, 'cm')
L_innen_anfang_kk = Q_(67.0, 'cm')

L_linse = (L_außen_anfang - L_innen_anfang) / 2

L_konkav_konkav = Q_(np.array([76.9, 82.2, 87.0, 91.9, 97.0, 101.6, 107.0, 112.0, 116.9, 122.0, 132.0, 151.5]), 'cm') #in cm

I_konkav_konkav = Q_(np.array([0.14, 0.145, 0.161, 0.17, 0.18, 0.208, 0.207, 0.224, 0.211, 0.234, 0.257, 0.001]), 'mA') #in mA

# konkav-planar

L_außen_anfang_kp = Q_(68.8, 'cm') #in cm

L_konkav_planar = Q_(np.array([68.8, 72.8, 78.0, 83.0, 88.0]), 'cm')

I_konkav_planar = Q_(np.array([2.57, 2.40, 1.83, 1.48, 1.40]), 'mA') #in muA

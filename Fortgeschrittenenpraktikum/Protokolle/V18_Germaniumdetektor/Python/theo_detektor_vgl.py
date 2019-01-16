import numpy as np
from pint import UnitRegistry

u = UnitRegistry()
Q_ = u.Quantity

def E_aufloesung(F, E_EL):
    E_gamma = Q_(500, 'keV')
    return (2.35 * np.sqrt(F * E_gamma * E_EL)).to('eV')

##### Halbleiter (Fano-Faktor, Bandlücke)
Si = ('Si', 0.115, Q_(3.65, 'eV'))
Diamond = ('Diamond', 0.08, Q_(13.1, 'eV'))
GaAs = ('GaAs', 0.1, Q_(4.35, 'eV'))
CdTe = ('CdTe', 0.1, Q_(4.43, 'eV'))

halbleiter = [Si, Diamond, GaAs, CdTe]

for i in halbleiter:
    print(f'\nHalbleiter: {i[0]}\nEnergieauflösung = {E_aufloesung(i[1], i[2])}\n')

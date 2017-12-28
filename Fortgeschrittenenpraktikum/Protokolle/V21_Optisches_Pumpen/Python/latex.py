import collections
import numpy as np
import uncertainties
import pint
from uncertainties import ufloat
from uncertainties import ufloat_fromstr
from pint import UnitRegistry
import string
#import latex
from uncertainties.unumpy import (nominal_values as noms, std_devs as stds)
import uncertainties.unumpy as unp
import scipy.constants as const

u = UnitRegistry()
Q_ = u.Quantity


class Latexdocument(object):
    def __init__(self, filename):
        self.name = filename

    def tabular(self, spalten, header, places, caption, label):
        with open(self.name, 'w') as f:
            f.write('\\begin{table} \n\\centering \n\\caption{' + caption + '} \n\\label{tab: ' + label + '} \n\\begin{tabular}{')
            f.write(len(spalten) * 'S ')
            f.write('} \n\\toprule  \n')
            f.write(header + '  \\\ \n')
            f.write('\\midrule  \n ')
            for i in range(0, len(spalten[0])):
                for j in range(0, len(spalten)):
                    if j == len(spalten) - 1:
                        f.write(('{:.' + str(places[j]) + 'f}' + '\\\ \n').format(spalten[j][i]))
                    else:
                        f.write(('{:.' + str(places[j]) + 'f} ' + ' & ').format(spalten[j][i]))
            f.write('\\bottomrule \n\\end{tabular} \n\\end{table}')

mu_bohr = Q_(const.physical_constants['Bohr magneton'][0], 'joule/tesla')
e_0 = Q_(const.e, 'coulomb')
e_0_dimlos = const.e
m_0 = Q_(const.m_e, 'kg')
m_0_dimlos = const.m_e
mu_0 = Q_(const.mu_0, 'N / A**2')

### Angaben aus Protokoll ###

N_sweep = 11
N_horizontal = 154
R_sweep = Q_(16.39, 'cm').to('m')
R_horizontal = Q_(15.79, 'cm').to('m')


### Messdaten aus Messprogramm c.) ###


frequenz = Q_(np.array([101, 210, 300, 400, 502, 600, 700, 800, 904, 1001]), 'kHz')

I_sweep_1 = Q_(np.array([5.4, 3.75, 5.53, 4.71, 1.13, 1.77, 0.92, 3.55, 3.97, 5.17]) * 0.1, 'A')
I_sweep_2 = Q_(np.array([6.61, 6.32, 9.04, 9.41, 7.10, 8.86, 9.19, 7.51, 7.65, 7.21]) * 0.1, 'A')

I_seven_horizontal = Q_(np.array([0, 29, 31, 53, 93, 105, 128]), 'mA')
I_ten_horizontal_1 = Q_(np.array([126, 140, 148]), 'mA')
I_ten_horizontal_2 = Q_(np.array([164, 188, 216]), 'mA')
I_horizontal_1 = np.append(I_seven_horizontal, I_ten_horizontal_1)
I_horizontal_2 = np.append(I_seven_horizontal, I_ten_horizontal_2)

### Magnetfelder aus Spulenstrom berechnen ###

def B_Helmholtz(I, N, R):
    return mu_0 * 8 * I * N / (np.sqrt(125) * R)


### B-Feld sweep, horizontal ###

B_sweep_1 = B_Helmholtz(I_sweep_1, N_sweep, R_sweep).to('millitesla')
B_sweep_2 = B_Helmholtz(I_sweep_2, N_sweep, R_sweep).to('millitesla')


B_seven_horizontal = B_Helmholtz(I_seven_horizontal, N_horizontal, R_horizontal).to('millitesla')
B_ten_horizontal_1 = B_Helmholtz(I_ten_horizontal_1, N_horizontal, R_horizontal).to('millitesla')
B_ten_horizontal_2 = B_Helmholtz(I_ten_horizontal_2, N_horizontal, R_horizontal).to('millitesla')
B_horizontal_1 = np.append(B_seven_horizontal, B_ten_horizontal_1)
B_horizontal_2 = np.append(B_seven_horizontal, B_ten_horizontal_2)
### B-Felder an Resonanzstelle ###

B_Resonanz_1 = Q_(np.append(B_sweep_1.magnitude[0:7] + B_seven_horizontal.magnitude, B_sweep_1.magnitude[7:] + B_ten_horizontal_1.magnitude), 'millitesla')
B_Resonanz_2 = Q_(np.append(B_sweep_2.magnitude[0:7] + B_seven_horizontal.magnitude, B_sweep_2.magnitude[7:] + B_ten_horizontal_2.magnitude), 'millitesla')

#frequenz = frequenz.magnitude
#I_sweep_1 = I_sweep_1.magnitude
#B_sweep_1 = B_sweep_1.magnitude
#I_horizontal_1 = I_horizontal_1.magnitude
#B_horizontal_1 = B_horizontal_1.magnitude
#B_Resonanz_1 = B_Resonanz_1.magnitude
#
#I_sweep_2 = I_sweep_2.magnitude
#B_sweep_2 = B_sweep_2.magnitude
#I_horizontal_2 = I_horizontal_2.magnitude
#B_horizontal_2 = B_horizontal_2.magnitude
#B_Resonanz_2 = B_Resonanz_2.magnitude

Latexdocument('Tabelle_Messdaten_1.tex').tabular([frequenz, I_sweep_1, B_sweep_1, I_horizontal_1, B_horizontal_1, B_Resonanz_1], '{$\\nu$ in $\si{\kilo\hertz}$} & {$I_{sweep}$ in  $\si{\\ampere}$} & {$B_{sweep}$ in $\si{\milli\\tesla}$} & {$I_{horizontal}$ in  $\si{\milli\\ampere}$} & {$B_{horizontal}$ in $\si{\milli\\tesla}$} & {$B_{ges}$ in $\si{\milli\\tesla}$}', [0, 2, 3, 0, 3, 3], caption = 'Messdaten der ersten Resonanzstelle', label = 'Messdaten_Resonanz_1')

Latexdocument('Tabelle_Messdaten_2.tex').tabular([frequenz, I_sweep_2, B_sweep_2, I_horizontal_2, B_horizontal_2, B_Resonanz_2], '{$\\nu$ in $\si{\kilo\hertz}$} & {$I_{sweep}$ in  $\si{\\ampere}$} & {$B_{sweep}$ in $\si{\milli\\tesla}$} & {$I_{horizontal}$ in  $\si{\milli\\ampere}$} & {$B_{horizontal}$ in $\si{\milli\\tesla}$} &  {$B_{ges}$ in $\si{\milli\\tesla}$}', [0, 2, 3, 0, 3, 3], caption = 'Messdaten der zweiten Resonanzstelle', label = 'Messdaten_Resonanz_2')

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

I_pol = Q_(np.array([0.116, 0.067, 0.034, 0.011, 0.001, 0.004, 0.020, 0.049, 0.086,
0.137, 0.187, 0.238, 0.281, 0.307, 0.308, 0.288, 0.251, 0.198, 0.137, 0.083, 0.040,
0.013, 0.001, 0.005, 0.024, 0.053, 0.094, 0.146, 0.208, 0.264, 0.295, 0.296, 0.279,
0.252, 0.214, 0.167, 0.111]), 'mA') #in mA

winkel = Q_(np.linspace(0, 360, 37), 'degree')

I_grundmode = Q_(np.array([0.12, 0.26, 0.47, 0.90, 1.48, 2.17, 3.28, 4.41, 4.95, 5.79,
6.09, 5.86, 5.48, 5.19, 4.54, 3.76, 2.76, 2.17, 1.55, 0.96, 0.54, 0.32, 0.18, 0, 0, 0]), 'microampere') #in muA
verschiebung_grundmode = Q_(np.linspace(0, 22, 23), 'mm') #in mm


verschiebung_mode = Q_(np.linspace(0, 25, 26), 'mm')

I_mode = Q_(np.array([0.23, 0.33, 0.40, 0.49, 0.56, 0.65, 0.66, 0.53, 0.30, 0.15,
0.04, 0.02, 0.03, 0.08, 0.17, 0.26, 0.34, 0.39, 0.43, 0.47, 0.39, 0.32, 0.29, 0.19,
0.10, 0.04]), 'microampere') #in muA

L_außen_anfang_kk = Q_(76.9, 'cm')
L_innen_anfang_kk = Q_(67.0, 'cm')

L_linse = (L_außen_anfang_kk - L_innen_anfang_kk)

L_konkav_konkav = Q_(np.array([76.9, 82.2, 87.0, 91.9, 97.0, 101.6, 107.0, 112.0,
116.9, 122.0, 132.0]) - L_linse.magnitude, 'cm') #in cm

I_konkav_konkav = Q_(np.array([0.14, 0.145, 0.161, 0.17, 0.18, 0.208, 0.207, 0.224,
0.211, 0.234, 0.257]), 'mA') #in mA

L_außen_anfang_kp = Q_(68.8, 'cm') #in cm

L_konkav_planar = Q_(np.array([68.8, 72.8, 78.0, 83.0, 88.0]) - L_linse.magnitude, 'cm')

I_konkav_planar = Q_(np.array([2.57, 2.40, 1.83, 1.48, 1.40]), 'mA') #in muA


#Latexdocument('Polarisationsmessung.tex').tabular([I_pol.magnitude, winkel.magnitude], '{I_{\symup{Pol}} in $\si{\milli\ampere}$} & {$\phi$ in  $\si{\degree}$}', [3, 0], caption = 'Messdaten der Polarisationsmessung.', label = 'pol')

#Latexdocument('Moden.tex').tabular([I_grundmode.magnitude, I_mode.magnitude, verschiebung_mode.magnitude], '{$I_{(0, 0)}$ in $\si{\micro\ampere}$} & {$I_{(0, 1)}$ in $\si{\micro\ampere}$} & {$d$ in $\si{\milli\meter}$}', [2, 2, 0], caption = 'Messdaten der Modenmessung.', label = 'tem')

#Latexdocument('kk.tex').tabular([L_konkav_konkav.magnitude, I_konkav_konkav.magnitude], '{$\Delta L}$ in $\si{\centi\meter}$} & {$I$ in $\si{\milli\ampere}$}', [1, 2], caption = 'Messdaten der Resonatorstabilitätemessung für die Spiegelkombination konkav-konkav.', label = 'kk')

#Latexdocument('kp.tex').tabular([L_konkav_planar.magnitude, I_konkav_planar.magnitude], '{$\Delta L}$ in $\si{\centi\meter}$} & {$I$ in $\si{\micro\ampere}$}', [1, 2], caption = 'Messdaten der Resonatorstabilitätemessung für die Spiegelkombination konkav-planar.', label = 'kp')

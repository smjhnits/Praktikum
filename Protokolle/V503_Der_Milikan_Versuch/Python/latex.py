import collections
import numpy as np
import uncertainties
import pint
from uncertainties import ufloat
from uncertainties import ufloat_fromstr
from pint import UnitRegistry
import string
import latex
from uncertainties.unumpy import (nominal_values as noms, std_devs as stds)
import uncertainties.unumpy as unp
import scipy.constants as const
ureg = UnitRegistry()
Q_ = ureg.Quantity


def Brennweite_Bessel(e, d):
    return (e**2- d**2) / (4 * e)

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

R, t_0, U_g, r_oel, r_err, q, q_err = np.genfromtxt('Messdaten.txt', unpack=True)

q *= 10**19
q *= 10
q_err *= 10
q_err *= 10**19
r_oel *= 10**6

Latexdocument('Messwerte.tex').tabular([R, t_0, U_g, r_oel, q, q_err], r'{$\Omega$ in $\si{\mega\ohm}$} & {$t_0$ in $\si{\second}$} & {$\symup{U}_{\symup{g}}$ in $\si{\volt}$} & {$r$ in $\si{\nano\meter}$} & {$q$ in $10^{-20}\si{\coulomb}$} & {$\Delta_q$}', [2, 2, 0, 2, 2, 2], caption = 'Messdaten von V503.', label = 'Messdaten')

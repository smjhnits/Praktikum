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
import auswertung as a




class Latexdocument(object):
    def __init__(self, filename):
        self.name = filename

    def tabular(self, spalten, header, places, caption, label):
        with open(self.name, 'w') as f:
            f.write('\\begin{table} \n\\centering \n\\caption{' + caption + '} \n\\label{tab:' + label + '} \n\\begin{tabular}{')
            f.write(len(spalten) * 'S ')
            f.write('} \n\\toprule  \n')
            f.write(header + '  \\\ \n')
            f.write('\\midrule  \n')
            for i in range(0, len(spalten[0])):
                for j in range(0, len(spalten)):
                    if j == len(spalten) - 1:
                        f.write(('{:.' + str(places[j]) + 'f}' + '\\\ \n').format(spalten[j][i]))
                    else:
                        f.write(('{:.' + str(places[j]) + 'f} ' + ' & ').format(spalten[j][i]))
            f.write('\\bottomrule \n\\end{tabular} \n\\end{table}')


#Latexdocument('C_p.tex').tabular([a.C_p_cu.magnitude, a.U.magnitude, a.I.magnitude * 10**3, a.delta_t.magnitude, a.delta_T_probe.magnitude], {$C_p / \si{\joule \per \kelvin \per \mol}$} & {$U / \si{\\volt}$} & {$ I / \si{\milli\\ampere}$} & {$ \increment t / \si{\s}$} & {$ \increment T / \si{\kelvin}$}', [2, 2, 2, 0, 2], caption = 'Messdaten zu der Wärmekapazität $C_p$', label = 'c_p')
#Latexdocument('C_V.tex').tabular([a.C_V_cu.magnitude, a.alpha_von_T.magnitude * 1e6], '{$C_V / \si{\joule \per \kelvin \per \mol}$} & {$ \\alpha / \si{\per1e6\kelvin}$}', [2, 2], caption = 'Ergebnisse der Wärmekapazität $C_V$.', label = 'c_v')

Latexdocument('T_debye.tex').tabular([a.debye_experimentell.magnitude, a.C_V_cu_debye.magnitude, a.T_probe_bis170K[1:].magnitude, a.data.debye_tabelle], '{$\\theta_{\symup{D}} / \si{\kelvin}$} & {$C_V / \si{\joule \per \kelvin \per \mol}$} & {$T / \si{\kelvin}$} & {$\\frac{\\theta_{\symup{D}}}{T}$}', [2, 2, 2, 2], caption = 'Gefundene Werte von $\\theta_{\symup{D}}$', label = 'debye')

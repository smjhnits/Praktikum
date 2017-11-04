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


B_auf = np.array([4, 87, 112,174, 230, 290, 352, 419,
476, 540, 600, 662, 714, 775, 823,872, 916, 959, 987,
1015, 1046, 1072])

B_ab = np.array([7, 57, 120, 180, 251, 306, 361, 428,
480, 550, 612, 654, 715, 780, 830, 878, 924, 962,
993, 1020, 1050, 1072])

I = np.linspace(0, 21, 22)



Latexdocument('Tabelle_Hysterese.tex').tabular([I, B_auf, B_ab], '{Stromstärke in  $\si{\\ampere}$} & {B-Feldstärke aufsteigend in  $\si{\milli\\tesla}$} & {B-Feldstärke aufsteigend in  $\si{\milli\\tesla}$}', [0, 0, 0], caption = 'Messdaten der Hysterese', label = 'Hysterese')

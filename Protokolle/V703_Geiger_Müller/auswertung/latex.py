import collections
import numpy as np
import uncertainties
import pint
from uncertainties import ufloat
from uncertainties import ufloat_fromstr
from pint import UnitRegistry
import string
import latex
ureg = UnitRegistry()
Q_ = ureg.Quantity


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



Zählrate = np.array([33062, 33816, 33883, 34142, 34549, 34491, 34815, 34818,
                     34975, 35219, 34923, 35100, 34947, 35133, 35390, 35342,
                     35359, 35363, 35234, 35695, 35722, 35332, 35523, 35617,
                     35747, 35433, 35827, 35757, 35908, 35868, 35853, 36340,
                     36405, 36758, 37352, 37824, 38535, 39689, 41082])

I = np.array([0.3, 0.45, 0.6, 0.7, 0.85, 0.95, 1.1, 1.2,  1.25, 1.4,
                                              1.6,  1.7, 1.8, 1.9,  2.1,  2.3, 2.4, 2.5,  2.6, 2.8,
                                              2.9,  3.0, 3.0, 3.2,  3.3,  3.4, 3.5, 3.6, 3.8, 3.95,
                                              4.0,  4.1, 4.4, 4.5,  4.7,  4.8, 4.9, 5.2, 5.4])
Zählrate_err = np.sqrt(Zählrate)
testXAchse = np.linspace(320, 700, 39)
Latexdocument('Tabelle_Charakteristik.tex').tabular([testXAchse, Zählrate,Zählrate_err, I], '   {Spannung in  $\si{volt}$} & {Zählrate $N$ in $\frac{1}{\si{\minute}}$} & {$\Delta N$} &  {Stromstärke in $\si{\milli\ampere}$}', [0, 0, 0, 2], caption = 'bla', label = 'bla')

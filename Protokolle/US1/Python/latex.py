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

### Impuls-Echo-Verfahren ###

puls_1 = np.array([[0.9, 0.97, 0.98, 1, 0.97, 0.98, 0.97, 1],
                   [0.4, 0.4, 0.5, 0.4, 0.4, 0.5, 0.4, 0.5]
                   ])

puls_2 = np.array([[0.17, 0.02, 0.01, 0.12, 0.25, 0.19, 0.04, 0.12],
                  [30.3, 59.8, 59.8, 76.49, 23.7, 29.8, 46.2, 75.7]
                  ])


### Durchschallungsverfahren ###

laufzeit_2 = np.array([15.21, 29.78, 30.18, 38.48, 11.98, 15.21, 23.27])

### Spektrale Analyse und Cepstrum ###

peakdifferenzen = np.array([37.1 - 29.8, 41.6 - 37.1, 41.6 - 29.8])

### Auge ###

auge = np.array([[0.2, 6.22, 4.61, 5.76, 41.7],
                [0.2, 6.64, 11.05, 16.81, 70.26]]) # erster Eintrag Peakabstände, zweiter Eintrag die Absoluten Abstände


Latexdocument('Tabelle_Impuls-Echo.tex').tabular([puls_1[0, :], puls_1[1, :], puls_2[0, :], puls_2[1, :]], r'{$\su{U}\ua{1}$ in $\si{\volt}$} & {$t_1$ in $\si{\mu\second}$} & {$\su{U}\ua{2}$ in $\si{\volt}$} & {$t_2$ in $\si{\mu\second}$}', [2, 2, 2, 2], caption = r'Messdaten zu dem Impuls-Echo-Verfahren. Die Werte sind den Zylindern 1 - 7 derReihe nach zuzuordnen. Der achte Messert entspricht einem Zylinder der Länge $\su{Z}_1 + \su{Z}_7$.', label = 'Messdaten')

Latexdocument('Tabelle_Durchschallung.tex').tabular([laufzeit_2], '{Laufzeiten in \si{\mu\second}}', [2], caption = 'Messdaten zu dem Durchschallungsverfahren. Die Messdaten sind der Reihe nach den Zylindern 1 - 7 zuzuordnen.', label = 'tab:durchschall')

Latexdocument('Tabelle_Auge.tex').tabular([auge[0, :], auge[1, :]], '{Peakabstand $\Delta_{\symup{peak}}$ in \si{\mu\second}}  & {Absoluter Abstand}', [2, 2], caption = 'Messdaten zur biometrischen Untersuchung des Auges. Die Messdaten sind der Reihe den Bestandteile des Auges zuzuordnen.', label = 'tab:Auge')

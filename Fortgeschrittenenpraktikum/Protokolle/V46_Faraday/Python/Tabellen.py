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


Latexdocument('B.tex').tabular([a.B.magnitude, a.s.magnitude], '{$B / \si{\milli\\tesla}$} & {$s / \si{\milli\meter}$}', [0, 0], caption='Gemessene Magnetfeldstärken $B$ bei Veränderter Tiefe der Hall-Sonde.', label='B')
Latexdocument('Probe1.tex').tabular([a._lambda, a.theta_1_1, a.theta_1_2, a.theta_1, a.theta_1_norm.magnitude, a.theta_1_norm.magnitude - a.hr_theta_norm.magnitude], '{$\lambda / \si{\micro\meter}$} & {$\\theta_1(B_+) / \si{\\radian}$} & {$\\theta_1(B_-) / \si{\\radian}$} & {$\\theta_1 / \si{\\radian}$} & {$\\theta{_\symup{1, Norm}} / \si{\\radian\per\mm}$} & {$\Delta\\theta_\symup{1, Norm} / \si{\\radian\per\milli\meter}$}', [2, 2, 2, 3, 3, 3], caption='Messwerte der dotierten GaAs Probe, mit der Dicke $d = \SI{1.36}{\mm}$. $\\theta_1$ beschreibt den Faraday-Rotationswinkel und $\Delta\\theta_\symup{1, Norm}$ den mit der Dicke $d$ normierten Wert abzüglich des normierten Faraday-Rotationswinkels der hochreinen Probe.', label='probe1')
Latexdocument('Probe2.tex').tabular([a._lambda, a.theta_2_1, a.theta_2_2, a.theta_2, a.theta_2_norm.magnitude, a.theta_2_norm.magnitude - a.hr_theta_norm.magnitude], '{$\lambda / \si{\micro\meter}$} & {$\\theta_2(B_+) / \si{\\radian}$} & {$\\theta_2(B_-) / \si{\\radian}$} & {$\\theta_2 / \si{\\radian}$} & {$\\theta{_\symup{1, Norm}} / \si{\\radian\per\mm}$} & {$\Delta\\theta_\symup{2, Norm} / \si{\\radian\per\milli\meter}$}', [2, 2, 2, 3, 3, 3], caption='Messwerte der dotierten GaAs Probe, mit der Dicke $d = \SI{1.296}{\mm}$. $\\theta_2$ beschreibt den Faraday-Rotationswinkel und $\Delta\\theta_\symup{1, Norm}$ den mit der Dicke $d$ normierten Wert abzüglich des normierten Faraday-Rotationswinkels der hochreinen Probe.', label='probe2')
Latexdocument('hr_GaAs.tex').tabular([a._lambda, a.hr_theta_1, a.hr_theta_2, a.hr_theta, a.hr_theta_norm.magnitude], '{$\lambda / \si{\micro\meter}$} & {$\\theta(B_+) / \si{\\radian}$} & {$\\theta(B_-) / \si{\\radian}$} & {$\\theta / \si{\\radian}$} ', [2, 2, 2, 3, 3], caption='Messwerte der reinen GaAs Probe, mit der Dicke $d = \SI{5.11}{\mm}$. $\\theta$ beschreibt den Faraday-Rotationswinkel und $\\theta_\symup{Norm}$ den über die Dicke normierten Faraday-Rotationswinkel.', label='hr')

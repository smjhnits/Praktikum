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

err = np.ones(10) * 0.05
err_5 = np.ones(5) * 0.05
g_1 = unp.uarray(np.linspace(15, 60, 10) * 10**(-2), err) * 10**2 # Gegenstandsweite erste Messung cm in m
b_1 = unp.uarray(np.array([27.8, 18.4, 15.3, 13.85, 13.1, 12.5, 12.05, 11.7, 11.4, 11.25]) * 10**(-2), err) * 10**2 # Bildweite erste Messung cm in m
B_1 = unp.uarray(np.array([2.8, 1.9, 1.45, 1.15, 0.95])* 10**(-2), err_5) * 10**2 # cm in m

# Messung bei unbekannter Brennweite

g_2 = unp.uarray(np.linspace(15, 60, 10) * 10**(-2), err) * 10**2
b_2 = unp.uarray(np.array([18.55, 14.3, 12.5, 11.7, 11.1, 10.5, 10.3, 10.1, 9.95, 9.9]) * 10**(-2), err) * 10**2

# Messung nach Bessel

b_plus_g_3 = unp.uarray(np.array([40, 45, 50, 52.5, 55, 57.5, 60, 62.5, 65, 70]) * 10**(-2), err) * 10**2
g_eins_3 = unp.uarray(np.array([16.6, 14.15, 13.2, 12.9, 12.6, 12.4, 12.2, 12.2, 12, 11.8]) * 10**(-2), err) * 10**2 # erster Brennpkt
b_eins_3 = b_plus_g_3 - g_eins_3
g_zwei_3 = unp.uarray(np.array([23.7, 31.05, 37, 40, 42.6, 45.35, 48, 50.75, 53.35, 58.45]) * 10**(-2), err) * 10**2 # zweiter Brennpkt
b_zwei_3 = b_plus_g_3 - g_zwei_3

d_eins_3 = g_eins_3 - b_eins_3
d_zwei_3 = g_zwei_3 - b_zwei_3

# chromatische Abberation

b_plus_g_4 = unp.uarray(np.linspace(45, 65, 5) * 10**(-2), err_5) * 10**2
g_eins_rot_4 = unp.uarray(np.array([14.35, 13.2, 12.6, 12.35, 12]) * 10**(-2), err_5) * 10**2
b_eins_rot_4 = b_plus_g_4 - g_eins_rot_4
g_zwei_rot_4 = unp.uarray(np.array([31, 37, 42.5, 48.1, 53.5]) * 10**(-2), err_5) * 10**2
b_zwei_rot_4 = b_plus_g_4 - g_zwei_rot_4
d_eins_rot_4 = g_eins_rot_4 - b_eins_rot_4
d_zwei_rot_4 = g_zwei_rot_4 - b_zwei_rot_4

g_eins_blau_4 = np.array([14.1, 13.25, 12.7, 12.4, 12.1])
b_eins_blau_4 = b_plus_g_4 - g_eins_blau_4
g_zwei_blau_4 = np.array([31.2, 37.1, 42.7, 48.2, 53.3])
b_zwei_blau_4 = b_plus_g_4 - g_zwei_blau_4
d_eins_blau_4 = g_eins_blau_4 - b_eins_blau_4
d_zwei_blau_4 = g_zwei_blau_4 - b_zwei_blau_4

# Nach Abbe Streulinse -100 mm, Sammellinse 100mm

B_5 = unp.uarray(np.array([5.2, 3.9, 2.8, 2.2, 1.8, 1.5, 1.3, 1.2, 1, 0.95]) * 10**(-2), err) * 10**2
b_plus_g_5 = unp.uarray(np.array([70, 67.3, 66.6, 68.1, 71.4, 75, 79, 83.3, 87.5, 92.1]) * 10**(-2), err) * 10**2
g_5 = unp.uarray(np.array([17, 20, 25, 30, 35, 40, 45, 50, 55, 60]) * 10**(-2), err) * 10**2
b_5 = b_plus_g_5 - g_5

brennweite_3 = Brennweite_Bessel(np.append(b_plus_g_3, b_plus_g_3), np.append(d_eins_3, d_zwei_3))

#Latexdocument('Tabelle_Messung_unbekannte_brennweite.tex').tabular([noms(g_2), stds(g_2),noms(b_2), stds(b_2)], '{$g$ in $\si{\centi\meter}} & {Fehler $g$} & {$b$ in $\si{\centi\meter}$} & {Fehler $b$} \\', [0, 2, 2, 2], caption = 'Messdaten der Linse mit unbekannter Brennweite.', label = 'tab:unbekannte_brennweite')

Latexdocument('Tabelle_Brennweiten_Bessel.tex').tabular([noms(brennweite_3), stds(brennweite_3)], '', [2, 2], caption = 'Brennweite nach der Methode von Bessel.', label = 'tab:brennweiteBessel')

#Latexdocument('Tabelle_Brennweite_Bessel.tex').tabular([noms(noms(bbrennweite_3)), stds(brennweite_3)], '{$f\ua{Bessel}$ in $\si{\centi\meter}} & {Fehler $f\ua{Bessel}$} \\', [2, 2], caption = 'Messdaten der Linse mit unbekannter Brennweite.', label = 'tab:unbekannte_brennweite')

#Latexdocument('Tabelle_Messung_bekannte_brennweite.tex').tabular([noms(g_1), stds(g_1),noms(b_1), stds(b_1), np.append(noms(B_1), [0, 0, 0, 0, 0]), np.append(stds(B_1), [0, 0, 0, 0, 0])], '{$g$ in $\si{\centi\meter}} & {Fehler $g$} & {$b$ in $\si{\centi\meter}$} & {Fehler $b$} & {Bildgröße $B$} & {Fehler $B$} \\', [0, 2, 2, 2, 2, 2], caption = 'Messdaten der ersten Messung. Brennweite der verwendeten Linse ist bekannt ($\SI{10}{\centi\meter}$).', label = 'tab:bekannte_brennweite')


#Latexdocument('Tabelle_Messung_nach_Bessel.tex').tabular([noms(b_plus_g_3), stds(b_plus_g_3),noms(g_eins_3), stds(g_eins_3), noms(g_zwei_3), stds(g_zwei_3)], '{$e$ in $\si{\centi\meter}} & {Fehler $e$} & {$g_1$ in $\si{\centi\meter}$} & {Fehler $g_1$} & {$g_2$ in $\si{\centi\meter}$} & {Fehler $g_2$} \\', [0, 2, 1, 2, 2, 2], caption = 'Messdaten der Methode nach Bessel', label = 'tab:bessel')

#Latexdocument('Tabelle_Messung_chromatische_abberration.tex').tabular([noms(b_plus_g_4), stds(b_plus_g_4),noms(g_eins_rot_4), stds(g_eins_rot_4), noms(g_zwei_rot_4), stds(g_zwei_rot_4) , noms(g_eins_blau_4), stds(g_eins_blau_4), noms(g_zwei_blau_4), stds(g_zwei_blau_4)], '{$e$ in $\si{\centi\meter}} & {Fehler $e$} & {$g_{1,\symup{rot}}$ in $\si{\centi\meter}$} & {Fehler $g_{1,\symup{rot}}$} & {$g_{2,\symup{rot}}$ in $\si{\centi\meter}$} & {Fehler $g_{2,\symup{rot}}$} & {$g_{1,\symup{blau}}$ in $\si{\centi\meter}$} & {Fehler $g_{1,\symup{blau}}$} & {$g_{2,\symup{blau}}$ in $\si{\centi\meter}$} & {Fehler $g_{2,\symup{blau}}$}\\', [0, 2, 2, 2, 1, 2, 2, 2, 1, 2], caption = 'Messdaten zur chromatischen Abberration', label = 'tab:chromatische_abberration')

#Latexdocument('Tabelle_Messung_nach_Abbe.tex').tabular([noms(B_5), stds(B_5),noms(b_plus_g_5), stds(b_plus_g_5), noms(g_5), stds(g_5)], '{Bildgröße $B$ in $\si{\centi\meter}} & {Fehler $B$} & {$b + g$ in $\si{\centi\meter}$} & {Fehler $g + b$} & {$g$ in $\si{\centi\meter}$} & {Fehler $g$} \\', [1, 2, 1, 2, 0, 2], caption = 'Messdaten der Methode nach Abbe', label = 'tab:Abbe')

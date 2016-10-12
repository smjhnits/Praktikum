import numpy as np
import sys
import os

i = 0

with open('daten.txt', 'r') as f:
    a, b, c = np.genfromtxt('daten.txt', unpack = True)
    length = len(a)
    with open('Test.tex', 'w') as t:
        t.write(r'\documentclass[caption=tableheading]{scrartcl}')
        t.write('\n')
        t.write(r'\input{/home/sebastian/Dokumente/Präambel.tex}')
        t.write('\n')
        t.write(r'\begin{document}')
        t.write('\n')
        t.write(r'\begin{table}')
        t.write('\n')
        t.write(r'   \centering')
        t.write('\n')
        t.write(r'   \label{tab:some_data}')
        t.write('\n')
        t.write(r'   \sisetup{table-format=1.2}')
        t.write('\n')
        t.write(r'   \begin{tabular}{S S S}')
        t.write('\n')
        t.write(r'       \toprule')
        t.write('\n')
        t.write(r'       {$Data A$} & {$Data B$} & {$Data C$} \\')
        t.write('\n')
        t.write(r'       \midrule')
        t.write('\n')
        while i < length:
            t.write(r'       {:.2f} & {:.2f} & {:.2f} \\'.format(a[i], b[i], c[i]))
            i += 1
        t.write('\n')
        t.write(r'      \bottomrule')
        t.write('\n')
        t.write(r'  \end{tabular}')
        t.write('\n')
        t.write(r'\end{table}')
        t.write('\n')
        t.write(r'\end{document}')

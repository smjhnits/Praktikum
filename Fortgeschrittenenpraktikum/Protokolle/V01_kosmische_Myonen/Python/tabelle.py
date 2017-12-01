import numpy as np

Kanaele = np.linspace(1, 512, 512)
Messwerte = np.genfromtxt('Messwert_table.tex', unpack=True)

Kanal1 = Kanaele[0:80]
Kanal2 = Kanaele[80:160]
Kanal3 = Kanaele[160:240]
Kanal4 = Kanaele[240:320]
Kanal5 = Kanaele[320:400]
Kanal6 = Kanaele[400:480]
Kanal7 = Kanaele[480:518]

Mess1 = Messwerte[0:80]
Mess2 = Messwerte[80:160]
Mess3 = Messwerte[160:240]
Mess4 = Messwerte[240:320]
Mess5 = Messwerte[320:400]
Mess6 = Messwerte[400:480]
Mess7 = Messwerte[480:518]

np.savetxt('Kanal7.txt', np.column_stack([Kanal7, Mess7]))


#print(len(Kanal1))
#print(len(Kanal2))
#print(len(Kanal3))
#print(len(Kanal4))
#print(len(Kanal5))
#print(len(Kanal6))
#print(len(Kanal7))

leng = len(Mess1)
i = 0




#with open('tabelle.tex', 'w') as f:
#
#
#    f.write(r'\input{header.tex}')
#    f.write('\\begin{document} \n')
#
#    f.write('\\begin{table} \n \\centering \n \\caption{Testtabelle} \n \\label{tab:some_data} \n \\begin{tabular}{c | c | c | c | c | c | c} \n \\toprule \\\ \n')# \\\ \n $\\alpha$ & $\\beta$ & $\\gamma$ & $\\theta$ & $\\kappa$ \\\ \n  \\midrule \\\ \n ')
#
#    while i < leng:
#        f.write('{:.2f} {:.2f} & {:.2f} {:.2f} & {:.2f} {:.2f} & {:.2f} {:.2f} & {:.2f} {:.2f} & {:.2f} {:.2f}  \\\ \n '.format(Kanal1[i], Mess1[i], Kanal2[i], Mess2[i], Kanal3[i], Mess3[i], Kanal4[i], Mess4[i], Kanal5[i], Mess5[i], Kanal6[i], Mess6[i]))
#        i += 1
#
#
#
#    f.write('\\bottomrule \n \\end{tabular} \n \\end{table}')
#    f.write('\\end{document} \n ')

import numpy as np
import csv

csv.register_dialect(
    'mydialect',
    delimiter = ',',
    quotechar = '"',
    doublequote = True,
    skipinitialspace = True,
    lineterminator = '\r\n',
    quoting = csv.QUOTE_MINIMAL)

x, y, i, k= np.genfromtxt('data.txt', unpack = True)
print(x)
print(y)

header = ['Messwerte', 'Messdaten', 'Zahlen', 'Ingas Summen']
n = np.transpose(np.array([ x, y, i, k]))

print(header)
print(n)


with open('mydata.csv', 'w') as mycsvfile:
    thedatawriter = csv.writer(mycsvfile, dialect='mydialect')
    thedatawriter.writerow(header)
    for row in n:
        thedatawriter.writerow(row)

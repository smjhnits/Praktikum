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

data = np.genfromtxt('data.txt', unpack = True)
print(data)

header = ['Messwerte', 'Messdaten', 'Zahlen', 'Gruppe 3']
n = np.transpose(data)

print(header)
print(n)


with open('mydata.csv', 'w') as mycsvfile:
    thedatawriter = csv.writer(mycsvfile, dialect='mydialect')
    thedatawriter.writerow(header)
    for row in n:
        thedatawriter.writerow(row)

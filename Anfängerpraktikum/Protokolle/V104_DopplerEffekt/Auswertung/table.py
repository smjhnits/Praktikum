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

data = np.genfromtxt('Speed.txt', unpack = True)

header = [ 'Gang', 'Impulse', 'Fehler', 'Zeit [s]', 'Fehler [s]', 'Geschwindikgeit [m/s]', 'Fehler [m/s]']
n = np.transpose(data)
print(data)

with open('Speed.csv', 'w') as mycsvfile:
    thedatawriter = csv.writer(mycsvfile, dialect='mydialect')
    thedatawriter.writerow(header)
    for row in n:
        thedatawriter.writerow(row)

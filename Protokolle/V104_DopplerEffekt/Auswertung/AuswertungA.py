import numpy as np
from scipy.stats import sem
from uncertainties import ufloat
import uncertainties.unumpy as unp

Mittelwert, Fehler = np.genfromtxt('ErgebnisseA.txt', unpack = True)

#print(Mittelwert)
#print(Fehler)

Z2  = ufloat(Mittelwert[1], Fehler[1])
Z3  = ufloat(Mittelwert[2], Fehler[2])
Z4  = ufloat(Mittelwert[3], Fehler[3])
Z5  = ufloat(Mittelwert[4], Fehler[4])
Z6  = ufloat(Mittelwert[5], Fehler[5])
Z7  = ufloat(Mittelwert[6], Fehler[6])
Z8  = ufloat(Mittelwert[7], Fehler[7])
Z9  = ufloat(Mittelwert[8], Fehler[8])
Z10 = ufloat(Mittelwert[9], Fehler[9])
Z11 = ufloat(Mittelwert[10], Fehler[10])

ZBG = ufloat(10**-6, 10**-11)
Length = ufloat(0.202, 0.001)

pulses = np.array([ 0.0, Z2, Z3, Z4, Z5, Z6, Z7, Z8, Z9, Z10, Z11 ])

times    = ZBG * 10**2 * pulses
times[0] = 1
times[1] = ZBG * 10**3 * Z2
times[2] = ZBG * 10**3 * Z3

TM = np.array(unp.nominal_values(times))
TF = np.array(unp.std_devs(times))

Speed = Length/times

VM = np.array(unp.nominal_values(Speed))
VF = np.array(unp.std_devs(Speed))

TM[0] = 0.0
TF[0] = 0.0
VM[0] = 0.0
VF[0] = 0.0

np.savetxt('Speed2.txt', np.column_stack([Mittelwert, Fehler, TM, TF, VM, VF]))
np.savetxt('Geschwindigkeiten2.txt', np.column_stack([VM, VF]))

import numpy as np
from scipy.stats import sem
from uncertainties import ufloat
import uncertainties.unumpy as unp

V_m, V_f = np.genfromtxt('Geschwindigkeiten.txt', unpack = True)

I1_m, I1_f = np.genfromtxt('ErgebnisseC.txt', unpack = True)
I2_m, I2_f = np.genfromtxt('ErgebnisseC2.txt', unpack = True)

Gang = np.array([6, 12, 18, 24, 30, 36, 42, 48, 54, 60])
Gangk = np.array([6, 12, 18, 24, 30, 36, 42, 48])
Gangs = np.array([6, 12, 18, 24, 30, 36])

ZBG = ufloat(10**-6, 10**-11)
time = ZBG * 8 * 10**2

Vk = np.array([- V_m[0], - V_m[1], - V_m[2], - V_m[3], - V_m[4], - V_m[5], - V_m[6], - V_m[7]])
Vs = np.array([V_m[0], V_m[1], V_m[2], V_m[3], V_m[4], V_m[5]])

RF = np.array([20742, 20742, 20742, 20742, 20742, 20742, 20742, 20742, 20742, 20742])
RFk = np.array([20742, 20742, 20742, 20742, 20742, 20742, 20742, 20742])

D1 = I1_m - RF
D2 = I2_m - RFk
print(I1_m)
print(D1)
print(D2)

#np.savetxt('Delta1.txt', np.column_stack([Gang, V_m, I1_m, D1]))
#np.savetxt('Delta2.txt', np.column_stack([Gangk, Vk, I2_m, D2]))

messungCS = np.genfromtxt("MessungCS.txt")
messungCS = np.transpose(messungCS)
CS = np.array([[0, 0]])

for row in messungCS:
    s = 1 / np.sqrt(len(row))
    XM = np.mean(row)
    SD = np.std(row, ddof = 1)
    SD = s * SD
    Z  = np.array([[XM, SD]])
    CS = np.concatenate((CS, Z))


Werte = np.array([30, 17, 8, 30, 10, 30, 30, 30, 31, 30])
s = 1 / np.sqrt(len(Werte))
WM = np.mean(Werte)
WD = np.std(Werte, ddof = 1)
SD = s * SD

CS_m, CS_f, = np.split(np.transpose(CS), 2)
CS_m = CS_m[0]
CS_f = CS_f[0]

CSm = np.array([CS_m[1], CS_m[2], CS_m[3], CS_m[4], WM, CS_m[5]])
CSf = np.array([CS_f[1], CS_f[2], CS_f[3], CS_f[4], WD, CS_f[5]])

#np.savetxt('Schwebung.txt', np.column_stack([Gangs, Vs, CSm, CSf]))

import numpy as np
from scipy.stats import sem

messungA = np.genfromtxt("MessungA.txt")
messungA = np.transpose(messungA)
A = np.array([[0, 0]])

for row in messungA:
    s = 1 / np.sqrt(len(row))
    XM = np.mean(row)
    SD = np.std(row, ddof = 1)
    SD = s * SD
    Z  = np.array([[XM, SD]])
    A = np.concatenate((A, Z))

#print(A)

messungC = np.genfromtxt("MessungC.txt")
messungC = np.transpose(messungC)
C = np.array([[0, 0]])

for row in messungC:
    s = 1 / np.sqrt(len(row))
    XM = np.mean(row)
    SD = np.std(row, ddof = 1)
    SD = s * SD
    Z  = np.array([[XM, SD]])
    C = np.concatenate((C, Z))

#print(C)

messungC2 = np.genfromtxt("MessungC2.txt")
messungC2 = np.transpose(messungC2)
C2 = np.array([[0, 0]])

for row in messungC2:
    s = 1 / np.sqrt(len(row))
    XM = np.mean(row)
    SD = np.std(row, ddof = 1)
    SD = s * SD
    Z  = np.array([[XM, SD]])
    C2 = np.concatenate((C2, Z))

#print(C2)

a1 , a2,  = np.split(np.transpose(A), 2)
c1 , c2,  = np.split(np.transpose(C), 2)
c21, c22, = np.split(np.transpose(C2), 2)

a1  = a1[0]
a2  = a2[0]
c1  = c1[0]
c2  = c2[0]
c21 = c21[0]
c22 = c22[0]

#np.savetxt('ErgebnisseA.txt', np.column_stack([a1, a2]))
#np.savetxt('ErgebnisseC.txt', np.column_stack([c1, c2]))
np.savetxt('ErgebnisseC2.txt', np.column_stack([c21, c22]))

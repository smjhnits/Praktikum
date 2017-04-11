import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import scipy.constants as const
from uncertainties import ufloat
import uncertainties.unumpy as unp

Stromstärken = np.array([0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5])

Messung_1 = np.array([237, 93, 37, 25, 14, 10, 7, 5, 4, 3, 2])
Messung_2 = np.array([256, 179, 125, 79, 58, 41, 38, 31, 21, 18, 14])
Messung_3 = np.array([272, 244, 210, 165, 124, 98, 84, 70, 60, 50, 44])

Dämpfung1 = ufloat(Messung_1[10], 0.5) / ufloat(Messung_1[0], 0.5)
Dämpfung2 = ufloat(Messung_2[10], 0.5) / ufloat(Messung_2[0], 0.5)
Dämpfung3 = ufloat(Messung_3[10], 0.5) / ufloat(Messung_3[0], 0.5)

print("Die Dämpfung bei der ungeschlitzten Aluminiumplatte beträgt ca. ", Dämpfung1*100, "%.", '\n')
print("Die Dämpfung bei der mittel geschlitzten Aluminiumplatte beträgt ca. ", Dämpfung2*100, "%.", '\n')
print("Die Dämpfung bei der maximal geschlitzten Aluminiumplatte beträgt ca. ", Dämpfung3*100, "%.", '\n')

#Messung 1

plt.clf()
plt.plot(Stromstärken, Messung_1, 'kx', label = r'Messung1')
plt.ylim(0, 300)
plt.xlim(-0.5, 5.5)
plt.xlabel(r'Stromstärke in A')
plt.ylabel(r'Zeit in s')
plt.legend(loc = 'best')
plt.savefig('Messung1.pdf')
#plt.show()

#Messung 2

plt.clf()
plt.plot(Stromstärken, Messung_2, 'kx', label = r'Messung2')
plt.ylim(0, 300)
plt.xlim(-0.5, 5.5)
plt.xlabel(r'Stromstärke in A')
plt.ylabel(r'Zeit in s')
plt.legend(loc = 'best')
plt.savefig('Messung2.pdf')
#plt.show()

#Messung 3

plt.clf()
plt.plot(Stromstärken, Messung_3, 'kx', label = r'Messung3')
plt.ylim(0, 300)
plt.xlim(-0.5, 5.5)
plt.xlabel(r'Stromstärke in A')
plt.ylabel(r'Zeit in s')
plt.legend(loc = 'best')
plt.savefig('Messung3.pdf')
#plt.show()

#Übereinander

plt.clf()
plt.plot(Stromstärken, Messung_1, 'kx', label = r'Messung1')
plt.plot(Stromstärken, Messung_2, 'rx', label = r'Messung2')
plt.plot(Stromstärken, Messung_3, 'bx', label = r'Messung3')
plt.ylim(0, 300)
plt.xlim(-0.5, 5.5)
plt.xlabel(r'Stromstärke in A')
plt.ylabel(r'Zeit in s')
plt.legend(loc = 'best')
plt.savefig('Kombiniert.pdf')
#plt.show()

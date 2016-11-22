import numpy as np
from scipy.stats import sem
from uncertainties import ufloat
import uncertainties.unumpy as unp

Masse = 0.33821

#Torso:
Ht = 0.13114
Rt = 0.023034

#Arme
Ha = 0.17864
Ra = 0.01002

#Beine
Hb = 0.20042
Rb = 0.01136

#Kopf
Hk = 0.071
Rk = 0.015805

#Volumen
Vt = Ht * np.pi * Rt**2
Va = Ha * np.pi * Ra**2
Vb = Hb * np.pi * Rb**2
Vk = Hk * np.pi * Rk**2

Vgesamt = Vt + 2*Va + 2*Vb + Vk

#Einzelmassen
Dichte = Masse / Vgesamt
Mt = Vt * Dichte
Ma = Va * Dichte
Mb = Vb * Dichte
Mk = Vk * Dichte

#Position 1
It1 = 1/2 * Mt * Rt**2
Ik1 = 1/2 * Mk * Rk**2
Ib1 = 1/2 * Mb * Rb**2 + Ma * (Rt/2)**2
Ia1 = Ma * ((Ra**2)/4 + (Ha**2)/12) + Ma * (Rt + Ha/2)**2

Iges1 = It1 + 2*Ib1 + 2*Ia1 + Ik1

print(Iges1)

#Position 2
Delta1 = np.sqrt((Rt + Ra)**2 + (Ha**2)/4)
Delta2 = np.sqrt((Rt + Rb)**2 + (Hb**2)/4)

It2 = 1/2 * Mt * Rt**2
Ik2 = 1/2 * Mk * Rk**2
Ib2 = 1/2 * Mb * Rb**2 + Mb * (Rt/2)**2 + Mb *((Rb**2)/4 + (Hb**2)/12) + Mb * Delta2**2
Ia2 = 1/2 * Ma * Ra**2 + Ma * (Rt + Ra)**2 + Ma *((Ra**2)/4 + (Hb**2)/12) + Ma * Delta1**2

Iges2 = It2 + Ik2 + Ib2 + Ia2

print(Iges2)

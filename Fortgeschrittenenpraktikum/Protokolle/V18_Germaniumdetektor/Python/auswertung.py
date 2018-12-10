import numpy as np
import matplotlib.pyplot as plt
import uncertainties
from scipy.signal import find_peaks

C_Eu = np.genfromtxt('2018-12-10_Nitschke_Pape/Europium1.Spe', unpack = True)
Channels = np.linspace(0,len(C_Eu)-1, len(C_Eu))
Limit_Eu = np.int(np.round(1500/2600 * len(C_Eu),0))

#plt.plot(Channels[:Limit_Eu], C_Eu[:Limit_Eu],  label = "Europium")
#plt.hist(C_Eu[:Limit_Eu], bins = np.round(len(C_Eu[:Limit_Eu])/2,0), label = 'Europium')
plt.hist(range(0, len(C_Eu[:4000]), 1),
         bins=np.linspace(0, len(C_Eu[:4000]), len(C_Eu[:4000])),
         weights=C_Eu[:4000], label='Spektrum')
plt.yscale('log')
plt.legend()
plt.show()

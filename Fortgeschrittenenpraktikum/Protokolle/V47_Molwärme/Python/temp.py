import numpy as np
import matplotlib.pyplot as plt

def T(R):
    return 0.00134 * R**2 + 2.296 * R - 243.02 + 273.15

start_R = 18
ende_R = 115

R = np.linspace(start_R, ende_R, 100000)
#Temp = np.array([T(n) for n in R])
Temp = T(R)

plt.plot(R, T(R))
plt.xlabel('R')
plt.ylabel('T in °C')
plt.xlim(start_R, ende_R)
plt.xticks(np.round(np.linspace(start_R, ende_R, 10)), np.round(np.linspace(start_R, ende_R, 10)))
plt.yticks(np.round(np.linspace(-200, 40, 10)), np.round(np.linspace(-200, 40, 10)))

for i in range(45):
    print(np.mean(R[np.round(Temp) == 80 + 5 * i]), "\n", 80 + 5 * i)

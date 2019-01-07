import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('scope_0.csv', skiprows=2, dtype=np.float64, names=['msecond', 'diode'])
df.head(5)
print(df.diode)

x = range(len(df.diode))

plt.clf()
plt.plot(x, df.diode)
plt.xlim(700, 1800)
plt.ylim(1.5, 4.5)
plt.show()

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Data

threshold_lase = 3.34 # V
threshold_no_lase = 3.32 # V

R = 100 # Ohm

I_lase = threshold_lase / R
I_no_lase = threshold_no_lase / R

print(f'Threshold lase = {I_lase}\n\nThreshold no lase = {I_no_lase}\n')

# Rb spectrum

df_1 = pd.read_csv('scope_0.csv', skiprows=2, dtype=np.float64, names=['msecond', 'diode'])

x_1 = np.array(range(len(df_1.diode)))
verschiebung_1 = 0 # default war 700
verschiebung = 700

plt.clf()
plt.plot(x_1 - verschiebung, df_1.diode, label='PD')
plt.xlim(0 + verschiebung_1, 1800 - verschiebung)
plt.ylim(1.4, 4.5)
plt.text(220 + verschiebung_1, 2.5, '87b', fontsize=12)
plt.text(360 + verschiebung_1, 1.5, '85b', fontsize=12)
plt.text(670 + verschiebung_1, 2.6, '85a', fontsize=12)
plt.text(930 + verschiebung_1, 2.5, '87a', fontsize=12)
plt.ylabel('U / V')
plt.xlabel('t / ms')
plt.savefig('../Pics/Rb_spectrum.pdf')


# Rb spectrum, substraction technique

df_2 = pd.read_csv('scope_1.csv', skiprows=2, dtype=np.float64, names=['msecond', 'diode'])

x_2 = np.array(range(len(df_2.diode)))
verschiebung_2 = 0 # default war 650
verschiebung -= 50

plt.clf()
plt.plot(x_2 - verschiebung, -df_2.diode, label='PD')
plt.xlim(0 + verschiebung_2, 1700 - verschiebung)
plt.text(120 + verschiebung_2, -0.37, '87b', fontsize=12)
plt.text(260 + verschiebung_2, -0.64, '85b', fontsize=12)
plt.text(590 + verschiebung_2, -0.18, '85a', fontsize=12)
plt.text(870 + verschiebung_2, -0.07, '87a', fontsize=12)
plt.ylim(-0.66, 0.1)
plt.ylabel('U / V')
plt.xlabel('t / ms')
plt.savefig('../Pics/Rb_spectrum_subst.pdf')

# Example spectrum

df_3 = pd.read_csv('scope_2.csv', skiprows=2, dtype=np.float64, names=['msecond', 'volt_1', 'volt_2'])

x_3 = np.array(range(len(df_3.volt_1)))

plt.clf()
plt.plot(x_3, df_3.volt_1, label='PD')
plt.ylabel('U / V')
plt.xlabel('t / ms')
plt.savefig('../Pics/example_spectrum.pdf')

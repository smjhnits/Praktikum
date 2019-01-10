import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Data

threshold_lase = 3.34 # V
threshold_no_lase = 3.32 # V

R_multimeter = 100 # Ohm

I_lase = threshold_lase / R_multimeter
I_no_lase = threshold_no_lase / R_multimeter

print(f'Threshold lase = {I_lase}\n\nThreshold no lase = {I_no_lase}\n')

# Rb spectrum

df_1 = pd.read_csv('scope_0.csv', skiprows=2, dtype=np.float64, names=['msecond', 'diode'])

x_1 = np.array(range(len(df_1.diode)))

plt.clf()
plt.plot(x_1 - 700, df_1.diode, label='PD')
plt.xlim(0, 1100)
plt.ylim(1.4, 4.5)
plt.text(220, 2.5, '87b', fontsize=12)
plt.text(360, 1.5, '85b', fontsize=12)
plt.text(670, 2.6, '85a', fontsize=12)
plt.text(930, 2.5, '87a', fontsize=12)
plt.ylabel('U / V')
plt.xlabel('t / ms')
plt.savefig('../Pics/Rb_spectrum.pdf')


# Rb spectrum, substraction technique

df_2 = pd.read_csv('scope_1.csv', skiprows=2, dtype=np.float64, names=['msecond', 'diode'])

x_2 = np.array(range(len(df_2.diode)))

plt.clf()
plt.plot(x_2 - 650, -df_2.diode, label='PD')
plt.xlim(0, 1050)
plt.text(120, -0.37, '87b', fontsize=12)
plt.text(260, -0.64, '85b', fontsize=12)
plt.text(590, -0.18, '85a', fontsize=12)
plt.text(870, -0.07, '87a', fontsize=12)
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
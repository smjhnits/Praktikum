import numpy as np
from pint import UnitRegistry

u = UnitRegistry()
Q_ = u.Quantity

frequenz = Q_(np.array([101, 210, 300, 400, 502, 600, 700, 800, 904, 1001]), 'kHz')

I_one_seven = Q_(np.array([0, 29, 31, 53, 93, 105, 128]), 'mA')
I_eight_ten_1 = Q_(np.array([126, 140, 148]), 'mA')
I_eight_ten_2 = Q_(np.array([164, 188, 216]), 'mA')


B_sweep_1 = Q_(np.array([5.4, 3.75, 5.53, 4.71, 1.13, 1.77, 0.92, 3.55, 3.97, 5.17]) * 0.1, 'A')
B_sweep_2 = Q_(np.array([6.61, 6.32, 9.04, 9.41, 7.10, 8.86, 9.19, 7.51, 7.65, 7.21]) * 0.1, 'A')


vertical = Q_(2.28 * 0.1, 'A')

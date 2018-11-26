import numpy as np

# B-Felsstärke für verschiedene Tiefe der Hallsonde in dem Elektromagneten
B = np.array([0, 0, 0, 1, 1, 1, 2, 4, 7, 13, 23, 43, 84, 166, 272, 351, 393, 413, 416, 423, 421, 426, 421, 422, 414, 411, 389, 343, 249, 136, 67, 35, 19, 10, 6, 3, 2, 1, 1, 0])

# Tiefe der Hallsonde in dem Elektromagneten
s = np.array([145, 143, 141, 139, 137, 135, 133, 131, 129, 127, 125, 123, 121, 119, 117, 115, 113, 111, 110, 109, 108, 107, 106, 105, 104, 103, 101, 99, 97, 95, 93, 91, 89, 87, 85, 83, 81, 79, 77, 75])

# Durchlass Wellenlönge des Monochromators / Intereferenzfilter
_lambda = np.array([1000, 1100, 1200, 1300, 1400, 1500, 1550, 1600])

# Winkel des hochreinen GaAs
hr_d = 5.11 

hr_theta_1_grad = np.array([137, 139, 140, 142, 144, 144, 156, 155])
hr_theta_2_grad = np.array([164, 160, 159, 159, 158, 156, 162, 162])

hr_theta_1_min = np.array([34, 0, 10, 15, 55, 0, 26, 8])
hr_theta_2_min = np.array([35, 32, 44, 24, 40, 26, 26, 25])

# Winkel des dotierten GaAs mit N = 1.2e18
N_1 = 1.2e18
d_1 = 1.36
theta_1_grad_1= np.array([144, 144, 146, 146, 147, 147, 154, 154])
theta_2_grad_1 = np.array([152, 153, 153, 153, 154, 159, 162, 161])

theta_1_min_1 = np.array([17, 0, 39, 0, 11, 40, 26, 34])
theta_2_min_1 = np.array([23, 37, 20, 32, 12, 0, 19, 55])

# Winkel des dotierten GaAs mit N = 2.8e18
N_2 = 2.8e18
d_2 = 1.296
theta_1_grad_2= np.array([147, 146, 147, 148, 146, 146, 153, 153])
theta_2_grad_2 = np.array([160, 156, 156, 154, 156, 156, 164, 162])

theta_1_min_2 = np.array([7, 51, 6, 22, 47, 15, 27, 40])
theta_2_min_2 = np.array([25, 11, 9, 40, 8, 50, 51, 0])
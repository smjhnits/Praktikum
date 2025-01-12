import numpy as np

# Stromstärke I in A und B-Feld B in mT

I_aufsteigend = np.linspace(0, 5, 11)
I_abfallend = np.linspace(5, 0, 11)
B_aufsteigend = np.array([7.7, 142, 272, 420, 556, 700, 840, 975, 1077, 1158, 1220])
B_abfallend = np.array([1220, 1169, 1095, 977, 845, 703, 563, 422, 279, 138, 8.3])

# Abmessungen der Proben [1] = Höhe, [2] = Breite, [3] = Dicke, Angaben in cm

Zink = np.array([2.603, 4.406, 0.043])
Kupfer = np.array([2.80, 2.53, 0.0018])

# Bestimmung der Widerstände von Zink und Kupfer, I in A, U in mV

I = np.linspace(0, 10, 11)
U_Zink = np.array([-0.02, 14.13, 27.7, 41.1, 55.5, 68.3, 81.5, 94.7, 107.1, 120.3, 133.7])
U_Kupfer = np.array([0, 7.83, 15.54, 23.3, 30.9, 38.6, 46.3, 53.9, 61.5, 68.8, 76.5])

# Messung der Hall-Spannung bei konstantem Probenstrom U_H in mV, Zink I_p: = 8 A, Kupfer: I_p = 10 A

I_s_Zink = np.linspace(0, 5, 11)
I_s_Kupfer = np.linspace(0, 3.5, 8)
Zink_Is_U_H_1 = np.array([0.644, 0.648, 0.651, 0.654, 0.657, 0.659, 0.661, 0.663, 0.664, 0.665, 0.666])
Kupfer_Is_U_H_1 = - np.array([0.342, 0.340, 0.338, 0.336, 0.334, 0.332, 0.330, 0.328])

# Umpolen

Zink_Is_U_H_2 = np.array([0.647, 0.646, 0.645, 0.644, 0.642, 0.641, 0.639, 0.638, 0.636, 0.635, 0.634])
Kupfer_Is_U_H_2 = - np.array([0.340, 0.342, 0.343, 0.345, 0.347, 0.349, 0.351, 0.3530])

# Messung der Hall-Spannung bei konstantem Spulenstrom U_H in mV, Zink: I_s = 5 A, Kupfer: I_s = 3 A

I_p = np.linspace(0, 8, 11)
I_p_Kupfer = np.linspace(0, 10, 11)
Zink_Ip_U_H_1 = np.array([-0.020, 0.045, 0.109, 0.174, 0.234, 0.304, 0.365, 0.431, 0.495, 0.560, 0.626])
Kupfer_Ip_U_H_1 = - np.array([0.336, 0.338, 0.340, 0.342, 0.343, 0.345, 0.347, 0.348, 0.350, 0.351, 0.352])

# Umpolen
Zink_Ip_U_H_2 = np.array([-0.020, 0.047, 0.116, 0.184, 0.250, 0.318, 0.389, 0.456, 0.527, 0.597, 0.666])
Kupfer_Ip_U_H_2 = - np.array([0.338, 0.337, 0.336, 0.335, 0.335, 0.334, 0.333, 0.332, 0.332, 0.332, 0.330])

import numpy as np

# Apparaturkonstanten

L  = 1.217
C_1 = 20.13
C_2 = 9.41
Wellenwiderstand_C = np.sqrt(L / C_1)
Wellenswiderstand_C1C2 = np.sqrt(2 * L / (C_1 + C_2))
return('Wellenwiderstand_C: ', Wellenwiderstand_C)
return('Wellenswiderstand_C1C2: ', Wellenswiderstand_C1C2)

# a.) Durchlasskurve

nu_C_Duchlasskurve = np.array([1338, 2055, 2843, 3730, 5023, 6471, 8624])
nu_C1C2_Durchlasskurve = np.array([7345, 10478, 21072,30336, 50353, 79169])

# b.) Dispersionrelation

nu_C_Dispersion = np.array([0, 7927, 15610, 23372, 30703, 38072, 43171, 49000])
nu_C1C2_Dispersion = np.array([0, 7158, 14188, 21078, 27714, 34188, 40094, 45378, 50298, 54295, 57976, 60550, 62625])

# d.) Messung der Spannungsamplituden der offenen LC-Kette

nu_1 = 7133
Kettenglieder_C = np.array([1.55, 1.425, 1.2, 0.95, 0.66, 0.3, 0.027, 0.3, 0.95, 1.2, 1.4, 1.55, 1.575])
nu_2 = 14307
Kettenglieder_C1C2 = np.array([0.925, 0.65, 0.25, 0.2, 0.61, 0.9, 1, 0.98, 0.71, 0.28, 0.17, 0.65, 1, 1.05])

# e.) Messung der Spannungsamplituden einer abgeschlossenen LC-Kette

nu_3 = 7337
Kettenglieder_C_e = np.array([25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 24.5, 24.5, 24.5])

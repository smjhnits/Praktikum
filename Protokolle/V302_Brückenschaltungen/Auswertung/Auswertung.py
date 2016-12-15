import numpy as np
from scipy.stats import sem
from uncertainties import ufloat
import uncertainties.unumpy as unp
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Wheatstone

Messung_Wert_10 = np.array([[1000, 196, 804],
                           [664 , 268, 732],
                           [332 , 422, 578]])

Messung_Wert_12 = np.array([[332 , 543, 457],
                           [664 , 373, 627],
                           [1000, 284, 716]])

Wheatstone10= np.array([row[0] * row[1] / row[2] for row in Messung_Wert_10])
Wheatstone12 = np.array([row[0] * row[1] / row[2] for row in Messung_Wert_12])

print("Ergebnisse für Wheatstone: ", '\n', "Wert 10: ", Wheatstone10, '\n', "Wert 12: ", Wheatstone12, '\n')

# Kapazität

Messung_Wert_3 = np.array([[450, 519, 481],
                          [399, 490, 510],
                          [597, 590, 410]])

Messung_Wert_1 = np.array([[450, 407, 593],
                          [399, 380, 620],
                          [597, 478, 522]])

Kapazitäten3 = np.array([row[0] * row[2] / row[1] for row in Messung_Wert_3])
Kapazitäten1 = np.array([row[0] * row[2] / row[1] for row in Messung_Wert_1])

print("Ergebnisse für Kapazitäten: ", '\n', "Wert 3: ", Kapazitäten3, '\n', "Wert 1: ", Kapazitäten1, '\n')

# RC - Glied

Messung_Wert_8 = np.array([[450, 371, 606, 394],
                          [399, 418, 578, 422],
                          [597, 278, 673, 327]])

Messung_Wert_9 = np.array([[450, 466, 511, 489],
                          [399, 524, 482, 518],
                          [597, 352, 581, 419]])

Kapazitäten8 = np.array([row[0] * row[3] / row[2] for row in Messung_Wert_8])
Kapazitäten9 = np.array([row[0] * row[3] / row[2] for row in Messung_Wert_9])
Wiederstand8 = np.array([row[1] * row[2] / row[3] for row in Messung_Wert_8])
Wiederstand9 = np.array([row[1] * row[2] / row[3] for row in Messung_Wert_9])

print("Ergebnisse für RC-Glied: ", '\n')
print("Ergebnisse Kapazitäten: ", '\n', "Wert 8: ", Kapazitäten8, '\n', "Wert 9: ", Kapazitäten9,)
print("Ergebnisse Wiederstände: ", '\n', "Wert 8: ", Wiederstand8, '\n', "Wert 9: ", Wiederstand9, '\n')

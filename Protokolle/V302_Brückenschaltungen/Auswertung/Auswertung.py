import numpy as np
from scipy.stats import sem
from uncertainties import ufloat
import uncertainties.unumpy as unp
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def Mean_Std(Werte):
    s = 1/np.sqrt(len(Werte))
    return ufloat(np.mean(Werte), s * np.std(Werte, ddof = 1))

# Wheatstone

Messung_Wert_10 = np.array([[1000, 196, 804],
                           [664 , 268, 732],
                           [332 , 422, 578]])

Messung_Wert_12 = np.array([[332 , 543, 457],
                           [664 , 373, 627],
                           [1000, 284, 716]])

Wheatstone10= np.array([row[0] * row[1] / row[2] for row in Messung_Wert_10])
Wheatstone12 = np.array([row[0] * row[1] / row[2] for row in Messung_Wert_12])

print("Ergebnisse für Wheatstone: ", '\n', "Wert 10: ", Wheatstone10, Mean_Std(Wheatstone10), '\n', "Wert 12: ", Wheatstone12, Mean_Std(Wheatstone12), '\n')

# Kapazität

Messung_Wert_3 = np.array([[450, 519, 481],
                          [399, 490, 510],
                          [597, 590, 410]])

Messung_Wert_1 = np.array([[450, 407, 593],
                          [399, 380, 620],
                          [597, 478, 522]])

Kapazitäten3 = np.array([row[0] * row[2] / row[1] for row in Messung_Wert_3])
Kapazitäten1 = np.array([row[0] * row[2] / row[1] for row in Messung_Wert_1])

print("Ergebnisse für Kapazitäten: ", '\n', "Wert 3: ", Kapazitäten3, Mean_Std(Kapazitäten3), '\n', "Wert 1: ", Kapazitäten1, Mean_Std(Kapazitäten1), '\n')

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
print("Ergebnisse Kapazitäten: ", '\n', "Wert 8: ", Kapazitäten8, Mean_Std(Kapazitäten8), '\n', "Wert 9: ", Kapazitäten9, Mean_Std(Kapazitäten9))
print("Ergebnisse Wiederstände: ", '\n', "Wert 8: ", Wiederstand8, Mean_Std(Wiederstand8), '\n', "Wert 9: ", Wiederstand9, Mean_Std(Wiederstand9), '\n')

# RL - Glied klassisch

Klassisch_Wert_16 = np.array([[14.6, 45, 907, 83],
                           [20.1, 57, 875, 125],
                           [27.5, 85, 837, 163]])

Klassisch_Wert_18 = np.array([[14.6, 108, 775, 225],
                           [20.1, 143, 715, 285],
                           [27.5, 197, 648, 352]])

Induktivität16 = np.array([row[0] * row[2] / row[3] for row in Klassisch_Wert_16])
Induktivität18 = np.array([row[0] * row[2] / row[3] for row in Klassisch_Wert_18])
Wiederstand16 = np.array([row[1] * row[2] / row[3] for row in Klassisch_Wert_16])
Wiederstand18 = np.array([row[1] * row[2] / row[3] for row in Klassisch_Wert_18])

print("Ergebnisse für RL-Glied klassisch: ", '\n')
print("Ergebnisse Induktivität: ", '\n', "Wert 16: ", Induktivität16, Mean_Std(Induktivität16), '\n', "Wert 18: ", Induktivität18, Mean_Std(Induktivität18))
print("Ergebnisse Wiederstände: ", '\n', "Wert 16: ", Wiederstand16, Mean_Std(Wiederstand16), '\n', "Wert 18: ", Wiederstand18, Mean_Std(Wiederstand18), '\n')

# RL - Glied Maxwell

C4 = 399 * 10**(-6)

Maxwell_Wert_18 = np.array([[1000, 128, 347],
                           [664, 193, 349],
                           [332, 382, 348]])

Maxwell_Wert_16 = np.array([[1000, 347, 829],
                           [664, 523, 829],
                           [332, 1036, 829]])

mInduktivität16 = np.array([row[0] * row[1] * C4 for row in Maxwell_Wert_16])
mInduktivität18 = np.array([row[0] * row[1] * C4 for row in Maxwell_Wert_18])
mWiederstand16 = np.array([row[1] * row[0] / row[2] for row in Maxwell_Wert_16])
mWiederstand18 = np.array([row[1] * row[0] / row[2] for row in Maxwell_Wert_18])

print("Ergebnisse für RL-Glied Maxwell: ", '\n')
print("Ergebnisse Induktivität: ", '\n', "Wert 16: ", mInduktivität16, Mean_Std(mInduktivität16), '\n', "Wert 18: ", mInduktivität18, Mean_Std(mInduktivität18))
print("Ergebnisse Wiederstände: ", '\n', "Wert 16: ", mWiederstand16, Mean_Std(mWiederstand16), '\n', "Wert 18: ", mWiederstand18, Mean_Std(mWiederstand18), '\n')

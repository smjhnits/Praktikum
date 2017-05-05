import numpy as np
from scipy.stats import sem
from uncertainties import ufloat
import uncertainties.unumpy as unp
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

Weglänge         = np.array([1.79, 1.71, 1.77, 1.76, 1.73, 1.73, 1.74, 1.75, 1.75, 1.73]) * 10**(-3)
Anzahl_Messung1  = np.array([1051, 1002, 1044, 1036, 1013, 1031, 1027, 1034, 1029, 1022])

Druck_Luft       = np.array([0.76, 0.8, 0.8, 0.8, 0.82, 0.83, 0.8, 0.81, 0.82, 0.8])
Anzahl_Messung2  = np.array([35, 34, 34, 35, 35, 35, 34, 35, 35, 33])

Druck_CO2        = np.array([0.8, 0.8, 0.64, 0.6, 0.56, 0.52, 0.48, 0.44, 0.4, 0.37])
Anzahl_Messung3  = np.array([58, 50, 36, 39, 37, 35, 29, 28, 25, 24])

Länge_Gaskammer  = 0.05
T_0 = 273.15
T   = 293.15
p_0 = 1.0132
Übersetzung = 5.046

def Wert(A):
    Fehler = np.std(A, ddof=1) * 1 / np.sqrt(len(A))
    return ufloat( np.mean(A), Fehler)

def Brechung(A, B):
    return np.array([ (n * A / (2 * Länge_Gaskammer)) for n in B])

def Brechungsindex(A, B):
    return np.array([ (1 + n * (T/T_0) * (p_0/B[i])) for i,n in enumerate(A)])

Wellenlängen   = np.array([Weglänge[i] / Übersetzung * 2 / n for i,n in enumerate(Anzahl_Messung1)])
Wellenlänge = Wert(Wellenlängen)

Brechung_Luft = Brechung(Wellenlänge, Anzahl_Messung2)
Brechungsindex_Luft = Brechungsindex(Brechung_Luft, Druck_Luft)

Brechung_CO2 = Brechung(Wellenlänge, Anzahl_Messung3)
Brechungsindex_CO2 = Brechungsindex(Brechung_CO2, Druck_CO2)

#Ausgabe Messung a
#print("Weglängen: ", Weglänge/Übersetzung *10**3, '\n')
#print("Gemessene Intensitätsmaxima: ", Anzahl_Messung1, '\n')
#print("Berechnete Wellenlängen: ", Wellenlängen*10**9, '\n' )
#print("Gemittelte Wellenlänge: ", Wellenlänge, '\n')

#Ausgabe Messung b Luft
#print("Gemessene Druckdifferenzen: ", Druck_Luft, '\n')
#print("Gemessene Intensitätsmaxima: ", Anzahl_Messung2, '\n')
#print("Berechnete Brechungsdifferenzen: ", Brechung_Luft, '\n')
#print("Berechnete Brechungsindize: ", Brechungsindex_Luft, '\n')
#print("Brechungsindex Luft: ", np.mean(Brechungsindex_Luft), '\n')

#Ausgabe Messung b Kohlenstoffdioxid
print("Gemessene Druckdifferenzen: ", Druck_CO2, '\n')
print("Gemessene Intensitätsmaxima: ", Anzahl_Messung3, '\n')
print("Berechnete Brechungsdifferenzen: ", Brechung_CO2, '\n')
print("Berechnete Brechungsindize: ", Brechungsindex_CO2, '\n')
print("Brechungsindex CO2: ", np.mean(Brechungsindex_CO2), '\n')

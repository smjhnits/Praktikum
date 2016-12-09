import numpy as np
from scipy.stats import sem
from uncertainties import ufloat
import uncertainties.unumpy as unp
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

daten = np.genfromtxt("Daten.txt", unpack = True)

DurchmesserGr  = np.array([1.561, 1.560, 1.560])
DurchmesserKl  = np.array([1.543, 1.544, 1.543])

RadiusGr  = DurchmesserGr / 2
RadiusKl  = DurchmesserKl / 2
GewichtGr = np.array([4.96, 4.96, 4.96])
GewichtKl = np.array([4.45, 4.45, 4.45])

s = 1 / np.sqrt(3)

Rgr = ufloat(np.mean(RadiusGr), np.std(RadiusGr, ddof = 1) * s)
Rkl = ufloat(np.mean(RadiusKl), np.std(RadiusKl, ddof = 1) * s)
Ggr = ufloat(np.mean(GewichtGr), np.std(GewichtGr, ddof = 1) * s)
Gkl = ufloat(np.mean(GewichtKl), np.std(GewichtKl, ddof = 1) * s)


print("Durchmesser große Kugel: ", np.mean(DurchmesserGr), np.std(DurchmesserGr, ddof = 1) *s)
print("Durchmesser kleine Kugel: ", np.mean(DurchmesserKl), np.std(DurchmesserKl, ddof = 1) *s)
print("Radius große Kugel: ", Rgr, " cm")
print("Gewicht große Kugel: ", Ggr, " g")
print("Radius kleine Kugel: ", Rkl, " cm")
print("Gewicht kleine Kugel: ", Gkl, " g")
print('\n')

#Auslesen und Mitteln der Daten
FallzeitKugel2 = ufloat(np.mean(daten[0]), np.std(daten[0], ddof = 1) * 1/np.sqrt(len(daten[0])))
FallzeitKugel1 = ufloat(np.mean(daten[1]), np.std(daten[1], ddof = 1) * 1/np.sqrt(len(daten[1])))
Temperaturen = daten[2]
Temperaturen += 273.15
Messungen = np.array([daten[3], daten[4]])
Messungen = np.transpose(Messungen)

print("Fallzeit kleine Kugel: ", FallzeitKugel2)
print("Fallzeit große Kugel: ", FallzeitKugel1)
print("Temperaturen: ", '\n', Temperaturen)
print('\n')

Mittelwerte = np.array([ np.mean(row) for row in Messungen ])
Fehler = np.array([1/np.sqrt(len(row)) * np.std(row, ddof=1) for row in Messungen])
kombiniert = np.array([ufloat(n, Fehler[i]) for i,n in enumerate(Mittelwerte)])

#print("Messung der Fallzeiten: ", '\n', unp.nominal_values(kombiniert))
print("Messung der Fallzeiten: ", '\n', kombiniert)
print('\n')

#Ermittlung der Kugeldichte und benötigte Daten

DichteKl = Gkl / (4/3 * np.pi * Rkl**3)
#DichteKl /= 1000                         # Anpassung in g/cm^3
DichteGr = Ggr / (4/3 * np.pi * Rgr**3)
#DichteGr /= 1000                         # Anpassung in g/cm^3
DichteW = 0.998
DichteW_array = np.array([0.9957, 0.994, 0.9922, 0.9902, 0.9880, 0.9980, 0.9857, 0.9832, 0.9806, 0.9778])
Kkl = 0.07640                            # in mPa * cm^3 / g

print("Kugel 1 = große Kugel")
print("Kugel 2 = kleine Kugel")
print("Dichte der kleinen Kugel: ", DichteKl, " g/cm^3")
print("Dichte der großen Kugel: ", DichteGr, " g/cm^3")
print("Dichte Wasser: ", DichteW, " g/cm^3")
print('\n')

#Ermittlung von K

Viskositätkl20 = (Kkl * (DichteKl - DichteW) * FallzeitKugel2)
Kgr = Viskositätkl20 / ( (DichteGr - DichteW) * FallzeitKugel1)
print("Viskosität kleiner Kugel: ", Viskositätkl20, " mPa s")
print("Apparaturkonstante kleine Kugel: ", Kkl, " mPa s cm^3 7 g")
print("Apparaturkonstante große Kugel: ", Kgr, " mPa s cm^3 7 g")
print('\n')


#Ermittlung der ViskositäTemperaturen

Viskos = np.array([ Kgr * (DichteGr - DichteW_array[i]) * n for i,n in enumerate(kombiniert) ])

#print("Viskositäten: ",'\n',  unp.nominal_values(Viskos))

print("Viskositäten: ",'\n',  Viskos)
print('\n')

print("Temperaturen: ", '\n', Temperaturen)
print('\n')
Viskos *= 10**(-3)

#Literaturwerte einspeichern

ViskosLit = np.array([ 797.7, 653.1, 547.1, 466.8, 404.5, ])

ViskosLit *= 10**(-3)

Temperature = np.array([ 30.0, 40.0 , 50.0, 60.0, 70.0, ])
Temperature += 273.15

print("Viskositäten Literaturwerte: ", '\n' , ViskosLit)
print('\n')
print("Temperaturen Literatur: ", '\n', Temperature)
print('\n')
ViskosLit *= 10**(-3)
#Plot anfertigen

def f(x, A, B):
    return A * np.exp( B / x)

params, covariance = curve_fit(f, Temperaturen, unp.nominal_values(Viskos))
paramslit, covariancelit = curve_fit(f, Temperature, ViskosLit)

x_plot = np.linspace(300, 350, num = 100)

#Der Scheiß für Mareike

Viskoslog = np.log(unp.nominal_values(Viskos))
Viskoslitlog = np.log(unp.nominal_values(ViskosLit))

def g(x, A, B):
    return A * 1/x + B

paramslog, covariancelog = curve_fit(g, Temperaturen, Viskoslog)
errorsExperimentell = np.sqrt(np.diag(covariancelog))
paramslitlog, covariancelitlog = curve_fit(g, Temperature, Viskoslitlog)
errorsLit = np.sqrt(np.diag(covariancelitlog))

print("Parameter für Viskositäten Literatur: ", '\n', paramslit, " A in mPa s, B in K")
print("Parameter mit linearer Regression", '\n', paramslitlog)
print("Fehler der linearen Regression: ", '\n', errorsExperimentell[0], errorsExperimentell[1])
print('\n')

# Plot mit V gegen 1/T

plt.clf()
plt.plot(1/Temperaturen, unp.log(unp.nominal_values(Viskos)), "bx", label = "Viskositäten")
#plt.plot(1/x_plot, unp.log(f(x_plot, *params)), "r-", label = "Regressionskurve")
plt.plot(1/Temperature, unp.log(ViskosLit), "gx", label = "Viskositäten Literatur")
plt.plot(1/x_plot, g(x_plot, *paramslitlog), "k-", label = "Fit der Literaturwerte")
plt.plot(1/x_plot, g(x_plot, *paramslog), "r-", label = "Linearer Fit") #fwfewf
plt.grid(True, which = "both")
plt.xlabel(r"$1/T \,\, in \,\, 1/K$")
plt.ylabel(r"$ln(\eta)$ ")
plt.legend(loc = 'best')
plt.xlim(0.0029, 0.00333)
#plt.yscale('log')
plt.tight_layout()
plt.savefig("Plot_T_1.pdf")

print("Parameter für Viskositäten Experimentell: ", '\n', params, " A in mPa s, B in K")
print("Parameter mit linearem Fit: ",  '\n',paramslog,)
ParameterA = ufloat(paramslog[1], errorsExperimentell[1])
print("Parameter A : ", unp.exp(ParameterA))
print("Fehler der linearen Regression: ", '\n',  errorsLit[0], errorsLit[1])
print('\n')
#plt.show()

print("Parameter: ", params)
print('\n')

#Abweichungen Literatur und Experimentell

ViskosLit2 = np.array([ paramslit[0] * np.exp( paramslit[1] / n ) for n in Temperaturen])
Abweichungen = Viskos - ViskosLit2
print("Durchschnittliche Abweichung: ", np.mean(Abweichungen))
print('\n')

#Geschwindigkeiten

Strecke = 0.1
Geschwindigkeiten = Strecke / kombiniert
Vcm = Geschwindigkeiten * 100

#print("Geschwindigkeiten: ", '\n', unp.nominal_values(Vcm) )
print("Geschwindigkeiten:  Angaben in cm", '\n', Vcm)
print('\n')

#Reynoldszahl

Reynolds = np.array([DichteW_array[i] * Vcm[i] * 2 * Rgr  / 10 / n for i,n in enumerate(Viskos)])
#print("Reynoldszahl mit cm : ", '\n', unp.nominal_values(Reynolds))
print("Reynoldszahl große Kugel : ", '\n', Reynolds)
print('\n')

#Reynoldszahl kleine Kugel

Viskositätkl20 *= 10**(-3)

Reynoldskl = DichteW * Strecke * 2 * Rkl / 10 / Viskositätkl20
print("Reynoldszahl in cm kleine kugel : ", '\n' ,Reynoldskl)

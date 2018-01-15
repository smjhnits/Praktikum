import numpy as np
from scipy.stats import sem
from uncertainties import ufloat
import uncertainties.unumpy as unp
import matplotlib.pyplot as plt
import scipy.constants as sc
from scipy.optimize import curve_fit
from numpy.linalg import inv

A = np.matrix([[0, 0, 0, 0, 0, np.sqrt(2), 0, np.sqrt(2), 0],
               [0, 0, np.sqrt(2), 0, np.sqrt(2), 0, np.sqrt(2), 0, 0],
               [0, np.sqrt(2), 0, np.sqrt(2), 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 1, 1, 1],
               [0, 0, 0, 1, 1, 1, 0, 0, 0],
               [1, 1, 1, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, np.sqrt(2), 0, 0, 0, np.sqrt(2), 0],
               [np.sqrt(2), 0, 0, 0, np.sqrt(2), 0, 0, 0, np.sqrt(2)],
               [0, np.sqrt(2), 0, 0, 0, np.sqrt(2), 0, 0, 0],
               [1, 0, 0, 1, 0, 0, 1, 0, 0],
               [0, 1, 0, 0, 1, 0, 0, 1, 0],
               [0, 0, 1, 0, 0, 1, 0, 0, 1]])

A_t = np.transpose(A)

Alu_Werte = np.array([8206, 2268, 2135, 2336, 2837, 2186, 2138, 2204, 3057, 2504, 2228, 2446])
Alu_Zeiten = np.array([84, 30, 26, 26, 30, 24, 24, 29, 34, 26, 24, 23])
Alu_Fehler = np.sqrt(Alu_Werte)
Alu_Real = np.array([ufloat(n, Alu_Fehler[i]) for i,n in enumerate(Alu_Werte)])
Alu_Rate = Alu_Real/Alu_Zeiten
Alu_Rate_2 = Alu_Werte/Alu_Zeiten

Blei_Werte = np.array([1218, 1197, 1203, 1198, 1205, 1206, 1212, 1197, 1240, 1255, 1207, 1207])
Blei_Zeiten = np.array([110, 375, 203, 161, 183, 187, 99, 424, 182, 124, 192, 195])
Blei_Fehler = np.sqrt(Blei_Werte)
Blei_Real = np.array([ufloat(n, Blei_Fehler[i]) for i,n in enumerate(Blei_Werte)])
Blei_Rate = Blei_Real/Blei_Zeiten
Blei_Rate_2 = Blei_Werte/Blei_Zeiten

Unb_Werte = np.array([12575, 12758, 12622, 12916, 12965, 13018, 12905, 12840, 12898, 12888, 12510, 12536])
Unb_Zeiten = np.array([822, 1503, 690, 648, 700, 683, 341, 1345, 1193, 125, 1407, 799])
Unb_Fehler = np.sqrt(Unb_Werte)
Unb_Real = np.array([ufloat(n, Unb_Fehler[i]) for i,n in enumerate(Unb_Werte)])
Unb_Rate = Unb_Real/Unb_Zeiten
Unb_Rate_2 = Unb_Werte/Unb_Zeiten

Luft_Werte = np.array([16115, 16042, 16115, 15341, 15341, 15341, 16115, 16042, 16115, 15341, 15341, 15341])
Luft_Zeiten = np.array([87, 87, 87, 83, 83, 83, 87, 87, 87, 83, 83, 83])
Luft_Fehler = np.sqrt(Luft_Werte)
Luft_Real = np.array([ufloat(n, Luft_Fehler[i]) for i,n in enumerate(Luft_Werte)])
Luft_Rate = Luft_Real/Luft_Zeiten
Luft_Rate_2 = Luft_Werte/Luft_Zeiten

V_Al_N = np.matrix([[Alu_Fehler[0]**2,0,0,0,0,0,0,0,0,0,0,0],
                    [0,Alu_Fehler[1]**2,0,0,0,0,0,0,0,0,0,0],
                    [0,0,Alu_Fehler[2]**2,0,0,0,0,0,0,0,0,0],
                    [0,0,0,Alu_Fehler[3]**2,0,0,0,0,0,0,0,0],
                    [0,0,0,0,Alu_Fehler[4]**2,0,0,0,0,0,0,0],
                    [0,0,0,0,0,Alu_Fehler[5]**2,0,0,0,0,0,0],
                    [0,0,0,0,0,0,Alu_Fehler[6]**2,0,0,0,0,0],
                    [0,0,0,0,0,0,0,Alu_Fehler[7]**2,0,0,0,0],
                    [0,0,0,0,0,0,0,0,Alu_Fehler[8]**2,0,0,0],
                    [0,0,0,0,0,0,0,0,0,Alu_Fehler[9]**2,0,0],
                    [0,0,0,0,0,0,0,0,0,0,Alu_Fehler[10]**2,0],
                    [0,0,0,0,0,0,0,0,0,0,0,Alu_Fehler[11]**2]])

V_Pb_N = np.matrix([[Blei_Fehler[0]**2,0,0,0,0,0,0,0,0,0,0,0],
                    [0,Blei_Fehler[1]**2,0,0,0,0,0,0,0,0,0,0],
                    [0,0,Blei_Fehler[2]**2,0,0,0,0,0,0,0,0,0],
                    [0,0,0,Blei_Fehler[3]**2,0,0,0,0,0,0,0,0],
                    [0,0,0,0,Blei_Fehler[4]**2,0,0,0,0,0,0,0],
                    [0,0,0,0,0,Blei_Fehler[5]**2,0,0,0,0,0,0],
                    [0,0,0,0,0,0,Blei_Fehler[6]**2,0,0,0,0,0],
                    [0,0,0,0,0,0,0,Blei_Fehler[7]**2,0,0,0,0],
                    [0,0,0,0,0,0,0,0,Blei_Fehler[8]**2,0,0,0],
                    [0,0,0,0,0,0,0,0,0,Blei_Fehler[9]**2,0,0],
                    [0,0,0,0,0,0,0,0,0,0,Blei_Fehler[10]**2,0],
                    [0,0,0,0,0,0,0,0,0,0,0,Blei_Fehler[11]**2]])

V_Unb_N = np.matrix([[Unb_Fehler[0]**2,0,0,0,0,0,0,0,0,0,0,0],
                    [0,Unb_Fehler[1]**2,0,0,0,0,0,0,0,0,0,0],
                    [0,0,Unb_Fehler[2]**2,0,0,0,0,0,0,0,0,0],
                    [0,0,0,Unb_Fehler[3]**2,0,0,0,0,0,0,0,0],
                    [0,0,0,0,Unb_Fehler[4]**2,0,0,0,0,0,0,0],
                    [0,0,0,0,0,Unb_Fehler[5]**2,0,0,0,0,0,0],
                    [0,0,0,0,0,0,Unb_Fehler[6]**2,0,0,0,0,0],
                    [0,0,0,0,0,0,0,Unb_Fehler[7]**2,0,0,0,0],
                    [0,0,0,0,0,0,0,0,Unb_Fehler[8]**2,0,0,0],
                    [0,0,0,0,0,0,0,0,0,Unb_Fehler[9]**2,0,0],
                    [0,0,0,0,0,0,0,0,0,0,Unb_Fehler[10]**2,0],
                    [0,0,0,0,0,0,0,0,0,0,0,Unb_Fehler[11]**2]])


# Bestimmung der Itensitäten

I_Alu = np.array([unp.log(n/Alu_Rate[i]) for i,n in enumerate(Luft_Rate)])
I_Blei = np.array([unp.log(n/Blei_Rate[i]) for i,n in enumerate(Luft_Rate)])
I_Unb = np.array([unp.log(n/Unb_Rate[i]) for i,n in enumerate(Luft_Rate)])

I_Alu_2 = np.array([unp.log(n/Alu_Rate_2[i]) for i,n in enumerate(Luft_Rate_2)])
I_Blei_2 = np.array([unp.log(n/Blei_Rate_2[i]) for i,n in enumerate(Luft_Rate_2)])
I_Unb_2 = np.array([unp.log(n/Unb_Rate_2[i]) for i,n in enumerate(Luft_Rate_2)])

Alu_t = np.transpose(np.array([I_Alu]))
Blei_t = np.transpose(np.array([I_Blei]))
Unb_t = np.transpose(np.array([I_Unb]))

Alu_t_2 = np.transpose(np.array([I_Alu_2]))
Blei_t_2 = np.transpose(np.array([I_Blei_2]))
Unb_t_2 = np.transpose(np.array([I_Unb_2]))

#Bestimmung der Koeffizienten

V_Al_mu = inv(A_t*inv(V_Al_N)*A)
Al_mu_2 = inv(A_t*inv(V_Al_N)*A) * A_t*inv(V_Al_N)*Alu_t_2

V_Pb_mu = inv(A_t*inv(V_Pb_N)*A)
Pb_mu_2 = inv(A_t*inv(V_Pb_N)*A) * A_t*inv(V_Pb_N)*Blei_t_2

V_Unb_mu = inv(A_t*inv(V_Unb_N)*A)
Unb_mu_2 = inv(A_t*inv(V_Unb_N)*A) * A_t*inv(V_Unb_N)*Unb_t_2

print(np.mean(Al_mu_2),'\n')
print(np.mean(Pb_mu_2),'\n')
print(Unb_mu_2, '\n')

mu_Alu = (inv(A_t*A)*A_t)*Alu_t
mu_Blei= (inv(A_t*A)*A_t)*Blei_t
mu_Unb = (inv(A_t*A)*A_t)*Unb_t

print(np.mean(mu_Alu), '\n')
print(np.mean(mu_Blei), '\n')
print(mu_Unb, '\n')

print([V_Al_mu[i,i] for i,n in enumerate(mu_Alu)])

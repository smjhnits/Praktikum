import numpy as np
from scipy.stats import sem
from uncertainties import ufloat
import uncertainties.unumpy as unp
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def Mean_Std(Werte):
    s = 1/np.sqrt(len(Werte))
    return ufloat(np.mean(Werte), s * np.std(Werte, ddof = 1))

#Dunkelmessung

DM = np.array([218, 224])
DM_W = Mean_Std(DM)

#Indium

dt_indium = 240
tge_indium = 3600

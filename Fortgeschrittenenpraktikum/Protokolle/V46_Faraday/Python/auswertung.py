import numpy as np
import matplotlib.pyplot as plt
import scipy.constants as const
from pint import UnitRegistry
from scipy.optimize import curve_fit
from uncertainties import ufloat
import uncertainties.unumpy as unp
from uncertainties.unumpy import (nominal_values as noms, std_devs as stds)
import data
u = UnitRegistry()
Q_ = u.Quantity

def fit_fkt(x, a):
    return a * x

def winkel(a):
    return a * np.pi / 180

def eff_masse(wellenlänge, N, d, theta):
    return np.sqrt(e_0**3 / (8 * np.pi**2 * epsilon_0 * c**3 * n) * d * B_max * N * wellenlänge**2 / theta).to('kg')

e_0 = Q_(const.elementary_charge, 'C')
epsilon_0 = Q_(const.epsilon_0, 'A * s / (V * m)')
c = Q_(const.c, 'm / s')
n = 3.4 # siehe Protokoll S&S

_lambda = Q_(data._lambda, 'nm').to('micrometer'). magnitude
_lambda_einheit = Q_(data._lambda, 'nm').to('micrometer')

#  Daten der Probe

hr_d = Q_(data.hr_d, 'mm')
d_1 = Q_(data.d_1, 'mm')
d_2 = Q_(data.d_2, 'mm')

N_1 = Q_(data.N_1, '1 / cm**3')
N_2 = Q_(data.N_2, '1 / cm**3')

#  Daten der Winkel
hr_theta_1 = winkel(data.hr_theta_1_grad + data.hr_theta_1_min / 60)
hr_theta_2 = winkel(data.hr_theta_2_grad + data.hr_theta_2_min / 60)

hr_theta = np.abs(1 / 2 * (hr_theta_1 - hr_theta_2))
hr_theta_norm = hr_theta / hr_d

theta_1_1 = winkel(data.theta_1_grad_1 + data.theta_1_min_1 / 60)
theta_2_1 = winkel(data.theta_2_grad_1 + data.theta_1_min_1 / 60)

theta_1 = np.abs(1 / 2 * (theta_1_1 - theta_2_1))
theta_1_norm = theta_1 / d_1

theta_1_2 = winkel(data.theta_1_grad_2 + data.theta_1_min_2 / 60)
theta_2_2 = winkel(data.theta_2_grad_2 + data.theta_1_min_2 / 60)

theta_2 = np.abs(1 / 2 * (theta_1_2 - theta_2_2))
theta_2_norm = theta_2 / d_2

probe_1_fit, covariance_1 = curve_fit(fit_fkt, _lambda**2, theta_1_norm)
probe_2_fit, covariance_2 = curve_fit(fit_fkt, _lambda**2, theta_2_norm)
#hr_probe_fit, hr_covariance_2 = curve_fit(fit_fkt, _lambda**2, hr_theta_norm)

probe_1_err = np.sqrt(np.diag(covariance_1))
probe_2_err = np.sqrt(np.diag(covariance_2))

x = np.linspace(0.8, 2.7)
plt.clf()
plt.plot(_lambda**2, theta_1_norm, '.', color='C0', label=r'Probe 1', ms=10)
plt.plot(_lambda**2, theta_2_norm, '.', color='C1', label=r'Probe 2', ms=10)
plt.plot(x, fit_fkt(x, *probe_1_fit), '-', color='C0', label=r'Fit Probe 1')
plt.plot(x, fit_fkt(x, *probe_2_fit), '-', color='C1', label=r'Fit Probe 2')
plt.xlabel(r'$\lambda^2 / \mu m^2$')
plt.ylabel(r'$\Delta \theta_{Norm} / rad/mm$')
plt.xlim(0.9, 2.7)
plt.legend()
plt.savefig('../Plots/dotiert_GaAs.pdf')

plt.clf()
plt.plot(_lambda**2, hr_theta_norm, '.', color='C0', label=r'reine Probe', ms=10)
#plt.plot(x, fit_fkt(x, *hr_probe_fit), '-', color='C0', label=r'Fit reine Probe')
plt.xlabel(r'$\lambda^2 / \mu m^2$')
plt.ylabel(r'$\Delta \theta_{Norm} / rad/mm$')
plt.xlim(0.9, 2.7)
plt.legend()
plt.savefig('../Plots/hr_GaAs.pdf')

#  B-Feld

B = Q_(data.B, 'mT')
s = Q_(data.s, 'mm')

plt.clf()
plt.plot(s.magnitude, B.magnitude, 'b.', label=r'$B(s)$', ms = 10)
plt.xlabel(r'Strecke $s /$mm')
plt.ylabel(r'$B$-Feld in mT')
plt.legend()
plt.savefig('../Plots/B.pdf')

B_max = max(B)

print(f'maximale Flussdichte: {B_max}')

#  Faraday-Rotationen

print('\n',"-" * 100, "\n\n Faraday-Rotationen\n")
print(f'Hochreines GaAs: {hr_theta}\n\n Probe 1: {theta_1_1} \n\n Probe 2: {theta_2}')

print('\n\n','-'*100, '\nFit Parameter\n', f'Probe 1: {probe_1_fit} + {probe_1_err} \n')
print(f'Probe 2: {probe_2_fit} + {probe_2_err} \n')

#  effektive Masse

m_eff_probe_1 = eff_masse(_lambda_einheit, N_1, d_1, np.abs(theta_1_norm - hr_theta_norm) * u('mm'))
m_eff_1 = ufloat(np.mean(m_eff_probe_1.magnitude), np.std(m_eff_probe_1.magnitude))
m_eff_probe_2 = eff_masse(_lambda_einheit, N_2, d_2, np.abs(theta_2_norm - hr_theta_norm) * u('mm'))
m_eff_2 = ufloat(np.mean(m_eff_probe_2.magnitude), np.std(m_eff_probe_2.magnitude))


print('\n',"-" * 100, '\n \n effektive Masse\n\n')
print(f'Messung mit Probe 1: m_eff = {m_eff_probe_1}\n')
print(f'Mittelwert m_eff_1 = {m_eff_1}\n\n')
print(f'Messung mit Probe 2: m_eff = {m_eff_probe_2}\n')
print(f'Mittelwert m_eff_2 = {m_eff_2}\n\n')
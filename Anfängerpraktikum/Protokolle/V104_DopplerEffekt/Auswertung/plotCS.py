import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

y = [5.8, 11.8, 17.8, 23.8, 24.6, 35.8]
x = [0.0507, 0.101, 0.152, 0.203, 0.253, 0.303]
plt.plot(x, y, 'k.')

def f(x, a, b):
    return a * x + b

params, covariance = curve_fit(f, x, y)

errors = np.sqrt(np.diag(covariance))

print('a=', params[0], '+/-', errors[0])
print('b=', params[1], '+/-', errors[1])

x_plot = np.linspace(0, 0.6)

plt.plot(x, y, 'rx', label="Differenzen")
plt.plot(x_plot, f(x_plot, *params), 'b-', label='linearer Fit', linewidth=1)
plt.legend(loc="best")

plt.show()
plt.savefig('plotCS.pdf')

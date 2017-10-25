import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

y = [-20, -19.8, -18.23, -15.2, -12, -9, -6.2, -2.8, 3,  6, 9, 12.2, 15, 18, 21.6, 24.4, 27.2, 30]
x = [-0.402, -0.354, -0.303, -0.253, -0.203, -0.152, -0.101, -0.0507, 0.0507, 0.101, 0.152, 0.203, 0.253, 0.303, 0.354, 0.402, 0.452, 0.502]
plt.plot(x, y, 'k.')

def f(x, a, b):
    return a * x + b

params, covariance = curve_fit(f, x, y)

errors = np.sqrt(np.diag(covariance))

print('a=', params[0], '+/-', errors[0])
print('b=', params[1], '+/-', errors[1])

x_plot = np.linspace(-0.5, 0.6)

plt.plot(x, y, 'rx', label="Differenzen")
plt.plot(x_plot, f(x_plot, *params), 'b-', label='linearer Fit', linewidth=1)
plt.legend(loc="best")

plt.show()
plt.savefig('plotC.pdf')

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

U = np.array([0.0, 3.88])
T = np.array([0.0, 100.0])


def f(x, A, B):
    return A * x + B

params, covariance = curve_fit(f, U, T)

x_plot = np.linspace(0, 4, 1000)

plt.plot(U, T, "rx", label="Spannungen")
plt.plot(x_plot, f(x_plot, *params), "b-")
# plt.show()

print(params[0], params[1])
print(params[0] * 0.82 + params[1])

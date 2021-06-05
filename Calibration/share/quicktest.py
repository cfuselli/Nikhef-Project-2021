import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

x = np.linspace(1,10,11)
y = np.array([1,1.3,1.5,1.6,1.8,1.9,2.1,2.1,2.2,2.3,2.3])


def fit_func(x, *coeffs):
    y = np.polyval(coeffs, x)
    return y

popt, pcov = curve_fit(fit_func, x, y, p0 = np.ones(11))
print(popt)
xplot = np.linspace(1,10,1000)

fig = plt.figure()
plt.scatter(x,y)
plt.plot(xplot , fit_func(xplot, *popt ))



# close the plot when pressing a key
plt.draw()
plt.pause(1)
input('press any key to close')
plt.close(fig)

#   plt.close('all')

print('goodbye')
import numpy as np
import matplotlib.pyplot as plt


def invTan(h):
    return np.arctan(10/h)

def events(h):
    it = invTan(h)
    return 0.5 * (it + np.sin(it) * np.cos(it) )

label = "events $\sim \chi + sin(\chi)\cdot cos(\chi)$\n with $\chi = tan^{-1}(\\frac{10cm}{h})$" 

h = np.linspace(5,150,145)
plt.plot(h, events(h),label=label)
plt.xlabel("distance between scintillator layers [cm]")
plt.ylabel("events [a.u.]")
plt.legend()

plt.draw()
plt.savefig("../data/events_vs_height.png")

plt.pause(1)
input('press any key to close')
plt.close('all')


print('goodbye')
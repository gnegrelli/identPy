import numpy as np
import matplotlib.pyplot as plt

R1 = .641
R2 = .332
X1 = 1.106
X2 = .464
Xm = 26.3

V = 127

s = np.linspace(1, -1, 1000)

w_s = 120*np.pi

w = (1 - s)*w_s

Vth = V*1j*Xm/(R1 + 1j*(Xm + X1))

Zth = 1j*Xm*(R1 + 1j*X1)/(R1 + 1j*(Xm + X1))

Rth = np.real(Zth)

Xth = np.imag(Zth)

leg = []
marker = ["-", "--", "-.", ":", ",", "."]
count = 0
for R2 in np.linspace(.1, 1.1, 5):
    T = 3*R2*abs(Vth)**2/(s*((Rth + R2/s)**2 + (X2 + Xth)**2)*w_s)

    plt.plot(w, T, marker[count])

    leg.append("$R_{r}$ = " + '{:.2f}'.format(R2) + " $\Omega$")
    count += 1

plt.legend(leg)
plt.xlabel("$\omega\ (rad/s)$")
plt.ylabel("$T\ (N\cdot m)$")
plt.title("Torque x speed curve")
plt.show()

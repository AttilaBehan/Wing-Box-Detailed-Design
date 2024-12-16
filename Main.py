import scipy as sp
from scipy.integrate import quad
import numpy as np
import math
import matplotlib.pyplot as plt

from geometry_42 import b
from geometry_42 import moi_distribution

# Constants

semispan = 21.84 / 2
n1 = 0
t1 = 5.3e-3
n2 = 26
t2 = 2.4e-3
n3 = 40
t3 = 1e-3

# Control points

y_points = np.linspace(0,semispan, 25)

def moment_distribution(y):
    return -10.0332*y**5 + 273.5632*y**4 - 2785.227*y**3 + 26071.1829*y**2 - 290785.6037*y**1 + 1361285.416

# Max tensile stress occurs at largest z coordinate of each section which is sparheight(b)/2 according to our coordinate system with tension in +z coordinate

def sigma_max(y, n, t):
    sigma_max = ( moment_distribution(y) * ( b(y) / 2 ) ) / moi_distribution(y, n, t)
    return sigma_max

# Calculate K and Y at all points

Y = 1
PI = 3.14
a1 = 1.65e-3 # ULTRASOUND
a2 = 1.63e-3 # ULTRASOUND
a3 = 0.7*t3 # ULTRASOUND
Kc = 25e6

def K(y, n, t, a):
    K = Y * sigma_max(y, n, t) * ( (PI * a ) ** 0.5 )
    return K

# Generate Points

sigmacontrolpoints1 = [sigma_max(y, n1, t1) for y in y_points]
sigmacontrolpoints2 = [sigma_max(y, n2, t2) for y in y_points]
sigmacontrolpoints3 = [sigma_max(y, n3, t3) for y in y_points]

Kcontrolpoints1 = [K(y, n1, t1, a1) for y in y_points]
Kcontrolpoints2 = [K(y, n2, t2, a2) for y in y_points]
Kcontrolpoints3 = [K(y, n3, t3, a3) for y in y_points]

# Convert to NumPy arrays

Kcontrolpoints1 = np.array(Kcontrolpoints1)
Kcontrolpoints2 = np.array(Kcontrolpoints2)
Kcontrolpoints3 = np.array(Kcontrolpoints3)

# Element-wise division by Kc

MOS1 = Kc / Kcontrolpoints1
MOS2 = Kc / Kcontrolpoints2
MOS3 = Kc / Kcontrolpoints3

print(min(MOS1), min(MOS2), min(MOS3))

#Safety Margin Tensional Strength

print(450e6/max(sigmacontrolpoints1), 450e6/max(sigmacontrolpoints2), 450e6/max(sigmacontrolpoints3))

# Plotting the max stress graph
plt.figure(figsize=(8, 6))

# Plot each set of control points
plt.plot(y_points, sigmacontrolpoints1, marker='o', linestyle='-', color='blue', label='Wing Box 1')
plt.plot(y_points, sigmacontrolpoints2, marker='s', linestyle='--', color='grey', label='Wing Box 2')
plt.plot(y_points, sigmacontrolpoints3, marker='^', linestyle='-.', color='black', label='Wing Box 3')

# Adding labels and title
plt.xlabel('Spanwise Position [m]', fontsize=12)
plt.ylabel('Max Stress [Pa]', fontsize=12)
plt.title('Max Stress vs Spanwise Position', fontsize=14)

# Adding legend
plt.legend(fontsize=10)

# Spanwise margin of safety plot

plt.figure(figsize=(10, 6))

# Plot result1
plt.subplot(3, 1, 1)  # 3 rows, 1 column, 1st subplot
plt.plot(y_points, MOS1, label='Wing Box 1', color='b')
plt.title('Wing Box 1')
plt.xlabel('Spanwise Position [m]')
plt.ylabel('Margin of Safety')
plt.grid(True)
plt.ylim(0,10)
plt.yticks(np.arange(1, 10, 2))

# Plot result2
plt.subplot(3, 1, 2)  # 3 rows, 1 column, 2nd subplot
plt.plot(y_points, MOS2, label='Wing Box 2', color='grey')
plt.title('Wing Box 2')
plt.xlabel('Spanwise Position [m]')
plt.ylabel('Margin of Safety')
plt.grid(True)
plt.ylim(0,10)
plt.yticks(np.arange(1, 10, 2))

# Plot result3
plt.subplot(3, 1, 3)  # 3 rows, 1 column, 3rd subplot
plt.plot(y_points, MOS3, label='Wing Box 3', color='black')
plt.title('Wing Box 3')
plt.xlabel('Spanwise Position [m]')
plt.ylabel('Margin of Safety')
plt.grid(True)
plt.ylim(0,10)
plt.yticks(np.arange(1, 10, 2))

# Display the plots
plt.grid(True)
plt.tight_layout()
plt.show()





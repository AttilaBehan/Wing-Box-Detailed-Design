import math

def critical_buckling_stress(E, nu, kc, t, b):
    sigma_cr = (math.pi*2 * kc * E) / (12 * (1 - nu)) * (t / b)*2
    return sigma_cr

def bending_stress(Mx, y, Ixx):
    sigma_bending = (Mx*y)/Ixx
    return sigma_bending

# Input values
E = 72.4e9  # Young's modulus for aluminum (Pa)
nu = 0.33  # Poisson's ratio
kc = 7.8  # Buckling coefficient for clamped
t = 0.001  # Thickness of the panel (m)
b = 2  # Width of the panel (m)
a = 4.03 # Height of the panel (m)
x = 3 # Maximum x location
y = 0.28 # Maximum y location
Ixx = (a * b**3) / 12  # Moment of inertia for a rectangular section
Mx = 1.35*10**6  # Maximum bending moment for each section (N*m)

# Calculations
sigma_cr = critical_buckling_stress(E, nu, kc, t, b)
sigma_bending = bending_stress(Mx, t, Ixx)

# Display results
print(f"Critical Buckling Stress (\u03C3_cr): {sigma_cr:.2f} Pa")

print(f"Bending Stress (\u03C3_bending): {sigma_bending:.2f} Pa")

# Comparing stresses
if sigma_bending < sigma_cr:
    print("The panel will not buckle.")
else:
    print("The panel may buckle under the applied stress.")
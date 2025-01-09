import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad
import math

# Constants
ks = 9.6  # Shear buckling coefficient
E = 28 * 10 ** 9  # Young's modulus in Pascals
v = 0.33  # Poisson's ratio
t = 0.001 # Thickness of the web in meters
Q_stringers = 40  # Number of stringers
f = 1.4
w_stringer = 0.00001

def u_2835(x):
    return 0 if x>=2.835 else 1
# Web buckling stress function
def web_buckling_stress():
    tau_lst = []
    y_values = np.linspace(0, 8, 100)

    for y in y_values:
        b = ((0.460 - 0.02867 * y)-w_stringer*Q_stringers) / (Q_stringers + 1)
        tau_cr = ((math.pi ** 2 * ks * E) / (12 * (1 - v ** 2))) * ((t / b) ** 2)
        tau_lst.append(tau_cr)

    # Polynomial fit for the data
    poly_web = np.polyfit(y_values, tau_lst, 4)
    poly_web_func = np.poly1d(poly_web)

    # Plot the graph
    plt.figure(figsize=(10, 6))
    plt.plot(y_values, tau_lst, label="Spanwise Failure Stress")
    plt.plot(y_values, poly_web_func(y_values), '--', label="Polynomial Fit")
    plt.title("Spanwise Failure Stress for Web Buckling")
    plt.xlabel("Spanwise Position (m)")
    plt.ylabel("Failure Stress (Pa)")
    plt.grid()
    plt.legend()
    plt.show()

    print("Web Buckling Stress Polynomial (4th degree):")
    print(poly_web_func)

    return poly_web_func, y_values


# Applied stress function for Spar 1 and Spar 2
def tau_appl():
    tau1_app_lst = []
    tau2_app_lst = []
    y_values = np.linspace(0, 8, 100)

    for y in y_values:
        b = 0.460 - 0.02867 * y
        w = 1.8045 - 0.1107 * y

        if b <= 0 or w <= 0:
            tau1_app_lst.append(0)
            tau2_app_lst.append(0)
            continue

        # Torque-induced shear stress
        torque_stress, _ = (quad(lambda x: q_torque(x), y, 10.98))/(b*t)

        # Lift-induced shear stress
        lift_stress, _ = quad(lambda x: -0.12*x**7+4.1617*x**6-57.363*x**5+399.4055*x**4-1470.8353*x**3+2536.1491*x**2-2163.9095*x+38619.7891, y, 10.98)
        shear_lift_1 = (lift_stress * (0.35 / 0.1)) / (t * b)
        shear_lift_2 = (lift_stress * (0.1 / 0.35)) / (t * b)

        # Engine weight shear stress
        weight_engine = 17254 * u_387(y)
        shear_weng_1 = weight_engine / (t * b)
        shear_weng_2 = 0

        #landing_gear_weight stress
        weight_landing_gear = 968.15*0.5*9.81*u_2835(y)
        shear_wlg_1 = (weight_landing_gear / (t * b))
        shear_wlg_2 = (weight_landing_gear / (t * b))

        # Distributed weight shear stress
        distributed_stress, _ = quad(lambda x: 4652.7156 - 289.69 * x, y, 10.98)
        shear_wdistr_1 = (distributed_stress * 0.5) / (t * b)
        shear_wdistr_2 = (distributed_stress * 0.5) / (t * b)

        # Total shear stress for spar 1 and spar 2
        shear_1 = (shear_lift_1 - shear_weng_1 - shear_wdistr_1 - torque_stress - shear_wlg_1)*f
        shear_2 = (shear_lift_2 - shear_weng_2 - shear_wdistr_2 + torque_stress - shear_wlg_2)*f
        tau1_app_lst.append(shear_1)
        tau2_app_lst.append(shear_2)

    # Polynomial fits
    poly_spar1 = np.polyfit(y_values, tau1_app_lst, 15)
    poly_spar2 = np.polyfit(y_values, tau2_app_lst, 15)
    poly_spar1_func = np.poly1d(poly_spar1)
    poly_spar2_func = np.poly1d(poly_spar2)

    # Plot applied stress for spar 1
    plt.figure(figsize=(10, 6))
    plt.plot(y_values, tau1_app_lst, label="Spanwise Applied Stress for Spar 1")
    plt.plot(y_values, poly_spar1_func(y_values), '--', label="Polynomial Fit")
    plt.title("Spanwise Applied Stress for Spar 1")
    plt.xlabel("Spanwise Position (m)")
    plt.ylabel("Applied Stress (Pa)")
    plt.grid()
    plt.legend()
    plt.show()

    # Plot applied stress for spar 2
    plt.figure(figsize=(10, 6))
    plt.plot(y_values, tau2_app_lst, label="Spanwise Applied Stress for Spar 2")
    plt.plot(y_values, poly_spar2_func(y_values), '--', label="Polynomial Fit")
    plt.title("Spanwise Applied Stress for Spar 2")
    plt.xlabel("Spanwise Position (m)")
    plt.ylabel("Applied Stress (Pa)")
    plt.grid()
    plt.legend()
    plt.show()

    print("Applied Stress for Spar 1 Polynomial (5th degree):")
    print(poly_spar1_func)
    print("Applied Stress for Spar 2 Polynomial (5th degree):")
    print(poly_spar2_func)

    return poly_spar1_func, poly_spar2_func, y_values


# Torque shear flow function
def q_torque(y):
    w = 1.8045 - 0.1107 * y
    b = 0.460 - 0.02867 * y
    Torque = (
            0.1609 * y ** 5 - 5.418 * y ** 4 + 64.46 * y ** 3 + 443.9 * y ** 2
            - 1.797 * 10 ** 4 * y + 1.114 * 10 ** 5
    )
    return Torque / (2 * w * b)


def u_387(x):
    return 0 if x >= 3.87 else 1


# Function to compute and plot the quotient for both spars
def plot_quotient_no_remainder(poly_web_func, poly_appl_func, y_values, spar_label):
    # Compute the quotient numerically
    quotient_values = poly_web_func(y_values) / poly_appl_func(y_values)

    # Polynomial fit for the quotient
    poly_quotient = np.polyfit(y_values, quotient_values, 12)
    poly_quotient_func = np.poly1d(poly_quotient)

    # Plot the quotient
    plt.figure(figsize=(10, 6))
    plt.plot(y_values, quotient_values, label=f"Numerical Quotient ({spar_label})")
    plt.plot(y_values, poly_quotient_func(y_values), '--', label=f"Polynomial Fit for Quotient ({spar_label})")
    plt.title(f"Quotient of Web Buckling Stress and Applied Stress for {spar_label}")
    plt.xlabel("Spanwise Position (m)")
    plt.ylabel("Quotient Value")
    plt.ylim(-50, 50)
    plt.grid()
    plt.legend()
    plt.show()

    print(f"Quotient Polynomial for {spar_label} (4th degree):")
    print(poly_quotient_func,quotient_values)


# Main block
if __name__ == "__main__":
    print("Calculating web buckling stress...")
    web_buckling_poly, y_values = web_buckling_stress()

    print("Calculating applied stress...")
    applied_stress_spar1_poly, applied_stress_spar2_poly, _ = tau_appl()

    print("Computing and plotting the quotient for Spar 1...")
    plot_quotient_no_remainder(web_buckling_poly, applied_stress_spar1_poly, y_values, "Spar 1")

    print("Computing and plotting the quotient for Spar 2...")
    plot_quotient_no_remainder(web_buckling_poly, applied_stress_spar2_poly, y_values, "Spar 2")

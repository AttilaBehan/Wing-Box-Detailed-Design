import math 
import numpy as np
import scipy as sp
import ast

def critical_buckling_stress(E, nu, kc, t, b):
    sigma_cr = (math.pi**2 * kc * E) / (12 * (1 - nu**2)) * (t / b)**2
    return sigma_cr

def bending_stress(Mx, y, Ixx):
    sigma_bending = (Mx*y)/Ixx
    return sigma_bending

def f(x):
    #Mx
    return -10.0332*x**5+273.5632*x**4-2785.2272*x**3+26071.1829*x**2-290785.6037*x**1+1356183.4157

def getMoment(integrand, start, end):
    return sp.integrate.quad(integrand, start, end)[0]

# Input values
E = 72.4e9  # Young's modulus for aluminum (Pa)
nu = 0.33  # Poisson's ratio
kc = 1.21  # Buckling coefficient for clamped
t = 0.001  # Thickness of the panel (m)
i=1        #index that parses through the initial rib list each time as kc has to be manually found from a graph            
initriblist=[0, 0.65, 1.35, 2.11, 2.84, 3.77, 3.8, 4.9, 6.29, 8.51, 10.91]    #initial rib list which has to be checked against wing skin buckling
b = initriblist[i]-initriblist[i-1]# Width of the panel (m)

#calculation of average chord length of the selected wing box bay
cr=4.03
ct=1.29
span=21.82
a=((cr-((cr-ct)*2/span)*float(initriblist[i]))+(cr-((cr-ct)*2/span)*float(initriblist[i-1])))/2

#always prints a/b or b/a such that it is larger than one in order to find kc from the graph 
if a/b>1:
    print("a/b =",a/b)
else:
    print("b/a =",b/a)
x = 3 # Maximum x location
y = 0.23 # Maximum y location
Ixx = (b * a**3) / 12  # Moment of inertia for a rectangular section
moments=[]
for j in np.arange(initriblist[i-1],initriblist[i]+0.01,0.01):          
    moments.append(float(f(j)))    
Mx = (max(moments))  # Maximum bending moment for each section (N*m)    

# Calculations
sigma_cr = critical_buckling_stress(E, nu, kc, t, b)
sigma_bending = bending_stress(Mx, y, Ixx)

#once kc has been selected data is stored in lists in an external file which will then be imported into overleaf as the final values
got_a_over_b=False 
if got_a_over_b==True:
    with open(r"lists.txt","r+") as file:
        kc_List=ast.literal_eval(file.readline().strip("\n"))
        riblist=ast.literal_eval(file.readline().strip("\n"))
        Ixx_List=ast.literal_eval(file.readline().strip("\n"))
        Mx_List=ast.literal_eval(file.readline().strip("\n"))
        scr_List=ast.literal_eval(file.readline().strip("\n"))
        sbnd_List=ast.literal_eval(file.readline().strip("\n"))
        MOS_List=ast.literal_eval(file.readline().strip("\n"))
        file.seek(0) 
        file.truncate(0)
        kc_List.append(kc)
        riblist.append(initriblist[i])
        Ixx_List.append(Ixx)
        Mx_List.append(Mx)
        scr_List.append(sigma_cr)
        sbnd_List.append(sigma_bending)
        MOS_List.append(sigma_cr/sigma_bending)
        file.write(str(kc_List)+"\n"+str(riblist)+"\n"+str(Ixx_List)+"\n"+str(Mx_List)+"\n"+str(scr_List)+"\n"+str(sbnd_List)+"\n"+str(MOS_List))

# Display results
print(f"Critical Buckling Stress (\u03C3_cr): {sigma_cr:.2f} Pa")

print(f"Bending Stress (\u03C3_bending): {sigma_bending:.2f} Pa")

print("MOS =", sigma_cr/sigma_bending)
# Comparing stresses
if sigma_bending < sigma_cr:
    print("The panel will not buckle.")
else:
    print("The panel may buckle under the applied stress.")

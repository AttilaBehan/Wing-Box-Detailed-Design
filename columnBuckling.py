import numpy as np
import scipy as sp

E = 72.4*10**9 #material property to change to correct one

def g(x):
    #My
    return 0.1609*x - 5.418*x + 64.46* x + 443.9 *x - 1.797e+04* x + 1.114e+05 if x < 3.87 else 0.1609*x - 5.418*x + 64.46* x + 443.9 *x - 1.797e+04* x + 1.114e+05+25971.03-7211.58


def f(x):
    #Mx
    return -10.0332*x**5+273.5632*x**4-2785.2272*x**3+26071.1829*x**2-290785.6037*x**1+1356183.4157*x


Ixx = 69781.901*(10**(-12))
Iyy = 69781.901*(10**(-12))
Ixy = 37353.516*(10**(-12)) 
A = 400*10**(-6) 

# the three points where stress could be maximum
points = [(1, 1), (1,1), (1,1)]
p2 = (1,1)
p3 = (1,1)

def getMoment(integrand, start, end):
    return sp.integrate.quad(integrand, start, end)[0]

#Equation given in Appendix
def criticalColBuckling(start, end, clamped=True):
    #Kpi^2EI/(LA^2)
    L = end - start
    k = 1
    #around x:
    stressX = (k*np.pi**2 * E * Ixx)/(L*A**2)
    stressY = (k*np.pi**2 * E * Iyy)/(L*A**2)
    return min(stressX, stressY)


#Calculate the actual stress
def stringerStress(start, end):
    stresses = []
    Mx = getMoment(f, start, end)
    My = getMoment(f, start, end)
    a = (Mx*Iyy-My*Ixy)
    b = (My*Ixx-Mx*Ixy)
    c = Ixx*Iyy-Ixy**2

    #the three points will always have the critical one
    for point in points:
        stresses.append((a*point[1]+ b*point[0])/c)
    
    #return the largest of the stresses as that will be most critical for margin of safety
    #the *1.5 is the safety factor
    return max(stresses)*1.5

def colSafetyMargin(start, end, clamped = True):
    return (criticalColBuckling(start, end, clamped = clamped)/stringerStress(start, end) )

# criticalColBuckling(Ixx, Iyy, 1, 1)
# stringerStress(Ixx, Iyy, Ixy, My, Mx)


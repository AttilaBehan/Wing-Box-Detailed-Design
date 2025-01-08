import numpy as np
import scipy as sp

E = 72.4*10**9 #material property to change to correct one

def g(x):
    #My
    return 0.1609*x**5 - 5.418*x**4 + 64.46* x**3 + 443.9 *x**2 - 1.797*(10**4)*x + 1.114*(10**5) if x < 3.87 else 0.1609*x**5 - 5.418*x**4 + 64.46*x**3 + 443.9*x**2 - 1.797*(10**4)*x + 1.114*(10**5)+25971.03-7211.58

def f(x):
    #Mx
    return -10.0332*x**5+273.5632*x**4-2785.2272*x**3+26071.1829*x**2-290785.6037*x**1+1356183.4157

Ixx = 138824.640*(10**(-12))
Iyy = 138824.640*(10**(-12))
Ixy = 79046.445*(10**(-12)) 
A = 400*10**(-6) 

# the three points where stress could be maximum
mm = 10**(-3)
points = [(-14.6475*mm,-14.6475*mm), (-14.6475*mm,44.2425*mm), (44.2425*mm,-14.6475*mm)]

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
    My = getMoment(g, start, end)
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
    #print(criticalColBuckling(start, end, clamped = clamped))
    #print(stringerStress(start, end))
    return (criticalColBuckling(start, end, clamped = clamped)/stringerStress(start, end))

# criticalColBuckling(Ixx, Iyy, 1, 1)
# stringerStress(Ixx, Iyy, Ixy, My, Mx)

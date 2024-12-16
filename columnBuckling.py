import numpy as np

E = 1 #material property to change to correct one

#These just for testing
# My = 1
# Mx = 1
# Ixx = 2
# Iyy = 1
# Ixy = 1

# the three points where stress could be maximum
points = [(1, 1), (1,1), (1,1)]
p2 = (1,1)
p3 = (1,1)

#Equation given in Appendix
def criticalColBuckling(Ixx, Iyy, A, L, clamped=True):
    #Kpi^2EI/(LA^2)
    k = 4 if clamped else 1/4
    #around x:
    stressX = (k*np.pi**2 * E * Ixx)/(L*A**2)
    stressY = (k*np.pi**2 * E * Iyy)/(L*A**2)
    return (stressX, stressY)


#Calculate the actual stress
def stringerStress(Ixx, Iyy, Ixy, My, Mx):
    stresses = []
    a = (Mx*Iyy-My*Ixy)
    b = (My*Ixx-Mx*Ixy)
    c = Ixx*Iyy-Ixy**2

    #the three points will always have the critical one
    for point in points:
        stresses.append((a*point[1]+ b*point[0])/c)
    
    #return the largest of the stresses as that will be most critical for margin of safety
    return max(stresses)

# criticalColBuckling(Ixx, Iyy, 1, 1)
# stringerStress(Ixx, Iyy, Ixy, My, Mx)


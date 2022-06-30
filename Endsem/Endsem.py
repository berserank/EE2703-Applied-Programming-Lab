

#         EE2703 Applied Programming Lab Endsem
#         Endsem
#         Aditya Nanda Kishore
#         EE20B062  
#         Currents along Half Wave Dipole Antenna 

import numpy as np
import matplotlib.pyplot as plt 

#Question 1

"""
We are given a dipole antenna and it's basic parameters and we are asked to find currents along the antenna.
They are listed down below. we calculate dz as half length/N. and we can calculate k as pi.
"""
half_length = 0.5
N = 1000
dz = half_length/N
l = 0.5
Im = 1
a = 0.01
k = np.pi

"""

I defined a linspace array "points" that goes from -0.5 to 0.5 and has 2*N divisions. With the help of this I defined array 'z'
that has the z co-ordinates of the sampled points.I also defined the current array with current at every point and also unknows. 
They are I and J respectively. u is an another array that has the list of z co-ordinates where I is unknown.

"""
points = np.linspace(-half_length,half_length,2*N+1)
z = np.zeros(2*N+1)
for i in range(len(points)):
    z[i] = (i-N)*dz

I = np.zeros(len(z))
I[N] = Im
I[0] = 1
I[2*N] = 1
u = []
for i in range(len(I)):
    if I[i] == 0:
        u.append(z[i])
I[0] = 0
I[2*N] = 0
# print(I)
# print(u)
J = np.zeros(2*N-2)


"""
I defined a function that generates the diagonal matrix M as required in the question.
"""

#Question 2
def M_generator(N,a):
    M = np.identity(2*N-2)
    M = M/(2*np.pi*a)
    return M 

M = M_generator(N,a)



"""
Here, I have started building everything from genrtating Rz, Ru first. For generating Rz, 
I need array of z co-ordinates and an array with all a-s. I made a meshgrid with z,z and subtracted teh output and then 
multiplied both of them with j so that I can take absoulte values for distance there. I added the matrix with all a's and 
took the magnitude and returned the matrix later.
"""
#Question 3
def R_generator(r,z):
    z1, z2 = np.meshgrid(z,z)
    z = 1j*(z1-z2)
    distance_matrix =  r+z
    distance_matrix = np.abs(distance_matrix)
    return distance_matrix

rz = np.meshgrid(a*np.ones(2*N+1), a*np.ones(2*N+1))[0]
ru = np.meshgrid(a*np.ones(2*N-2), a*np.ones(2*N-2))[0]
Rz = R_generator(rz,z)
Ru = R_generator(ru,u)
Rn = []

"""
For Pb, I need Rz[N] without the Rz[0,N], Rz[N,N],Rz[2*N,N]. So I took them away and formed an Rn array.
"""
for i in range (2*N+1):
    if ((i>0 and i<N) or (i>N and i<2*N)):
        Rn.append(Rz[i,N])
Rn = np.array(Rn)
# print(Rz)
# print(Ru)
# print(Rn, np.size(Rn))
"""
Formed P, Pb as required in the question using Ru, Rn
"""
P = ((10**-7)* np.exp(-1j*k*Ru)/(Ru))*dz
Pb = ((10**-7)* np.exp(-1j*k*Rn)/Rn)*dz
# print(np.size(Rn))
# print(np.size(Pb))
"""
Formed Q, Qb as required in the question using Ru, Rn, P, Pb
"""
Q = P*a/(4*np.pi*(10**-7))*((1/(Ru**2)+ (k/Ru)*1j))
Qb = Pb*a/(4*np.pi*(10**-7))*((1/(Rn**2)+ (k/Rn)*1j))

# print(np.shape(M-Q))
# print(np.shape(Qb))

#Question 5
"""
I then implemented the formula given for J in the question and then made it a list and inserted the 3 known currents and 
completed the list and plotted it for N = 4 and N = 100.
"""
J = Im * np.matmul(np.linalg.inv(M-Q),Qb)
J_list = list(J)
J_list.insert(N-1,Im)
J_list.insert(0,0)
J_list.insert(2*N,0)
# print(np.abs(J))
plt.figure(0)
plt.plot(z,J_list)
plt.plot(z,Im*np.sin(k*(l+ np.abs(z))))
plt.legend(["Calculated J", "Sine Wave"])
plt.title("Half wave dipole antenna current")
plt.grid(True)
plt.savefig("Q5.png")
plt.show()


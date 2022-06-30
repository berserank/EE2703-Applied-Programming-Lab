
from pylab import *
# script to generate data files for the least squares assignment from pylab import *
import scipy.special as sp
import numpy as np
import matplotlib.pyplot as ax
N=101 # no of data points
k=9 # no of sets of data with varying noise
# generate the data points and add noise

t=linspace(0,10,N)     

def g(t,A,B):
    true_val =A*sp.jn(2,t)+B*t 
    return true_val
A0 = 1.05
B0 = -0.105


y = g(t, A0, B0)


# t vector

Y=meshgrid( y, ones(k),indexing = 'ij')[0] # make k copies
#print(Y)
scl=logspace(-1,-3,k)  # noise stdev
n=dot(randn(N,k),diag(scl)) # generate k vectors
yy=Y+n    # add noise to signal
# shadow plot
plot(t,yy)

xlabel( r'$t$' , size=20 )
ylabel(r'$f(t)+n$',size=20)
title(r'Q1,Q3 Plot')
grid(True)

#Q3 : Plottting Noise labels

ax.legend(scl)
ax.show() 
savetxt("fitting.dat",c_[t,yy]) # write out matrix to file
show()

#Q2 : Loading Data from the Text file

f = np.loadtxt("fitting.dat", dtype = float)
time, data = f[:,0], f[:, 1:] #data_arr has just the data with time extracted


#Q4

yy = np.hstack((yy, np.atleast_2d(y).T))
plot(t, yy)
xlabel( r'$t$' , size=20 )
title(r'Q4 Plot')
ax.legend(list(scl) + ["True Value"])
ax.show() 

#Q5

stdev = scl[0]
errorbar(t[::5],(data.T[0])[::5],stdev,fmt='ro')
plot(t, data.T[0])
xlabel( r'$t$' , size=20 )
title(r'Q5 Plot')
ax.legend(['data.T[0]', 'Error Bar'])
show()

#Q6

M_1 = t
M_0 = sp.jn(2,t)
M = np.c_[M_0, M_1]
A = np.array([A0,B0])
B = np.dot(M, A.T)
B = np.c_[B.T-y, y] #checking if they are same or not
plot(t, B)
title(r'Q6- Plot to check whether they are same plots')
ax.legend(['g(t,A,B)-g(t,A0,B0)', 'g(t,A0,B0)'])
show()

#Q7
f = data.T[0]
A = linspace(0,2,21)
B = linspace(-0.2,0,21)
def eij_form(A,B,f):
    E = np.zeros((21,21))
    for i in range(0,21):
        for j in range(0,21):
            sum = 0
            gij = g(t,A[i],B[j])
            sum = np.dot((f - gij), (f-gij).T)
            E[i][j] = float(sum)/101
    return E

#Q8
ax.contour(A, B, eij_form(A,B,f))
ax.contourf(A, B, eij_form(A,B,f))
xlabel( r'$A$' , size=20 )
ylabel(r'$B$',size=20)
title(r'Q8 Contour Plot')
ax.show()

#Q9

final_sol, lmse, *c = np.linalg.lstsq(M, y.T, rcond=None)


#Q10
error = np.zeros((k,2))
lmse = np.zeros((k,))
for i in range(0,k):
    f = data.T[i]
    E = eij_form(A,B,f)
    sol, lmse[i], *c = np.linalg.lstsq(M, f.T, rcond = None)
    error[i] = [abs(sol[0] - A0), abs(sol[1]-B0)]

plot(scl, ((error.T)[0]).T,'ro')
plot(scl, ((error.T)[1]).T,'bo')
plot(scl, lmse)
xlabel( r'$Noise$' , size=20 )
title(r'Q10 Plot')
ax.legend(['Error in A', 'Error in B', 'lmse'])
ax.show()

#Q11
loglog(scl, ((error.T)[0]).T,'ro')
loglog(scl, ((error.T)[1]).T,'bo')
loglog(scl, lmse)
xlabel( r'$log(Noise)$' , size=20 )
title(r'Q11  Plot')
ax.legend(['Error in A', 'Error in B', 'lmse'])
ax.show()
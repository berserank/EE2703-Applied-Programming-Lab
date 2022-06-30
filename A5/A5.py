from pylab import *
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.pyplot as plt
Nx=25; # size along x
Ny=25; # size along y
radius=8;# radius of central lead
Niter=1500; # number of iterations to perform

phi = zeros((Ny,Nx))


y = linspace(-0.5, 0.5, num=Ny, dtype = float) 
x = linspace(-0.5, 0.5, num=Nx, dtype = float) 
Y,X= np.meshgrid(y,x)
ii = np.where(X*X + Y*Y <= (0.35)**2 )
phi[ii] = 1

plt.figure(0)
plt.scatter(x[ii[0]],y[ii[1]], c = 'red', label ="V = 1V")
plt.axis(xmin=-0.5, xmax=0.5, ymin=-0.5, ymax=0.5)
plt.title("Initial Potential Graph")
plt.legend(["V = 1V"])
plt.grid(True)
plt.show()

plt.contourf(x,y,phi)
plt.axis(xmin=-0.5, xmax=0.5, ymin=-0.5, ymax=0.5)
plt.title("Initial Potential Contour Plot")
plt.grid(True)
plt.show()


errors= []
n = np.arange(0, Niter)
def iterate(oldphi):
    phi = np.zeros(shape(oldphi))
    phi[1:-1,1:-1]=0.25*(oldphi[1:-1,0:-2] + oldphi[1:-1,2:] + oldphi[2:, 1:-1] + oldphi[0:-2, 1:-1])
    return phi

def set_boundaries(phi):
    phi[1:-1,0]=phi[1:-1,1]
    phi[1:-1,-1]=phi[1:-1,-2]
    phi[0, 0:] = phi[1, 0:]
    return phi

for i in range(Niter):
    oldphi=phi.copy()
    phi = iterate(oldphi)
    phi = set_boundaries(phi)
    phi[ii]=1.0
    errors.append((abs(phi-oldphi)).max())

errors = np.array(errors)
plt.semilogy(n, errors)
plt.title("Error vs Iterations Semi-log Plot ")
plt.show()

plt.loglog(n, errors)
plt.title("Error vs Iterations log-log Plot ")
plt.show()

plt.plot(n[::50] ,errors[::50])
plt.title("Every 50th Error-Individual Values")
plt.show()

# Plotting of the actual and expected error in semilog, for  all values
M_0 = c_[np.ones(Niter), np.arange(Niter)]
c_all = np.linalg.lstsq(M_0,  np.log(errors), rcond=None)
a0, b0 = np.exp(c_all[0][0]), c_all[0][1]

M_1 = c_[np.ones(Niter-500), np.arange(500, Niter) ]
c_500 = np.linalg.lstsq(M_1, np.log(errors[500:]),rcond = None)
a1, b1 = np.exp(c_500[0][0]), c_500[0][1]
print(a0,b0)
print(a1,b1)
plt.semilogy(n, errors)
plt.semilogy(n, a0* np.exp(b0*n))
plt.legend(['Errors', 'Fit for all errors'])
plt.show()

# Plotting of the actual and expected error in semilog, for all values above n = 500
plt.semilogy(n[500:], errors[500:],  linewidth = 3)
plt.semilogy(n[500:], a1* np.exp(b1*n[500:]))
plt.legend(['Errors','Fit for values after 500'])
plt.show()

# Plotting the surface plots of phi (potential).
fig1=plt.figure(4)     # open a new figure
ax=p3.Axes3D(fig1) # Axes3D is the means to do a surface plot
surf = ax.plot_surface(Y, X, phi.T, rstride=1, cstride=1, cmap=cm.jet)
plt.title('The 3-D surface plot of the potential')
plt.show()

# Plotting of the contour of phi (potential).
plt.contourf(-X, -Y, phi.T)
plt.scatter(x[ii[0]],y[ii[1]], c = 'red', label ="V = 1V")
plt.title("Contour plot of potential")
plt.colorbar()
plt.grid(True)
plt.show()

#Current
J_x = np.zeros((Ny, Nx))
J_y = np.zeros((Ny, Nx))
J_x[1:-1,1:-1] = 0.5*(-phi.T[1:-1,0:-2]+phi.T[1:-1,2:])
J_y[1:-1,1:-1] = 0.5*(phi.T[0:-2, 1:-1]-phi.T[2:, 1:-1])
plt.quiver(X,-Y,J_y,J_x, color='blue', scale = 5)
plt.scatter(x[ii[0]],y[ii[1]], c = 'red', linewidths = 0.5, label ="V = 1V")
plt.title("The vector plot of the current flow")
plt.show()






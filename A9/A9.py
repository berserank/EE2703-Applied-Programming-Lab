import numpy as np
import matplotlib.pyplot as plt 

#I am using a similar spectrum function as that of the previous assignment to make the code compact

def spectrum(func,T,t_0,time_check, N, windowing, xlim,plot, plot_name, fig_name):
    if (time_check):
        t = np.linspace(-T,T, N+1)[:-1]
    elif (time_check == False):
        t = t_0
    dt=t[1]-t[0];fmax=1/dt
    y= func(t)
    y[0]=0
    if (windowing) :
        n=np.arange(N)
        wnd=np.fft.fftshift(0.54+0.46*np.cos(2*np.pi*n/(N-1)))
        y = y*wnd

    y=np.fft.fftshift(y) # make y start with y(t=0)
    Y=np.fft.fftshift(np.fft.fft(y))/N
    w=np.linspace(-np.pi*fmax,np.pi*fmax,N+1);w=w[:-1]
    if (plot):
        plt.figure()
        plt.subplot(2,1,1)
        plt.plot(w,abs(Y), lw = 2)
        plt.xlim([-xlim, xlim])
        plt.ylabel(r"$|Y|$",size=16)
        plt.title(plot_name)
        plt.grid(True)
        plt.subplot(2,1,2)
        np.angle(Y)[np.where(np.abs(Y)<3e-3)] = 0
        plt.plot(w,np.angle(Y),'ro',lw=2)
        plt.xlim([-xlim, xlim])
        plt.ylabel(r"Phase of $Y$",size=16)
        plt.xlabel(r"$k$",size=16)
        plt.grid(True)
        plt.savefig(fig_name)
        plt.show()
    return Y,w
#Examples
t_0 = np.zeros(64)

def sinsqrt(t, w0 = np.sqrt(2)):
    return(np.sin(t*w0))
#Without Hamming

spectrum(sinsqrt,np.pi, t_0,True, 64, False, 10, True,"Spectrum of $sin(\sqrt{2}t)$", "Q1a.png")

#With Hamming
spectrum(sinsqrt,np.pi,t_0,True, 64, True, 10, True, "Spectrum of $sin(\sqrt{2}t)$, with Windowing", "Q1b.png")

spectrum(sinsqrt,4*np.pi,t_0,True, 128, True, 10, True, "Improved Spectrum of $sin(\sqrt{2}t)$, with Windowing", "Q1c.png")


#Question 2
def cos3(t,w0=0.86):
    return (np.cos(w0*t))**3


#Without Hamming

spectrum(cos3,4*np.pi,t_0,True, 64, False, 5, True,"Spectrum of $cos^3(0.86t)$", "Q2a.png")

#With Hamming
spectrum(cos3,4*np.pi,t_0,True, 64, True, 5, True, "Spectrum of $cos^3(0.86t)$, with windowing ", "Q2b.png")

#Question 3
def cos(t,w0 = 1.5, delta = 0.5):
    return(np.cos(w0*t+delta))

Y,w=spectrum(cos,np.pi, t_0,True,128, True, 5, True,"Spectrum of $cos(1t+0.8)$", "Q3.png")

ii = np.where(w>0)
omega = (sum(abs(Y[ii])**2*w[ii])/sum(abs(Y[ii])**2))
print ("omega_0 = ", omega)


i = abs(w-omega).argmin()
delta = np.angle(Y[i])
print ("delta = ", delta)

#Question 4
def noisycos(t,w0 = 1.5, delta = 0.5):
    return(np.cos(w0*t+delta)+0.1*np.random.randn(128))

Y,w=spectrum(noisycos,np.pi,t_0,True, 128, True, 5, True, "Spectrum of Noisy $cos(1t+0.8)$", "Q4.png")

ii = np.where(w > 0)
omega = (sum(abs(Y[ii])**2*w[ii])/sum(abs(Y[ii])**2))
print ("noisy signal's omega_0 = ", omega)



i = abs(w-omega).argmin()
delta = np.angle(Y[i])
print ("noisy signal's delta = ", delta)

#Question 5
def chirp(t):
    return (np.cos(24*t+ 16*(t**2)/(2*np.pi)))

spectrum(chirp,np.pi, t_0, True,1024, True, 100, True,"Spectrum of Chirped Signal", "Q5.png")

#Question 6
t=np.linspace(-np.pi,np.pi,1025);t=t[:-1]
t_arrays=np.split(t,16)

Y_mag=np.zeros((16,64))
Y_phase=np.zeros((16,64))

Y_mag1=np.zeros((16,64))
Y_phase1=np.zeros((16,64))

for i in range(len(t_arrays)):
    Y,w = spectrum(chirp, np.pi, t_arrays[i], False, 64,False, 60, False,"Spectrum of Chirp Function", "Q5.png")
    Y_mag[i] = np.abs(Y)
    Y_phase[i] = np.angle(Y)

for i in range(len(t_arrays)):
    Y1,w1 = spectrum(chirp, np.pi, t_arrays[i], False, 64,True, 60, False,"Spectrum of Chirp Function", "Q5.png")
    Y_mag1[i] = np.abs(Y1)
    Y_phase1[i] = np.angle(w1)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

t=np.linspace(-np.pi,np.pi,1025);t=t[:-1]
fmax = 1/(t[1]-t[0])
t=t[::64]
w=np.linspace(-fmax*np.pi,fmax*np.pi,64+1);w=w[:-1]
t,w=np.meshgrid(t,w)

surf=ax.plot_surface(w,t,Y_mag1.T,cmap=plt.cm.coolwarm,linewidth=0, antialiased=False)
fig.colorbar(surf, shrink=0.5, aspect=5)
plt.ylabel("Frequency")
plt.xlabel("Time")
plt.title("Surface Plot- Magnitude")
plt.savefig("Q6c.png")
plt.show()


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

t=np.linspace(-np.pi,np.pi,1025);t=t[:-1]
fmax = 1/(t[1]-t[0])
t=t[::64]
w=np.linspace(-fmax*np.pi,fmax*np.pi,64+1);w=w[:-1]
t,w=np.meshgrid(t,w)

surf=ax.plot_surface(w,t,Y_mag.T,cmap=plt.cm.coolwarm,linewidth=0, antialiased=False)
fig.colorbar(surf, shrink=0.5, aspect=5)
plt.ylabel("Frequency")
plt.xlabel("Time")
plt.title("Surface Plot- Magnitude")
plt.savefig("Q6a.png")
plt.show()

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
surf=ax.plot_surface(w,t,Y_phase.T,cmap=plt.cm.coolwarm,linewidth=0, antialiased=False)
fig.colorbar(surf, shrink=0.5, aspect=5)
plt.ylabel("Frequency")
plt.xlabel("Time")
plt.title("Surface Plot-Phase")
plt.savefig("Q6b.png")
plt.show()


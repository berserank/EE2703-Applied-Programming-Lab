import numpy as np
import matplotlib.pyplot as plt 


func_list = {'sin(5x)': lambda x : np.sin(5*x),'(1+0.1cost)*cos(10t)': lambda x : (1+0.1*np.cos(x))*np.cos(10*x), 'cos^3' : lambda x : np.cos(x)**3,'sin^3' : lambda x : np.sin(x)**3,'fm' : lambda x : np.cos(20*x+5*np.cos(x)),
               'gauss' : lambda x : np.exp(-x**2/2) }

def spectrum(func,start, end, N, w, magnitude_split_plot, phase_split_plot, mag_min, xlim, plot_name, fig_name):
    t= np.linspace(start,end, N+1)[:-1]
    w= np.linspace(-w,w,N+1)[:-1]
    y= func_list[func](t)
    if func == 'gauss' :
        Y = np.fft.fftshift(np.fft.fft(y))/N
        Y = Y/max(Y) 
    else:
        Y= np.fft.fftshift(np.fft.fft(y))/N
    plt.figure()
    plt.subplot(2,1,1)
    plt.plot(w,abs(Y), lw = 2)
    plt.xlim([-xlim, xlim])
    plt.ylabel(r"$|Y|$",size=16)
    plt.title(plot_name)
    plt.grid(True)
    plt.subplot(2,1,2)
    if phase_split_plot == False:
        plt.plot(w,np.angle(Y),'ro',lw=2)
    if (magnitude_split_plot == True):
        ii= np.where(abs(Y)>mag_min)
        plt.plot(w[ii],np.angle(Y[ii]),'go',lw=2)
    plt.xlim([-xlim, xlim])
    plt.ylim([-2, 2])
    plt.ylabel(r"Phase of $Y$",size=16)
    plt.xlabel(r"$k$",size=16)
    plt.grid(True)
    plt.savefig(fig_name)
    plt.show()
    return Y,w

#Question 1
Y,w = spectrum('sin(5x)', 0, 2*np.pi, 128 , 64 ,True,False, 1e-3, 10, 'Spectrum of sin(5t)','Q1a.png')
Y,w = spectrum('(1+0.1cost)*cos(10t)', -4*np.pi, 4*np.pi, 512 , 64, False,False, 1e-3, 15, 'Spectrum of $(1+0.1cost)cos(10t)$ ', "Q1b.png")

#Question 2
Y,w = spectrum('sin^3', -4*np.pi, 4*np.pi, 512 , 64 , False,False, 1e-3, 5, 'Spectrum of $sin^3(t)$', "Q2a.png")
Y,w = spectrum('cos^3', -4*np.pi, 4*np.pi, 512 , 64 ,  False,False, 1e-3, 5, 'Spectrum of $cos^3(t)$', "Q2b.png")

#Question 3
Y,w = spectrum('fm', -32*np.pi, 32*np.pi, 16384 , 256 , True,True, 1e-3, 30, 'Spectrum of $cos(20t+5cos(t))$', "Q3.png")

#Question 4

T = 4*np.pi
N = 256
w = 64
Y,w = spectrum('gauss', -T/2, T/2, N, w, True, False, 1e-3, 10, 'Normalised Spectrum of $e^{-t^2/2}$', 'Q4.png')
Y_acc = np.exp(-0.5*(w**2))
error = max(abs(abs(Y)- Y_acc))
print(error)




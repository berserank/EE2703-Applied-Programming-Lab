from pylab import *
import numpy as np
import scipy.signal as sp

w = 1.5
d = 0.5

#Question 1
H = sp.lti([1,d], polymul([1,0,2.25],[1,2*w,w**2 + d**2]))
t,x=sp.impulse(H,None, linspace(0,50,501))
plot(t,x)
title('x(t) with decay 0.5')
xlabel('time')
ylabel('x(t)')
show()

#Question 2
d = 0.05
H = sp.lti([1,0.05], polymul([1,0,2.25],[1,0.1,2.2525]))
t,x2=sp.impulse(H,None, linspace(0,50,501))
plot(t,x2)
title('x(t) with decay 0.05')
xlabel('time')
ylabel('x(t)')
show()

#Question 3
transfer_function = poly1d([1,0,2.25])
t=linspace(0,100,1001)
#cos(1.5t)e−0.5t
w = 1.4
figure(0)
for i in range(5):
    u= np.cos(w*t)* np.exp(-d*t)
    H = sp.lti([1,d], polymul([1,0,2.25],[1,2*w,w**2 + d**2]))
    t,y,svec=sp.lsim(H,u,t)
    w += 0.05
    subplot(2,3,i+1)
    plot(t,y)
    title(f'w = {w-0.05}')
    xlabel('time')
    ylabel('x(t)')

show()


#Question 4
figure(1)
Y = sp.lti([2], [1,0,3,0])
t,y=sp.impulse(Y,None, linspace(0,20,201))
plot(t,y)
X = sp.lti([1,0,2], [1,0,3,0])
t,x = sp.impulse(X,None, linspace(0,20,201))
plot(t,x)
xlabel('time')
legend(['y(t)', 'x(t)'])
show()

#Question 5
figure(2)
H5 = sp.lti([1], [10**-12, 10**-4, 1])
W,S,phi=H5.bode()
subplot(1,2,1)
xlabel('frequency')
ylabel('Magnitude')
title('Magnitude plot of Steady State Response')
semilogx(W,S)
subplot(1,2,2)
semilogx(W,phi)
xlabel('frequency')
ylabel('Phase')
title('Phase plot of Steady State Response')
show()

#Question 6
figure(3)
subplot(1,2,1)
t = linspace(0,10**-2,10**4)
Vi = np.cos(1000*t) - np.cos(10**6 * t)
t,Vo_long,svec=sp.lsim(H5,Vi,t)
plot(t, Vo_long)
xlabel('time')
ylabel('Voltage')
title(r'$V_o$ long term response')
subplot(1,2,2)
t_small = linspace(0, 30* (10**-6), 301)
Vi = np.cos(1000*t_small) - np.cos(10**6 * t_small)
t,Vo_small,svec=sp.lsim(H5,Vi,t_small)
plot(t, Vo_small)
xlabel('time')
ylabel('Voltage')
title(r'$V_o$ short term response')
show()

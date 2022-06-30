import sympy as sym
import scipy.signal as sp
import numpy as np
import matplotlib.pyplot as plt


s= sym.symbols('s')
def lowpass(R1,R2,C1,C2,G,Vi):
      s= sym.symbols('s')
      A=sym.Matrix([[0,0,1,-1/G],[-1/(1+s*R2*C2),1,0,0],[0,-G,G,1],[-1/R1-1/R2-s*C1,1/R2,0,s*C1]])
      b=sym.Matrix([0,0,0,-Vi/R1])
      V=A.inv()*b
      return (A,b,V)


#Question 1
def sympyToH(V):
    n,d=sym.fraction(V)
    n,d=sym.Poly(n,s),sym.Poly(d,s)
    num,den = n.all_coeffs(), d.all_coeffs()
    num,den = [float(f) for f in num], [float(f) for f in den]
    H = sp.lti(num,den)
    return H

A,b,V=lowpass(10000,10000,1e-9,1e-9,1.586,1)
Vo_Q1 = V[3]
H_low = sympyToH(Vo_Q1)
t = np.linspace(0, 1e-3, 1001)
t,x,svec = sp.lsim(H_low , np.ones(1001),t)
plt.plot(t,x)
plt.title('Step Response')
plt.xlabel('time')
plt.ylabel('V')
plt.show()


#Question 2
t = np.linspace(0,2e-2,100001)
t,x,svec=sp.lsim(H_low, np.sin(2000*np.pi*t)+np.cos(2e6*np.pi*t),t)
plt.plot(t,np.sin(2000*np.pi*t))
plt.plot(t,x)
plt.title('Response of LPF to a super-positioned input')
plt.xlabel('time')
plt.ylabel('V')
plt.legend(['Low Frequency Input','Output'])
plt.show()
plt.plot(t,x)
plt.title('Response of LPF to a super-positioned input')
plt.xlabel('time')
plt.ylabel('V')
plt.legend(['Output'])
plt.show()


#Question 3
def highpass(R1,R3,C1,C2,G,Vi):
    s=sym.symbols('s')
    A = sym.Matrix([[0,0,-1,1/G],[0,G,-G,-1],[s*C1+s*C2+1/R1,-s*C2,0,-1/R1],[-s*C2*R3/(1+s*C2*R3),1,0,0]])
    b = sym.Matrix([0,0,s*C1*Vi,0])
    V = A.inv()*b
    return (A,b,V)
A,b,Vh=highpass(10000,10000,1e-9,1e-9,1.586,1)
H_high=Vh[3]

ww=np.logspace(0,8,801)
ss=1j*ww
hf=sym.lambdify(s,H_high,"numpy")
v=hf(ss)
plt.loglog(ww,abs(v),lw=2)
plt.grid(True)
plt.xlabel('ω')
plt.ylabel('|H(jω)|')
plt.title('High Pass Filter')
plt.show()


H_high = sympyToH(H_high)



#Question 4
t=np.linspace(0,5e-7*np.pi,5001)
t,x,svec=sp.lsim(H_high,np.sin(1e7*np.pi*t)*np.exp(-1e6*t) + np.sin(1e3*np.pi*t)*np.exp(-1e6*t),t)
plt.plot(t,x)
plt.plot(t,np.sin(1e7*np.pi*t)*np.exp(-1e6*np.pi*t))
plt.title('Damped Response of High Pass Filter')
plt.xlabel('time')
plt.ylabel('V')
plt.legend(['Output', 'High Freq Input'])
plt.show()



#Question 5
t=np.linspace(0,1e-3,1001)
t,x,svec=sp.lsim(H_high,np.ones(1001),t)
plt.plot(t,x)
plt.title('Step Response of High Pass Filter')
plt.xlabel('time')
plt.ylabel('V')
plt.show()

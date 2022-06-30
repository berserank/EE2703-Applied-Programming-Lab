from pylab import *
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate
#Q1
def cos_cos(x):
    y = np.cos(np.cos(x))
    return y

def exp(x):
    y = np.exp(x)
    return y

x = np.arange(-2*np.pi, 4*np.pi, 0.01)
M_0 = np.array(cos_cos(x))
M_1 = np.array(np.log(exp(x)))
M = np.vstack((M_0,M_1)).T
plt.plot(x, M_0)
plt.xlabel('x')
plt.legend(['cos(cos(x))'])
plt.grid()
plt.show()

plt.plot(x, M_1)
plt.xlabel('x')
plt.legend(['log(exp(x))'])
plt.grid()
plt.show()

# plt.plot(x,M)
# plt.xlabel('x')
# plt.legend(['cos(cos(x))', 'log(exp(x))' ])
# plt.grid()
# plt.show()

#Q2

def coefficents_find(f):

    def u(x,k):
        return f(x)* np.cos(k*x)
    def v(x,k):
        return f(x)* np.sin(k*x) 
    a = []
    a0 = (1/( 2* np.pi)) * (integrate.quad(u , 0, 2* np.pi, args = 0))[0]
    a.append(a0)
    for i in range(1,26):
        a.append((1/np.pi) * integrate.quad(u, 0, 2*np.pi, args= i)[0]) 
        a.append((1/np.pi) * integrate.quad(v, 0, 2*np.pi, args= i)[0])
    return a



#Q3

arr_1 = np.array(coefficents_find(cos_cos))
arr_1a = []
arr_1b = []
arr_1a.append(arr_1[0])
for i in range(1,len(arr_1)):
    if i%2 == 0:
        arr_1b.append(arr_1[i])
    else:
         arr_1a.append(arr_1[i])


arr_2 = np.array(coefficents_find(exp))
arr_2a = []
arr_2b = []
arr_2a.append(arr_2[0])
for i in range(1,len(arr_2)):
    if i%2 == 0:
        arr_2b.append(arr_2[i])
    else:
         arr_2a.append(arr_2[i])
n1 = np.arange(0,26)
n2 = np.arange(1,26)

fig, axs = plt.subplots(2)
fig.suptitle('Semilog Plots of First 25 Fourier Coefficients')
axs[0].semilogy(n1, np.abs(arr_1a), 'ro')
axs[0].semilogy(n2, np.abs(arr_1b), 'ro')
axs[0].set_title("Cos(Cos(x))")
axs[0].grid()


axs[1].semilogy(n1, np.abs(arr_2a), 'ro')
axs[1].semilogy(n2, np.abs(arr_2b), 'ro')
axs[1].set_title("exp(x)")
axs[1].grid()


plt.show()

fig, axs = plt.subplots(2)

fig.suptitle('Log-log Plots of First 25 Fourier Coefficients')
axs[0].loglog(n1, np.abs(arr_1a), 'ro')
axs[0].loglog(n2, np.abs(arr_1b), 'ro')
axs[0].set_title("Cos(Cos(x))")
axs[0].grid()
axs[0].legend(['a', 'b'])

axs[1].loglog(n1, np.abs(arr_2a), 'ro')
axs[1].loglog(n2, np.abs(arr_2b), 'ro')
axs[1].set_title("exp(x)")
axs[1].grid()

plt.show()


#Q4,Q5

x = linspace(0, 2*np.pi, 401)
x = x[:-1]
b = cos_cos(x)
A=np.zeros((400,51)) 
A[:,0]=1
for k in range(1,26):
        A[:,2*k-1]=np.cos(k*x)
        A[:,2*k]=np.sin(k*x)

c_double_cos = np.linalg.lstsq(A,b, rcond = None)[0]
c_double_cosa = []
c_double_cosb = []
c_double_cosa.append(c_double_cos[0])
for i in range(1,len(c_double_cos)):
    if i%2 == 0:
        c_double_cosb.append(c_double_cos[i])
    else:
         c_double_cosa.append(c_double_cos[i])


b = exp(x)
c_exp = np.linalg.lstsq(A,b, rcond = None)[0]
c_expa = []
c_expb = []
c_expa.append(c_exp[0])
for i in range(1,len(c_exp)):
    if i%2 == 0:
        c_expb.append(c_exp[i])
    else:
         c_expa.append(c_exp[i])

fig, axs = plt.subplots(2)
fig.suptitle('Semilog Plots of First 25 Fourier Coefficients')
axs[0].semilogy(n1, np.abs(arr_1a), 'ro')
axs[0].semilogy(n2, np.abs(arr_1b), 'ro')
axs[0].semilogy(n1, np.abs(c_double_cosa), 'go')
axs[0].semilogy(n2, np.abs(c_double_cosb), 'go')
axs[0].set_title("Cos(Cos(x))")
axs[0].grid()


axs[1].semilogy(n1, np.abs(arr_2a), 'ro')
axs[1].semilogy(n2, np.abs(arr_2b), 'ro')
axs[1].semilogy(n1, np.abs(c_expa), 'go')
axs[1].semilogy(n2, np.abs(c_expb), 'go')
axs[1].set_title("exp(x)")
axs[1].grid()

plt.show()


#Q6
#Deviation for Double Cos
dev_double_cos = list(np.abs(arr_1 - c_double_cos))
print("The Maximum deviation for double cos function's coefficients is" , max(dev_double_cos))

#Deviation for Exp
dev_exp = list(np.abs(arr_2 - c_exp))
print("The Maximum deviation for Exp function's coefficients is" , abs(max(dev_exp)))

#Q7
approx_double_cos = A. dot(c_double_cos)
approx_exp = A. dot(c_exp) 

fig, axs = plt.subplots(2)
fig.suptitle('Comparison of two functions')

axs[0].semilogy(x, cos_cos(x), 'ro')
axs[0].semilogy(x, approx_double_cos, 'go')
axs[0].set_title("Cos(Cos(x)) Comparison")
axs[0].grid()

axs[1].semilogy(x, exp(x), 'ro')
axs[1].semilogy(x, approx_exp, 'go')
axs[1].set_title("Exp(x) Comparison")
axs[1].grid()
plt.show()
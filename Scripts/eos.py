import numpy as np
import matplotlib.pyplot as plt
import sys

Lsize = int(sys.argv[1])    # length of third direction
nparm=5                     # number of fit parameters

#  read in data from files in standard format
b=np.loadtxt('cond_m01_Ls'+'{:02d}'.format(Lsize),usecols=0,unpack=True)
nbeta=b.size  # number of beta values in data
beta=np.empty((nbeta))
cond=np.empty((nbeta))
dcond=np.empty((nbeta))
m=np.empty((nbeta))
mlabel=np.empty(6) # number of mass values in data = 5

for im in range(1,6):
    filename='cond_m0'+str(im)+'_Ls'+'{:02d}'.format(Lsize)
    b,c,d=np.loadtxt(filename,unpack=True)
    beta=np.vstack((beta,b))   # beta values
    cond=np.vstack((cond,c))   # condensate values
    dcond=np.vstack((dcond,d)) # condensate errors
    mlabel[im]=0.01*im
    am=mlabel[im]*np.ones((nbeta))
    m=np.vstack((m,am))        # mass values 

# put data into one dimensional array suitable for least squares fit
# could eliminate points from fit by judicious slicing at this point...
x  =  beta.flatten()[nbeta:beta.size]
y  =  cond.flatten()[nbeta:cond.size]
dy = dcond.flatten()[nbeta:dcond.size]
am =     m.flatten()[nbeta:m.size]
ndat=x.size

#  perform least squares fit using Levenberg-Marquardt
from scipy.optimize import least_squares

def fun(a,x,y,dy,am):
    """Powerlaw equation of state"""
    return (a[0]*(x-a[1])*y**a[2]+a[3]*y**a[4]-am)/dy

def jac(a,x,y,dy,am):
    J=np.zeros((ndat,nparm))
    J[:,0] = (x-a[1])*y**a[2]/dy
    J[:,1] = - (a[0]*y**a[2])/dy
    J[:,2] = (np.log(y)*a[0]*(x-a[1])*y**a[2])/dy
    J[:,3] = (y**a[4])/dy
    J[:,4] = (np.log(y)*a[3]*y**a[4])/dy
    return J

a0 = np.array((2.0,0.3,1.0,12.0,3.0)) # array of intial guesses for fit
res = least_squares(fun, a0, jac=jac, args=(x,y,dy,am), xtol=1e-10, method='lm',
verbose=1) 
Hessian=np.matrix(res.jac.T.dot(res.jac))
Covar=Hessian.I

# Print out fit parameters and their estimated errors, and the chisq/dof
A=res.x[0]
betac=res.x[1]
p=res.x[2]
B=res.x[3]
delta=res.x[4]

dA=np.sqrt(Covar[0,0])
dbetac=np.sqrt(Covar[1,1])
dp=np.sqrt(Covar[2,2])
dB=np.sqrt(Covar[3,3])
ddelta=np.sqrt(Covar[4,4])

print()
print('A={:<12.4f} betac={:<12.4f} p={:<12.4f} '.format(A,betac,p),end='')
print('B={:<12.4f} delta={:<12.4f}'.format(B,delta))
print()
print('dA={:<11.4f} dbetac={:<11.4f} dp={:<11.4f} '.format(dA,dbetac,dp),end='')
print('dB={:<11.4f} ddelta={:<11.4f}'.format(dB,ddelta))
print()
chisq=2*res.cost
c2pdof=chisq/(ndat-nparm)
print('ndat={:<9} chi^2/dof={:<12.3f}'.format(ndat,c2pdof))

#  now find root of EOS to produce  curve of psibarpsi vs. beta
def scalarfun(y,x,am,A,betac,p,B,delta):
    """Powerlaw equation of state"""
    return A*(x-betac)*y**p+B*y**delta-am

from scipy.optimize import brentq

npoints=200     #  number of ponts to define fitted curve
x=np.zeros((6,npoints))
y=np.zeros((6,npoints))
for im in range(1,6):
    for ind in range(npoints):
        x[im,ind] = 0.2+0.004*ind
        y[im,ind] = brentq(scalarfun,0.0,0.5,args=(x[im,ind],mlabel[im],A,betac,p,B,delta))

# Also calculate the curve in the m->0 limit
for ind in range(npoints):
    x[0,ind] = 0.05+0.004*ind
    if x[0,ind] > betac:
        break
    y[0,ind] = (A*(betac-x[0,ind])/B)**(1.0/(delta-p))

# enables economic display of errors in plot title
def fancyerror(dA,nplaces):
    err=int(10**nplaces*dA+0.5)
    if dA<1:
        return err
    return err/10**nplaces

#  Finally plot a figure to show data plus fit
fig=plt.figure()
fig.suptitle((r'$L_s=${}:'
r' $\beta_c=${:4.3f}({}),'
r' $p=${:4.3f}({}),'
r' $\delta=${:4.3f}({})'.format(Lsize,
betac,fancyerror(dbetac,3),p,fancyerror(dp,3),delta,fancyerror(ddelta,3))))
ax=fig.add_subplot(111)
for im in range(1,6):
    ax.plot(x[im,:],y[im,:],c='k',ls='--',lw=0.5)
    ax.errorbar(beta[im,:],cond[im,:],yerr=dcond[im,:],fmt='.',ms=2.5,label='m={}'.format(mlabel[im]))
ax.plot(x[0,:],y[0,:],c='grey',ls='-',lw=0.5,label='m=0')
ax.text(0.4,0.85,r'$\chi^2$/dof={:4.3}'.format(c2pdof),transform=ax.transAxes)
ax.set_xlabel(r'$\beta$')
ax.set_xlim(left=0)
ax.set_ylabel(r'$\langle\bar\psi\psi\rangle$')
ax.set_ylim(0,0.25)
plt.legend()
plt.show()

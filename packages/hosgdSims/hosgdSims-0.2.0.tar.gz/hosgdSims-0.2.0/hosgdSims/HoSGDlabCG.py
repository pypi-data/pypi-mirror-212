import numpy as np
import scipy as sc
from scipy import signal

import matplotlib.pylab as PLT

import requests
from io import BytesIO
from PIL import Image, ImageOps


import HoSGDdefs as hosgdDef


class hosgdFunLS(object):
    r""" Linear system is given by
                Au = b,
         where
         * A = A^T
    """

    def __init__(self, matA, z, gNormOrd=2, Nstats=3, verbose=10):

        self.matA = matA
        self.z    = z
        self.Nstats   = Nstats
        self.verbose  = verbose

        self.bNormVal = None
        self.b        = None

    # ---------

    def bNorm(self):

        if self.b is None:
           self.computeB()

        if self.bNormVal is None:
           self.bNormVal = np.linalg.norm( self.b.ravel(), ord=2)

        return self.bNormVal

    # ---------

    def initSol(self):

        if self.b is None:
           self.computeB()

        return 0*self.b

    # ---------

    def computeStats(self, u, k, rho):

        cost  = self.costFun(u)

        return np.array([k, cost, rho])

    # ---------

    def printStats(self, k, nIter, v):

        if k == 0:
            print('\n')

        if self.verbose > 0:

            if np.remainder(k,self.verbose)==0 or k==nIter-1:
               print('{:>3d}\t {:.3e}\t {:.2e}'.format(int(v[k,0]),v[k,1],v[k,2]))

        return

    # ---------

    def A(self, u):

        if self.matA.shape[0] == self.matA.shape[1]:            # --> linear system: Au = z
            v = self.matA.dot(u)
        else:
            v = self.matA.transpose().dot( self.matA.dot(u) )   # --> linear system A^TA u = A^T z

        return v

    # ---------

    def costFun(self, u):   # 0.5 || A*u - b ||_2^2

        return 0.5*np.linalg.norm( self.A(u).ravel()-self.b.ravel(), ord=2)**2

    # ---------

    def computeB(self):

        if self.matA.shape[0] == self.matA.shape[1]:  # --> linear system: Au = z
           self.b = self.z
        else:
           self.b = self.matA.transpose().dot(self.z)             # --> linear system A^TA u = A^T z
    # ---------




class hosgdFunLSConv(hosgdFunLS):
    r""" Observed data z = h*u
         then the linear system is given by
                Au = b,
         where
         * Au = h^T*h*u
         * b  = h^T*z
    """

    def __init__(self, h, z, Nstats=3, verbose=10):

        self.h = h
        self.z = z
        self.Nstats   = Nstats
        self.verbose  = verbose

        self.bNormVal = None
        self.b        = None

    # ---------
    # ---------

    def colorConv2D(self, u, h):

        v = 0*u
        for k in range( v.shape[2] ):
            v[:,:,k] = signal.convolve2d(u[:,:,k], h, mode='same', boundary='symm')

        return v

    def conv2D(self, u, h):

      if len(u.shape) == 3:
         v = self.colorConv2D(u, h)
      else:
         v = signal.convolve2d(u, h, mode='same', boundary='symm')

      return v


    def fwOp(self, u):
        v = self.conv2D(u, self.h)
        return v

    # ---------

    def fwAdjOp(self, u):
        v = self.conv2D(u, np.flip(np.flip(self.h,1),0) )
        return v

    # ---------

    def A(self, u):
        v = self.fwAdjOp(self.fwOp(u))
        return v

    # ---------


    def computeB(self):

        if self.b is None:
           self.b = self.fwAdjOp(self.z)

        return

    # ---------

    def costFun(self, u):   # 0.5 || h*u - z ||_2^2

        return 0.5*np.linalg.norm( self.fwOp(u).ravel()-self.z.ravel(), ord=2)**2


    # ---------




class hosgdFunTikConv(hosgdFunLSConv):
    r""" Observed data z = h*u
         then the optimization problem is given by

                0.5|| h*u - z ||_2^2 + 0.5*lambda|| u ||_2^2

         which results in the linear system

                Au = b
        where
         * Au = h^T*h*u + lambda\cdot u
         * b  = h^T*z
    """

    def __init__(self, h, z, lmbda, Nstats=3, verbose=10):

        self.h = h
        self.z = z
        self.lmbda = lmbda
        self.Nstats   = Nstats
        self.verbose  = verbose

        self.bNormVal = None
        self.b        = None

    # ---------
    # ---------


    # ---------

    def A(self, u):
        v = self.fwAdjOp(self.fwOp(u)) + self.lmbda*u
        return v

    # ---------


    def costFun(self, u):   # 0.5 || h*u - z ||_2^2

        return 0.5*np.linalg.norm( self.fwOp(u).ravel()-self.z.ravel(), ord=2)**2 + 0.5*self.lmbda*u.ravel().dot( u.ravel() )


    # ---------



def hosgdCG(OptProb, nIter, epsilon):

    u = OptProb.initSol()
    r = OptProb.b - OptProb.A(u)

    stats = np.zeros( [nIter, OptProb.Nstats] )

    for k in range(nIter):

        rho = r.ravel().dot( r.ravel() )

        if np.sqrt(rho)/OptProb.bNorm() < epsilon:
           break

        if k == 0:
           p = r.copy()
        else:
           beta = rho/rho0
           p = r + beta*p

        w     = OptProb.A(p)

        alpha = rho/p.ravel().dot(w.ravel())

        u = u + alpha*p

        r = r - alpha*w

        rho0 = rho

        stats[k,:] = OptProb.computeStats(u, k, rho/OptProb.bNorm())
        OptProb.printStats(k, nIter, stats)


    return u, stats


def gauss2D(shape=(3,3), sigma=0.5):

	m,n = [(ss-1.)/2. for ss in shape]

	y,x = np.ogrid[-m:m+1,-n:n+1]

	h = np.exp( -(x*x + y*y) / (2.*sigma*sigma) )
	h[ h < np.finfo(h.dtype).eps*h.max() ] = 0
	sumh = h.sum()

	if sumh != 0:
		h /= sumh

	return h


def hosgdCGTestConv(val = 0, sigma = 0.0):


    fname = {0: requests.get('http://sipi.usc.edu/database/misc/5.2.10.tiff'),       # bridge (grayscale)
             1: requests.get('http://sipi.usc.edu/database/misc/boat.512.tiff'),     # boat (grayscale)
             2: requests.get('http://sipi.usc.edu/database/misc/4.2.03.tiff'), # mandrill (color)
        }

    img = Image.open(BytesIO(fname.get(val).content))

    I = np.asarray(img).astype(float)/255.   # Datos representados en Array (matriz)

    h = gauss2D((5,5), 2.)

    if len(I.shape) == 2:
       Ib = sc.signal.convolve2d(I,h,mode='same',boundary='symm')
    else:
       Ib = 0*I
       for k in range(I.shape[2]):
           Ib[:,:,k] = sc.signal.convolve2d(I[:,:,k],h,mode='same',boundary='symm')

    rng = np.random.default_rng()
    Ib += sigma*rng.normal(size=Ib.shape)


    OptProb = hosgdFunLSConv(h, Ib)

    u, stats = hosgdCG(OptProb, 50, 1e-6)


    PLT.figure()
    PLT.imshow(Ib,cmap='gray')
    PLT.show(block=False)

    PLT.figure()
    PLT.imshow( np.clip(u,0,1), cmap='gray')
    PLT.show(block=False)

    return u, stats


def hosgdCGTestTikConv(lmbda, val = 0, sigma = 0.05):


    fname = {0: requests.get('http://sipi.usc.edu/database/misc/5.2.10.tiff'),       # bridge (grayscale)
             1: requests.get('http://sipi.usc.edu/database/misc/boat.512.tiff'),     # boat (grayscale)
             2: requests.get('http://sipi.usc.edu/database/misc/4.2.03.tiff'), # mandrill (color)
        }

    img = Image.open(BytesIO(fname.get(val).content))

    I = np.asarray(img).astype(float)/255.   # Datos representados en Array (matriz)

    h = gauss2D((5,5), 2.)

    if len(I.shape) == 2:
       Ib = sc.signal.convolve2d(I,h,mode='same',boundary='symm')
    else:
       Ib = 0*I
       for k in range(I.shape[2]):
           Ib[:,:,k] = sc.signal.convolve2d(I[:,:,k],h,mode='same',boundary='symm')

    rng = np.random.default_rng()
    Ib += sigma*rng.normal(size=Ib.shape)


    OptProb = hosgdFunTikConv(h, Ib, lmbda)

    u, stats = hosgdCG(OptProb, 50, 1e-6)


    PLT.figure()
    PLT.imshow(Ib,cmap='gray')
    PLT.show(block=False)

    PLT.figure()
    PLT.imshow( np.clip(u,0,1), cmap='gray')
    PLT.show(block=False)

    return u, stats



def hosgdCGTest(N=500, M=2000, sigma=0.05, r=0.5):


    # --- Data generation
    # -------------------
    rng = np.random.default_rng()

    if N==M: # force matrix to be symmetric
       B = rng.normal(size=[N,N])
       A = B.transpose().dot(B) + np.sqrt(N)*np.eye(N)
    else:
       A = rng.normal(size=[N,M])

    A /= np.linalg.norm(A,axis=0)

    ind = np.random.permutation(M)
    R = int( np.floor(r*M) )

    xOrig = np.random.randn(M,1)
    xOrig[R::] *= 0.

    b = A.dot(xOrig) + sigma*np.random.randn(N,1)

    # --- Problem
    # -------------------

    OptProb = hosgdFunLS(A, b)


    # --- Call CG
    # -------------------

    u, stats = hosgdCG(OptProb, 50, 1e-6)

    return u, stats

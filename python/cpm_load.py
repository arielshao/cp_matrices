import numpy
from numpy import linspace,pi,real,imag,exp
from numpy import array as a
import cptree
#reload(cptree)
import pylab
from pylab import plot

#from scipy.linalg import norm
import scipy.sparse
#import scipy.linsolve
#import scipy.sparse.linalg.eigen
import scipy.sparse.linalg.eigen.arpack as arpack
import scipy.linalg

from time import time

#global SURF_SR
# SURF_SR = 1.0
# import cp_sphere
# cp_sphere.init(center=a([0,0,0]), radius=SURF_SR)
# cpfun_inner = cp_sphere.cp_sphere

# import cp_hemisphere
# cp_hemisphere.init(center=a([0,0,0]), radius=SURF_SR)
# cpfun_inner = cp_hemisphere.cp_hemisphere

import closestpoint

q = closestpoint.Hemisphere()

cpfun = q.cp
#cpfun = cpbar
#cpfun = cpfun_inner
#cpfun = cp_sphere.cp_sphere

# This function that helps with boundary conditions when the surface
# has a boundary.  TODO: ties into "CPBar" boundary conditions as in
# Macdonald, Brandman, Ruuth preprint.  TODO: think about cleaning
# this up
def bdyfcn(bdy):
    if bdy==1:
        return 'dirichlet_0th_order'
    elif bdy==2:
        return 'dirichlet_0th_order'
    else:
        return None

print 'start'


#x = numpy.array([-2.0, -2.0])
#dx = 4.0

#f96 = numpy.float96
#x = numpy.array([f96(-2.0), f96(-2.0), f96(-2.0)])
#dx = f96(8.0)

x = numpy.array([-2.0, -2.0, -2.0])
dx = 8.0

dim = len(x)
maxlev = 7
g = cptree.CPGrid('test', cpfun, dim, x, dx, interp_degree=3, levels=maxlev+1)


## a parameterized grid for plotting
x,y,z = q.ParamGrid(rez=64)

# this can be used to view like this:
#from enthought.mayavi import mlab
#s = mlab.mesh(x, y, z, scalars=z**2)
#mlab.show()

x2 = x.reshape(x.shape[0]*x.shape[1],)
y2 = y.reshape(x.shape[0]*x.shape[1],)
z2 = z.reshape(x.shape[0]*x.shape[1],)
PlotPts = numpy.vstack((x2,y2,z2)).transpose()


j = maxlev - 0
g.findStencilSets(j)
g.buildListsFromStencilSets(j)
g.findStencilsOnStencilSets(j, bdyfcn)
D = g.buildDiffMatrix(j)
#D3xb,D3xf,D3yb,D3yf = g.buildDiffMatrixTempDxDyTest(j)
E = g.buildExtensionMatrix(j)
Eplot = cptree.buildEPlotMatrix(g, j, PlotPts)
dx = g.Levolve[j][0].dx
#D = D.tocsr()
#E = E.tocsr()
#Eplot = Eplot.tocsr()


# the implicit closest point method matrix.  Almost a product of D and
# E (see Macdonald and Ruuth 2009)
now = time()
M = cptree.LinearDiagonalSplitting(D, E)
print "splitting took %.3g s" % (time()-now)


# keep a copy of the original extended precision matrix
#M_f96 = M.copy()
#M = M.astype(numpy.float64)


# minnz = 1e42
# M = E3
# for i in range(0,M.shape[0]):
#     for j in range(0,M.shape[1]):
#         if M[i,j] != 0:
#             minnz = min(minnz, abs(M[i,j]))
# print minnz



def pause(howlong=None):
    import time as timemod
    if howlong == None:
        raw_input('Paused, press enter to continue')
    else:
        timemod.sleep(howlong)

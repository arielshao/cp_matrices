'''
Created on Aug 10, 2012

@author: nullas
'''
import scipy as sp
from mayavi import mlab
from mpi4py import MPI
from cp.surfaces.MeshWrapper import MeshWrapper
from cp.petsc.band import Band


if __name__ == '__main__':
    opt = {'M':50,'m':5}
    surface = MeshWrapper()
    mlab.triangular_mesh(surface.v[:,0],surface.v[:,1],surface.v[:,2],surface.f,opacity = 0.2)
    comm = MPI.COMM_WORLD
    band = Band(surface,comm,opt)
    band.SelectBlock()
    v = band.getCoordinates()
    print v
    mlab.points3d(v[:,0],v[:,1],v[:,2],mode = 'point')
    mlab.show()
    
    
    
    
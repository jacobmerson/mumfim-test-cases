import sys
import os
import numpy as np
from scipy.sparse.linalg import eigs,eigsh
import matplotlib.pyplot as plt
from scipy.sparse import csr_matrix

sys.path.append('/Users/jacobmerson/spack/opt/spack/darwin-monterey-m1/clang-13.0.0/petsc-3.17.1-cggk5j2evdpqoym5mkge4au77lbos526/lib/petsc/bin/')
os.environ['PETSC_DIR'] = '/Users/jacobmerson/spack/opt/spack/darwin-monterey-m1/clang-13.0.0/petsc-3.17.1-cggk5j2evdpqoym5mkge4au77lbos526/'

import PetscBinaryIO

#filename = "./stiffness_matrix.mtx"
#filename = "./simple_model_stiffness_matrix.mtx"
filename = "./jacobian.mtx"
io = PetscBinaryIO.PetscBinaryIO()
objects = io.readBinaryFile(filename,mattype='scipy.sparse')
print(len(objects))
hand = objects[0]
petsc = objects[1]

difference = hand+petsc
print(difference)

#print(hand)
#print(petsc)
plt.plot(hand.toarray().flatten(),'o')
plt.plot(-1*petsc.toarray().flatten(),'^')
plt.figure()
plt.plot(difference.toarray().flatten())
plt.show()

#vals, vecs = eigs(objects[0])
#vals, vecs = eigsh(objects[0],return_eigenvectors=False)
#num_evals = 10
##objects = objects[0:10]
#
##large_vals = eigsh(objects[0],k=num_evals, return_eigenvectors=False,which='LM')
##small_vals = eigsh(objects[0],k=num_evals, return_eigenvectors=False,which='SM')
#condition_number = np.ones_like(objects)
#fig,ax = plt.subplots(1,1)
##for frame in range(len(objects)):
#for frame in range(len(objects)):
#    evals = eigsh(objects[0],k=num_evals, return_eigenvectors=False,which='BE')
#    frames = [frame]*len(evals)
#    condition_number[frame] = np.abs(np.max(evals))/np.abs(np.min(evals))
#    ax.plot(frames,evals, 'ko')
#    print(frame, ", ",end='')
#ax = plt.gca()
#ax.set_yscale("log")
#fig2, ax2 = plt.subplots(1,1)
#ax2.plot(condition_number, 'x')
#print(condition_number)
#np.savetxt("condition_number.txt",condition_number)
#fig.savefig("eigenvalues.png")
#fig2.savefig("condition_number.png")
#
#plt.show()
#

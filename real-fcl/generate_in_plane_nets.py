from __future__ import print_function
from fibernetgen import *
import numpy as np
import os
from scipy.spatial.transform import Rotation as Rot
from scipy.optimize import fsolve


def generate_network(num_pts,gen_size,trim_size,align_stretch,R):
    dn = DelaunayNetwork(num_pts, gen_size, trim_size)
    U = np.array(((align_stretch, 0, 0),
                        (0, 1.0/np.sqrt(align_stretch), 0),
                        (0, 0, 1.0/np.sqrt(align_stretch))))
    dn.stretch(np.dot(R, U))
    dn.trim()
    lc = dn.compute_mean_length()
    num_removed, sweeps = dn.remove_short_edges(lc/10)
    lc = dn.compute_mean_length()
    dn.remove_disconnected_regions()
    num_removed, sweeps = dn.remove_hanging_nodes()
    return dn

def gen_outer_func(gen_size,trim_size,align_stretches,R,network,target_density):
    def opt_gen_net(num_pts):
        num_pts = int(num_pts)
        network[0] = generate_network(num_pts,gen_size,trim_size,align_stretches,R)
        residual_sq = (network[0].compute_density() - target_density)**2
        if residual_sq<100:
            return 0
        return residual_sq
    return opt_gen_net

def num_pts_outer_func(align_value,density):
    def func(num_seeds):
        c = np.array((1.09440676e+02, -1.12001322e+02,  1.96832140e-01,  3.66218934e-02,
              4.20182055e+01,-2.90826194e-05))
        return c[0]+c[1]*align_value+c[2]*num_seeds+ \
               c[3]*align_value*num_seeds+\
               c[4]*align_value**2+\
               c[5]*num_seeds**2 - density
    return func


def main():
    #### ORIGINAL PARAMETERS
    trim_size = 1.0
    #trim_size = np.array((1.0,0.5,0.5))
    gen_size = 2*trim_size
    #num_pts = 1200
    num_pts = 2400
    num_realizations=10
    num_angles = 20
    num_alignments = 10
    # do not want to crush the network...
    min_alignment = 1.0
    max_alignment=2.0
    #### ORIGINAL PARAMETERS
    #### TEST PARAMETERS
    #trim_size = 1.0
    #gen_size = 2*trim_size
    #num_pts = 2400
    #num_realizations=1
    #num_angles = 1
    #num_alignments = 1
    ## do not want to crush the network...
    #min_alignment = 1.0
    #max_alignment=2.0
    #### TEST PARAMETERS

    # Don't need to include the endpoint since
    # 0 is the same as pi w.r.t. the fibers
    theta = np.linspace(0,np.pi,num_angles,endpoint=False)
    align_stretches = np.linspace(min_alignment, max_alignment, num_alignments)

    # FCL in in the XZ Plane...
    r = Rot.from_euler('y',theta)
    R = r.as_dcm() # convert the euler angles to a rotation matrix

    fiber_rad = 5E-5
    fiber_young_mod = 1E8
    fiber_density = 1000.0
    # density from the uniform nets (which I'm not recomputing currently)
    target_density = 442.742764542
    params = [BiotissueNetworkParams(fiber_young_mod, fiber_rad, fiber_density),]
    network = [None,]
    with open("network_collection_summary.txt", 'w') as summary_file:
        summary_file.write("# theta_idx, align_idx, realization, theta_value, align_value, seedpoints, density\n")
        for i in range(len(theta)):
            for j in range(len(align_stretches)):
                for k in range(num_realizations):
                    # realizations start at 1 (legacy reasons in biotissue code
                    # all other bins start at 0
                    filename = "theta_{}_align_{}_realization_{}".format(i,j,k+1)
                    print("Generating: "+filename)

                    num_pts_func = num_pts_outer_func(align_stretches[j],target_density)
                    num_pts =  fsolve(num_pts_func,num_pts)
                    gen_net = gen_outer_func(gen_size,trim_size,align_stretches[j], R[i],network,target_density)
                    gen_net(num_pts)
                    print("Density Residual: {}".format(np.linalg.norm(target_density-network[0].compute_density())))
                    dn = network[0]
                    dn.assign_params(params, [0 for idx in range(len(dn.edges))])
                    dn.write_biotissue_input(filename+".txt")
                    with open(filename+"_summary.txt", 'w') as f:
                        f.write(str(dn))
                    summary_file.write("{}, {}, {}, {}, {}, {}, {}\n".format(i,j,k,theta[i],align_stretches[j],num_pts[0],network[0].compute_density()))

if __name__ == "__main__":
    main()

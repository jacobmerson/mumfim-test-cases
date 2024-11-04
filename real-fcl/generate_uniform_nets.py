from __future__ import print_function
from fibernetgen import *
import numpy as np
import os

from scipy.spatial.transform import Rotation as Rot

trim_size = 1.0
#trim_size = np.array((1.0,0.5,0.5))
gen_size = 2*trim_size
#num_pts = 1200
num_pts = 2400
num_realizations=1000


fiber_rad = 5E-5
fiber_young_mod = 1E8
fiber_density = 1000.0
params = [BiotissueNetworkParams(fiber_young_mod, fiber_rad, fiber_density),]
for k in range(num_realizations):
    # realizations start at 1 (legacy reasons in biotissue code
    # all other bins start at 0
    filename = "realization_{}".format(k+1)
    print("Generating: "+filename)

    dn = DelaunayNetwork(num_pts, gen_size, trim_size)
    dn.trim()
    lc = dn.compute_mean_length()
    num_removed, sweeps = dn.remove_short_edges(lc/10)
    lc = dn.compute_mean_length()
    dn.remove_disconnected_regions()
    num_removed, sweeps = dn.remove_hanging_nodes()
    dn.assign_params(params, [0 for idx in range(len(dn.edges))])
    dn.write_biotissue_input(filename+".txt")
    with open(filename+"_summary.txt", 'w') as f:
        f.write(str(dn))

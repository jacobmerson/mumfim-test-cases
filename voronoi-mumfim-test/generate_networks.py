from __future__ import print_function
from fibernetgen import *
import numpy as np

def generate_network(trim_size,gen_size,num_pts,output_name, NetworkCls=VoronoiNetwork):
    vn = NetworkCls(num_pts, gen_size, trim_size)
    vn.trim()
    lc = vn.compute_mean_length()
    vn.remove_short_edges(lc/10)
    vn.remove_disconnected_regions()
    vn.remove_hanging_nodes()
    vn.assign_params([BiotissueNetworkParams(100,0.1,1000),], [0]*len(vn.edges))
    vn.write_biotissue_input(output_name)
    with open(output_name+".summary", 'w') as f:
        f.write(str(vn))
    vn.summary()


if __name__ == "__main__":
    trim_size = 1.0
    gen_size = trim_size*2
    num_pts = 800
    generate_network(trim_size,gen_size,num_pts,"voronoi_1.txt",VoronoiNetwork)
    generate_network(trim_size,gen_size,num_pts,"delaunay_1.txt",DelaunayNetwork)

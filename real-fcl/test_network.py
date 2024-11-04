from fibernetgen import DelaunayNetwork, VoronoiNetwork
#import networkx
import numpy as np

num_pts = 100000
gen_size=2
trim_size=1
#dn = DelaunayNetwork(num_pts,gen_size,trim_size)
dn = VoronoiNetwork(num_pts,gen_size,trim_size)
dn.trim()
dn._construct_graph()
dn.construct_boundary_set()
bound_set = set(dn.right) |set(dn.left) | \
            set(dn.front) | set(dn.back) | \
            set(dn.top) | set(dn.bot)

net_degree = dn.graph.degree

not_bounds = [degree for node,degree in net_degree if node not in bound_set]
all_nodes = [degree for _,degree in net_degree]
bound_nodes = [degree for node,degree in net_degree if node in bound_set]
print(len(not_bounds), np.mean(not_bounds),np.max(not_bounds),np.min(not_bounds))
print(len(all_nodes), np.mean(all_nodes),np.max(all_nodes),np.min(all_nodes))
print(len(bound_nodes), np.mean(bound_nodes),np.max(bound_nodes),np.min(bound_nodes))

import numpy as np
import glob

for align in range(0,10):
    if align == 0:
        folder = "/lore/mersoj/real-fcl/uniform_nets/"
        summary_files = glob.glob(folder+"/*realization*_summary.txt")
    else:
        folder = "/lore/mersoj/real-fcl/nets_theta_0_2PI_20_stretch_1_2_10/"
        summary_files = glob.glob(folder+"/*align_{}_realization*_summary.txt".format(align))
    #print("Num files: {}".format(len(summary_files)))
    density = []
    for summary_file in summary_files:
        with open(summary_file, 'r') as f:
            line = "" 
            for line in f:
                if "density" in line:
                    break
            density.append(float(line.strip().split("=")[1]))
    print("{},{}".format(align,np.mean(density)))
    #print(align, np.mean(density))


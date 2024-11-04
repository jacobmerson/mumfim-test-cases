import glob
import os
#import subprocess
import sys
# same as write_macro, but for a different file naming scheme

def write_steps(prefix, pvdFile):
    # msh_stp_0_iter_1
    loadStepsMeshes = glob.glob(prefix+"*")
    loadStepsMeshes = [x for x in loadStepsMeshes if os.path.splitext(x)[1] not in [".pvd",]]
    # key gives the step, followed by the iteration
    ky = lambda val: int(val.split("_")[2])
    loadStepsMeshes.sort(key=ky)
    successfulSteps = [x for x in loadStepsMeshes if ky(x) > 0]
    with open(pvdFile, 'w') as f:
        f.write('<VTKFile type="Collection" version="0.1">\n')
        f.write('  <Collection>\n')
        for meshName in loadStepsMeshes:
            print(meshName)
            outputPrefix = os.path.splitext(os.path.basename(meshName))[0]
            loadStep = ky(meshName)
            pvtuFile = outputPrefix+"/"+outputPrefix+".pvtu"
            f.write('    <DataSet timestep="{}" group="" part="0" file="{}"/>\n'.format(loadStep, pvtuFile))
        f.write('  </Collection>\n')
        f.write('</VTKFile>\n')

if __name__ =="__main__":
    prefix = "msh_stp"
    pvdFile = prefix+".pvd"
    write_steps(prefix, pvdFile)

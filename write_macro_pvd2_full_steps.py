import glob
import os
#import subprocess
import sys
# same as write_macro, but for a different file naming scheme

def write_steps(prefix, pvdFile):
    # msh_stp_0_iter_1
    loadStepsMeshes = glob.glob(prefix+"*iter*")

    # key gives the step, followed by the iteration
    ky = lambda val: (int(val.split("_")[2]), int(val.split("_")[4]))
    #print(ky(loadStepsMeshes[0]))
    loadStepsMeshes.sort(key=ky)

    onlyStepMeshes = []
    prevStep = loadStepsMeshes[0]
    for step in loadStepsMeshes:
        if ky(step)[0] > ky(prevStep)[0]:
            onlyStepMeshes.append(prevStep)
        prevStep = step
    onlyStepMeshes.append(loadStepsMeshes[-1])
    print(onlyStepMeshes)

    with open(pvdFile, 'w') as f:
        f.write('<VTKFile type="Collection" version="0.1">\n')
        f.write('  <Collection>\n')
        for meshName in onlyStepMeshes:
            outputPrefix = os.path.splitext(os.path.basename(meshName))[0]
            loadStep, iteration = ky(meshName)
            pvtuFile = outputPrefix+"/"+outputPrefix+".pvtu"
            f.write('    <DataSet timestep="{}" group="" part="0" file="{}"/>\n'.format(loadStep, pvtuFile))
        f.write('  </Collection>\n')
        f.write('</VTKFile>\n')

if __name__ =="__main__":
    prefix = "msh_stp"
    pvdFile = prefix+".pvd"
    write_steps(prefix, pvdFile)

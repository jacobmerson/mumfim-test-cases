import numpy as np
from scipy.optimize import fsolve




def outer_func(align_value,density):
    def func(num_seeds):
        c = np.array((1.09440676e+02, -1.12001322e+02,  1.96832140e-01,  3.66218934e-02,
              4.20182055e+01,-2.90826194e-05))
        return c[0]+c[1]*align_value+c[2]*num_seeds+ \
               c[3]*align_value*num_seeds+\
               c[4]*align_value**2+\
               c[5]*num_seeds**2 - density
    return func

f = outer_func(1.0,415)
res = fsolve(f,399)
print(res[0])

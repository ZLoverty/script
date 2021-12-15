# use this file to debug code
# %% codecell
from pivLib import read_piv
import numpy as np
import os
import pdb
import matplotlib.pyplot as plt
import sys
# %% codecell
d = sys.argv[1]
print(d)
d1 = d.rstrip(os.sep)
print(d1)

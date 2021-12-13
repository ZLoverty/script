from pivLib import read_piv
import numpy as np
import os
import pdb
from corrLib import cav_imseq

if __name__=="__main__":
    X, Y, U, V = read_piv(os.path.join("test_images", "cav_imseq", "00000-00001.csv"))
    x, y, ca, cv = corrS(X, Y, U, V)
    print(cv)

#
import matplotlib.pyplot as plt
import numpy as np
#
a = np.arange(100)
plt.plot(a)
a

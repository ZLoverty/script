# use this file to debug code
# %% codecell
from pivLib import read_piv
import numpy as np
import os
import pdb
import matplotlib.pyplot as plt
def corrS(X, Y, U, V):
    """Compute the spatial autocorrelations of a velocity field.
    Args:
    X, Y, U, V -- the result of PIV analysis. Each is a 2D array.
                    Use pivLib.read_piv to construct thses arrays from PIV data files.
    Returns:
    x, y, CA, CV -- The angle autocorrelation (CA) and velocity autocorrelation (CV).
                    x, y are the associated distances.
                    Note that we only consider half of the length in each dimension, so x, y are different from the input X, Y.
    EDIT
    ====
    Dec 13, 2021 -- i) Replace all the `mean()` function to nanmean, to handle masked PIV data. ii) Add doc string.
    """
    row, col = X.shape
    r = int(row/2)
    c = int(col/2)
    vsqrt = (U ** 2 + V ** 2) ** 0.5
    vsqrt[vsqrt==0] = np.nan
    U = U - np.nanmean(U)
    V = V - np.nanmean(V)
    Ax = U / vsqrt
    Ay = V / vsqrt
    CA = np.ones((r, c))
    CV = np.ones((r, c))
    for xin in range(0, c):
        for yin in range(0, r):
            if xin != 0 or yin != 0:
                CA[yin, xin] = np.nanmean((Ax[0:row-yin, 0:col-xin] * Ax[yin:row, xin:col] + Ay[0:row-yin, 0:col-xin] * Ay[yin:row, xin:col]))
                CV[yin, xin] = np.nanmean((U[0:row-yin, 0:col-xin] * U[yin:row, xin:col] + V[0:row-yin, 0:col-xin] * V[yin:row, xin:col])) / (np.nanstd(U)**2+np.nanstd(V)**2)
    return X[0:r, 0:c], Y[0:r, 0:c], CA, CV

# %% codecell
X, Y, U, V = read_piv(r"test_images\batch_spatial_correlation\piv_folder\00\06972-06973.csv")
x, y, ca, cv = corrS(X, Y, U, V)
plt.imshow(ca)
# %%
vsqrt = (U ** 2 + V ** 2) ** 0.5
vsqrt[~np.isnan(vsqrt)]
plt.imshow(U)
plt.imshow(vsqrt)
plt.imshow(U / vsqrt)
vsqrt[vsqrt==0]
# %% codecell
# set vsqrt == 0 to np.nan
vsqrt[vsqrt==0] = np.nan
plt.imshow(U / vsqrt)

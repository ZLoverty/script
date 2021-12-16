import numpy as np
from pivLib import read_piv

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
    Dec 15, 2021 -- if norm `vsqrt` is 0, set it to np.nan to avoid divided by zero warning!
    Dec 16, 2021 -- Shift the output X, Y origin to 0, 0, so that 0 distance will have the correlation function = 1. More intuitive.
    """
    row, col = X.shape
    r = int(row/2)
    c = int(col/2)
    vsqrt = (U ** 2 + V ** 2) ** 0.5
    vsqrt[vsqrt==0] = np.nan # if norm is 0, set it to np.nan to avoid divided by zero warning!
    U = U - np.nanmean(U)
    V = V - np.nanmean(V)
    Ax = U / vsqrt
    Ay = V / vsqrt
    CA = np.ones((r, c))
    CV = np.ones((r, c))
    # pdb.set_trace()
    for xin in range(0, c):
        for yin in range(0, r):
            if xin != 0 or yin != 0:
                CA[yin, xin] = np.nanmean((Ax[0:row-yin, 0:col-xin] * Ax[yin:row, xin:col] + Ay[0:row-yin, 0:col-xin] * Ay[yin:row, xin:col]))
                CV[yin, xin] = np.nanmean((U[0:row-yin, 0:col-xin] * U[yin:row, xin:col] + V[0:row-yin, 0:col-xin] * V[yin:row, xin:col])) / (np.nanstd(U)**2+np.nanstd(V)**2)
    return X[0:r, 0:c] - X[0, 0], Y[0:r, 0:c] - Y[0, 0], CA, CV

    # %% codecell
    x, y, u, v = read_piv(r"test_images\batch_spatial_correlation\piv_folder\01\06974-06975.csv")
    X, Y, CA, CV = corrS(x, y, u, v)

    Y

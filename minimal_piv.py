from openpiv import tools, pyprocess, validation, filters, scaling
import numpy as np
from scipy.signal import medfilt2d
from skimage import io
import matplotlib.pyplot as plt

# %% codecell

def PIV(I0, I1, winsize, overlap, dt):
    """ Normal PIV """
    u0, v0, sig2noise = pyprocess.extended_search_area_piv(
        I0.astype(np.int32),
        I1.astype(np.int32),
        window_size=winsize,
        overlap=overlap,
        dt=dt,
        search_area_size=winsize,
        sig2noise_method='peak2peak',
    )
    # get x, y
    x, y = pyprocess.get_coordinates(
        image_size=I0.shape,
        search_area_size=winsize,
        overlap=overlap,
        window_size=winsize
    )
    u1, v1, mask_s2n = validation.sig2noise_val(
        u0, v0,
        sig2noise,
        threshold = 1.05,
    )
    # replace_outliers
    u2, v2 = filters.replace_outliers(
        u1, v1,
        method='localmean',
        max_iter=3,
        kernel_size=3,
    )
    # median filter smoothing, optional
    # u3 = medfilt2d(u2, 3)
    # v3 = medfilt2d(v2, 3)
    u3 = u2
    v3 = v2
    return x, y, u3, v3

# %% codecell

if __name__=="__main__":
    # %% codecell

    np.random.seed(0)
    x = np.arange(100)
    I0 = np.broadcast_to(np.sin(0.01*np.pi*x), (100, 100)).T
    I1 = np.roll(I0, 5, axis=0) # move I0 5 pixels downwards as I1
    fig, ax = plt.subplots(figsize=(6, 3), ncols=2)
    ax[0].imshow(I0)
    ax[1].imshow(I1)

    # %% codecell

    winsize = 20
    overlap = 10
    dt = 1
    x, y, u, v = PIV(I0, I1, winsize, overlap, dt)
    plt.imshow(I0)
    plt.quiver(x, y, u, v)

    # %% codecell

    print("Vertical mean velocity is {:.1f}".format(v.mean()))

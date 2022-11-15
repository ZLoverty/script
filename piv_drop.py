# from openpiv import tools, pyprocess, validation, filters, scaling
from pivLib import PIV_masked
import numpy as np
from skimage import io
import os
# from scipy.signal import medfilt2d
import pandas as pd
import sys
from corrLib import readdata
import time
from multiprocessing import Pool
from itertools import repeat
from deLib import droplet_image

"""
piv_drop
========

Perform PIV analysis on an image sequence of **bacteria in a droplet**. 

.. rubric:: Syntax

.. code-block:: console

   python piv_drop.py image_folder save_folder winsize overlap dt mask_dir

* image_folder -- folder containing .tif image sequence
* save_folder -- folder to save PIV data
* winsize, overlap, dt -- regular params
* mask_dir -- mask image dir

.. rubric:: Test

.. code-block:: console

   python piv_drop.py test_images\piv_drop test_images\piv_drop 40 20 0.02 test_images\piv_drop\mask.tif

.. rubric:: Edit

* Dec 09, 2021 -- Initial commit.
* Dec 16, 2021 -- i) use `PIV_masked()` as the core algorithm, ii) implement multiprocessing with `Pool`
* Jan 16, 2022 -- add info print, can be used with ">>" to write log.
* Feb 15, 2022 -- remove printing steps to avoid log file spamming.
* Mar 03, 2022 -- i) Reverse the multi-thread code to linear, ii) use `droplet_image` class for the script, iii) no longer print PIV settings to screen, save a `piv_params` json instead
"""

# temporarily deprecated
def PIV_droplet(I0dir, I1dir, I0name, I1name, winsize, overlap, dt, mask, save_folder):
    """Perform PIV analysis on the image sequence in given folder. Specific for images of droplets.
    Args:
    I0, I1 -- adjacent images in a sequence
    winsize, overlap, dt -- regular PIV params
    mask -- a binary image of the same size as I0 and I1
    Returns:
    None"""
    # apply ROI
    I0 = io.imread(I0dir)
    I1 = io.imread(I1dir)
    x, y, u, v = PIV_masked(I0, I1, winsize, overlap, dt, mask)
    frame_data = pd.DataFrame({"x": x.flatten(), "y": y.flatten(), "u": u.flatten(), "v": v.flatten()})
    frame_data.to_csv(os.path.join(save_folder, "{0}-{1}.csv".format(I0name, I1name)), index=False)

if __name__=="__main__":
    image_folder = sys.argv[1]
    save_folder = sys.argv[2]
    winsize = int(sys.argv[3])
    overlap = int(sys.argv[4])
    dt = float(sys.argv[5])
    mask_dir = sys.argv[6]

    if os.path.exists(save_folder) == 0:
        os.makedirs(save_folder)

    print(time.asctime())
    print("Fixed mask PIV on {}".format(image_folder))

    l = readdata(image_folder, 'tif')
    l = l.loc[l.Name!="mask"]
    if len(l) % 2 != 0:
        l = l[:-1]

    DI = droplet_image(l)
    DI.fixed_mask_piv(save_folder, winsize, overlap, dt, mask_dir)

    """ Old code
    with Pool(10) as p:
        p.starmap(PIV_droplet,
                zip(l[::2].Dir, l[1::2].Dir, l[::2].Name, l[1::2].Name, repeat(winsize), repeat(overlap),
                repeat(dt), repeat(mask), repeat(save_folder)))
    """

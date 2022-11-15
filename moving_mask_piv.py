# from openpiv import tools, pyprocess, validation, filters, scaling
import numpy as np
import matplotlib.pyplot as plt
from skimage import io
import os
# from scipy.signal import medfilt2d
import pandas as pd
import time
# from xcorr_funcs import *
from corrLib import readdata
import sys
import time
import matplotlib.pyplot as plt
from deLib import droplet_image
import json
# %% codecell
"""
moving_mask_piv
===============

This script performs PIV on the flow field in a moving droplet. In short, the job is done in 3 steps:

1. determine droplet trajectory
2. generate cropped images
3. perform normal PIV on cropped images

For more information, see my note `here <https://github.com/ZLoverty/DE/blob/main/Notes/2022-03-02_moving-mask-droplet-frame-piv.pdf>`_.

.. rubric:: Syntax

.. code-block:: console

   python moving_mask_piv.py image_folder save_folder winsize overlap dt mask x0 y0 maskw maskh

* image_folder: folder containing tif images
* save_folder: folder to save .csv PIV data
* winsize, overlap, dt: PIV settings
* mask: dir of mask image (tif)
* x0, y0, maskw, maskh: initial mask information, for computing the offset of the trajectory. Can be read from positions.csv file.

.. rubric:: Test

.. code-block:: console

   python moving_mask_piv.py test_images\moving_mask_piv\raw test_images\moving_mask_piv\piv_result 20 10 0.02 test_images\moving_mask_piv\mask.tif 178 161 174 174

.. rubric:: Edit

* Mar 03, 2022 -- Initial commit.
"""

if __name__ == "__main__":
    image_folder = sys.argv[1]
    save_folder = sys.argv[2]
    winsize = int(sys.argv[3])
    overlap = int(sys.argv[4])
    dt = float(sys.argv[5])
    mask_dir = sys.argv[6]
    # the position and size of initial mask, check positions.csv [X, Y, Major, Minor]
    x0 = int(sys.argv[7])
    y0 = int(sys.argv[8])
    maskw = int(sys.argv[9])
    maskh = int(sys.argv[10])

    print(time.asctime())
    print("Moving mask PIV on {}".format(image_folder))

    # create a droplet_image object
    image_sequence = readdata(image_folder, "tif")
    DI = droplet_image(image_sequence)

    # perform PIV analysis
    DI.moving_mask_piv(save_folder, winsize, overlap, dt, mask_dir, (x0, y0), (maskw, maskh))

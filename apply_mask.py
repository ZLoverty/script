import pandas as pd
import numpy as np
import os
import sys
from skimage import io
from myImageLib import readdata, show_progress
import cv2

"""
apply_mask
==========

Apply mask on PIV data. It sets all the irrelevant (x, y in the False region of the mask) PIV velocity to np.nan.

.. rubric:: Syntax

.. code-block:: console

   python apply_mask.py piv_folder mask_dir [erode=32]

* piv_folder: folder containing PIV data (csv sequence)
* mask_dir: directory of a tif binary mask, of the same shape as raw images.
* erode: number of pixels to erode from the True region (this makes the mask smaller, reducing boundary effect). Default to 32, a good value is the winsize of PIV.

.. note::

   The original PIV data will be overwritten, since they are no longer useful.

.. rubric:: Edit

* 11032022 -- Initial commit.
"""

piv_folder = sys.argv[1]
mask_dir = sys.argv[2]
erode = 32
if len(sys.argv) > 3:
    erode = sys.argv[3]
    erode = int(erode)
mask_raw = io.imread(mask_dir)

l = readdata(piv_folder, "csv")
numFiles = len(l)
pivData = pd.read_csv(l.at[0, "Dir"])
mask_shrink = cv2.erode(mask_raw, np.ones((erode, erode), dtype="uint8"))
mask_bool_ij = mask_shrink.astype("bool")[pivData.y.astype("int"), pivData.x.astype("int")] # could cause error due to float index
for num, i in l.iterrows():
    show_progress((num+1)/numFiles, num+1)
    pivData = pd.read_csv(i.Dir)
    pivData.loc[~mask_bool_ij, "u"] = np.nan
    pivData.loc[~mask_bool_ij, "v"] = np.nan
    pivData.to_csv(i.Dir, index=False)

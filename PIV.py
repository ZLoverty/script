from pivLib import PIV
import sys
import os
from skimage import io
from myImageLib import readdata, show_progress
import pandas as pd

"""
PIV
===

This is the most basic version of PIV.

.. rubric:: Syntax

.. code-block:: console

   python PIV.py img_folder winsize dt piv_folder

* img_folder: tif sequence folder to be analyzed.
* winsize: interrogation window size.
* dt: time interval between adjacent frames (1/FPS).
* piv_folder: folder to save PIV results.

.. note::

   In this implementation, we set overlap as half of winsize.

.. rubric:: Edit

* Nov 03, 2022 -- Initial commit.
"""

img_folder = sys.argv[1]
winsize = int(sys.argv[2])
dt = float(sys.argv[3])
piv_folder = sys.argv[4]
if os.path.exists(piv_folder) == False:
    os.makedirs(piv_folder)

overlap = winsize // 2

l = readdata(img_folder, "tif")
numImages = len(l)

for ind0, ind1 in zip(l.index[::2], l.index[1::2]):
    show_progress((ind0+1)/numImages, ind0+1)
    I0 = io.imread(l.at[ind0, "Dir"])
    I1 = io.imread(l.at[ind1, "Dir"])
    x, y, u, v = PIV(I0, I1, winsize, overlap, dt)
    pivData = pd.DataFrame({"x": x.flatten(), "y": y.flatten(), "u": u.flatten(), "v": v.flatten()})
    pivData.to_csv(os.path.join(piv_folder, "{0}-{1}.csv".format(l.at[ind0, "Name"], l.at[ind1, "Name"])), index=False)

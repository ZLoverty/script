import pandas as pd
import numpy as np
import os
import sys
from skimage import io
from myImageLib import readdata, show_progress
from pivLib import apply_mask

"""
apply_mask
==========

Apply mask on PIV data. It calls :py:func:`pivLib.apply_mask` to treat the input PIV data, and save the results (masked PIV data) in the same files. See `here <https://zloverty.github.io/mylib/pivLib/pivLib.apply_mask.html>`_ for more details.

.. rubric:: Syntax

.. code-block:: console

   python apply_mask.py piv_folder mask_dir

* piv_folder: folder containing PIV data (csv sequence)
* mask_dir: directory of a tif binary mask, of the same shape as raw images.
* erode: number of pixels to erode from the True region (this makes the mask smaller, reducing boundary effect). Default to 32, a good value is the winsize of PIV.

.. rubric:: Test

.. code-block:: console

   python apply_mask.py test_images\apply_mask test_images\apply_mask\A.tif

.. rubric:: Edit

* Nov 03, 2022 -- Initial commit.
* Dec 01, 2022 -- Remove erosion step. Mask should be used as it is.
* Dec 13, 2022 -- Fix a bug.
* Dec 19, 2022 -- More accurate docstring.
"""

piv_folder = sys.argv[1]
mask_dir = sys.argv[2]

mask = io.imread(mask_dir)

l = readdata(piv_folder, "csv")
numFiles = len(l)

for num, i in l.iterrows():
    show_progress((num+1)/numFiles, num+1)
    pivData = pd.read_csv(i.Dir)
    pivData = apply_mask(pivData, mask)
    pivData.to_csv(i.Dir, index=False)

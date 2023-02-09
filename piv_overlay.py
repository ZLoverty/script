"""
Generate PIV arrow overlayed images for PIV visual inspection and illustration.

.. rubric:: Syntax

.. code-block:: console

   python piv_overlay.py piv_folder img_folder output_folder sparcity

* piv_folder -- folder containing PIV data in the form of .csv files
* img_folder -- folder containing .tif images
* output_folder -- folder to save the PIV overlay images in .jpg files (rescaled to 360 pixels in width)
* sparcity -- density of PIV arrows, higher value corresponds to sparcer arrows

.. rubric:: Test

.. code-block:: console

   python piv_overlay.py test_images\piv_drop test_images\piv_drop test_images\piv_overlay 1

.. rubric:: Edit

* Jan 03, 2022 --
    1. move from PIV to script,
    2. set scale,
    3. update docstring
    4. minor structural changes

    .. note::
       See `PIV technical report Sec II.A.1 <https://github.com/ZLoverty/DE/blob/main/Notes/PIV_technical_report.pdf>`_ for the reasoning of scale settings.

* Jan 22, 2022 -- reduce scale by 1.5 to increase the arrow size
* Mar 03, 2022 -- (i) Use `droplet_image` class to rewrite the script, (ii) remove logging
* Jan 05, 2023 -- Adapt myimagelib import style.
* Feb 08, 2023 -- Rewrite in function wrapper form, to make autodoc work properly. (autodoc import the script and execute it, so anything outside ``if __name__=="__main__"`` will be executed, causing problems)
"""

import os
import sys
import numpy as np
from myimagelib.myImageLib import to8bit, readdata
from skimage import io
import time
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from myimagelib.pivLib import read_piv
from myimagelib.deLib import droplet_image



def determine_arrow_scale(u, v, sparcity):
    row, col = u.shape
    return max(np.nanmax(u), np.nanmax(v)) * col / sparcity / 1.5

if __name__=="__main__": # whether the following script will be executed when run this code
    piv_folder = sys.argv[1]
    image_folder = sys.argv[2]
    out_folder = sys.argv[3]
    sparcity = 1
    if len(sys.argv) > 4:
        sparcity = int(sys.argv[4])

    if os.path.exists(out_folder) == False:
        os.makedirs(out_folder)

    seq = readdata(image_folder, "tif")
    DI = droplet_image(seq)

    DI.piv_overlay_fixed(piv_folder, out_folder, sparcity=sparcity)

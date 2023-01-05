from skimage import io
# import numpy as np
from nd2reader import ND2Reader
import time
import os
import sys
import shutil
from myimagelib.myImageLib import rawImage

"""
to_tif
======

Convert *\*.nd2* or *\*.raw* file to image sequence of raw and 8-bit grayscale images. For  *\*.nd2*, output image sequences are saved in a subfolder under the same folder as the  *\*.nd2* file with corresponding name as the  *\*.nd2* file name.
For raw, output image sequences are saved in subfolders in the same folder as the .raw files.

.. note::

   Autocontrast is applied to *8-bit* folder, but not to *raw* folder.

.. rubric:: Syntax

.. code-block:: console

   python to_tif.py nd2Dir remove

.. rubric:: Test

.. code-block:: console

   python to_tif.py test_images\test.nd2
   python to_tif.py test_images\raw\RawImage.raw

.. rubric:: Edit

* 06162020 -- No longer export 16-bit images.
* 08162020 --
    1. write input arguments in log.txt
    2. (important) add illumination correction. All frames will be corrected according to the whole video.
* 08182020 -- Add argument 'remove', determining if background subtraction is applied or not. Default to False.
* 10282021 -- Remove "8-bit" folder, export original images instead of converting to 8-bit
* 11042021 --
    1. Set `check_contrast` to False to avoid CLI spamming
    2. Add 'exp1' before the image number, in accordance to Cristian's image naming convention
* 11262021 --
    1. Remove the 'exp1' flag at the beginning of each image file
    2. Add saturated 8-bit image output for visualization (this means we need a big overhead of disk space!)
* 11302021 -- Add disk_capacity_check function to avoid running out disk space
* Jan 22, 2022 -- disk_capacity_check, use os.split(file)[1] to check, because windows does not recognize file directory as a valid directory for disk size check
* Feb 02, 2022 -- Print dir info, so in batch_to_tif I can follow the progress.
* Mar 15, 2022 --
    1. Rewrite using the rawImage class defined in myImageLib.
    2. Temporarily discontinue the "remove background functionality".
    3. Include .raw functionality -- with memory check.
    4. Update the doc string.
* Jan 05, 2023 -- Adapt myimagelib import style.
"""

nd2Dir = sys.argv[1]
remove = False
if len(sys.argv) > 2:
    remove = bool(int(sys.argv[2]))

# print(time.asctime() + " // Exporting {}".format(nd2Dir))

raw = rawImage(nd2Dir)
raw.extract_tif()

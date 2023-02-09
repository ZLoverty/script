"""
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

* Jun 16, 2020 -- No longer export 16-bit images.
* Aug 16, 2020 -- (i) write input arguments in log.txt (ii) (important) add illumination correction. All frames will be corrected according to the whole video.
* Aug 18, 2020 -- Add argument 'remove', determining if background subtraction is applied or not. Default to False.
* Oct 28, 2021 -- Remove "8-bit" folder, export original images instead of converting to 8-bit
* Nov 04, 2021 -- (i) Set `check_contrast` to False to avoid CLI spamming, (ii) Add 'exp1' before the image number, in accordance to Cristian's image naming convention
* Nov 26, 2021 -- (i) Remove the 'exp1' flag at the beginning of each image file, (ii) Add saturated 8-bit image output for visualization (this means we need a big overhead of disk space!)
* Nov 30, 2021 -- Add disk_capacity_check function to avoid running out disk space
* Jan 22, 2022 -- disk_capacity_check, use os.split(file)[1] to check, because windows does not recognize file directory as a valid directory for disk size check
* Feb 02, 2022 -- Print dir info, so in batch_to_tif I can follow the progress.
* Mar 15, 2022 -- (i) Rewrite using the rawImage class defined in myImageLib.
    2. Temporarily discontinue the "remove background functionality".
    3. Include .raw functionality -- with memory check.
    4. Update the doc string.
* Jan 05, 2023 -- Adapt myimagelib import style.
* Feb 08, 2023 -- Rewrite in function wrapper form, to make autodoc work properly. (autodoc import the script and execute it, so anything outside ``if __name__=="__main__"`` will be executed, causing problems)
"""

from skimage import io
from nd2reader import ND2Reader
import time
import os
import sys
import shutil
from myimagelib.myImageLib import rawImage


if __name__ == "__main__":
    nd2Dir = sys.argv[1]
    remove = False
    if len(sys.argv) > 2:
        remove = bool(int(sys.argv[2]))

    raw = rawImage(nd2Dir)
    raw.extract_tif()

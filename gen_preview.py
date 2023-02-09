"""
Generete preview images of given folder.

Assumed folder structure:

.. code-block:: console

   folder
   |-- 00.nd2
   |-- 01.nd2
   |-- ...

The script will extract the images of each \*.nd2 file and save as a tif image with the same name as the corresponding \*.nd2 files. 

.. rubric:: Syntax

.. code-block:: console

   python gen_preview.py nd2Dir

* nd2Dir -- nd2 file directory
* out_folder -- folder to save a tif file with the same name as the nd2 file

.. rubric:: Test

.. code-block:: console

   python gen_preview.py test_images\batch_to_tif\day1\00.nd2 test_images\batch_to_tif\preview\day1


.. rubric:: Edit

* Dec 12, 2021 -- Initial commit
* Dec 13, 2021 -- `cp` command is not platform independent. Use python native tools `shutil.copy` instead.
* Dec 14, 2021 -- Now work on single .nd2 file, instead of a folder of tif sequences.
* Dec 06, 2022 -- Now save first and last frames for a single nd2. Change of default behavior!
* Jan 05, 2023 -- Adapt myimagelib import style.
* Feb 08, 2023 -- Rewrite in function wrapper form, to make autodoc work properly. (autodoc import the script and execute it, so anything outside ``if __name__=="__main__"`` will be executed, causing problems)
"""

import sys
import os
from myimagelib.myImageLib import to8bit
from skimage import io
from tifffile import imwrite
from nd2reader import ND2Reader
import numpy as np



def extract_first_frame(nd2Dir):
    """Extract the first image in .nd2 and convert to 8-bit.
    Args:
    nd2 -- directory of .nd2 file
    Returns:
    img -- the 8-bit version of the first frame
    """
    with ND2Reader(nd2Dir) as images:
        img = to8bit(images[0])
    return img

def extract_frames(nd2Dir, indices=[0, -1]):
    """Extract multiple frames from nd2 images and return as a 3D array.
    nd2Dir -- dir of nd2 file
    indices -- indices of frames to preview"""
    img = []
    with ND2Reader(nd2Dir) as images:
        for i in indices:
            img.append(images[i])
    return np.stack(img)

if __name__=="__main__":
    nd2Dir = sys.argv[1]
    indices = [0, -1]
    if len(sys.argv) > 2:
        indices = [int(sys.argv[2])]
    # create preview folder
    preview_folder = os.path.join(os.path.split(nd2Dir)[0], "preview")
    outDir = os.path.join(preview_folder, os.path.split(nd2Dir)[1].split(".")[0] + ".tif")
    if os.path.exists(preview_folder) == False:
        os.makedirs(preview_folder)
    img = extract_frames(nd2Dir, indices=indices)
    imwrite(outDir, img)
    print("{0} -> {1}".format(nd2Dir, outDir))

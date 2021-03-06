import sys
import time
import os
from myImageLib import dirrec, to8bit
from shutil import copy
from skimage import io
from nd2reader import ND2Reader

"""
Generete preview images of given folder.

Assumed folder structure:
Folder
|- 00
  |- 8-bit
    |- 00000.tif
    |- ...
  |- raw
|- preview (newly generated by this script)
  |- 00.tif
  |- ...

The script will copy all the 00000.tif under 8-bit folder to a new "preview" folder

USAGE
=====
python gen_preview.py nd2Dir outDir

folder should be two levels above the 00000.tif file.
Deeper directories won't be searched.

TEST
====
python gen_preview.py test_images\batch_to_tif\day1\00.nd2 test_images\batch_to_tif\preview\day1\00.tif

LOG
===
test_images\batch_to_tif\day1\00.nd2 -> test_images\batch_to_tif\preview\day1\00.tif

EDIT
====
Dec 12, 2021 -- Initial commit
Dec 13, 2021 -- `cp` command is not platform independent. Use python native tools `shutil.copy` instead.
Dec 14, 2021 -- Now work on single .nd2 file, instead of a folder of tif sequences.
"""

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

if __name__=="__main__":
    nd2Dir = sys.argv[1]
    outDir = sys.argv[2]
    # create preview folder
    preview_folder = os.path.split(outDir)[0]
    if os.path.exists(preview_folder) == False:
        os.makedirs(preview_folder)
    img = extract_first_frame(nd2Dir)
    io.imsave(outDir, img)
    print("{0} -> {1}".format(nd2Dir, outDir))

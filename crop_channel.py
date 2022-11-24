import sys
import os
import cv2
from skimage import io
import pandas as pd
from myImageLib import readdata, show_progress, to8bit
from imutils import rotate
from tifffile import imwrite
from nd2reader import ND2Reader
import numpy as np

"""
crop_channel
============

Crop channels from bifurcation AN images. In a typical bifurcation experiment, we have a 3-way micro-channel photoprinted on a resin. This micro-channel is cast on the active microtubule system at an oil-water interface. The chaotic turbulent-like motions of microtubules will be rectified by the micro-channels. Ratchet structures are used to set one of the channels as inlet. The flow then goes into either remaining channels, or into both at certain fractions. We study what is the "preferred" bifurcation of the flow. In the cropped images, predetermined positive (+) direction always points upward.

This code crops the original multi-microchannel images into single channels, to allow more efficient PIV analysis. Ono top of cropping, the code also remove the background static feature from the images, by dividing the images by the median of the image stack. The images are then converted from float64 to 8-bit to save the storage space.

.. rubric:: Syntax

.. code-block:: console

   python crop_channel.py crop_data nd2Dir

* crop_data: the directory to a \*.csv file specifying how the raw images should be cropped. Typically, it consists 6 rows, where rows 1, 3, 5 contain rotation information, rows 2, 4, 6 contain cropping information. The image will rotate according to row 1, and cropped according to row 2, and so on so forth. The file is typically generated using ImageJ measurement tool.
* nd2Dir: full directory of the \*.nd2 file to be cropped.

The folder structure is illustrated below:

.. code-block:: console

   |-- nd2_folder
       |-- 00.nd2
       |-- 01.nd2
       |-- ...
       |-- crop_channel
           |-- 00_A.tif
           |-- 00_B.tif
           |-- 00_C.tif

.. note::

   * When creating crop_data in ImageJ, only select "bounding rectangle" in "Analyze -> Set measurements..."
   * When creating crop_data, DO remember to remove the scale !!!

.. rubric:: Edit

:Nov 03, 2022: Initial commit.
:Nov 23, 2022: To make the workflow consistent with Claire's, it is more convenient to crop the channel region directly from the \*.nd2 file, and save as tifstack. Now crop directly from \*.nd2 files to  tifstack.
"""

crop_data_dir = sys.argv[1]
nd2Dir = sys.argv[2]

crop_data = pd.read_csv(crop_data_dir)

crop_folder = os.path.join(os.path.split(nd2Dir)[0], "crop_channel")
if os.path.exists(crop_folder) == False:
    os.makedirs(crop_folder)

# create a dist that holds the cropped images in all regions
crops = {}
for j in range(0, len(crop_data)//2):
     crops[j] = []

# crop nd2
with ND2Reader(nd2Dir) as images:
    nImages = len(images)
    for num, image in enumerate(images):
        show_progress((num+1)/nImages, num)
        for j in range(0, len(crop_data)//2): # loop over all possible croppings
            # convert to angle, xy, wh
            angle = 90 - crop_data.at[2*j, "Angle"]
            x, y, w, h = crop_data.at[2*j+1, "BX"], crop_data.at[2*j+1, "BY"], crop_data.at[2*j+1, "Width"], crop_data.at[2*j+1, "Height"]
            imgr = rotate(image, angle=angle) # rotate
            crop = imgr[y:y+h, x:x+w] # crop
            crops[j].append(crop)

# remove background and save
for j in crops:
    crops[j] = np.stack(crops[j])
    imwrite(os.path.join(crop_folder,  "{0}_{1}.tif".format(os.path.split(nd2Dir)[1].split(".")[0], chr(65+j))), to8bit(crops[j] / np.median(crops[j], axis=0)))

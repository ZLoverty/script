import sys
import os
import cv2
from skimage import io
import pandas as pd
from myImageLib import readdata, show_progress
from imutils import rotate

"""
DESCRIPTION
===========
Crop channels from bifurcation AN images.
In a typical bifurcation experiment, we have a 3-way micro-channel photoprinted on a resin. This micro-channel is cast on the active microtubule system at an oil-water interface. The chaotic turbulent-like motions of microtubules will be rectified by the micro-channels. Ratchet structures are used to set one of the channels as inlet. The flow then goes into either remaining channels, or into both at certain fractions. We study what is the "preferred" bifurcation of the flow.

In the cropped images, predetermined positive (+) direction always points upward. 

SYNTAX
======
python crop_channel.py crop_data img_folder crop_folder

crop_data: a table specifying how the raw images should be cropped. Typically, it consists 6 rows, where rows 1, 3, 5 contain rotation information, rows 2, 4, 6 contain cropping information.
img_folder: raw images folder
crop_folder: folder to save cropped images

NOTE
====
1. When creating crop_data in ImageJ, only select "bounding rectangle" in "Set measurements..."

EDIT
====
11032022 -- Initial commit.
"""

crop_data_dir = sys.argv[1]
img_folder = sys.argv[2]
crop_folder = sys.argv[3]

crop_data = pd.read_csv(crop_data_dir)

# Create subfolders for cropped images
if os.path.exists(crop_folder) == False:
    os.makedirs(crop_folder)
for j in range(0, len(crop_data)//2):
    crop_subfolder = os.path.join(crop_folder, "crop-{:d}".format(j))
    if os.path.exists(crop_subfolder) == False:
        os.makedirs(crop_subfolder)

l = readdata(img_folder, "tif")
numImages = len(l)
for num, i in l.iterrows():
    img = io.imread(i.Dir)
    show_progress((num+1)/numImages, num+1)
    for j in range(0, len(crop_data)//2): # loop over all possible croppings
        # convert to angle, xy, wh
        angle = 90 - crop_data.at[2*j, "Angle"]
        x, y, w, h = crop_data.at[2*j+1, "BX"], crop_data.at[2*j+1, "BY"], crop_data.at[2*j+1, "Width"], crop_data.at[2*j+1, "Height"]        
        imgr = rotate(img, angle=angle) # rotate
        crop = imgr[y:y+h, x:x+w] # crop
        io.imsave(os.path.join(os.path.join(crop_folder, "crop-{:d}".format(j)), "{}.tif".format(i.Name)), crop, check_contrast=False)
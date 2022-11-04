from skimage import io
import numpy as np
import os
import sys
from myImageLib import readdata, show_progress

"""
DESCRIPTION
===========
This script removes the stationary background of a tif sequence in a given folder. Specifically, it does:
- Median z-projection
- divide raw images by the projection

By default, it saves the output images to a "..._rb" folder, where "..." is the original folder name. For example, images from crop_channel/crop-0 will be processed and saved in crop_channel/crop-0_rb.

SYNTAX
======
python remove_background.py img_folder

img_folder: tif sequence folder to be processed.

NOTE
====
Here the processed images are rescaled 

EDIT
====
11032022 -- Initial commit.
"""

img_folder = sys.argv[1]
rb_folder = img_folder.rstrip(os.sep) + "_rb"
if os.path.exists(rb_folder) == False:
    os.makedirs(rb_folder)
l = readdata(img_folder, "tif")
numImages = len(l)
imgs = []

print("Reading images ...")
for num, i in l.iterrows():
    img = io.imread(i.Dir)
    imgs.append(img)
stack = np.stack(imgs, axis=0) # TXY image stack

med = np.median(stack, axis=0)

# set rescaling factor according to the first image
# to convert float32 images to 8-bit, save storage capacity
imgr0 = stack[0] / med
low, high = imgr0.min(), imgr0.max()
for num, img in enumerate(stack):
    show_progress((num+1)/numImages, num+1)
    imgr = img / med
    img8 = ((imgr - low) / (high - low) * 255).astype(np.uint8)
    io.imsave(os.path.join(rb_folder, "{:05d}.tif".format(num)), img8)
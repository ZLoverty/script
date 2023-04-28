"""
Crop channels from bifurcation AN images. In a typical bifurcation experiment, we have a 3-way micro-channel photoprinted on a resin. This micro-channel is cast on the active microtubule system at an oil-water interface. The chaotic turbulent-like motions of microtubules will be rectified by the micro-channels. Ratchet structures are used to set one of the channels as inlet. The flow then goes into either remaining channels, or into both at certain fractions. We study what is the "preferred" bifurcation of the flow. In the cropped images, predetermined positive (+) direction always points upward.

This code crops the original multi-microchannel images into single channels, to allow more efficient PIV analysis. On top of cropping, the code also remove the background static feature from the images, by dividing the images by the median of the image stack. The images are then converted from float64 to 8-bit to save the storage space.

.. rubric:: Syntax

.. code-block:: console

   python crop_channel.py crop_data nd2Dir method

* crop_data: the directory to a \*.csv file specifying how the raw images should be cropped. Typically, it consists 6 rows, where rows 1, 3, 5 contain rotation information, rows 2, 4, 6 contain cropping information. The image will rotate according to row 1, and cropped according to row 2, and so on so forth. The file is typically generated using ImageJ measurement tool.
* nd2Dir: full directory of the \*.nd2 file to be cropped.
* method: rotate or map. 

.. warning::

   rotate and map methods use different crop_data. 

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

* Nov 03, 2022 -- Initial commit.
* Nov 23, 2022 -- To make the workflow consistent with Claire's, it is more convenient to crop the channel region directly from the \*.nd2 file, and save as tifstack. Now crop directly from \*.nd2 files to  tifstack.
* Jan 05, 2023 -- Adapt myimagelib import style.
* Jan 24, 2023 -- (i) Check the existence of output files, e.g. 00_A.tif, 00_B.tif, 00_C.tif, (ii) print nd2 file name as progress bar label.
* Feb 08, 2023 -- Rewrite in function wrapper form, to make autodoc work properly. (autodoc import the script and execute it, so anything outside ``if __name__=="__main__"`` will be executed, causing problems)
* Mar 30, 2023 -- (i) Add "map" method, in addtion to "rotate", (ii) generate a crop region indicator on the raw image.
* Mar 31, 2023 -- Explicitly convert image dtype to float32 when dividing median to reduce memory usage. 
"""

if __name__ == "__main__":
    import sys
    import os
    import cv2
    from skimage import io
    import pandas as pd
    from myimagelib.myImageLib import readdata, show_progress, to8bit
    from imutils import rotate
    from tifffile import imwrite
    from nd2reader import ND2Reader
    import numpy as np
    from scipy.ndimage import map_coordinates

    def rotate_crop(nd2Dir, crop_data):
        """
        Use the rotate-crop approach to generate image ROIs. This is the traditional method, where manual crop_data generated in ImageJ is required. For more information, see Section 1 of "bifurcation data analysis" notebook. 
        """
        crops = {}
        for j in range(0, len(crop_data)//2):
            crops[j] = []
        with ND2Reader(nd2Dir) as images:
            nImages = len(images)
            for num, image in enumerate(images):
                show_progress((num+1)/nImages, os.path.split(nd2Dir)[1])
                for j in range(0, len(crop_data)//2): # loop over all possible croppings
                    # convert to angle, xy, wh
                    angle = 90 - crop_data.at[2*j, "Angle"]
                    x, y, w, h = crop_data.at[2*j+1, "BX"], crop_data.at[2*j+1, "BY"], crop_data.at[2*j+1, "Width"], crop_data.at[2*j+1, "Height"]
                    imgr = rotate(image, angle=angle) # rotate
                    crop = imgr[y:y+h, x:x+w] # crop
                    crops[j].append(crop)
        return crops

    def map_crop(nd2Dir, crop_data):
        """
        Use ``scipy.ndimage.map_coordinates`` to generate image ROIs. This is a new method, which prevents the loss of image information due to rotation. The crop_data should be generated using the "faster_cropping.py" script and should contain [BX, BY, hu0, hu1, wu0, wu1, h, w].
        """
        crops = {}
        X = {}
        Y = {}
        for j in range(0, len(crop_data)):
            crops[j] = []
            # read crop_data
            x, y, hu0, hu1, wu0, wu1, h, w = crop_data[["BX", "BY", "hu0", "hu1", "wu0", "wu1", "h", "w"]].loc[j]
            # xb = np.array([x, y])
            # h_unit = np.array([hu0, hu1])
            # w_unit = np.array([wu0, wu1])
            YY, XX = np.mgrid[0:h, 0:w]
            YY = np.flip(YY, axis=0)
            X[j] = x + XX * wu0 + YY * hu0
            Y[j] = y + XX * wu1 + YY * hu1

        with ND2Reader(nd2Dir) as images:
            nImages = len(images)
            for num, image in enumerate(images):
                show_progress((num+1)/nImages, os.path.split(nd2Dir)[1])
                for j in range(0, len(crop_data)): # loop over all possible croppings
                    crops[j].append(map_coordinates(image, [Y[j], X[j]], order=0, mode="constant"))
        return crops


    crop_data_dir = sys.argv[1]
    nd2Dir = sys.argv[2]
    method = sys.argv[3]

    # crop_data_dir = r"C:\Users\liuzy\Documents\test-crop\crop_data_map.csv"
    # nd2Dir = r"C:\Users\liuzy\Documents\test-crop\04.nd2"
    # method = "map"

    crop_data = pd.read_csv(crop_data_dir)

    crop_folder = os.path.join(os.path.split(nd2Dir)[0], "crop_channel")
    if os.path.exists(crop_folder) == False:
        os.makedirs(crop_folder)

    # create a dist that holds the cropped images in all regions
    # check the existence of ouput tif files
    
    crop_name = {}
    prev_name = {}
    exists = []
    if method == "map":
        numChannels = len(crop_data)
    elif method == "rotate":
        numChannels = len(crop_data) // 2

    for j in range(0, numChannels): 
        crop_name[j] = os.path.join(crop_folder, "{0}_{1}.tif".format(os.path.split(nd2Dir)[1].split(".")[0], chr(65+j)))
        exists.append(os.path.exists(crop_name[j]))

    if all(exists) == False: # if not all the output files exist, run the script
        # crop nd2
        
        if method == "rotate": # rotate crop
            crops = rotate_crop(nd2Dir, crop_data)        
        elif method == "map": # map crop
            crops = map_crop(nd2Dir, crop_data)

        # remove background and save
        for j in crops:
            crops[j] = np.stack(crops[j])
            imwrite(crop_name[j], to8bit(crops[j].astype("float32") / np.median(crops[j], axis=0).astype("float32")))
        
    else:
        print("All the output files: ")
        for j in crop_name:
            print(crop_name[j])
        print("exist, skip {}".format(os.path.split(nd2Dir)[1]))

